# Exploration

Computational evidence and exploratory scripts for the inverse hyperoperator conjecture. None of this is proof — it's numerical experiments and visualizations.

## gap-detection/

The core evidence. Four scripts that trace the inverse of z^z around closed loops in the w-plane and show:

1. **01** — Single loop: the inverse path in C doesn't close (monodromy gap)
2. **02** — Two loops: each gives a different integer branch shift
3. **03** — The path closes if you allow the sheet shift (deck closure)
4. **04** — Summary figure with quotient residuals

Also includes a LaTeX write-up (`computational-evidence.pdf`) and a schematic (`schematic_2d_4d_quotient.py`).

```bash
python exploration/gap-detection/01_demo_inverse_z_to_z.py
```

## quaternion-state/

Embeds the 4D state (z, k, m) as a quaternion q = z + kj + mk and shows the path is open in H but closes in the quotient H/(Zj + Zk).

```bash
python exploration/quaternion-state/state_in_H.py
```

## quaternion-playground/

Separate from the monodromy experiments. Shows that i^j = k (exponentiation forces you out of C into H), power tower behavior, and superroot heatmaps.

```bash
python exploration/quaternion-playground/inverse_tetration_quaternion.py
```
