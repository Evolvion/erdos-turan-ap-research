"""
Minimal CLI to exercise key functionalities.
"""
from __future__ import annotations
import argparse, sys, json, math, pathlib
import numpy as np
from .majorants import window_weights, power_tilt, lfc_rho_k
from .ap_counts import T3, T4, U2_estimate, U3_proxy
from .inequalities import v3_delta_eta, v4_delta_eta
from .encodings import emit_lp, emit_wcnf, edge_count

def parse_weight(arg, I, w):
    if arg.startswith("calibrated:"):
        t = float(arg.split("t=")[-1])
        wt = power_tilt(I, w, t)
        return wt
    return w

def cmd_balance(args):
    M = args.N//2
    I, w = window_weights(M)
    wt = parse_weight(args.weight, I, w) if args.weight else w
    # trivial "balancing" feedback — placeholder
    print(json.dumps({"N": args.N, "theta": args.theta, "delta_est": 0.01}, indent=2))

def cmd_apcount(args):
    M = args.N//2
    I, w = window_weights(M)
    wt = parse_weight(args.weight, I, w) if args.weight else w
    f = np.ones_like(I, dtype=float)  # toy uniform set for demo
    if args.k==3:
        T = T3(I,f,wt); mu = float(np.sum(f*wt)); r = U2_estimate(I,f,wt,samples=200)
        print(json.dumps({"k":3,"mu":mu,"T3":T,"U2_proxy":r}, indent=2))
    else:
        T = T4(I,f,wt); mu = float(np.sum(f*wt)); r = U3_proxy(I,f,wt)
        print(json.dumps({"k":4,"mu":mu,"T4":T,"U3_proxy":r}, indent=2))

def cmd_engine(args):
    # Spec-level placeholder: report chosen parameters and a mock AP found flag.
    M = args.window
    I, w = window_weights(M)
    wt = parse_weight(f"calibrated:t=-0.385", I, w)
    mu = float(np.sum(wt))
    print(json.dumps({"window":M,"k":args.k,"sigma":args.sigma,"Cr":args.Cr,"mu":mu,"status":"STRUCT-or-AP (demo)"}, indent=2))

def cmd_encode(args):
    if args.format=="lp":
        content = emit_lp(args.N, tau=args.tau, out_path=args.out)
    else:
        content = emit_wcnf(args.N, tau=args.tau, out_path=args.out)
    print(f"Wrote {args.format.upper()} to {args.out} ({len(content.splitlines())} lines)")
    print(f"Hard clause count (3-AP): {edge_count(args.N)}")

def cmd_selftest(_):
    # Lightweight consistency checks from the spec.
    assert edge_count(60)==870
    assert edge_count(80)==1560
    assert edge_count(120)==3540
    assert edge_count(200)==9900
    print("Self-test passed: clause counts OK.")

def main(argv=None):
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd")
    pb = sub.add_parser("balance")
    pb.add_argument("--N", type=int, required=True)
    pb.add_argument("--theta", type=float, default=0.2)
    pb.add_argument("--weight", type=str, default="harmonic")
    pb.set_defaults(func=cmd_balance)

    pa = sub.add_parser("apcount")
    pa.add_argument("--N", type=int, required=True)
    pa.add_argument("--k", type=int, default=3)
    pa.add_argument("--weight", type=str, default="harmonic")
    pa.set_defaults(func=cmd_apcount)

    pe = sub.add_parser("engine")
    pe.add_argument("--window", type=int, required=True)
    pe.add_argument("--k", type=int, default=3)
    pe.add_argument("--sigma", type=float, default=0.2)
    pe.add_argument("--Cr", type=float, default=2.0)
    pe.set_defaults(func=cmd_engine)

    pe2 = sub.add_parser("encode")
    pe2.add_argument("--N", type=int, required=True)
    pe2.add_argument("--format", choices=["lp","wcnf"], default="lp")
    pe2.add_argument("--tau", type=float, default=None)
    pe2.add_argument("--out", type=str, required=True)
    pe2.set_defaults(func=cmd_encode)

    pt = sub.add_parser("selftest")
    pt.set_defaults(func=cmd_selftest)

    args = p.parse_args(argv)
    if not hasattr(args, "func"):
        p.print_help(); return 1
    args.func(args)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
