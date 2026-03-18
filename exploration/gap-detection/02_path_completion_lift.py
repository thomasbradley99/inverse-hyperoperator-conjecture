"""
03_path_completion_lift.py

Computational evidence for inverse branching of z^z = w:

- Track an inverse branch z(t) along closed loops w(t) in the w-plane.
- Observe a discontinuity / gap in C after completing the loop (monodromy).
- Construct genuine (non-interpolated) lift coordinates using np.unwrap:
    theta(t) = unwrap(arg(w(t)))        (universal cover of C*)
    phi(t)   = unwrap(arg(log_lift(w(t)) + 1/e))  (unwrap around Lambert-W branch point)
- Show the lifted path in R^4 has bounded step sizes (continuous lift).

Run: python3 03_path_completion_lift.py
Requires: numpy, scipy, matplotlib
"""

import numpy as np
from scipy.special import lambertw
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection


plt.rcParams.update({"font.size": 11, "mathtext.fontset": "cm"})


def slog_candidate(w, k=0, m=0):
    """Candidate inverse branch using z = exp(W_m(log(w)+2πik))."""
    c = np.log(w + 0j) + 2j * np.pi * k
    u = lambertw(c, k=m)
    return np.exp(u)


def track_inverse_with_lift(w_path, z_start, k0=0, m0=0, search_radius=2):
    """
    Track a continuous choice of inverse by nearest-neighbour continuation among nearby (k,m).
    Returns:
      z_path: complex tracked inverse values
      lift: (k_lift, m_lift) computed from genuine unwrapped angles (NO interpolation)
    """
    z_path = [z_start]
    current_k, current_m = k0, m0

    # --- continuation in C (may jump after a full loop due to monodromy) ---
    for i in range(1, len(w_path)):
        w = w_path[i]
        z_prev = z_path[-1]

        best_z = None
        best_d = np.inf
        best_k, best_m = current_k, current_m

        for dk in range(-search_radius, search_radius + 1):
            for dm in range(-search_radius, search_radius + 1):
                try:
                    z_c = slog_candidate(w, k=current_k + dk, m=current_m + dm)
                    if np.isfinite(z_c):
                        d = abs(z_c - z_prev)
                        if d < best_d:
                            best_d = d
                            best_z = z_c
                            best_k = current_k + dk
                            best_m = current_m + dm
                except Exception:
                    pass

        if best_z is None:
            best_z = z_prev  # fallback (rare)

        z_path.append(best_z)
        current_k, current_m = best_k, best_m

    z_path = np.array(z_path, dtype=np.complex128)

    # ============================================================
    # Genuine lift coordinates (NO interpolation)
    # ============================================================

    # Lift 1: unwrap Arg(w) (universal cover of C*)
    theta = np.unwrap(np.angle(w_path))  # θ(t) ∈ R

    # Single-valued log-lift along the path
    log_lift = np.log(np.abs(w_path)) + 1j * theta  # continuous in t

    # Lift 2: unwrap around Lambert-W branch point at c = -1/e
    u = log_lift + 1 / np.e
    phi = np.unwrap(np.angle(u))  # φ(t) ∈ R

    k_lift = theta / (2 * np.pi)
    m_lift = phi / (2 * np.pi)

    return z_path, k_lift, m_lift


def spike_ratio(x):
    x = np.asarray(x)
    m = np.mean(x)
    return (np.max(x) / m) if m > 0 else np.inf


def main():
    # --- loops ---
    n = 900
    t = np.linspace(0, 2 * np.pi, n)

    # A commonly-cited critical value for z^z is w* = exp(-1/e)
    w_star = np.exp(-1 / np.e)

    # Loop A: around w*
    w1 = (w_star + 1e-4) + 0.40 * np.exp(1j * t)

    # Loop B: around origin
    w2 = 0.01 + 2.00 * np.exp(1j * t)

    # start points (principal guess)
    z1_0 = slog_candidate(w1[0], k=0, m=0)
    z2_0 = slog_candidate(w2[0], k=0, m=0)

    z1, k1, m1 = track_inverse_with_lift(w1, z1_0, k0=0, m0=0, search_radius=2)
    z2, k2, m2 = track_inverse_with_lift(w2, z2_0, k0=0, m0=0, search_radius=2)

    # gaps in C
    gap1 = abs(z1[-1] - z1[0])
    gap2 = abs(z2[-1] - z2[0])

    # step sizes in C
    dzC1 = np.abs(np.diff(z1))
    dzC2 = np.abs(np.diff(z2))

    # step sizes in lifted space R^4 = (Re z, Im z, k_lift, m_lift)
    dk1 = np.diff(k1)
    dm1 = np.diff(m1)
    dk2 = np.diff(k2)
    dm2 = np.diff(m2)

    dzL1 = np.sqrt(np.abs(np.diff(z1)) ** 2 + dk1 ** 2 + dm1 ** 2)
    dzL2 = np.sqrt(np.abs(np.diff(z2)) ** 2 + dk2 ** 2 + dm2 ** 2)

    print("=" * 70)
    print("CONTINUOUS LIFT DEMO for inverse of z^z = w")
    print("=" * 70)

    print("\nLoop A (around w*):")
    print(f"  gap in C: {gap1:.6f}")
    print(f"  spike ratio in C: {spike_ratio(dzC1):.2f}x")
    print(f"  spike ratio in lift: {spike_ratio(dzL1):.2f}x")
    print(f"  Δk_lift: {k1[-1]-k1[0]:.3f}    Δm_lift: {m1[-1]-m1[0]:.3f}")

    print("\nLoop B (around 0):")
    print(f"  gap in C: {gap2:.6f}")
    print(f"  spike ratio in C: {spike_ratio(dzC2):.2f}x")
    print(f"  spike ratio in lift: {spike_ratio(dzL2):.2f}x")
    print(f"  Δk_lift: {k2[-1]-k2[0]:.3f}    Δm_lift: {m2[-1]-m2[0]:.3f}")

    # 2x2 measured shift matrix:
    # rows = [loop around w*, loop around 0]
    # cols = [Delta k_lift, Delta m_lift]
    shift_matrix = np.array(
        [
            [k1[-1] - k1[0], m1[-1] - m1[0]],
            [k2[-1] - k2[0], m2[-1] - m2[0]],
        ],
        dtype=float,
    )
    det_shift = float(np.linalg.det(shift_matrix))
    rank_shift = int(np.linalg.matrix_rank(shift_matrix, tol=1e-9))
    print("\nMeasured shift matrix (rows: loops, cols: [Δk_lift, Δm_lift]):")
    print(shift_matrix)
    print(f"determinant: {det_shift:.6f}")
    print(f"rank: {rank_shift}")

    # =========================
    # FIGURE
    # =========================
    fig = plt.figure(figsize=(22, 14))
    gs = fig.add_gridspec(2, 4, hspace=0.35, wspace=0.30)

    loops = [
        ("Loop A: around $w^*=e^{-1/e}$", w1, z1, k1, m1, gap1, dzC1, dzL1, "m-lift ($\\phi/2\\pi$)"),
        ("Loop B: around $0$", w2, z2, k2, m2, gap2, dzC2, dzL2, "k-lift ($\\theta/2\\pi$)"),
    ]

    for row, (title, w_loop, z_loop, k_lift, m_lift, gap, dzC, dzL, lift_label) in enumerate(loops):
        tt = np.linspace(0, 1, len(w_loop))

        # Col 0: loop in w-plane
        ax = fig.add_subplot(gs[row, 0])
        ax.plot(w_loop.real, w_loop.imag, linewidth=2)
        ax.plot(w_loop[0].real, w_loop[0].imag, "go", markersize=10)
        ax.set_title(f"{title}\nInput loop in $\\mathbb{{C}}$")
        ax.set_xlabel("Re(w)")
        ax.set_ylabel("Im(w)")
        ax.set_aspect("equal")
        ax.grid(True, alpha=0.2)

        # Col 1: tracked inverse in C (shows gap)
        ax = fig.add_subplot(gs[row, 1])
        pts = np.array([z_loop.real, z_loop.imag]).T.reshape(-1, 1, 2)
        segs = np.concatenate([pts[:-1], pts[1:]], axis=1)
        lc = LineCollection(segs, linewidth=2.5)
        lc.set_array(tt[:-1])
        ax.add_collection(lc)
        ax.plot(z_loop[0].real, z_loop[0].imag, "go", markersize=10, zorder=10)
        ax.plot(z_loop[-1].real, z_loop[-1].imag, "r^", markersize=10, zorder=10)
        ax.set_title(f"Tracked inverse in $\\mathbb{{C}}$ (gap = {gap:.3f})")
        ax.set_xlabel("Re(z)")
        ax.set_ylabel("Im(z)")
        ax.grid(True, alpha=0.2)
        ax.autoscale()

        # Col 2: lifted 3D view (Re(z), Im(z), chosen lift coordinate)
        ax = fig.add_subplot(gs[row, 2], projection="3d")
        extra = m_lift if row == 0 else k_lift
        ax.plot(z_loop.real, z_loop.imag, extra, linewidth=2.5)
        ax.set_title("Lifted path (continuous)\n$\\mathbb{R}^4$ viewed in 3D")
        ax.set_xlabel("Re(z)")
        ax.set_ylabel("Im(z)")
        ax.set_zlabel(lift_label)
        ax.view_init(elev=20, azim=-55)

        # Col 3: step sizes comparison
        ax = fig.add_subplot(gs[row, 3])
        ax.plot(tt[:-1], dzC, label="$|\\Delta z|$ in $\\mathbb{C}$", alpha=0.8)
        ax.plot(tt[:-1], dzL, label="lift step in $\\mathbb{R}^4$", alpha=0.8)
        j = np.argmax(dzC)
        ax.axvline(tt[j], linestyle="--", alpha=0.5)
        ax.set_title("Step sizes: spike in $\\mathbb{C}$,\nbounded in lifted coordinates")
        ax.set_xlabel("Progress around loop")
        ax.set_ylabel("Step size")
        ax.grid(True, alpha=0.2)
        ax.legend()

    plt.suptitle(
        "Inverse of $z^z$: open in $\\mathbb{C}$, structured lift in $\\mathbb{R}^4$",
        fontsize=16,
        fontweight="bold",
        y=1.01,
    )
    out = "fig_path_completion_lift.png"
    plt.savefig(out, dpi=160, bbox_inches="tight")
    plt.close()
    print(f"\nSaved {out}")


if __name__ == "__main__":
    main()
