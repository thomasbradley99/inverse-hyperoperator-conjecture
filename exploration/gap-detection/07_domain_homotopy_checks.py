#!/usr/bin/env python3
"""
Domain/homotopy diagnostics for loop-order effects.

This script checks whether order-sensitive monodromy results can be explained
by loop classes in a punctured domain, rather than by a tracker quirk.

For each based loop case it reports:
- symbolic loop word and reduced word (free-group style)
- winding numbers around punctures {0, w*}
- nearest distance to each puncture
- measured branch shift (Delta k, Delta m)
- closure residual

Outputs:
- domain_homotopy_checks.csv
- fig_07_domain_homotopy_checks.png
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


def winding_number(path: np.ndarray, point: complex) -> int:
    """Integer winding number of a closed path around a point."""
    ang = np.unwrap(np.angle(path - point))
    total = ang[-1] - ang[0]
    return int(np.rint(total / (2 * np.pi)))


def inverse_token(tok: str) -> str:
    return tok[:-3] if tok.endswith("_inv") else f"{tok}_inv"


def reduce_word(tokens: list[str]) -> list[str]:
    """Cancel adjacent generator/inverse pairs."""
    st: list[str] = []
    for tok in tokens:
        if st and inverse_token(tok) == st[-1]:
            st.pop()
        else:
            st.append(tok)
    return st


def evaluate_case(
    case_name: str,
    tokens: list[str],
    w_path: np.ndarray,
    punctures: dict[str, complex],
) -> dict:
    z_path, k_path, m_path = track_inverse_with_branch_indices(w_path)
    dk = int(k_path[-1] - k_path[0])
    dm = int(m_path[-1] - m_path[0])
    raw_gap = abs(z_path[-1] - z_path[0])
    predicted_end = slog(w_path[0], k=dk, m=dm)
    resid = abs(z_path[-1] - predicted_end)

    reduced = reduce_word(tokens)

    row = {
        "case": case_name,
        "word": " ".join(tokens),
        "reduced_word": " ".join(reduced) if reduced else "identity",
        "points": len(w_path),
        "delta_k": dk,
        "delta_m": dm,
        "raw_gap": float(raw_gap),
        "sheet_residual": float(resid),
    }

    for name, point in punctures.items():
        row[f"wind_{name}"] = winding_number(w_path, point)
        row[f"min_dist_{name}"] = float(np.min(np.abs(w_path - point)))

    return row


def write_csv(rows: list[dict], out_csv: Path) -> None:
    fields = [
        "case",
        "word",
        "reduced_word",
        "points",
        "delta_k",
        "delta_m",
        "raw_gap",
        "sheet_residual",
        "wind_0",
        "wind_wstar",
        "min_dist_0",
        "min_dist_wstar",
    ]
    with out_csv.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def make_plot(cases: dict[str, np.ndarray], punctures: dict[str, complex], out_png: Path) -> None:
    fig, ax = plt.subplots(figsize=(7.5, 7.0))

    highlight = ["A_then_B", "B_then_A", "commutator"]
    colors = {"A_then_B": "tab:blue", "B_then_A": "tab:orange", "commutator": "tab:green"}

    for name in highlight:
        p = cases[name]
        ax.plot(p.real, p.imag, linewidth=2, alpha=0.85, label=name, color=colors[name])

    for pname, pt in punctures.items():
        ax.plot([pt.real], [pt.imag], "x", markersize=10, markeredgewidth=2, label=f"puncture {pname}")

    # Basepoint marker
    p0 = cases["A_then_B"][0]
    ax.plot([p0.real], [p0.imag], "ko", markersize=5, label="basepoint")

    ax.set_title("Based loops with same abelian winding can differ by order")
    ax.set_xlabel("Re(w)")
    ax.set_ylabel("Im(w)")
    ax.grid(True, alpha=0.3)
    ax.set_aspect("equal", adjustable="box")
    ax.legend(loc="best")

    fig.tight_layout()
    fig.savefig(out_png, dpi=160)
    plt.close(fig)


def main() -> None:
    n_per_turn = 900
    w_star = np.exp(-1 / np.e)
    r_a = 0.40
    w0 = float(np.real(w_star + r_a))
    r_b = w0

    # Based generators (same start/end basepoint).
    A = closed_circle(center=w_star, radius=r_a, n_per_turn=n_per_turn, turns=1, orientation=1)
    A_inv = closed_circle(center=w_star, radius=r_a, n_per_turn=n_per_turn, turns=1, orientation=-1)
    B = closed_circle(center=0.0, radius=r_b, n_per_turn=n_per_turn, turns=1, orientation=1)
    B_inv = closed_circle(center=0.0, radius=r_b, n_per_turn=n_per_turn, turns=1, orientation=-1)

    case_tokens = {
        "A": ["A"],
        "B": ["B"],
        "A_then_B": ["A", "B"],
        "B_then_A": ["B", "A"],
        "two_A": ["A", "A"],
        "three_B": ["B", "B", "B"],
        "A_then_Ainv": ["A", "A_inv"],
        "commutator": ["A", "B", "A_inv", "B_inv"],
    }

    cases = {
        "A": concat_paths([A]),
        "B": concat_paths([B]),
        "A_then_B": concat_paths([A, B]),
        "B_then_A": concat_paths([B, A]),
        "two_A": concat_paths([A, A]),
        "three_B": concat_paths([B, B, B]),
        "A_then_Ainv": concat_paths([A, A_inv]),
        "commutator": concat_paths([A, B, A_inv, B_inv]),
    }

    punctures = {"0": 0.0 + 0.0j, "wstar": w_star + 0.0j}

    rows = []
    for name, w_path in cases.items():
        rows.append(evaluate_case(name, case_tokens[name], w_path, punctures))

    out_dir = Path(__file__).resolve().parent
    out_csv = out_dir / "domain_homotopy_checks.csv"
    out_png = out_dir / "fig_07_domain_homotopy_checks.png"
    write_csv(rows, out_csv)
    make_plot(cases, punctures, out_png)

    by_name = {r["case"]: r for r in rows}
    ab = by_name["A_then_B"]
    ba = by_name["B_then_A"]

    print("=" * 76)
    print("DOMAIN / HOMOTOPY DIAGNOSTICS")
    print("=" * 76)
    for r in rows:
        print(
            f"{r['case']:>12}: shift=({r['delta_k']:>2},{r['delta_m']:>2}) "
            f"wind=(0:{r['wind_0']:>2}, w*:{r['wind_wstar']:>2}) "
            f"min-dist=(0:{r['min_dist_0']:.4f}, w*:{r['min_dist_wstar']:.4f}) "
            f"resid={r['sheet_residual']:.2e}"
        )

    print("\nOrder check:")
    print(
        f"  A_then_B winding = (0:{ab['wind_0']}, w*:{ab['wind_wstar']}), "
        f"shift = ({ab['delta_k']},{ab['delta_m']}), word = {ab['reduced_word']}"
    )
    print(
        f"  B_then_A winding = (0:{ba['wind_0']}, w*:{ba['wind_wstar']}), "
        f"shift = ({ba['delta_k']},{ba['delta_m']}), word = {ba['reduced_word']}"
    )
    print("  Note: same abelian winding does not imply same reduced loop word.")
    print("  In a punctured plane with >=2 punctures, based-loop order can matter.")

    print(f"\nSaved {out_csv.name}")
    print(f"Saved {out_png.name}")


if __name__ == "__main__":
    main()
