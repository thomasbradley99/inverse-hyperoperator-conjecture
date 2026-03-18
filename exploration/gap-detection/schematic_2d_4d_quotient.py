#!/usr/bin/env python3
"""
Schematic: path open in 2D (z), open in 4D, closed in quotient.
Conceptual diagram only (no data) — makes the conjecture's story explicit.
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

fig, axes = plt.subplots(1, 3, figsize=(12, 4))

# Panel 1: Output = C (z only) — path OPEN
ax = axes[0]
t = np.linspace(0, 1, 50)
# Simple open curve (e.g. spiral that doesn't close)
x = 0.5 + 0.4 * np.cos(2 * np.pi * t)
y = 0.5 + 0.4 * np.sin(2 * np.pi * t)
y[-1] += 0.3  # endpoint displaced so path is open
ax.plot(x, y, "b-", linewidth=2)
ax.plot(x[0], y[0], "go", markersize=12, label="start")
ax.plot(x[-1], y[-1], "r^", markersize=12, label="end")
ax.set_title("Output = C (z only)\npath does NOT close", fontsize=11)
ax.set_xlabel("Re(z)")
ax.set_ylabel("Im(z)")
ax.legend(loc="upper right", fontsize=9)
ax.set_aspect("equal")
ax.grid(True, alpha=0.3)
ax.set_xlim(0, 1)
ax.set_ylim(0, 1.2)

# Panel 2: Output = 4D (z, k, m) — path still OPEN
ax = axes[1]
# Same idea: curve in 2D projection that suggests 4D (start and end different)
x2 = 0.5 + 0.35 * np.cos(2 * np.pi * t)
y2 = 0.5 + 0.35 * np.sin(2 * np.pi * t)
y2[-1] += 0.25
ax.plot(x2, y2, "b-", linewidth=2)
ax.plot(x2[0], y2[0], "go", markersize=12, label="start")
ax.plot(x2[-1], y2[-1], "r^", markersize=12, label="end")
ax.set_title("Output = 4D (z, k, m) or H\npath still does NOT close", fontsize=11)
ax.set_xlabel("(z, k) or 1-i-j slice")
ax.set_ylabel("(z, m) or 1-i-k slice")
ax.legend(loc="upper right", fontsize=9)
ax.set_aspect("equal")
ax.grid(True, alpha=0.3)
ax.set_xlim(0, 1)
ax.set_ylim(0, 1.2)

# Panel 3: Quotient 4D / (deck lattice) — path CLOSES
ax = axes[2]
# Closed circle
theta = np.linspace(0, 2 * np.pi, 50)
xc = 0.5 + 0.4 * np.cos(theta)
yc = 0.5 + 0.4 * np.sin(theta)
ax.plot(xc, yc, "b-", linewidth=2)
ax.plot(xc[0], yc[0], "go", markersize=12, label="start = end")
ax.set_title("Output = 4D / (Zj + Zk) (quotient)\npath CLOSES", fontsize=11)
ax.set_xlabel("equivalence classes")
ax.set_ylabel("")
ax.legend(loc="upper right", fontsize=9)
ax.set_aspect("equal")
ax.grid(True, alpha=0.3)
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)

plt.suptitle(
    "Where does the path close? 2D and 4D: open. Quotient of 4D: closed.",
    fontsize=12,
    fontweight="bold",
)
plt.tight_layout()
import os
out = os.path.join(os.path.dirname(__file__), "schematic_2d_4d_quotient.png")
plt.savefig(out, dpi=150, bbox_inches="tight")
plt.close()
print(f"Saved {out}")
