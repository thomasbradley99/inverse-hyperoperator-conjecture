## Quaternion Super-Root Playground

This repo bundles two small scripts that support the ladder idea:

- `inverse_tetration_quaternion.py`: proves the hole in `ℂ` and shows the quaternion solution to `i^x = k`.
- `quaternion_power_tower.py`: experiments with finite-height power towers to see how quickly iterates leave the complex plane.
- `explore_superroot.py`: generates visualisations (heatmap + tower norms) to map where inverse exponentiation forces quaternion components.

### Environment

Assumes macOS with Python 3.9+ and `python3` on `PATH`.

Optional: install TeX Live (`brew install texlive`) if you want to compile the LaTeX note.

### Run the witness script

```bash
python3 inverse_tetration_quaternion.py
```

Expected highlight:

```
log(i) = (0.000000 + 1.570796i + 0.000000j + 0.000000k)
(log i) * j = (0.000000 + 0.000000i + 0.000000j + 1.570796k)
i^j = exp((log i) * j) = (0.000000 + 0.000000i + 0.000000j + 1.000000k)
Matches basis k? True
```

### Run the power-tower explorer

```bash
python3 quaternion_power_tower.py
```

Outputs tower levels for a few sample bases, plus the `i^j = k` witness.

### Generate visualisations

Install plotting deps locally (once):

```bash
pip3 install --target ./vendor numpy matplotlib
```

Then run with a headless backend:

```bash
MPLCONFIGDIR=./mplconfig MPLBACKEND=Agg python3 explore_superroot.py
```

This saves `superroot_heatmap.png` (magnitude of the quaternion component for exponents in `span{j,k}`) and `tower_norms.png` (growth/decay of quaternion magnitude across tower levels for representative bases).

### Build the write-up

```bash
pdflatex inverse_tetration_quaternion.tex
```

Requires a TeX distribution (TeX Live / MacTeX / Overleaf).

### Interpretation

1. Logic shows `z^z = 0` has no solution in `ℂ`.
2. Computation shows `i^x = k` has solution `x = j`, forcing a move to quaternions.

This is the rung that supports the ladder story: inverting exponentiation on the standard field reveals a hole that is naturally filled by `ℍ`.

