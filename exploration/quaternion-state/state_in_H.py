#!/usr/bin/env python3
"""
Represent the 4D state (z, k_lift, m_lift) of inverse z^z as a quaternion
  q = Re(z) + Im(z)*i + k_lift*j + m_lift*k
and check that the deck action is translation in the (j,k)-plane.

Run from repo root: python quaternion-state/state_in_H.py
"""

import numpy as np
from scipy.special import lambertw
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def slog(w, k=0, m=0):
    c = np.log(w + 0j) + 2j * np.pi * k
    return np.exp(lambertw(c, k=m))


def track_with_lift(w_path, z_start, k0=0, m0=0, search_radius=2):
    z_path = [z_start]
    ck, cm = k0, m0
    for i in range(1, len(w_path)):
        w = w_path[i]
        z_prev = z_path[-1]
        best_z, best_d = None, np.inf
        best_k, best_m = ck, cm
        for dk in range(-search_radius, search_radius + 1):
            for dm in range(-search_radius, search_radius + 1):
                try:
                    z_c = slog(w, k=ck + dk, m=cm + dm)
                    if np.isfinite(z_c):
                        d = abs(z_c - z_prev)
                        if d < best_d:
                            best_d, best_z = d, z_c
                            best_k, best_m = ck + dk, cm + dm
                except Exception:
                    pass
        z_path.append(best_z if best_z is not None else z_prev)
        ck, cm = best_k, best_m
    z_path = np.array(z_path)
    theta = np.unwrap(np.angle(w_path))
    log_lift = np.log(np.abs(w_path)) + 1j * theta
    phi = np.unwrap(np.angle(log_lift + 1 / np.e))
    k_lift = theta / (2 * np.pi)
    m_lift = phi / (2 * np.pi)
    return z_path, k_lift, m_lift, (ck - k0, cm - m0)  # integer shifts


def main():
    n = 600
    t = np.linspace(0, 2 * np.pi, n)
    w_star = np.exp(-1 / np.e)
    wA = (w_star + 1e-4) + 0.40 * np.exp(1j * t)
    wB = 0.01 + 2.00 * np.exp(1j * t)

    zA, kA, mA, (dkA, dmA) = track_with_lift(wA, slog(wA[0]), 0, 0)
    zB, kB, mB, (dkB, dmB) = track_with_lift(wB, slog(wB[0]), 0, 0)

    # State as quaternion q = w + x*i + y*j + z*k  with (w,x,y,z) = (Re z, Im z, k_lift, m_lift)
    def to_q(z, k_l, m_l):
        return np.array([z.real, z.imag, k_l, m_l])

    qA = np.array([to_q(zA[i], kA[i], mA[i]) for i in range(len(zA))])
    qB = np.array([to_q(zB[i], kB[i], mB[i]) for i in range(len(zB))])

    # Displacement in H: q_end - q_start = (Re gap, Im gap, Δk_lift, Δm_lift)
    dqA = qA[-1] - qA[0]
    dqB = qB[-1] - qB[0]

    print("=" * 60)
    print("State in H: q = Re(z) + Im(z)*i + k_lift*j + m_lift*k")
    print("=" * 60)
    print("Loop A (around w*):")
    print(f"  Integer branch shift (Δk, Δm) = ({dkA}, {dmA})")
    print(f"  q_end - q_start = (Re gap, Im gap, Δk_lift, Δm_lift) = {dqA}")
    print(f"  (j,k) part of displacement = ({dqA[2]:.6f}, {dqA[3]:.6f})  [should be ~(0,1)]")
    print()
    print("Loop B (around 0):")
    print(f"  Integer branch shift (Δk, Δm) = ({dkB}, {dmB})")
    print(f"  q_end - q_start = {dqB}")
    print(f"  (j,k) part of displacement = ({dqB[2]:.6f}, {dqB[3]:.6f})  [should be ~(1,0.22)]")
    print()
    print("Deck action on state = translation in (j,k)-plane by (Δk, Δm)")
    print("  plus the change in (Re z, Im z). So 4D state lives in H.")
    print()
    print("Path does NOT close in H (q_end ≠ q_start).")
    print("Path CLOSES in the quotient H / (Zj + Zk) (same as closure modulo sheets).")
    print("=" * 60)

    # 3D projections of path in H: (1,i,j) and (1,i,k)
    fig, axes = plt.subplots(1, 2, subplot_kw={"projection": "3d"}, figsize=(12, 5))

    for ax, q, title, lbl in [
        (axes[0], qA, "Loop A in H (1,i,j)", "m_lift"),
        (axes[1], qB, "Loop B in H (1,i,j)", "m_lift"),
    ]:
        # (w,x,y) = (Re z, Im z, k_lift), colour = m_lift
        sc = ax.scatter(q[:, 0], q[:, 1], q[:, 2], c=q[:, 3], cmap="viridis", s=4)
        ax.set_xlabel("Re(z)")
        ax.set_ylabel("Im(z)")
        ax.set_zlabel("k_lift (j)")
        ax.set_title(title)
        plt.colorbar(sc, ax=ax, label="m_lift (k)")
        ax.view_init(elev=20, azim=-60)

    plt.suptitle(
        "Path in H: open in 4D (q_end ≠ q_start); closes in H / (Zj + Zk)",
        fontsize=11,
        fontweight="bold",
    )
    plt.tight_layout()
    import os
    out = os.path.join(os.path.dirname(__file__), "path_in_H.png")
    plt.savefig(out, dpi=150, bbox_inches="tight")
    plt.close()
    print("Saved path_in_H.png")


if __name__ == "__main__":
    main()
