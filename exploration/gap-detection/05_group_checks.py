#!/usr/bin/env python3
"""
Monodromy group checks for inverse z^z = w.

This script extends the two-loop evidence by testing:
- composition: A then B vs B then A
- linearity in winding: 2A, 3B
- cancellation: A then A^{-1}

Outputs:
- group_checks.csv
- fig_05_group_checks.png
"""

from __future__ import annotations

import csv
from pathlib import Path

import matplotlib
import numpy as np
from scipy.special import lambertw

matplotlib.use("Agg")
import matplotlib.pyplot as plt


def slog(w: complex, k: int = 0, m: int = 0) -> complex:
    c = np.log(w + 0j) + 2j * np.pi * k
    u = lambertw(c, k=m)
    return np.exp(u)


def track_inverse_with_branch_indices(
    w_path: np.ndarray, k0: int = 0, m0: int = 0, search_radius: int = 2
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Nearest-neighbour continuation with explicit integer branch tracking."""
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


def closed_circle(
    center: complex, radius: float, n_per_turn: int, turns: int = 1, orientation: int = 1
) -> np.ndarray:
    """Closed circle path with explicit endpoint = startpoint."""
    t = np.linspace(0.0, 2 * np.pi * turns, n_per_turn * turns + 1)
    return center + radius * np.exp(1j * orientation * t)


def concat_paths(paths: list[np.ndarray]) -> np.ndarray:
    """Concatenate closed paths that share the same basepoint."""
    out = paths[0].copy()
    for p in paths[1:]:
        out = np.concatenate([out, p[1:]])
    return out


def run_case(name: str, segments: list[np.ndarray]) -> dict:
    w_path = concat_paths(segments)
    z_path, k_path, m_path = track_inverse_with_branch_indices(w_path)

    delta_k = int(k_path[-1] - k_path[0])
    delta_m = int(m_path[-1] - m_path[0])
    raw_gap = abs(z_path[-1] - z_path[0])
    predicted_end = slog(w_path[0], k=delta_k, m=delta_m)
    sheet_residual = abs(z_path[-1] - predicted_end)

    return {
        "case": name,
        "points": len(w_path),
        "delta_k": delta_k,
        "delta_m": delta_m,
        "raw_gap": float(raw_gap),
        "sheet_residual": float(sheet_residual),
    }


def write_csv(rows: list[dict], out_csv: Path) -> None:
    fieldnames = ["case", "points", "delta_k", "delta_m", "raw_gap", "sheet_residual"]
    with out_csv.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def make_plot(rows: list[dict], out_png: Path) -> None:
    fig, ax = plt.subplots(figsize=(8, 6))

    # Draw shift vectors from origin.
    for r in rows:
        x = r["delta_k"]
        y = r["delta_m"]
        ax.scatter([x], [y], s=70)
        ax.annotate(r["case"], (x, y), xytext=(6, 4), textcoords="offset points")

    ax.axhline(0.0, color="gray", linewidth=1)
    ax.axvline(0.0, color="gray", linewidth=1)
    ax.set_xlabel("Delta k")
    ax.set_ylabel("Delta m")
    ax.set_title("Measured monodromy shifts by loop composition")
    ax.grid(True, alpha=0.3)
    ax.set_aspect("equal", adjustable="box")

    fig.tight_layout()
    fig.savefig(out_png, dpi=160)
    plt.close(fig)


def main() -> None:
    n_per_turn = 900
    w_star = np.exp(-1 / np.e)
    r_a = 0.40
    w0 = float(np.real(w_star + r_a))
    r_b = w0  # makes loop B share basepoint with loop A

    # Generator loops with shared basepoint w0 on positive real axis.
    A = closed_circle(center=w_star, radius=r_a, n_per_turn=n_per_turn, turns=1, orientation=1)
    A_inv = closed_circle(center=w_star, radius=r_a, n_per_turn=n_per_turn, turns=1, orientation=-1)
    B = closed_circle(center=0.0, radius=r_b, n_per_turn=n_per_turn, turns=1, orientation=1)

    rows = [
        run_case("A", [A]),
        run_case("B", [B]),
        run_case("A_then_B", [A, B]),
        run_case("B_then_A", [B, A]),
        run_case("two_A", [A, A]),
        run_case("three_B", [B, B, B]),
        run_case("A_then_Ainv", [A, A_inv]),
    ]

    # Basic consistency diagnostics for quick reading.
    by_name = {r["case"]: r for r in rows}
    dA = np.array([by_name["A"]["delta_k"], by_name["A"]["delta_m"]], dtype=int)
    dB = np.array([by_name["B"]["delta_k"], by_name["B"]["delta_m"]], dtype=int)
    dAB = np.array([by_name["A_then_B"]["delta_k"], by_name["A_then_B"]["delta_m"]], dtype=int)
    dBA = np.array([by_name["B_then_A"]["delta_k"], by_name["B_then_A"]["delta_m"]], dtype=int)
    d2A = np.array([by_name["two_A"]["delta_k"], by_name["two_A"]["delta_m"]], dtype=int)
    d3B = np.array([by_name["three_B"]["delta_k"], by_name["three_B"]["delta_m"]], dtype=int)
    d_cancel = np.array(
        [by_name["A_then_Ainv"]["delta_k"], by_name["A_then_Ainv"]["delta_m"]], dtype=int
    )

    out_dir = Path(__file__).resolve().parent
    out_csv = out_dir / "group_checks.csv"
    out_png = out_dir / "fig_05_group_checks.png"
    write_csv(rows, out_csv)
    make_plot(rows, out_png)

    print("=" * 74)
    print("GROUP CHECKS FOR INVERSE z^z MONODROMY")
    print("=" * 74)
    for r in rows:
        print(
            f"{r['case']:>12}: shift=({r['delta_k']:>2},{r['delta_m']:>2})  "
            f"gap={r['raw_gap']:.6f}  resid={r['sheet_residual']:.2e}"
        )
    print("\nWinding-linearity checks:")
    print(f"  2*A        = {2 * dA}    |  two_A       = {d2A}")
    print(f"  3*B        = {3 * dB}    |  three_B     = {d3B}")
    print(f"  A + A_inv  = [0 0]       |  A_then_Ainv = {d_cancel}")
    print("\nComposition-order diagnostic:")
    print(f"  A_then_B = {dAB}")
    print(f"  B_then_A = {dBA}")
    if np.array_equal(dAB, dBA):
        print("  observed: same shift for both orders (commuting at this resolution)")
    else:
        print("  observed: order-sensitive shift (possible non-abelian action or tracker ambiguity)")
    print(f"\nSaved {out_csv.name}")
    print(f"Saved {out_png.name}")


if __name__ == "__main__":
    main()
