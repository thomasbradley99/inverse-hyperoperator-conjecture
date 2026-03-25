#!/usr/bin/env python3
"""
Cross-check monodromy shifts across two continuation trackers.

Goal:
- Distinguish likely geometric monodromy effects from nearest-neighbour artifacts.
- Compare branch-shift outputs for the same loops/compositions under:
  1) local nearest-neighbour continuation in z
  2) lift-guided continuation (targets unwrapped lift coordinates first)

Outputs:
- tracker_crosscheck.csv
- fig_06_tracker_crosscheck.png
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


def closed_circle(
    center: complex, radius: float, n_per_turn: int, turns: int = 1, orientation: int = 1
) -> np.ndarray:
    t = np.linspace(0.0, 2 * np.pi * turns, n_per_turn * turns + 1)
    return center + radius * np.exp(1j * orientation * t)


def concat_paths(paths: list[np.ndarray]) -> np.ndarray:
    out = paths[0].copy()
    for p in paths[1:]:
        out = np.concatenate([out, p[1:]])
    return out


def track_nearest(
    w_path: np.ndarray, k0: int = 0, m0: int = 0, search_radius: int = 2
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Local nearest-neighbour tracker (baseline used in earlier scripts)."""
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


def track_lift_guided(
    w_path: np.ndarray, k0: int = 0, m0: int = 0, search_radius: int = 2
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Lift-guided tracker:
    - compute continuous target lifts from unwrapped angles
    - prefer candidates nearest to (k_target, m_target)
    - tie-break by nearest neighbour in z
    """
    theta = np.unwrap(np.angle(w_path))
    log_lift = np.log(np.abs(w_path)) + 1j * theta
    phi = np.unwrap(np.angle(log_lift + 1 / np.e))

    k_target = theta / (2 * np.pi)
    m_target = phi / (2 * np.pi)

    z_path = [slog(w_path[0], k=k0, m=m0)]
    k_path = [k0]
    m_path = [m0]
    ck, cm = k0, m0

    for i in range(1, len(w_path)):
        w = w_path[i]
        z_prev = z_path[-1]
        best_z = None
        best_score = np.inf
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

                # Primary objective: stay close to continuous lift target.
                lift_err = np.hypot(kc - k_target[i], mc - m_target[i])
                # Secondary objective: local continuity in C.
                z_err = abs(zc - z_prev)
                score = (10.0 * lift_err) + z_err
                if score < best_score:
                    best_score = score
                    best_z = zc
                    best_k, best_m = kc, mc
        if best_z is None:
            best_z = z_prev
        z_path.append(best_z)
        k_path.append(best_k)
        m_path.append(best_m)
        ck, cm = best_k, best_m

    return np.array(z_path), np.array(k_path), np.array(m_path)


def evaluate_case(name: str, w_path: np.ndarray, tracker_name: str, tracker_fn) -> dict:
    z_path, k_path, m_path = tracker_fn(w_path)
    dk = int(k_path[-1] - k_path[0])
    dm = int(m_path[-1] - m_path[0])
    raw_gap = abs(z_path[-1] - z_path[0])
    predicted_end = slog(w_path[0], k=dk, m=dm)
    resid = abs(z_path[-1] - predicted_end)
    return {
        "tracker": tracker_name,
        "case": name,
        "points": len(w_path),
        "delta_k": dk,
        "delta_m": dm,
        "raw_gap": float(raw_gap),
        "sheet_residual": float(resid),
    }


def write_csv(rows: list[dict], out_csv: Path) -> None:
    fields = ["tracker", "case", "points", "delta_k", "delta_m", "raw_gap", "sheet_residual"]
    with out_csv.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def make_plot(rows: list[dict], out_png: Path) -> None:
    cases = ["A", "B", "A_then_B", "B_then_A", "two_A", "three_B", "A_then_Ainv"]
    trackers = ["nearest", "lift_guided"]
    colors = {"nearest": "tab:blue", "lift_guided": "tab:orange"}
    x = np.arange(len(cases))

    fig, axes = plt.subplots(1, 2, figsize=(12, 5), sharex=True)

    for j, comp in enumerate(["delta_k", "delta_m"]):
        ax = axes[j]
        for i, tr in enumerate(trackers):
            vals = []
            for c in cases:
                row = next(r for r in rows if r["tracker"] == tr and r["case"] == c)
                vals.append(row[comp])
            ax.plot(
                x,
                vals,
                marker="o",
                linestyle="-",
                color=colors[tr],
                label=tr if j == 0 else None,
                alpha=0.9,
            )
        ax.set_title(comp)
        ax.grid(True, alpha=0.3)
        ax.set_xticks(x)
        ax.set_xticklabels(cases, rotation=35, ha="right")

    axes[0].set_ylabel("integer shift")
    axes[0].legend(loc="best")
    fig.suptitle("Tracker cross-check: branch-shift outputs by case", fontsize=12, fontweight="bold")
    fig.tight_layout()
    fig.savefig(out_png, dpi=160)
    plt.close(fig)


def main() -> None:
    n_per_turn = 900
    w_star = np.exp(-1 / np.e)
    r_a = 0.40
    w0 = float(np.real(w_star + r_a))
    r_b = w0

    A = closed_circle(center=w_star, radius=r_a, n_per_turn=n_per_turn, turns=1, orientation=1)
    A_inv = closed_circle(center=w_star, radius=r_a, n_per_turn=n_per_turn, turns=1, orientation=-1)
    B = closed_circle(center=0.0, radius=r_b, n_per_turn=n_per_turn, turns=1, orientation=1)

    loops = {
        "A": A,
        "B": B,
        "A_then_B": concat_paths([A, B]),
        "B_then_A": concat_paths([B, A]),
        "two_A": concat_paths([A, A]),
        "three_B": concat_paths([B, B, B]),
        "A_then_Ainv": concat_paths([A, A_inv]),
    }

    trackers = {
        "nearest": track_nearest,
        "lift_guided": track_lift_guided,
    }

    rows: list[dict] = []
    for tname, tfn in trackers.items():
        for cname, w_path in loops.items():
            rows.append(evaluate_case(cname, w_path, tname, tfn))

    out_dir = Path(__file__).resolve().parent
    out_csv = out_dir / "tracker_crosscheck.csv"
    out_png = out_dir / "fig_06_tracker_crosscheck.png"
    write_csv(rows, out_csv)
    make_plot(rows, out_png)

    print("=" * 74)
    print("TRACKER CROSS-CHECK FOR INVERSE z^z MONODROMY")
    print("=" * 74)
    for tname in trackers:
        print(f"\nTracker: {tname}")
        for cname in loops:
            r = next(rr for rr in rows if rr["tracker"] == tname and rr["case"] == cname)
            print(
                f"  {cname:>12}: shift=({r['delta_k']:>2},{r['delta_m']:>2})  "
                f"gap={r['raw_gap']:.6f}  resid={r['sheet_residual']:.2e}"
            )

    print("\nComparison focus (order sensitivity):")
    for tname in trackers:
        r_ab = next(rr for rr in rows if rr["tracker"] == tname and rr["case"] == "A_then_B")
        r_ba = next(rr for rr in rows if rr["tracker"] == tname and rr["case"] == "B_then_A")
        print(
            f"  {tname:>11}: A_then_B=({r_ab['delta_k']},{r_ab['delta_m']}) "
            f"vs B_then_A=({r_ba['delta_k']},{r_ba['delta_m']})"
        )

    print(f"\nSaved {out_csv.name}")
    print(f"Saved {out_png.name}")


if __name__ == "__main__":
    main()
