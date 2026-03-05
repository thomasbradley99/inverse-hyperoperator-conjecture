#!/usr/bin/env python3
"""
Show closure modulo sheet shift for inverse z^z = w.

Key idea:
- In C, tracked inverse endpoints after a closed loop are generally different.
- If we keep branch sheet indices (k, m), the endpoint is often explained by an
  integer sheet shift (Delta k, Delta m).
- We test whether z_end approximately equals slog(w0, k=Delta k, m=Delta m):
  this is a numerical "closure modulo deck shift" check.
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


def track_inverse_with_branch_indices(
    w_path: np.ndarray, k0: int = 0, m0: int = 0, search_radius: int = 2
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Track nearest inverse branch and record integer branch indices per step."""
    z_path = [slog(w_path[0], k=k0, m=m0)]
    k_path = [k0]
    m_path = [m0]
    current_k, current_m = k0, m0

    for i in range(1, len(w_path)):
        w = w_path[i]
        z_prev = z_path[-1]
        best_z = None
        best_d = np.inf
        best_k, best_m = current_k, current_m

        for dk in range(-search_radius, search_radius + 1):
            for dm in range(-search_radius, search_radius + 1):
                kc = current_k + dk
                mc = current_m + dm
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
        current_k, current_m = best_k, best_m

    return np.array(z_path), np.array(k_path), np.array(m_path)


def run_loop(w_path: np.ndarray, label: str) -> dict:
    z_path, k_path, m_path = track_inverse_with_branch_indices(w_path)
    z0 = z_path[0]
    zend = z_path[-1]
    delta_k = int(k_path[-1] - k_path[0])
    delta_m = int(m_path[-1] - m_path[0])

    raw_gap = abs(zend - z0)
    predicted_end = slog(w_path[0], k=delta_k, m=delta_m)
    sheet_residual = abs(zend - predicted_end)

    return {
        "label": label,
        "w_path": w_path,
        "z_path": z_path,
        "k_path": k_path,
        "m_path": m_path,
        "raw_gap": raw_gap,
        "delta_k": delta_k,
        "delta_m": delta_m,
        "predicted_end": predicted_end,
        "sheet_residual": sheet_residual,
    }


def main() -> None:
    n = 900
    t = np.linspace(0, 2 * np.pi, n)
    w_star = np.exp(-1 / np.e)

    loop_a = (w_star + 1e-4) + 0.40 * np.exp(1j * t)
    loop_b = 0.01 + 2.00 * np.exp(1j * t)

    res_a = run_loop(loop_a, "Loop A around w*")
    res_b = run_loop(loop_b, "Loop B around 0")
    results = [res_a, res_b]

    print("=" * 72)
    print("CLOSURE MODULO SHEET SHIFT (inverse of z^z = w)")
    print("=" * 72)
    for r in results:
        print(f"\n{r['label']}:")
        print(f"  raw gap in C: {r['raw_gap']:.6f}")
        print(f"  branch shift: (Delta k, Delta m) = ({r['delta_k']}, {r['delta_m']})")
        print(f"  closure residual after applying sheet shift: {r['sheet_residual']:.6e}")

    # Resolution stability check (requested often in discussion).
    print("\nResolution sweep:")
    for nn in [100, 200, 400, 800, 1600, 3200, 6400]:
        tt = np.linspace(0, 2 * np.pi, nn)
        la = (w_star + 1e-4) + 0.40 * np.exp(1j * tt)
        lb = 0.01 + 2.00 * np.exp(1j * tt)
        ra = run_loop(la, "A")
        rb = run_loop(lb, "B")
        print(
            f"  n={nn:>4} | A gap={ra['raw_gap']:.6f}, shift=({ra['delta_k']},{ra['delta_m']}), "
            f"resid={ra['sheet_residual']:.2e} | "
            f"B gap={rb['raw_gap']:.6f}, shift=({rb['delta_k']},{rb['delta_m']}), resid={rb['sheet_residual']:.2e}"
        )

    # Figure: clear two-panel explanation for Loop A.
    r = res_a
    fig = plt.figure(figsize=(14, 6))

    ax1 = fig.add_subplot(121)
    ax1.plot(r["z_path"].real, r["z_path"].imag, linewidth=2)
    ax1.plot(r["z_path"][0].real, r["z_path"][0].imag, "go", markersize=9, label="start")
    ax1.plot(r["z_path"][-1].real, r["z_path"][-1].imag, "r^", markersize=9, label="end")
    ax1.set_title(f"Tracked inverse in C (open)\nraw gap = {r['raw_gap']:.3f}")
    ax1.set_xlabel("Re(z)")
    ax1.set_ylabel("Im(z)")
    ax1.grid(True, alpha=0.3)
    ax1.legend(loc="best")

    ax2 = fig.add_subplot(122, projection="3d")
    ax2.plot(r["z_path"].real, r["z_path"].imag, r["m_path"], linewidth=2)
    ax2.plot([r["z_path"][0].real], [r["z_path"][0].imag], [r["m_path"][0]], "go", markersize=8)
    ax2.plot([r["z_path"][-1].real], [r["z_path"][-1].imag], [r["m_path"][-1]], "r^", markersize=8)
    ax2.set_title(
        "Same path with sheet coordinate m\n"
        f"Delta m = {r['delta_m']}, sheet-shift residual = {r['sheet_residual']:.2e}"
    )
    ax2.set_xlabel("Re(z)")
    ax2.set_ylabel("Im(z)")
    ax2.set_zlabel("m-sheet index")
    ax2.view_init(elev=23, azim=-56)

    fig.suptitle(
        "Open in C, but closes modulo integer sheet shift",
        fontsize=14,
        fontweight="bold",
    )
    out = "fig_closure_mod_sheet_shift.png"
    fig.tight_layout()
    fig.savefig(out, dpi=160, bbox_inches="tight")
    plt.close(fig)
    print(f"\nSaved {out}")


if __name__ == "__main__":
    main()
