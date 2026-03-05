# Computational Gap Detection

Numerical evidence for the inverse hyperoperator conjecture, focused on inverse `z^z = w`.

## Write-Up

- `computational-evidence.tex`: full LaTeX document covering problem setup, method, all four experiments, results, and limitations.

Build with:

```bash
pdflatex -interaction=nonstopmode computational-evidence.tex
```

## Scripts

Run from the repository root with the project venv active:

```bash
source .venv/bin/activate
python computational-gap-detection/01_demo_inverse_z_to_z.py
python computational-gap-detection/02_path_completion_lift.py
python computational-gap-detection/03_closure_mod_sheet_shift.py
python computational-gap-detection/04_quotient_closure_demo.py
```

| Script | What it does |
|---|---|
| `01_demo_inverse_z_to_z.py` | Single-loop branch-lift baseline |
| `02_path_completion_lift.py` | Two-loop monodromy test, lift coordinates |
| `03_closure_mod_sheet_shift.py` | Closure modulo integer sheet shift (deck-action check) |
| `04_quotient_closure_demo.py` | Summary figure — open in C, closed modulo sheets |

## Output Figures

- `inverse_z_to_z_demo.png`
- `fig_path_completion_lift.png`
- `fig_closure_mod_sheet_shift.png`
- `fig_04_quotient_closure_demo.png`
