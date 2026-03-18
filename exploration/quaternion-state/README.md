# Quaternion State: Testing Whether the 4D Output Is ℍ

**Confused what we have and how it relates?** → **[WHAT_WE_HAVE_AND_HOW_IT_RELATES.md](WHAT_WE_HAVE_AND_HOW_IT_RELATES.md)**

---

The conjecture says inverse z^z needs 4 real dimensions; the stronger form says that 4D space is the **normed division algebra ℍ**, not just ℝ⁴. This folder explores that step.

## Embedding the state in ℍ

The tracked state is: a complex number *z* (inverse value) plus branch indices *(k, m)* ∈ ℤ×ℤ (or continuous lifts *k_lift*, *m_lift*). So we have 4 real numbers: (Re *z*, Im *z*, *k*, *m*).

**Quaternion embedding:** Identify ℍ = span{1, i, j, k} over ℝ and set

- **q = (Re z) + (Im z) i + k j + m k**

So the "complex" part of the inverse lives in the 1–i plane; the two branch indices live in the j–k plane. The deck group (going around loops) adds integer multiples of j and k: **q ↦ q + (Δk) j + (Δm) k** (plus the z-part changes by the inverse map). So the discrete branch structure is **translation in the (j, k) plane** of ℍ.

## What we actually show in H

- **The path does *not* close in ℍ.** After one loop, q_end = q_start + (complex gap) + (Δk)j + (Δm)k, so the 4D point is different.
- **Closure is in the quotient.** If we quotient ℍ by the lattice ℤj + ℤk (identify q and q + n j + m k for integers n, m), then start and end differ only by the complex gap; and we already know from `computational-gap-detection/` that the complex gap is exactly the sheet-shifted preimage, so **modulo the deck action the path closes**. So: open in ℍ, closed in ℍ/(deck lattice).
- **The graph `path_in_H.png`** is a 3D view of the path in ℍ: axes = Re(z), Im(z), k_lift (j-component), colour = m_lift (k-component). So you see the state moving through ℍ as we go around the loop; the path is a spiral/curve that does not return to its starting point in 4D, but the (j,k) part of the displacement is exactly (Δk, Δm), so the *branch* part of the motion is clean translation in the j–k plane.

That already gives a **natural 4D home**: the state space is ℍ, and the deck action is translation by a lattice in the (j, k)-plane. So "outputs live in the quaternion plane" can be given a precise meaning: **state = quaternion, branch = (j, k) components.**

## What would show "outputs only fully describable in ℍ"?

1. **Minimum (what we do here):** Show the 4D state embeds cleanly in ℍ and the deck action is translation in (j, k). So the *geometry* of the covering space matches ℍ with a distinguished (j, k) plane.
2. **Stronger:** Show that when you *compose* paths or compare different loops, the transition maps behave like (left or right) multiplication by a **unit quaternion** — so the dynamics respect the quaternion product, not just the linear structure.
3. **Strongest:** Show that the only 4D algebra that supports both the inverse map and the observed monodromy is ℍ (e.g. by ruling out other 4D real algebras). That would be an algebraic/structural argument, not just numerics.

This folder only does (1): embed state in ℍ, visualise the path in ℍ, and check that the displacement q_end − q_start decomposes as (complex gap) + (Δk) j + (Δm) k.

## Script

- **`state_in_H.py`** — Runs the same two loops as in `computational-gap-detection/`, represents each state as a quaternion q = Re z + Im z i + k_lift j + m_lift k, and:
  - Plots the path in ℍ (3D projections).
  - Verifies that the (j, k) part of q_end − q_start equals the integer shift (Δk, Δm), so the deck action is translation in the (j, k)-plane.

Run from repo root (needs numpy, scipy, matplotlib):

```bash
source .venv/bin/activate
python quaternion-state/state_in_H.py
```

Output:
- `path_in_H.png` — 3D view of the path in ℍ (open).
- `fig_open_in_H_closed_in_quotient.png` — **two-panel figure**: left = path in H (open, start ≠ end); right = path in quotient H/(ℤj+ℤk) (closed, with identification segment from end to start). Same style as the computational-gap-detection figures.

Regenerate: `python quaternion-state/fig_open_in_H_closed_in_quotient.py`
