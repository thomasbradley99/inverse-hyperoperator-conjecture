# Inverse Hyperoperator Information Conjecture

**Conjecture:** If the inverse of an operator has branch rank *r* (independent branch parameters), then any globally continuous representation requires at least *r* extra real coordinates beyond the base value coordinates.

**First test case:** Inverse `z^z = w` has branch rank 2, predicting a minimum of 4 real dimensions.

## Repo Layout

- `conjecture/` — the conjecture statement and proof roadmap (LaTeX).
- `computational-gap-detection/` — numerical evidence: scripts, figures, and a LaTeX write-up of experiments.

## Current Evidence

- Closed loops in the `w`-plane produce open inverse paths in C (nontrivial monodromy).
- Two loops produce independent lift displacements (rank-2 shift matrix).
- Paths close after applying integer sheet shifts (deck-action closure).
- Results are stable across resolution.

## What Is Not Yet Proved

- Formal proof that monodromy group is exactly Z x Z.
- Global minimal-dimension proof (4D everywhere, not just tested loops).
- Whether the 4D structure must be quaternionic H or a more general covering-state model.

## Quickstart

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install numpy scipy matplotlib

# Run experiments
python computational-gap-detection/01_demo_inverse_z_to_z.py
python computational-gap-detection/02_path_completion_lift.py
python computational-gap-detection/03_closure_mod_sheet_shift.py
python computational-gap-detection/04_quotient_closure_demo.py

# Build documents
cd conjecture && pdflatex -interaction=nonstopmode conjecture.tex && cd ..
cd computational-gap-detection && pdflatex -interaction=nonstopmode computational-evidence.tex && cd ..
```
