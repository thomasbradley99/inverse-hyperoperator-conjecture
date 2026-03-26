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
python exploration/gap-detection/01_demo_inverse_z_to_z.py
python exploration/gap-detection/02_path_completion_lift.py
python exploration/gap-detection/03_closure_mod_sheet_shift.py
python exploration/gap-detection/04_quotient_closure_demo.py
python exploration/gap-detection/05_group_checks.py
python exploration/gap-detection/06_tracker_crosscheck.py
python exploration/gap-detection/07_domain_homotopy_checks.py
```

| Script | What it does |
|---|---|
| `01_demo_inverse_z_to_z.py` | Single-loop branch-lift baseline |
| `02_path_completion_lift.py` | Two-loop monodromy test, lift coordinates |
| `03_closure_mod_sheet_shift.py` | Closure modulo integer sheet shift (deck-action check) |
| `04_quotient_closure_demo.py` | Summary figure — open in C, closed modulo sheets |
| `05_group_checks.py` | Composition/winding checks for monodromy shifts (`A∘B`, `B∘A`, `2A`, `3B`, `A∘A^{-1}`), including order-sensitivity diagnostics |
| `06_tracker_crosscheck.py` | Compare monodromy shifts across two continuation trackers to detect potential tracker artifacts |
| `07_domain_homotopy_checks.py` | Compare winding vectors vs reduced based-loop words in a punctured domain, and correlate with measured shifts |

## Output Figures

- `inverse_z_to_z_demo.png`
- `fig_path_completion_lift.png`
- `fig_closure_mod_sheet_shift.png`
- `fig_04_quotient_closure_demo.png`
- `fig_05_group_checks.png`
- `fig_06_tracker_crosscheck.png`
- `fig_07_domain_homotopy_checks.png`

## Output Table

- `group_checks.csv` (shift vectors, gaps, and closure residuals for composition tests)
- `tracker_crosscheck.csv` (same cases compared across two tracker strategies)
- `domain_homotopy_checks.csv` (loop words, winding numbers, puncture distances, and measured shifts)
