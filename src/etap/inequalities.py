"""
Inequality checks: (V3-δ,η), (V4-δ,η), generic (Vk-δ) skeleton.
"""
from __future__ import annotations
import math

def v3_delta_eta(mu: float, r: float, delta: float, eta: float, T3: float) -> float:
    rhs = 4*mu*(r**2) + 2*(r**3) + 12*delta + 6*eta
    return rhs - abs(T3 - mu**3)

def v4_delta_eta(mu: float, r: float, delta_v: float, delta_p: float, eta: float, T4: float) -> float:
    rhs = 8*mu*(r**3) + 4*(r**4) + 20*(delta_v + delta_p + eta)
    return rhs - abs(T4 - mu**4)

def vk_delta_template(k: int, mu: float, r: float, deltas_sum: float, T: float, Ck: float=2.0, Ckprime: float=2.0) -> float:
    # Coarse instantiation of (Vk-δ) residual; user can tune constants.
    poly = 0.0
    for j in range(2, k+1):
        # binomial coefficient absorbed into Ck
        poly += mu**(k-j) * r**(j-1)
    rhs = Ck*poly + Ckprime*deltas_sum
    return rhs - abs(T - mu**k)
