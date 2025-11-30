"""
AP counting and simple Gowers U^2/U^3 estimators under weights.
"""
from __future__ import annotations
import numpy as np

def HN(N:int)->float:
    return float(np.sum(1.0/np.arange(1, N+1)))

def lambda_k_3(I: np.ndarray, f: np.ndarray, w: np.ndarray) -> float:
    # Sum over x,d of product f*w at x,x+d,x+2d
    Imin, Imax = int(I[0]), int(I[-1])
    wdict = {n: w[i] for i,n in enumerate(I)}
    fdict = {n: f[i] for i,n in enumerate(I)}
    total = 0.0
    for d in range(1, (Imax-Imin)//2 + 1):
        for x in range(Imin, Imax-2*d+1):
            total += (fdict.get(x,0)*wdict.get(x,0) *
                      fdict.get(x+d,0)*wdict.get(x+d,0) *
                      fdict.get(x+2*d,0)*wdict.get(x+2*d,0))
    return float(total)

def lambda_k_4(I: np.ndarray, f: np.ndarray, w: np.ndarray) -> float:
    Imin, Imax = int(I[0]), int(I[-1])
    wdict = {n: w[i] for i,n in enumerate(I)}
    fdict = {n: f[i] for i,n in enumerate(I)}
    total = 0.0
    for d in range(1, (Imax-Imin)//3 + 1):
        for x in range(Imin, Imax-3*d+1):
            total += np.prod([fdict.get(x+j*d,0)*wdict.get(x+j*d,0) for j in range(4)])
    return float(total)

def T3(I,f,w)->float:
    ones = np.ones_like(f)
    num = lambda_k_3(I,f,w)
    den = lambda_k_3(I,ones,w)
    return num/den if den>0 else 0.0

def T4(I,f,w)->float:
    ones = np.ones_like(f)
    num = lambda_k_4(I,f,w)
    den = lambda_k_4(I,ones,w)
    return num/den if den>0 else 0.0

def U2_estimate(I, f, w, samples=2000, rng=None)->float:
    # Lightweight proxy: average squared correlation with shifts under weights
    rng = np.random.default_rng(rng)
    Imin, Imax = int(I[0]), int(I[-1])
    fdict = {n: f[i] for i,n in enumerate(I)}
    wdict = {n: w[i] for i,n in enumerate(I)}
    acc = 0.0; cnt = 0
    for _ in range(samples):
        d = rng.integers(1, max(2,(Imax-Imin)//2))
        s1=s2=0.0
        for x in range(Imin, Imax-d+1):
            s1 += (fdict.get(x,0)-np.sum(f*w))*(fdict.get(x+d,0)-np.sum(f*w))*wdict.get(x,0)*wdict.get(x+d,0)
            s2 += wdict.get(x,0)*wdict.get(x+d,0)
        if s2>0:
            acc += (s1/s2)**2; cnt += 1
    return float((acc/cnt)**0.5) if cnt>0 else 0.0

def U3_proxy(I,f,w)->float:
    # Crude monotone proxy for U^3 via triple shift correlations
    Imin, Imax = int(I[0]), int(I[-1])
    fdict = {n: f[i] for i,n in enumerate(I)}
    wdict = {n: w[i] for i,n in enumerate(I)}
    acc = 0.0; cnt = 0
    for d in range(1, max(2,(Imax-Imin)//3)):
        s1=s2=0.0
        for x in range(Imin, Imax-2*d+1):
            a = (fdict.get(x,0)-np.sum(f*w))
            b = (fdict.get(x+d,0)-np.sum(f*w))
            c = (fdict.get(x+2*d,0)-np.sum(f*w))
            ww = wdict.get(x,0)*wdict.get(x+d,0)*wdict.get(x+2*d,0)
            s1 += a*b*c*ww
            s2 += ww
        if s2>0:
            acc += (s1/s2)**2; cnt += 1
    return float((acc/cnt)**0.5) if cnt>0 else 0.0
