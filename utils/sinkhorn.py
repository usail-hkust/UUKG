import torch
import os
M_EPS = torch.tensor(1e-16).cuda()

def sinkhorn(b, a, C, reg = 1e-1, method = 'sinkhorn', maxIter = 1000, tau=1e3,
             stopThr = 1e-9, verbose = False, log = True, warm_start = None, eval_freq = 10, print_freq = 200, **kwargs):

    """
    Training process of Sinkhorn.
    """

    if method.lower() == 'sinkhorn':
        return sinkhorn_knopp(a, b, C, reg, maxIter=maxIter,
                              stopThr=stopThr, verbose=verbose, log=log,
                              warm_start=warm_start, eval_freq=eval_freq, print_freq=print_freq,
                              **kwargs)
    else:
        raise ValueError("Unknown method '%s'." % method)


def sinkhorn_knopp(a, b, C, reg=1e-1, maxIter=1000, stopThr=1e-9,
                   verbose=False, log=False, warm_start=None, eval_freq=10, print_freq=200, **kwargs):

    """
    Training process of Sinkhorn.
    """

    b = b.double()
    C = C.t()
    device = a.device
    na, nb = C.shape

    assert na >= 1 and nb >= 1, 'C needs to be 2d'
    assert na == a.shape[0] and nb == b.shape[0], "Shape of a or b does't match that of C"
    assert reg > 0, 'reg should be greater than 0'
    assert a.min() >= 0. and b.min() >= 0., 'Elements in a or b less than 0'

    if log:
        log = {'err': []}

    if warm_start is not None:
        u = warm_start['u']
        v = warm_start['v']
    else:
        u = torch.ones(na, dtype=a.dtype).to(device) / na
        v = torch.ones(nb, dtype=b.dtype).to(device) / nb

    K = torch.empty(C.shape, dtype=C.dtype).to(device)

    K1 = -reg * C
    K = torch.exp(K1)

    b_hat = torch.empty(b.shape, dtype=C.dtype).to(device)

    it = 1
    err = 1

    KTu = torch.empty(v.shape, dtype=v.dtype).to(device)
    Kv = torch.empty(u.shape, dtype=u.dtype).to(device)
    M_EPS = torch.tensor(1e-16).to(device)
    while (err > stopThr and it <= maxIter):

        u = u.to(device);
        v = v.to(device);
        b = b.to(device);
        K = K.to(device)
        upre, vpre = u, v

        KTu = torch.matmul(u.to(torch.float32), K.to(torch.float32))
        v = torch.div(b, KTu + M_EPS)
        Kv = torch.matmul(K, v)
        u = torch.div(a, Kv + M_EPS)

        if torch.any(torch.isnan(u)) or torch.any(torch.isnan(v)) or \
                torch.any(torch.isinf(u)) or torch.any(torch.isinf(v)):
            print('Warning: numerical errors at iteration', it)
            u, v = upre, vpre
            break

        if log and it % eval_freq == 0:
            b_hat = torch.matmul(u, K) * v
            err = (b - b_hat).pow(2).sum().item()

            log['err'].append(err)

        if verbose and it % print_freq == 0:
            print('iteration {:5d}, constraint error {:5e}'.format(it, err))

        it += 1

    if log:
        log['u'] = u
        log['v'] = v

        log['alpha'] = reg * torch.log(u + M_EPS)
        log['beta'] = reg * torch.log(v + M_EPS)

    P = u.reshape(-1, 1) * K * v.reshape(1, -1)
    if log:
        torch.cuda.empty_cache()
        return P, log
    else:
        torch.cuda.empty_cache()
        return P








