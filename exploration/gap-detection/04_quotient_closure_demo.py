#!/usr/bin/env python3
"""
Quotient-closure demonstration for inverse z^z = w.

Goal:
- Show the tracked inverse path is open in C.
- Show endpoints are equivalent under integer sheet shift (deck action),
  i.e. closed in the sheet-quotient sense.
"""

import numpy as np
from scipy.special import lambertw
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


def slog(w: complex, k: int = 0, m: int = 0) -> complex:
    c = np.log(w + 0j) + 2j * np.pi * k
    u = lambertw(c, k=m)
    return np.exp(u)


def track_with_indices(
    w_path: np.ndarray, k0: int = 0, m0: int = 0, search_radius: int = 2
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Nearest-neighbor continuation with integer branch bookkeeping."""
    z_path = [slog(w_path[0], k=k0, m=m0)]
    k_path = [k0]
    m_path = [m0]
    ck, cm = k0, m0

    for i in range(1, len(w_path)):
        w = w_path[i]
        z_prev = z_path[-1]
        best_z = None
        best_d = np.inf
        best_k, best_m = ck, cm

        for dk in range(-search_radius, search_radius + 1):
            for dm in range(-search_radius, search_radius + 1):
                kc = ck + dk
                mc = cm + dm
                try:
                    zc = slog(w, k=kc, m=mc)
                except Exception:
                    continue
                if not np.isfinite(zc):
                    continue
                d = abs(zc - z_prev)
                if d < best_d:
                    best_d = d
                    best_z = zc
                    best_k, best_m = kc, mc

        if best_z is None:
            best_z = z_prev

        z_path.append(best_z)
        k_path.append(best_k)
        m_path.append(best_m)
        ck, cm = best_k, best_m

    return np.array(z_path), np.array(k_path), np.array(m_path)


def analyze_loop(w_path: np.ndarray, label: str) -> dict:
    z_path, k_path, m_path = track_with_indices(w_path)
    z0 = z_path[0]
    zend = z_path[-1]
    dk = int(k_path[-1] - k_path[0])
    dm = int(m_path[-1] - m_path[0])

    # Raw C-space non-closure.
    raw_gap = abs(zend - z0)

    # Endpoint on shifted sheet predicted at same basepoint w0.
    shifted_endpoint = slog(w_path[0], k=dk, m=dm)

    # Quotient-closure residual: zero means endpoint class equals start class.
    quotient_residual = abs(zend - shifted_endpoint)

    return {
        "label": label,
        "w_path": w_path,
        "z_path": z_path,
        "k_path": k_path,
        "m_path": m_path,
        "raw_gap": raw_gap,
        "dk": dk,
        "dm": dm,
        "quotient_residual": quotient_residual,
    }


def main() -> None:
    n = 1200
    t = np.linspace(0, 2 * np.pi, n)
    w_star = np.exp(-1 / np.e)

    loop_a = (w_star + 1e-4) + 0.40 * np.exp(1j * t)
    loop_b = 0.01 + 2.00 * np.exp(1j * t)

    res_a = analyze_loop(loop_a, "Loop A around w*")
    res_b = analyze_loop(loop_b, "Loop B around 0")

    print("=" * 74)
    print("QUOTIENT-CLOSURE CHECK (inverse of z^z = w)")
    print("=" * 74)
    for r in [res_a, res_b]:
        print(f"\n{r['label']}:")
        print(f"  raw gap in C: {r['raw_gap']:.6f}")
        print(f"  sheet shift (Delta k, Delta m): ({r['dk']}, {r['dm']})")
        print(f"  quotient residual: {r['quotient_residual']:.6e}")

    fig = plt.figure(figsize=(14, 10))
    loops = [res_a, res_b]
    for row, r in enumerate(loops, start=1):
        ax = fig.add_subplot(2, 2, 2 * row - 1)
        z = r["z_path"]
        ax.plot(z.real, z.imag, linewidth=2)
        ax.plot(z[0].real, z[0].imag, "go", markersize=8, label="start")
        ax.plot(z[-1].real, z[-1].imag, "r^", markersize=8, label="end")
        ax.set_title(f"{r['label']}: open path in C (gap={r['raw_gap']:.3f})")
        ax.set_xlabel("Re(z)")
        ax.set_ylabel("Im(z)")
        ax.grid(True, alpha=0.3)
        ax.legend(loc="best")

        ax = fig.add_subplot(2, 2, 2 * row)
        msg = (
            f"{r['label']}\n\n"
            f"Raw gap in C: {r['raw_gap']:.6f}\n"
            f"Sheet shift: (Delta k, Delta m) = ({r['dk']}, {r['dm']})\n"
            f"Quotient residual: {r['quotient_residual']:.3e}\n\n"
            "Interpretation:\n"
            "Endpoint differs as a point in C,\n"
            "but matches after sheet identification."
        )
        ax.text(0.03, 0.95, msg, va="top", ha="left", fontsize=11)
        ax.axis("off")

    fig.suptitle(
        "Open in C, closed modulo sheet equivalence",
        fontsize=14,
        fontweight="bold",
    )
    fig.tight_layout()
    out = "fig_04_quotient_closure_demo.png"
    fig.savefig(out, dpi=170, bbox_inches="tight")
    plt.close(fig)
    print(f"\nSaved {out}")


if __name__ == "__main__":
    main()
