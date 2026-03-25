# Theorem Target (Near-Term)

This note pins down a realistic theorem to prove now, before the stronger
"must be quaternionic" claim.

## Target theorem

Work on a domain `U` in the `w`-plane that avoids the singular-value set of
`z^z` and supports analytic continuation of inverse branches along loops.

If the induced deck/monodromy action on inverse branches over `U` has rank 2
(two independent integer generators), then:

1. there is no globally continuous single-valued inverse into `C` that
   represents all branches; and
2. any faithful global continuous encoding of full branch state requires at
   least 2 extra real coordinates beyond `Re/Im`, i.e. at least 4 real
   coordinates total.

## Why this is the right next theorem

- It matches what the computations are already testing (`Delta k`, `Delta m`).
- It avoids overclaiming algebra structure (does not yet require `H`).
- It would formalize the main dimension claim in a checkable way.

## Proof skeleton

### Lemma A (nontrivial monodromy)

Show there exists a loop `gamma` in `U` such that analytic continuation of an
inverse branch along `gamma` returns to a different branch.

Consequence: a global single branch cannot be continuous on all loop classes.

### Lemma B (independence)

Show two loops `gamma_1`, `gamma_2` induce independent branch shifts, giving a
rank-2 subgroup of deck transformations.

Consequence: branch state contains at least two independent integer parameters.

### Proposition C (no global complex inverse branch)

From Lemma A: a single-valued globally continuous inverse `U -> C` cannot
represent all analytic continuations.

### Proposition D (dimension lower bound)

From Lemma B: any faithful continuous global state model must carry two
independent branch coordinates in addition to `Re/Im` of value coordinates.
Therefore `dim_R >= 4`.

## What remains open after this theorem

- Whether the 4D state must be specifically quaternionic (`H`) rather than an
  arbitrary 4D real model with equivalent deck bookkeeping.
- Whether stronger algebraic constraints force the Hurwitz ladder
  `R -> C -> H` uniquely.
