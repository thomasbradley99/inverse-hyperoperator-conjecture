#!/usr/bin/env python3
"""
Visual exploratory tools for inverse exponentiation (super-root) behaviour.

Generates:
  1. A heatmap showing how strongly i^q leaves the complex plane for
     exponents q = u*j + v*k.
  2. Line plots of the j/k-vector norm across power-tower levels for
     representative quaternion bases.

Outputs are written to PNG files in the repo root.
"""

import math
import os
import sys
from dataclasses import dataclass
from typing import List, Optional

VENDOR_DIR = os.path.join(os.path.dirname(__file__), "vendor")
if os.path.isdir(VENDOR_DIR) and VENDOR_DIR not in sys.path:
    sys.path.insert(0, VENDOR_DIR)

import matplotlib.pyplot as plt
import numpy as np


@dataclass
class Quaternion:
    w: float
    x: float
    y: float
    z: float

    def __add__(self, other: "Quaternion") -> "Quaternion":
        return Quaternion(
            self.w + other.w,
            self.x + other.x,
            self.y + other.y,
            self.z + other.z,
        )

    def __sub__(self, other: "Quaternion") -> "Quaternion":
        return Quaternion(
            self.w - other.w,
            self.x - other.x,
            self.y - other.y,
            self.z - other.z,
        )

    def __mul__(self, other: "Quaternion") -> "Quaternion":
        w1, x1, y1, z1 = self.w, self.x, self.y, self.z
        w2, x2, y2, z2 = other.w, other.x, other.y, other.z
        return Quaternion(
            w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2,
            w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2,
            w1 * y2 - x1 * z2 + y1 * w2 + z1 * x2,
            w1 * z2 + x1 * y2 - y1 * x2 + z1 * w2,
        )

    @property
    def norm(self) -> float:
        return math.sqrt(self.w**2 + self.x**2 + self.y**2 + self.z**2)

    @property
    def vector_norm(self) -> float:
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)


def quaternion_exp(q: Quaternion) -> Quaternion:
    a = q.w
    vx, vy, vz = q.x, q.y, q.z
    v_norm = math.sqrt(vx**2 + vy**2 + vz**2)
    exp_a = math.exp(a)
    if v_norm == 0.0:
        return Quaternion(exp_a, 0.0, 0.0, 0.0)
    c = math.cos(v_norm)
    s = math.sin(v_norm)
    factor = exp_a * s / v_norm
    return Quaternion(
        exp_a * c,
        factor * vx,
        factor * vy,
        factor * vz,
    )


def quaternion_log(q: Quaternion) -> Quaternion:
    r = q.norm
    if r == 0.0:
        raise ValueError("Log undefined for zero quaternion")
    a = q.w
    vx, vy, vz = q.x, q.y, q.z
    v_norm = math.sqrt(vx**2 + vy**2 + vz**2)
    ln_r = math.log(r)
    if v_norm == 0.0:
        return Quaternion(ln_r, 0.0, 0.0, 0.0)
    theta = math.acos(max(-1.0, min(1.0, a / r)))
    factor = theta / v_norm
    return Quaternion(
        ln_r,
        factor * vx,
        factor * vy,
        factor * vz,
    )


def quaternion_power(base: Quaternion, exponent: Quaternion) -> Quaternion:
    return quaternion_exp(quaternion_log(base) * exponent)


def heatmap_superroot(
    grid_lim: float = 2.0,
    resolution: int = 201,
    outfile: str = "superroot_heatmap.png",
) -> None:
    """
    Evaluate i^(u*j + v*k) over a grid and plot the magnitude of the
    resulting j/k components.
    """
    i = Quaternion(0.0, 1.0, 0.0, 0.0)
    u_vals = np.linspace(-grid_lim, grid_lim, resolution)
    v_vals = np.linspace(-grid_lim, grid_lim, resolution)
    magnitude = np.zeros((resolution, resolution))

    for ui, u in enumerate(u_vals):
        for vi, v in enumerate(v_vals):
            exponent = Quaternion(0.0, 0.0, u, v)
            result = quaternion_power(i, exponent)
            magnitude[vi, ui] = math.sqrt(result.y**2 + result.z**2)

    plt.figure(figsize=(6, 5))
    plt.imshow(
        magnitude,
        extent=[-grid_lim, grid_lim, -grid_lim, grid_lim],
        origin="lower",
        cmap="magma",
        interpolation="nearest",
    )
    plt.colorbar(label="|j/k component| of i^(u j + v k)")
    plt.title("Quaternion strength of i^q for q in span{j,k}")
    plt.xlabel("u (coefficient of j)")
    plt.ylabel("v (coefficient of k)")
    plt.tight_layout()
    plt.savefig(outfile, dpi=200)
    plt.close()
    print(f"[heatmap] saved {outfile}")


def power_tower_series(
    base: Quaternion,
    height: int,
    *,
    seed: Optional[Quaternion] = None,
) -> List[Quaternion]:
    if height < 1:
        raise ValueError("height must be >= 1")
    if seed is None:
        seed = base
    values = [seed]
    current = seed
    for _ in range(height):
        current = quaternion_power(base, current)
        values.append(current)
    return values


def plot_power_tower_norms(outfile: str = "tower_norms.png") -> None:
    """
    Track the j/k norm of power tower iterates for representative bases.
    """
    bases = {
        "i": Quaternion(0.0, 1.0, 0.0, 0.0),
        "0.5i + 0.5j": Quaternion(0.0, 0.5, 0.5, 0.0),
        "j + k": Quaternion(0.0, 0.0, 1.0, 1.0),
    }
    height = 6

    plt.figure(figsize=(6, 4))
    for label, base in bases.items():
        series = power_tower_series(base, height)
        norms = [math.sqrt(q.y**2 + q.z**2) for q in series]
        plt.plot(range(len(norms)), norms, marker="o", label=label)

    plt.title("Quaternion vector norms across tower levels")
    plt.xlabel("Level")
    plt.ylabel("√(j² + k²)")
    plt.legend()
    plt.grid(True, linestyle=":", alpha=0.4)
    plt.tight_layout()
    plt.savefig(outfile, dpi=200)
    plt.close()
    print(f"[tower norms] saved {outfile}")


def main() -> None:
    heatmap_superroot()
    plot_power_tower_norms()


if __name__ == "__main__":
    main()

