# Conclusion Status (Current)

This is the plain status snapshot after the new exploration scripts
`05_group_checks.py`, `06_tracker_crosscheck.py`, and
`07_domain_homotopy_checks.py`.

## What is now established (computationally)

1. **Monodromy gap in `C` is reproducible**  
   Closed loops in `w` produce open tracked inverse paths in `z`.

2. **Two independent branch shifts are observed**
   - Loop `A` gives `(Delta k, Delta m) = (0,1)`
   - Loop `B` gives `(Delta k, Delta m) = (1,0)`

3. **Deck closure is numerically exact (machine precision)**  
   After applying the measured integer sheet shift, closure residuals are near
   zero (`~1e-17` to `0` in tested cases).

4. **Winding linearity tests pass**
   - `2A -> (0,2)`
   - `3B -> (3,0)`
   - `A + A^{-1} -> (0,0)`

5. **Order-sensitive composition appears in tested setup**
   - `A_then_B -> (1,1)`
   - `B_then_A -> (1,0)`

6. **Tracker cross-check did not remove the order effect**  
   Both continuation variants (`nearest`, `lift_guided`) returned the same
   order-sensitive outputs in script `06`.

7. **Abelian winding totals alone are insufficient**  
   Script `07` shows:
   - `A_then_B` and `B_then_A` have the same winding vector but different shifts.
   - The commutator `A B A^{-1} B^{-1}` has zero total winding yet nontrivial
     measured shift `(0,1)` in this setup.

## What this means

- The data strongly supports that branch behavior is controlled by **based-loop
  class / continuation order**, not just by simple winding counts.
- The computational story is now significantly stronger than "two loops gave
  two shifts": it includes composition, cancellation, tracker cross-checking,
  and homotopy diagnostics.

## What is still open

1. **Formal theorem not yet proved**  
   The conjecture remains unproved.

2. **Dimension lower bound still needs formalization**  
   Need a rigorous argument from monodromy/deck structure to
   `dim_R >= 4` for global faithful encoding.

3. **Quaternion necessity is still open**  
   Current work shows a natural quaternion representation, not uniqueness of `H`.

4. **Potential continuation artifacts still need deeper elimination**  
   Even with tracker cross-check, additional certified continuation methods would
   strengthen confidence.

## Current best theorem target

See `conjecture/THEOREM_TARGET.md`:

- prove rank-2 monodromy/deck action on a chosen domain;
- conclude no global single-valued inverse map into `C` can represent full branch behavior continuously;
- conclude at least two extra real coordinates are required (total at least 4).

## Bottom line

This repository now contains:

- a clear conjecture statement,
- reproducible computational evidence that is materially stronger than before,
- and a concrete theorem roadmap.

It does **not** yet contain a full proof or a proof that quaternion structure is forced.
