import numpy as np
import torch
import torch.nn.functional as F
from torch import nn

from models.baseMME import KGModel
from utils.euclidean import givens_rotations
from utils.hyperbolic import mobius_add, expmap0, project, hyp_distance_multi_c, logmap0
from utils.sinkhorn import *
import os
MME_MODELS = ["MME"]


class BaseHS(KGModel):
    """Trainable curvature for each relationship."""

    def __init__(self, args):
        super(BaseHS, self).__init__(args.sizes, args.rank, args.dropout, args.gamma, args.dtype, args.bias,
                                    args.init_size)
        self.entity.weight.data = self.init_size * torch.randn((self.sizes[0], self.rank), dtype=self.data_type)
        self.rel.weight.data = self.init_size * torch.randn((self.sizes[1], 2 * self.rank), dtype=self.data_type)
        self.rel_diag = nn.Embedding(self.sizes[1], self.rank)
        self.rel_diag.weight.data = 2 * torch.rand((self.sizes[1], self.rank), dtype=self.data_type) - 1.0
        self.multi_c = args.multi_c

    def get_rhs(self, queries, eval_mode):
        """Get embeddings and biases of target entities."""
        if eval_mode:
            return self.entity.weight, self.bt.weight
        else:
            return self.entity(queries[:, 2]), self.bt(queries[:, 2])

    def similarity_score(self, lhs_e, rhs_e, eval_mode):
        """Compute similarity scores or queries against targets in embedding space."""
        lhs_e, c = lhs_e
        return - hyp_distance_multi_c(lhs_e, rhs_e, c, eval_mode) ** 2


class MME(BaseHS):
    def __init__(self, args):
        super(MME, self).__init__(args)
        graph_view_space_c_init = torch.ones((1, 1), dtype=self.data_type)

        self.graph_view_space_c = nn.Parameter(graph_view_space_c_init, requires_grad=True)

        rel_view_space_c_init = torch.ones((self.sizes[1], 1), dtype=self.data_type)
        self.rel_view_space_c = nn.Parameter(rel_view_space_c_init, requires_grad=True)

        entity_veiw_sapce_c_init = torch.ones((self.sizes[0], 1), dtype=self.data_type)
        self.entity_veiw_sapce_c = nn.Parameter(entity_veiw_sapce_c_init, requires_grad=True)

        general_c_init = torch.ones((self.sizes[0], 1), dtype=self.data_type)
        self.general_c = nn.Parameter(general_c_init, requires_grad=True)

        ## optimal transport parameters
        self.mats_entity_view = nn.Parameter(torch.Tensor(self.rank,  self.rank), requires_grad=True)
        nn.init.xavier_uniform(self.mats_entity_view)
        self.mats_graph_view = nn.Parameter(torch.Tensor(self.rank, self.rank), requires_grad=True)
        nn.init.xavier_uniform(self.mats_graph_view)

        ## select the parameter
        alpha=0.1
        gamma=0.1
        self.alpha = nn.Parameter(torch.tensor(alpha), requires_grad=False)
        self.gamma = nn.Parameter(torch.tensor(gamma), requires_grad=False)

        if args.dtype == "double":
            self.scale = torch.Tensor([1. / np.sqrt(self.rank)]).double().cuda()
        else:
            self.scale = torch.Tensor([1. / np.sqrt(self.rank)]).cuda()

    def optimal_transport(self, source_embeddings,target_embeddings,delta_ot):
        device = delta_ot.device
        number = 10

        source_dim = source_embeddings.shape[-1]
        target_dim = target_embeddings.shape[-1]
        source_dis = torch.ones_like(source_embeddings[0,:])
        source_dis = source_dis/source_dis.shape[-1]
        target_dis = torch.ones_like(target_embeddings[0,:])
        target_dis = target_dis/target_dis.shape[-1]

        # transport matrix
        matrix_temp = torch.zeros((number,source_dim,target_dim))

        with torch.no_grad():
            for i in range(number):
                cost = (source_embeddings[i,:].reshape(-1,source_dim) - target_embeddings[i,:].reshape(target_dim,-1)) ** 2 * self.scale
                matrix_temp[i,:,:] = sinkhorn(source_dis, target_dis, cost.t())[0].t()

        return matrix_temp.mean(dim=0).to(device) * target_dim * self.scale + delta_ot


    def get_graph_view_queries(self, queries, curvatue):

        c = F.softplus(curvatue[queries[:, 1]])
        head = expmap0(self.entity(queries[:, 0]), c)
        rel1, rel2 = torch.chunk(self.rel(queries[:, 1]), 2, dim=1)
        rel1 = expmap0(rel1, c)
        rel2 = expmap0(rel2, c)
        lhs = project(mobius_add(head, rel1, c), c)
        res1 = givens_rotations(self.rel_diag(queries[:, 1]), lhs)
        res2 = mobius_add(res1, rel2, c)
        res2 = logmap0(res2, c)
        return res2

    def get_rel_view_queries(self, queries, curvatue):

        c = F.softplus(curvatue[queries[:, 1]])
        head = expmap0(self.entity(queries[:, 0]), c)
        rel1, rel2 = torch.chunk(self.rel(queries[:, 1]), 2, dim=1)
        rel1 = expmap0(rel1, c)
        rel2 = expmap0(rel2, c)
        lhs = project(mobius_add(head, rel1, c), c)
        res1 = givens_rotations(self.rel_diag(queries[:, 1]), lhs)
        res2 = mobius_add(res1, rel2, c)
        res2 = logmap0(res2, c)
        return res2

    def get_entity_view_queries(self, queries, curvatue):

        c = F.softplus(curvatue[queries[:, 0]])
        head = expmap0(self.entity(queries[:, 0]), c)
        rel1, rel2 = torch.chunk(self.rel(queries[:, 1]), 2, dim=1)
        rel1 = expmap0(rel1, c)
        rel2 = expmap0(rel2, c)
        lhs = project(mobius_add(head, rel1, c), c)
        res1 = givens_rotations(self.rel_diag(queries[:, 1]), lhs)
        res2 = mobius_add(res1, rel2, c)
        res2 = logmap0(res2, c)
        return res2

    def get_queries(self, queries):
        entity_view_lhs_e = self.get_entity_view_queries(queries, self.entity_veiw_sapce_c)
        rel_view_lhs_e = self.get_rel_view_queries(queries, self.rel_view_space_c)
        graph_view_lhs_e = self.get_graph_view_queries(queries, self.graph_view_space_c)

        c = F.softplus(self.general_c[queries[:, 0]])

        # optimal transport
        matrix1 = self.optimal_transport(rel_view_lhs_e, entity_view_lhs_e, self.mats_entity_view)
        matrix2 = self.optimal_transport(graph_view_lhs_e, entity_view_lhs_e, self.mats_graph_view)
        rel_view_embeddings = rel_view_lhs_e.mm(matrix1)
        graph_view_embeddings = graph_view_lhs_e.mm(matrix2)
        # fusion
        embedding = (1 - self.alpha-self.gamma) * entity_view_lhs_e + self.alpha * rel_view_embeddings + self.gamma * graph_view_embeddings
        res = expmap0(embedding, c)

        return (res,c), self.bh(queries[:, 0])

    def score(self, lhs, rhs, eval_mode):
        lhs_e, lhs_biases = lhs
        rhs_e, rhs_biases = rhs
        score = self.similarity_score(lhs_e, rhs_e, eval_mode)
        if self.bias == 'constant':
            return self.gamma.item() + score
        elif self.bias == 'learn':
            if eval_mode:
                return lhs_biases + rhs_biases.t() + score
            else:
                return lhs_biases + rhs_biases + score
        else:
            return score

    def forward(self, queries, eval_mode=False):
        """ KGModel forward pass.

        Args:
            queries: torch.LongTensor with query triples (head, relation, tail)
            eval_mode: boolean, true for evaluation, false for training
        Returns:
            predictions: torch.Tensor with triples' scores
                         shape is (n_queries x 1) if eval_mode is false
                         else (n_queries x n_entities)
            factors: embeddings to regularize
        """
        # get embeddings and similarity scores
        lhs_e, lhs_biases = self.get_queries(queries)
        # queries = F.dropout(queries, self.dropout, training=self.training)
        rhs_e, rhs_biases = self.get_rhs(queries, eval_mode)
        # candidates = F.dropout(candidates, self.dropout, training=self.training)
        predictions = self.score((lhs_e, lhs_biases), (rhs_e, rhs_biases), eval_mode)

        # get factors for regularization
        factors = self.get_factors(queries)
        return predictions, factors

