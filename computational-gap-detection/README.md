# Computational Gap Detection

This folder centralizes computational evidence experiments for the inverse-hyperoperator conjecture around `z^z = w`.

## Scripts

- `01_demo_inverse_z_to_z.py`: baseline single-loop branch-lift demo.
- `02_path_completion_lift.py`: two-loop monodromy test with non-interpolated lift coordinates.
- `03_closure_mod_sheet_shift.py`: tests closure modulo integer sheet shift (deck-action style check).
- `04_quotient_closure_demo.py`: clear "open in C / closed modulo sheets" summary figure + metrics.

## Run With Project venv

From the repository root:

```bash
source .venv/bin/activate
python computational-gap-detection/01_demo_inverse_z_to_z.py
python computational-gap-detection/02_path_completion_lift.py
python computational-gap-detection/03_closure_mod_sheet_shift.py
python computational-gap-detection/04_quotient_closure_demo.py
```

## Outputs

- `inverse_z_to_z_demo.png`
- `fig_path_completion_lift.png`
- `fig_closure_mod_sheet_shift.png`
- `fig_04_quotient_closure_demo.png`

## Key Interpretation

`03_closure_mod_sheet_shift.py` does not claim the path closes as a point in plain `R^4`.
It shows a stronger and more precise statement: endpoints are equal after applying the
integer sheet shift `(Delta k, Delta m)` found by branch tracking (closure modulo sheets).
