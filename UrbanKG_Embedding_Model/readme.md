# Structure-aware UrbanKG Embedding 

This code is the official PyTorch implementation of [UUKG: Unified Urban Knowledge Graph Dataset for Urban Spatiotemporal Prediction](https://arxiv.org/pdf/2306.11443.pdf) as well as multiple state-of-the-art KG embedding models which can be trained for the link prediction task. 

## Installation

First, create a python 3.7 environment and install dependencies:

```bash
conda create -n python3.7 UUKG
source activate UUKG
pip install -r requirements.txt
```

## Datasets

The complete datasets could be found in  [Google Drive](https://drive.google.com/drive/folders/1egTmnKRzTQuyW_hsbFURUonGC-bJmBHW?usp=sharing), then you  can pre-process the datasets:

```bash
python datasets/process.py
```

## Usage

To train and evaluate a UrbanKG embedding model for the link prediction task, use the run.py script:

```bash
usage: run.py [-h] [--dataset {NYC, CHI}]
              [--model {TransE, RotH, ...}]
              [--regularizer {N3,N2}] [--reg REG]
              [--optimizer {Adagrad,Adam,SGD,SparseAdam,RSGD,RAdam}]
              [--max_epochs MAX_EPOCHS] [--patience PATIENCE] [--valid VALID]
              [--rank RANK] [--batch_size BATCH_SIZE]
              [--neg_sample_size NEG_SAMPLE_SIZE] [--dropout DROPOUT]
              [--init_size INIT_SIZE] [--learning_rate LEARNING_RATE]
              [--gamma GAMMA] [--bias {constant,learn,none}]
              [--dtype {single,double}] [--double_neg] [--debug] [--multi_c]

```
## How to get the embedding

We build the index between entities and learned embeddings and storage the index file in **./data/entity_idx_embedding.csv**. To obtain the learned UrbanKG embedding, run **`get_embedding.py`**.


## New models

To add a new Urban Knowledge Graph embedding model, implement the corresponding query embedding under models/, e.g.:

```
def get_queries(self, queries):
    head_e = self.entity(queries[:, 0])
    rel_e = self.rel(queries[:, 1])
    lhs_e = ### Do something here ###
    lhs_biases = self.bh(queries[:, 0])
    return lhs_e, lhs_biases
```

## References

Some of the code was forked from the original AttH implementation which can be found at: [https://github.com/HazyResearch/KGEmb](https://github.com/HazyResearch/KGEmb)

