# Inverse Hyperoperator Conjecture

Every time we invert a hyperoperator, the answer doesn't fit in the current number system — we're forced into a bigger one. The conjecture says this pattern continues into the quaternions.

## The pattern

| Level | Inverse of | What goes wrong | Extension |
|-------|-----------|-----------------|-----------|
| 1 | addition | 3 − 5 has no natural number answer | **Z** (negatives) |
| 2 | multiplication | 1 ÷ 3 has no integer answer | **Q** → **R** (fractions, limits) |
| 3 | exponentiation | log needs a branch choice (phase) | **C** (complex numbers) |
| 4 | z^z / tetration | inverse needs *two* branch choices | **H**? (quaternions) |

Levels 1–2 are algebraic. From level 3 onward the obstruction is *monodromy*: follow the inverse around a closed loop and you end up on a different branch.

## The conjecture (one sentence)

> If the inverse of a holomorphic operator has **branch rank r** (r independent integer branch parameters under analytic continuation), then any globally continuous single-valued representation of the full inverse needs at least **r extra real coordinates**.

For complex-valued outputs that means dim_R >= 2 + r.

## First prediction: inverse of z^z

The map w = z^z = exp(z log z) has two independent sources of multivaluedness in its inverse:

- a **log branch** k in Z
- a **Lambert-W branch** m in Z

So r = 2, and the conjecture predicts **dim_R >= 4**. The only 4-dimensional normed division algebra (Hurwitz, 1898) is the **quaternions H**.

### Stronger form

The general conjecture only predicts a dimension bound. The stronger form predicts the extensions land exactly on the normed division algebras: R → C → H — not just any space of the right dimension, but the specific algebra forced by the monodromy structure.

## What's in this repo

```
conjecture/          The formal statement (LaTeX paper + proof roadmap)
exploration/         All computational evidence and exploratory scripts
  gap-detection/     Monodromy experiments for inverse z^z (5 scripts)
  quaternion-state/  Embedding the 4D state in H, deck-action figures
  quaternion-playground/  i^j = k witness, power towers, heatmaps
```

## Quick start

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install numpy scipy matplotlib
```

### 1. See the monodromy gap

```bash
python exploration/gap-detection/01_demo_inverse_z_to_z.py
```

Draws a closed circle in the w-plane (w = z^z), then at each point along that circle finds the inverse z (i.e. solves z^z = w) by picking whichever branch (k, m) gives the z closest to the previous step. Plots the resulting path of z values. The punchline: even though the loop in w closes perfectly, **the path in z does not come back to where it started** — there's a visible gap. That gap is monodromy. One complex number can't keep track of which branch you're on.

Outputs: `inverse_z_to_z_demo.png` (left: open path in C, right: lifted 3D view) and prints the gap size.

### 2. See two independent branch shifts

```bash
python exploration/gap-detection/03_closure_mod_sheet_shift.py
```

Runs the same tracking on **two different loops** — Loop A circles a critical point w* = e^(-1/e), Loop B circles the origin. For each loop it records not just z but the integer branch indices (k, m) chosen at each step. The result:

- **Loop A** shifts branch indices by (Δk, Δm) = (0, 1) — only the Lambert-W branch changes
- **Loop B** shifts by (Δk, Δm) = (1, 0) — only the log branch changes

These are **independent**. And the residual after applying the sheet shift is ~10^-17 (machine epsilon), meaning the path **closes exactly once you account for the branch jump**. Also runs a resolution sweep (n = 100 to 6400) to show the shifts are stable — not numerical artifacts.

Outputs: `fig_closure_mod_sheet_shift.png` and a console table of gaps/shifts/residuals.

### 3. Run composition/winding group checks

```bash
python exploration/gap-detection/05_group_checks.py
```

Checks loop composition and winding behavior (`A∘B`, `B∘A`, `2A`, `3B`, `A∘A^{-1}`), then writes a machine-readable table and summary plot.

Outputs: `group_checks.csv`, `fig_05_group_checks.png`.

### 4. See the 4D state in quaternions

```bash
python exploration/quaternion-state/state_in_H.py
```

Takes the same two loops but now packs each point's state into a quaternion: q = Re(z) + Im(z)**i** + k_lift**j** + m_lift**k**, where k_lift and m_lift are continuous (unwrapped) versions of the branch indices. Plots the path in 3D slices of H (axes: Re z, Im z, k_lift; color: m_lift). The punchline: **the path doesn't close in H** (q_end != q_start, because the j/k components shifted by ~1). But if you identify points that differ by integer multiples of j and k — i.e. quotient out the lattice Zj + Zk — the path closes. So the 4D state lives naturally in H, and the monodromy action is translation in the (j, k)-plane.

Outputs: `path_in_H.png` (two 3D scatter plots, one per loop) and prints the quaternion displacement for each loop.

## Status

This is a **conjecture with numerical evidence**, not a proof. The experiments show the monodromy gap, two independent branch shifts, and deck closure — they do not prove the dimension bound or that H is required. The write-ups say this explicitly. See `conjecture/PROOF_STEPS.md` and `conjecture/THEOREM_TARGET.md` for the current proof roadmap.
