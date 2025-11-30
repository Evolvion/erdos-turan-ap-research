"""
Fourier-increment step on a window modulo q with weighted DFT.
"""
from __future__ import annotations
import numpy as np

def dft_mod_q(I, w, g, q):
    # returns max |hat| and arg (a)
    twopi = 2*np.pi
    Ivals = I.astype(float)
    best = (0.0, 0)
    for a in range(q):
        phase = np.exp(1j*twopi*a*(Ivals % q)/q)
        val = np.abs(np.sum(g * w * phase))
        if val > best[0]:
            best = (float(val), a)
    return best

def best_residue(I, w, f, q, a):
    # choose residue class r maximizing weighted mean of f on {n: n≡r mod q}
    Ilist = list(I)
    best_r, best_mu = 0, -1.0
    for r in range(q):
        idx = [i for i,n in enumerate(Ilist) if n % q == r]
        if not idx: 
            continue
        mu = float(np.sum(f[idx]*w[idx]) / np.sum(w[idx]))
        if mu > best_mu:
            best_mu, best_r = mu, r
    return best_r, best_mu
