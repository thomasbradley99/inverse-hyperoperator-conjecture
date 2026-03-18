#!/usr/bin/env python3
"""
Exploratory tools for quaternion power towers and inverse exponentiation.

Usage:
    python3 quaternion_power_tower.py

The script:
  • Reuses the Quaternion algebra from inverse_tetration_quaternion.py.
  • Provides iterative constructions of finite-height power towers.
  • Samples both complex bases and genuine quaternions to see when results
    leave the complex plane.
"""

import math
from dataclasses import dataclass
from typing import List, Optional


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
        """Hamilton product."""
        w1, x1, y1, z1 = self.w, self.x, self.y, self.z
        w2, x2, y2, z2 = other.w, other.x, other.y, other.z
        return Quaternion(
            w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2,
            w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2,
            w1 * y2 - x1 * z2 + y1 * w2 + z1 * x2,
            w1 * z2 + x1 * y2 - y1 * x2 + z1 * w2,
        )

    def scale(self, scalar: float) -> "Quaternion":
        return Quaternion(
            self.w * scalar,
            self.x * scalar,
            self.y * scalar,
            self.z * scalar,
        )

    def __repr__(self) -> str:
        return (
            f"({self.w:.6f} + {self.x:.6f}i +"
            f" {self.y:.6f}j + {self.z:.6f}k)"
        )

    @property
    def norm(self) -> float:
        return math.sqrt(self.w ** 2 + self.x ** 2 + self.y ** 2 + self.z ** 2)

    @property
    def vector_norm(self) -> float:
        return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)


def quaternion_exp(q: Quaternion) -> Quaternion:
    """Quaternion exponential."""
    a = q.w
    vx, vy, vz = q.x, q.y, q.z
    v_norm = math.sqrt(vx ** 2 + vy ** 2 + vz ** 2)
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
    """Principal branch quaternion logarithm."""
    r = q.norm
    if r == 0.0:
        raise ValueError("Log undefined for zero quaternion")
    a = q.w
    vx, vy, vz = q.x, q.y, q.z
    v_norm = math.sqrt(vx ** 2 + vy ** 2 + vz ** 2)
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


def power_tower(
    base: Quaternion,
    height: int,
    *,
    seed: Optional[Quaternion] = None,
) -> List[Quaternion]:
    """
    Build a finite-height power tower via downward iteration.

    Example: with base b and height 3 we compute
        b^(b^seed)
    returning the intermediate states for inspection.
    """
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


def describe_tower(base: Quaternion, height: int) -> None:
    print(f"\n=== Base {base} | height {height} ===")
    try:
        values = power_tower(base, height)
    except ValueError as exc:
        print(f"Failed: {exc}")
        return
    for idx, value in enumerate(values):
        label = "seed" if idx == 0 else f"level {idx}"
        print(f"{label:>7}: {value}")


def main() -> None:
    # Basis elements
    one = Quaternion(1.0, 0.0, 0.0, 0.0)
    i = Quaternion(0.0, 1.0, 0.0, 0.0)
    j = Quaternion(0.0, 0.0, 1.0, 0.0)
    k = Quaternion(0.0, 0.0, 0.0, 1.0)

    print("Exploring quaternion power towers\n")

    # 1. Classical complex bases (stay in C)
    describe_tower(i, height=3)
    describe_tower(Quaternion(0.0, math.sqrt(0.5), 0.0, 0.0), height=4)  # exp(i pi/4)

    # 2. Mixed quaternion bases (likely to leave C quickly)
    describe_tower(Quaternion(0.0, 0.5, 0.5, 0.0), height=3)
    describe_tower(Quaternion(0.0, 0.0, 1.0, 1.0), height=3)

    # 3. Inverse exponentiation witness (reuse from main script)
    print("\nInverse exponentiation witness:")
    print(f"log(i) = {quaternion_log(i)}")
    print(f"(log i) * j = {quaternion_log(i) * j}")
    print(f"i^j = {quaternion_power(i, j)}")
    print(f"j^i = {quaternion_power(j, i)}  (for comparison)")


if __name__ == "__main__":
    main()

