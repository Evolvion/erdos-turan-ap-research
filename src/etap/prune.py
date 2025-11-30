"""
√T3 pruning bound with explicit certificate sets S_i.
"""
from __future__ import annotations
import numpy as np

def build_APs(I, k=3):
    Imin, Imax = int(I[0]), int(I[-1])
    edges = []
    if k==3:
        for d in range(1, (Imax-Imin)//2 + 1):
            for x in range(Imin, Imax-2*d+1):
                edges.append((x, x+d, x+2*d))
    return edges

def phi_degrees(I, f, w):
    # normalized degree per vertex: (# of active edges incident)/ (w(n)*Λ_3(1))
    edges = build_APs(I, 3)
    wdict = {n: w[i] for i,n in enumerate(I)}
    fdict = {n: f[i] for i,n in enumerate(I)}
    # Λ_3(1)
    lam1 = 0.0
    for (a,b,c) in edges:
        lam1 += wdict.get(a,0)*wdict.get(b,0)*wdict.get(c,0)
    deg = {n:0.0 for n in I}
    for (a,b,c) in edges:
        wt = wdict.get(a,0)*wdict.get(b,0)*wdict.get(c,0)*fdict.get(a,0)*fdict.get(b,0)*fdict.get(c,0)
        deg[a]+=wt; deg[b]+=wt; deg[c]+=wt
    phi = {n:(deg[n]/(wdict[n]*lam1) if wdict[n]>0 and lam1>0 else 0.0) for n in I}
    return phi

def prune_schedule(I, f, w, s0=None):
    # Returns deletion sets and final remainder mask
    import math
    from .ap_counts import T3
    I = np.array(I, dtype=int)
    f = np.array(f, dtype=float); w = np.array(w, dtype=float)
    T = T3(I, f, w)
    if s0 is None:
        s0 = 3*math.sqrt(max(T,0.0))
    mask = np.ones_like(f, dtype=bool)
    S_list = []
    s = s0; curT = T
    for _ in range(20):
        phi = phi_degrees(I[mask], f[mask], w[mask])
        idx = np.array([i for i,n in enumerate(I[mask]) if phi.get(int(n),0.0)>=s], dtype=int)
        if idx.size==0:
            break
        # record deletion set indices in original coordinates
        orig_idx = np.where(mask)[0][idx]
        S_list.append(orig_idx.tolist())
        mask[orig_idx]=False
        from .ap_counts import T3 as T3fun
        curT = T3fun(I[mask], f[mask], w[mask])
        s = 3*math.sqrt(max(curT,0.0))
        if curT < 1e-12:
            break
    return S_list, mask
