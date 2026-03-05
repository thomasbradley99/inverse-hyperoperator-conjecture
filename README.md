# Inverse Hyperoperator Information Conjecture

Simple statement:

For inverse `z^z = w`, branch information is not fully representable in complex output coordinates alone. A continuous global model appears to require extra real coordinates for branch state (empirically suggesting 4 real dimensions total).

## Repo Layout (Simple)

- `conjecture/`: conjecture statement, current evidence write-up, and proof roadmap.
- `computational-gap-detection/`: exploration scripts and generated figures.

## Current Evidence (What We Actually Show)

- Closed loops in the `w`-plane produce nonzero endpoint gaps in tracked inverse paths in `C`.
- Gaps are stable across resolution and align with integer branch shifts.
- Two tested loops produce independent measured lift shifts (rank 2 matrix).
- Endpoints match after applying sheet shift (closure modulo sheets), with near-zero residual.

## What Is Not Yet Proved

- Global proof that monodromy is exactly `Z x Z`.
- Global minimal-dimension proof (`4D` everywhere, not only tested loops).
- Proof that the required 4D structure must be quaternion algebra `H` (vs a general 4D covering-state model).

## Quickstart

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install numpy scipy matplotlib

python computational-gap-detection/01_demo_inverse_z_to_z.py
python computational-gap-detection/02_path_completion_lift.py
python computational-gap-detection/03_closure_mod_sheet_shift.py
python computational-gap-detection/04_quotient_closure_demo.py

cd conjecture
pdflatex -interaction=nonstopmode conjecture.tex
```

## Output Figures

- `computational-gap-detection/inverse_z_to_z_demo.png`
- `computational-gap-detection/fig_path_completion_lift.png`
- `computational-gap-detection/fig_closure_mod_sheet_shift.png`
- `computational-gap-detection/fig_04_quotient_closure_demo.png`

## One-Line Summary

The inverse of `z^z` is open as a path in `C` for tested loops, but closes modulo integer sheet shifts; this is strong computational evidence for extra branch-state coordinates, not yet a full algebraic proof.
