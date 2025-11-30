"""
Dyadic windows and summable threshold schedules τ_k(M).
"""
from __future__ import annotations
import math

def tau_k(M:int, sigma:float, Ck:float)->float:
    return Ck * (math.log(M)**(-(1+sigma)))

def freq_lemma(mu_list, tau_list)->bool:
    # Returns True if infinitely many windows are dense (heuristic finite check)
    return any(mu >= tau for (mu,tau) in zip(mu_list, tau_list))
