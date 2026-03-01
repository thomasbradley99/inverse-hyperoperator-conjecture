#!/usr/bin/env python3
"""Quick closure-ladder demo:
1) [z1, z2] = 0 in C
2) [q1, q2] can be nonzero in H
3) z^z never appears to hit 0 in a finite complex scan
"""

from __future__ import annotations

import cmath
import math
import random
from dataclasses import dataclass


@dataclass(frozen=True)
class Quaternion:
    a: float
    b: float
    c: float
    d: float

    def __mul__(self, other: "Quaternion") -> "Quaternion":
        a1, b1, c1, d1 = self.a, self.b, self.c, self.d
        a2, b2, c2, d2 = other.a, other.b, other.c, other.d
        return Quaternion(
            a1 * a2 - b1 * b2 - c1 * c2 - d1 * d2,
            a1 * b2 + b1 * a2 + c1 * d2 - d1 * c2,
            a1 * c2 - b1 * d2 + c1 * a2 + d1 * b2,
            a1 * d2 + b1 * c2 - c1 * b2 + d1 * a2,
        )

    def __sub__(self, other: "Quaternion") -> "Quaternion":
        return Quaternion(
            self.a - other.a, self.b - other.b, self.c - other.c, self.d - other.d
        )

    def norm(self) -> float:
        return math.sqrt(self.a**2 + self.b**2 + self.c**2 + self.d**2)

    def __repr__(self) -> str:
        return f"({self.a:+.2f} {self.b:+.2f}i {self.c:+.2f}j {self.d:+.2f}k)"


def complex_commutator_demo() -> None:
    print("=== Complex commutator test ===")
    pairs = [
        (1 + 2j, 3 - 4j),
        (-2 + 0.5j, 7 + 1.25j),
        (cmath.exp(1j), -3j),
    ]
    for z1, z2 in pairs:
        comm = z1 * z2 - z2 * z1
        print(f"[{z1}, {z2}] = {comm}")
    print("Result: all are exactly 0j (complex multiplication is commutative).")
    print()


def quaternion_commutator_demo() -> None:
    print("=== Quaternion commutator test ===")
    i = Quaternion(0, 1, 0, 0)
    j = Quaternion(0, 0, 1, 0)
    k = Quaternion(0, 0, 0, 1)

    comm_ij = i * j - j * i
    print(f"[i, j] = {comm_ij}   (expected 2k = {Quaternion(0,0,0,2)})")

    random.seed(42)
    q1 = Quaternion(*(random.uniform(-2, 2) for _ in range(4)))
    q2 = Quaternion(*(random.uniform(-2, 2) for _ in range(4)))
    comm = q1 * q2 - q2 * q1
    print(f"q1 = {q1}")
    print(f"q2 = {q2}")
    print(f"[q1, q2] = {comm}")
    print(f"||[q1, q2]|| = {comm.norm():.6f}")
    print("Result: generally nonzero, so multiplication is non-commutative in H.")
    print()
    _ = k  # keep symbol explicit in code context


def zz_scan_demo() -> None:
    print("=== z^z scan near complex plane ===")
    # Principal branch: z^z = exp(z*log(z)) for z != 0.
    # We scan a finite grid and track min |z^z|.
    xs = [x / 10 for x in range(-30, 31)]
    ys = [y / 10 for y in range(-30, 31)]

    min_abs = float("inf")
    argmin_z = None
    argmin_val = None

    count = 0
    for x in xs:
        for y in ys:
            z = complex(x, y)
            if z == 0:
                continue
            val = cmath.exp(z * cmath.log(z))
            mag = abs(val)
            if mag < min_abs:
                min_abs = mag
                argmin_z = z
                argmin_val = val
            count += 1

    print(f"Scanned {count} points in [-3,3]x[-3,3] (step 0.1), z != 0.")
    print(f"Minimum |z^z| found: {min_abs:.12e} at z={argmin_z}")
    print(f"Value there: z^z = {argmin_val}")
    print("Result: never 0 in this scan, consistent with theorem (exp(w) != 0).")
    print()


def main() -> None:
    print("Quick demo: closure-ladder ideas in code\n")
    complex_commutator_demo()
    quaternion_commutator_demo()
    zz_scan_demo()
    print("Done.")


if __name__ == "__main__":
    main()
