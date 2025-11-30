# ET-AP Research Artifacts

This repository accompanies a research program toward the Erdős–Turán conjecture on arithmetic progressions (ET-AP) using **weighted transference**, **learned majorants**, **Fourier-based density increments**, and **algorithmic certificates**.

Key artifacts:
- δ,η-robust von Neumann–type inequalities (k=3,4,5).
- Power-tilt calibration to satisfy linear-forms constraints (LFC).
- √T₃ pruning bound and constructive deletion scheme.
- Dyadic-window engine that either finds a 3-AP or outputs a structure certificate.
- ILP / MaxSAT encodings for max harmonic mass of 3-AP-free sets with certified witnesses.

## Quickstart
```bash
make venv
make install
make reproduce           # demo engine on a small window
make test                # run spec-level tests (no heavy numerics)
make paper               # build the LaTeX preprint (requires LaTeX)
```

## CLI examples
```bash
python -m etap.cli balance --N 1000 --theta 0.2 --mode vertex --target-delta 0.01
python -m etap.cli apcount --N 512 --k 3 --weight calibrated:t=-0.385
python -m etap.cli engine --window 2048 --k 3 --sigma 0.2 --Cr 2
python -m etap.cli encode --N 60 --format lp --tau 0.46 --out M3N60.lp
```
