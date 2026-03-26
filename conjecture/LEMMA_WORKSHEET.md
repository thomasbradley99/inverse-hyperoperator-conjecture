# Lemma Worksheet (Actionable)

Use this as the collaboration board for the near-term theorem in
`THEOREM_TARGET.md` / `FORMAL_FRAMEWORK.md`.

## Goal

Prove (on a clearly specified domain `U`) that inverse `z^z` requires at least
two extra real coordinates for faithful global continuous branch encoding.

---

## A. Domain and continuation setup

### A1. Specify admissible domain `U` and excluded set `Sigma`

- **Task:** define `U` explicitly (not just "avoid singular values").
- **Need:** a statement precise enough for `pi_1(U, w0)` and continuation.
- **Candidate tools:** critical values of `z^z`, branch-value geometry, covering-space setup.
- **Status:** open.

### A2. Continuation along paths is well-defined on `U`

- **Task:** prove local inverse germs can be continued along piecewise smooth paths in `U`.
- **Need:** theorem citation + hypotheses check.
- **Candidate tools:** analytic continuation and monodromy theorem.
- **Status:** open.

### A3. Loop action depends only on based homotopy class

- **Task:** make `rho: pi_1(U, w0) -> Perm(B)` precise.
- **Need:** branch set `B`, action definition, homotopy invariance proof/citation.
- **Status:** open.

---

## B. Monodromy/deck structure

### B1. Nontrivial monodromy exists

- **Task:** prove at least one loop changes branch.
- **Computational hint:** loop `A` gives `(0,1)` with near-zero deck residual.
- **Need (formal):** analytic continuation argument, not only numerics.
- **Status:** evidence strong, proof open.

### B2. Two independent branch actions exist

- **Task:** prove existence of two independent loop actions.
- **Computational hint:** `A -> (0,1)`, `B -> (1,0)`, winding-linearity passes.
- **Need (formal):** independence in the monodromy image, not just sampled loops.
- **Status:** evidence strong, proof open.

### B3. Clarify non-abelian vs abelianized structure

- **Task:** resolve why `A_then_B` and `B_then_A` differ in measured shifts.
- **Computational hint:** script `07` shows equal winding totals but different outputs;
  commutator shows nontrivial measured shift.
- **Need:** precise group-theoretic interpretation on chosen `U`.
- **Status:** active investigation.

---

## C. Global obstruction and dimension bound

### C1. No global single-valued inverse branch `U -> C`

- **Task:** prove nontrivial monodromy obstructs global continuous branch selection.
- **Need:** clean proposition with assumptions and contradiction argument.
- **Status:** open.

### C2. Define "faithful global encoding" rigorously

- **Task:** formal definition of state model that resolves branch ambiguity.
- **Need:** distinguish value coordinates vs branch coordinates.
- **Status:** open (definition draft needed first).

### C3. Show at least two independent branch coordinates are required

- **Task:** derive lower bound on encoding degrees of freedom from monodromy image.
- **Need:** bridge from branch-action rank to coordinate lower bound.
- **Status:** open.

### C4. Conclude `dim_R >= 4`

- **Task:** combine C2/C3 with complex output dimension 2.
- **Status:** open.

---

## D. Optional stronger track (later)

### D1. Quaternion uniqueness (`H`) vs generic `R^4` model

- **Task:** prove or disprove that algebra structure is forced, not just dimension.
- **Status:** explicitly deferred until C-track theorem is done.

---

## Suggested division of labor

- **Analytic continuation specialist:** A2, A3, C1.
- **Topology / covering-space specialist:** A1, B2, B3, C3.
- **Numerics / verification specialist:** strengthen B-track stress tests and
  attempt independent continuation implementations.

---

## Current computational anchors

- `exploration/gap-detection/03_closure_mod_sheet_shift.py`
- `exploration/gap-detection/05_group_checks.py`
- `exploration/gap-detection/06_tracker_crosscheck.py`
- `exploration/gap-detection/07_domain_homotopy_checks.py`

These scripts anchor plausibility and diagnostics; they are not formal proofs.
