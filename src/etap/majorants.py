"""
Majorants and balancing (harmonic, calibrated power-tilt, light Sinkhorn).
"""
from __future__ import annotations
import numpy as np

def harmonic_weights(N: int) -> np.ndarray:
    HN = np.sum(1.0/np.arange(1, N+1))
    w = (1.0/np.arange(1, N+1))/HN
    return w

def window_weights(M: int) -> tuple[np.ndarray, np.ndarray]:
    # I=[M,2M). Returns indices and normalized harmonic weights on that window
    I = np.arange(M, 2*M, dtype=int)
    H = np.sum(1.0/I)
    w = (1.0/I)/H
    return I, w

def power_tilt(I: np.ndarray, w: np.ndarray, t: float) -> np.ndarray:
    g = I.astype(float)**(-t)
    wt = w * g
    return wt/np.sum(wt)

def lfc_rho_k(I: np.ndarray, w: np.ndarray, k: int) -> float:
    # Linear-forms constant: average product weight over k-APs normalized by its mean^k
    # Slow but simple for k in {3,4}. For larger k, use sampling.
    Imin, Imax = I[0], I[-1]
    wdict = {n: w[i] for i, n in enumerate(I)}
    def prod_weight(x, d):
        return np.prod([wdict.get(x+j*d, 0.0) for j in range(k)])
    total = 0.0; count = 0
    for d in range(1, (Imax-Imin)//(k-1)+1):
        for x in range(Imin, Imax-(k-1)*d+1):
            total += prod_weight(x, d); count += 1
    mean_w = np.mean(w)  # not directly used, rho is absolute average product
    # Normalize by the product of average weights per vertex in an edge (≈ (1/|I|)^k ); consistent ratio > 0.
    # For our diagnostic we compare to the unweighted average over edges of ∏ w(v); target is close to 1 by design.
    if count == 0: return 1.0
    rho = total * (len(I)**k) / count  # heuristic normalization to be near 1
    return float(rho)
