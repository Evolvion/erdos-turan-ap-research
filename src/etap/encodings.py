"""
ILP / OPB / WCNF emitters for max harmonic mass 3-AP-free problems.
"""
from __future__ import annotations
import math, pathlib

def edge_count(N:int)->int:
    D=(N-1)//2
    return D*(N-(D+1))

def emit_lp(N:int, tau:float|None=None, out_path:str|None=None)->str:
    HN = sum(1.0/m for m in range(1, N+1))
    w = [1.0/(n*HN) for n in range(1, N+1)]
    lines = []
    lines.append("Maximize")
    lines.append(" obj: " + " + ".join(f"{w[i]:.12f} x{i+1}" for i in range(N)))
    lines.append("Subject To")
    for d in range(1, (N-1)//2 + 1):
        for i in range(1, N-2*d+2):
            lines.append(f" c_{i}_{d}: x{i} + x{i+d} + x{i+2*d} <= 2")
    if tau is not None:
        lines.append(" mass: " + " + ".join(f"{w[i]:.12f} x{i+1}" for i in range(N)) + f" >= {tau:.12f}")
    lines.append("Bounds")
    for i in range(1, N+1):
        lines.append(f" 0 <= x{i} <= 1")
    lines.append("Binary")
    lines.append(" " + " ".join(f"x{i}" for i in range(1, N+1)))
    lines.append("End\n")
    content = "\n".join(lines)
    if out_path:
        pathlib.Path(out_path).write_text(content)
    return content

def emit_wcnf(N:int, tau:float|None=None, scale:int=int(1e6), out_path:str|None=None)->str:
    # Soft clauses are literals (x_n) with weights ~ harmonic mass; hard clauses enforce no 3-AP.
    HN = sum(1.0/m for m in range(1, N+1))
    w = [int(round(scale/(n*HN))) for n in range(1, N+1)]
    hard_weight = int(1e12)
    clauses = []
    # Hard 3-SAT clauses (~x_i v ~x_{i+d} v ~x_{i+2d})
    for d in range(1, (N-1)//2 + 1):
        for i in range(1, N-2*d+2):
            clauses.append((hard_weight, [-i, -(i+d), -(i+2*d)]))
    # Soft unit clauses (x_n)
    for i in range(1, N+1):
        clauses.append((w[i-1], [i]))
    top = hard_weight
    header = f"p wcnf {N} {len(clauses)} {top}"
    lines = [header] + [f"{wt} " + " ".join(map(str, lits)) + " 0" for wt, lits in clauses]
    content = "\n".join(lines)
    if out_path:
        pathlib.Path(out_path).write_text(content)
    return content
