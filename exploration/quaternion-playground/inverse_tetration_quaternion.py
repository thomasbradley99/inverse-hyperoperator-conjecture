#!/usr/bin/env python3
"""
Demonstration script: inverse tetration behaviour requiring quaternions.

We adopt the conventional extension a^q := exp((log a) * q) for quaternions,
then evaluate i^j and sample i^z for complex exponents z = a + bi to show that
the quaternion solution exits the complex plane.
"""

import math
from dataclasses import dataclass


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
    """Quaternion exponential via polar form."""
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
    """Exponentiation using exp((log base) * exponent)."""
    return quaternion_exp(quaternion_log(base) * exponent)


def approx_equal(a: float, b: float, tol: float = 1e-9) -> bool:
    return abs(a - b) < tol


def close_quaternions(a: Quaternion, b: Quaternion, tol: float = 1e-9) -> bool:
    return (
        approx_equal(a.w, b.w, tol)
        and approx_equal(a.x, b.x, tol)
        and approx_equal(a.y, b.y, tol)
        and approx_equal(a.z, b.z, tol)
    )


def main() -> None:
    one = Quaternion(1.0, 0.0, 0.0, 0.0)
    i = Quaternion(0.0, 1.0, 0.0, 0.0)
    j = Quaternion(0.0, 0.0, 1.0, 0.0)
    k = Quaternion(0.0, 0.0, 0.0, 1.0)

    ln_i = quaternion_log(i)
    exp_argument = ln_i * j
    w = quaternion_exp(exp_argument)

    print("log(i) =", ln_i)
    print("(log i) * j =", exp_argument)
    print("i^j = exp((log i) * j) =", w)
    print("Matches basis k?", close_quaternions(w, k))

    print("\nSample complex exponents z = a + bi and their i^z values:")
    samples = [
        (1.0, 0.0),
        (0.5, 0.25),
        (-1.0, 0.75),
        (2.0, -0.5),
    ]
    for a, b in samples:
        z = Quaternion(a, b, 0.0, 0.0)
        value = quaternion_power(i, z)
        print(f"z = {a:+.2f} {b:+.2f}i -> i^z = {value}")


if __name__ == "__main__":
    main()

