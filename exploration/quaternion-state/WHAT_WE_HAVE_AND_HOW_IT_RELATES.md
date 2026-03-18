# What We Have Here (quaternion-state) and How It Relates

## Where is the superlogarithm, and how does this relate to it?

The **superlogarithm** (in this project) is the **inverse of z^z**: the operator that takes *w* and returns *z* such that z^z = w. So:

- **Forward map:** z → w = z^z (exponentiation/tetration level).
- **Inverse = superlogarithm:** w → z with z^z = w.

**Where it appears in the repo:**

| Place | How the superlog appears |
|-------|---------------------------|
| **Conjecture** (`../conjecture/`) | States that the *inverse* of z^z (the superlog) has branch rank 2 and so needs 4D; predicts ℍ. |
| **Computational scripts** (`../computational-gap-detection/`) | We **evaluate** the superlog along closed loops in *w*: at each *w*(t) we pick a preimage *z*(t) with z^z = w. So we are literally following the superlog along a path in its **input** space (w). The **output** of the superlog is *z*; that’s where we see the gap (path in *z* doesn’t close). |
| **Quaternion-state** (this folder) | We take that same output — the superlog’s value *z* plus the branch (k, m) we’re on — and write it as a quaternion. So we’re looking at the **output space** of the superlog: not just *z* (2D) but (z, k, m) (4D), and we embed that in ℍ. |

**How it all ties together:** We loop in the **input** to the superlog (w). The **output** of the superlog is multivalued (many *z* for one *w*). We track one branch and get a path in (z, k, m). That path is open in ℂ (gap), open in ℍ, and closed in the quotient. The conjecture says the superlog’s “full” output space should be 4D (and maybe ℍ); the computations and this folder illustrate that.

---

## The big picture

1. **Conjecture:** Inverse z^z needs 4 real dimensions (branch rank 2). The stronger form says that 4D space is ℍ (quaternions).

2. **Computational evidence** (in `../computational-gap-detection/`): We show that if you only use 2D (the complex number z), the path **does not close** — there’s a gap. Two integers (Δk, Δm) fix it: the path **closes modulo sheets**. So we need more than ℂ; the natural extra state is two branch indices → 4D total.

3. **Quaternion-state** (this folder): We **represent** that 4D state as a quaternion and check how the path behaves in ℍ and in the quotient. We do **not** prove that 4D is necessary or that it must be ℍ.

---

## What’s in this folder

| Item | What it is |
|------|------------|
| **state_in_H.py** | Runs the same loop as the computational scripts, builds the 4D state (Re z, Im z, k_lift, m_lift), and prints that the displacement in ℍ is (complex gap) + (Δk)j + (Δm)k. |
| **path_in_H.png** | One 3D view of the path in ℍ (Re z, Im z, k_lift; colour = m_lift). The path is **open**: start and end are different points. |
| **fig_open_in_H_closed_in_quotient.py** | Builds a **two-panel figure**. |
| **fig_open_in_H_closed_in_quotient.png** | **Left:** Path in ℍ (3D) — **open** (green start, red end). **Right:** Path in the (k, m) part only — **closed**: we add one short “identification” segment from end back to start in (k_lift, m_lift), so you see one closed loop. |

---

## What the two panels mean

- **Left panel (path in H):**  
  The full state is q = Re z + Im z·i + k·j + m·k. We draw it in 3D (Re z, Im z, k_lift) with colour = m_lift. The curve does **not** return to its starting point: **open in ℍ**.

- **Right panel (path in quotient):**  
  We only draw the **(k_lift, m_lift)** part of the state. The path goes from (0,0) to (0,1). In the **quotient** we say “(0,1) is the same as (0,0)” (same sheet index mod ℤ). So we draw one extra segment from (0,1) back to (0,0). That gives **one closed loop** in the (k, m) plane. So: **in the quotient, the (k,m)-part of the path closes**.

The **full** quotient (ℍ modulo the lattice ℤj + ℤk) also identifies the z-part (via the deck action). So in the full quotient the whole path closes; we only draw the (k,m) part so the “closed” picture is simple and not one long line.

---

## How this relates to the conjecture

- **“Need 4D”:** That’s argued in **computational-gap-detection** (gap in ℂ, two independent shifts). This folder **uses** that 4D state; it doesn’t prove we need it.

- **“4D = ℍ”:** We **embed** the 4D state in ℍ (q = z + k j + m k) and see that the deck action is translation in the (j,k)-plane. So the story **fits** ℍ. We do **not** prove that the algebra must be ℍ; we only show it’s a natural 4D home.

- **“Path closes in quotient”:** The computational doc already shows closure modulo sheets (same idea). Here we draw it explicitly: **open in ℍ**, **closed** when we add the identification in (k,m) (and in the full quotient, the z-part is identified too).

---

## One-sentence summary

**We take the 4D state from the computational experiments, put it in ℍ, show the path is open in ℍ and closed in the (k,m) quotient (and hence in the full quotient), and so make the “4D and quaternions” part of the conjecture concrete — without proving that 4D or ℍ are forced.**
