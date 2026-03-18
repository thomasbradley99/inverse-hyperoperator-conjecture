#!/usr/bin/env python3
"""
Two-panel figure (same style as computational-gap-detection):
  Left:  path in H (open) — 3D view, start != end.
  Right: path in quotient H/(Zj+Zk) (closed) — same path + identification segment.

Run from repo root: python quaternion-state/fig_open_in_H_closed_in_quotient.py
"""

import os
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
    return z_path, k_lift, m_lift


def main():
    n = 600
    t = np.linspace(0, 2 * np.pi, n)
    w_star = np.exp(-1 / np.e)
    w_path = (w_star + 1e-4) + 0.40 * np.exp(1j * t)
    z_path, k_lift, m_lift = track_with_lift(w_path, slog(w_path[0]), 0, 0)

    # 3D view: (Re z, Im z, k_lift), colour = m_lift
    x, y, z_ax = z_path.real, z_path.imag, k_lift

    fig = plt.figure(figsize=(14, 6))

    # Left: path in H — OPEN (line + start/end markers)
    ax1 = fig.add_subplot(121, projection="3d")
    ax1.plot(x, y, z_ax, "b-", linewidth=2, alpha=0.9)
    ax1.plot(x[0], y[0], z_ax[0], "go", markersize=14, label="start")
    ax1.plot(x[-1], y[-1], z_ax[-1], "r^", markersize=14, label="end")
    ax1.set_xlabel("Re(z)")
    ax1.set_ylabel("Im(z)")
    ax1.set_zlabel("k_lift (j)")
    ax1.set_title("In H: path does NOT close\n(start and end are different points)", fontsize=11)
    ax1.legend(loc="upper left", fontsize=9)
    ax1.view_init(elev=22, azim=-58)

    # Right: path in (k_lift, m_lift) — no mod, so path is smooth; closing segment is short
    # For Loop A: path (0,0) -> (0,1); in quotient we identify (0,1) with (0,0), so one short segment closes it
    ax2 = fig.add_subplot(122)
    ax2.plot(k_lift, m_lift, "b-", linewidth=2.5, label="path")
    ax2.plot([k_lift[-1], k_lift[0]], [m_lift[-1], m_lift[0]], "C1-", linewidth=4, label="identification")
    ax2.plot(k_lift[0], m_lift[0], "go", markersize=14, label="start = end")
    ax2.set_xlabel("k_lift (j)")
    ax2.set_ylabel("m_lift (k)")
    ax2.set_title("In quotient: (k,m) path CLOSES\n(short identification segment)", fontsize=11)
    ax2.legend(loc="upper left", fontsize=9)
    ax2.set_aspect("equal")
    ax2.grid(True, alpha=0.3)
    # Slight margin so path and closing segment are visible
    ax2.margins(0.08)

    plt.suptitle(
        "Path in H is open; in the quotient H/(Zj+Zk) it closes (one loop)",
        fontsize=12,
        fontweight="bold",
    )
    plt.tight_layout()
    out = os.path.join(os.path.dirname(__file__), "fig_open_in_H_closed_in_quotient.png")
    plt.savefig(out, dpi=160, bbox_inches="tight")
    plt.close()
    print(f"Saved {out}")


if __name__ == "__main__":
    main()
