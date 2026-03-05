# Steps Toward Proof

This file is the simple roadmap from "interesting computation" to "checkable theorem."

## Conjecture (Simple Form)

For inverse `z^z = w`, branch state cannot be encoded globally by complex output alone.
At least two extra real coordinates are needed to track branch information continuously.

## What Is Already Done

1. Reproducible loops around `w*` and `0`.
2. Stable nonzero endpoint gap in `C`.
3. Integer branch-shift bookkeeping.
4. Closure modulo sheet shift with near-zero residual.
5. Rank-2 measured shift matrix from two loops.

## What To Prove Next

1. **Monodromy existence (formal):** prove nontrivial deck action for inverse `z^z`.
2. **Independence (formal):** prove at least two independent branch generators in a domain.
3. **Lower bound:** prove any global continuous state model needs at least `2 + 2 = 4` real coordinates.
4. **Structure question:** determine whether this 4D model must be quaternionic `H` or can be a more general 4D covering-state model.

## Minimal Theorem Skeleton

- **Lemma A:** There exists a loop in `w` whose analytic continuation changes inverse branch.
- **Lemma B:** There exist two loops with independent branch action.
- **Proposition C:** No single-valued global inverse map into `C` can represent all branches continuously.
- **Proposition D:** Any global continuous encoding needs at least 4 real coordinates.
- **Conjecture E (stronger):** The natural 4D encoding is quaternionic.

## Public-Facing Honesty Line

Current repository status: strong computational evidence and a clear monodromy pattern, but not yet a complete formal proof.
