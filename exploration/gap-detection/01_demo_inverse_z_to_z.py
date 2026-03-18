#!/usr/bin/env python3
"""
Numerical demo for branch-lifted inverse continuation of z^z = w.
"""

import numpy as np
from scipy.special import lambertw
import matplotlib

# Force a non-interactive backend so the script runs in terminals/headless.
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def slog(w: complex, k: int = 0, m: int = 0) -> complex:
    """Inverse of z^z = w on selected (k, m) branches."""
    c = np.log(w + 0j) + 2j * np.pi * k
    u = lambertw(c, k=m)
    return np.exp(u)


def track_inverse(w_path: np.ndarray, z_start: complex) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Greedy branch tracking: choose nearest inverse at each step."""
    z_path = [z_start]

    for i in range(1, len(w_path)):
        w = w_path[i]
        z_prev = z_path[-1]
        best_z = None
        best_dist = np.inf

        for k in range(-2, 3):
            for m in range(-2, 3):
                try:
                    z = slog(w, k, m)
                except Exception:
                    continue
                d = abs(z - z_prev)
                if d < best_dist:
                    best_dist = d
                    best_z = z

        z_path.append(z_prev if best_z is None else best_z)

    z_path = np.array(z_path)

    # Lift coordinates from unwrapped angular data.
    theta = np.unwrap(np.angle(w_path))
    log_lift = np.log(np.abs(w_path)) + 1j * theta
    u = log_lift + 1 / np.e
    phi = np.unwrap(np.angle(u))
    k_lift = theta / (2 * np.pi)
    m_lift = phi / (2 * np.pi)
    return z_path, k_lift, m_lift


def main() -> None:
    n = 600
    t = np.linspace(0, 2 * np.pi, n)
    w = 0.01 + 2 * np.exp(1j * t)
    z0 = slog(w[0])
    z_path, k_lift, m_lift = track_inverse(w, z0)

    fig = plt.figure(figsize=(14, 6))

    ax1 = fig.add_subplot(121)
    ax1.plot(z_path.real, z_path.imag)
    ax1.set_title("Inverse path in C")
    ax1.set_xlabel("Re(z)")
    ax1.set_ylabel("Im(z)")
    ax1.grid(True)

    ax2 = fig.add_subplot(122, projection="3d")
    ax2.plot(z_path.real, z_path.imag, k_lift)
    ax2.set_title("Lifted path (continuous)")
    ax2.set_xlabel("Re(z)")
    ax2.set_ylabel("Im(z)")
    ax2.set_zlabel("lift coordinate")

    out = "inverse_z_to_z_demo.png"
    fig.tight_layout()
    fig.savefig(out, dpi=160)
    plt.close(fig)

    closure_gap = abs(z_path[-1] - z_path[0])
    k_span = float(np.max(k_lift) - np.min(k_lift))
    m_span = float(np.max(m_lift) - np.min(m_lift))
    print(f"Saved figure: {out}")
    print(f"complex closure gap: {closure_gap:.6e}")
    print(f"lift span k: {k_span:.6f}")
    print(f"lift span m: {m_span:.6f}")


if __name__ == "__main__":
    main()
