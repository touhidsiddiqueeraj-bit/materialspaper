#!/usr/bin/env python3
"""Regenerate Fig. 2: clean schematic of the FTO/TiO2/RbGeI3/CuI/Au device stack."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Rectangle

fig, ax = plt.subplots(figsize=(6.9, 3.8), dpi=300)
ax.set_xlim(0, 10)
ax.set_ylim(0, 6)
ax.axis("off")

layers = [
    ("Au",          "Au",             2.15, 2.70, "#f5c542", "metal"),
    ("CuI",         "CuI",            2.70, 3.35, "#e8a33d", "HTL"),
    ("RbGeI$_3$",   "Absorber",       3.35, 4.55, "#c0504d", "absorber"),
    ("TiO$_2$",     "ETL",            4.55, 4.80, "#4c9f8d", "ETL"),
    ("FTO",         "Front contact",  4.80, 5.45, "#7fb3d5", "TCO"),
]

for name, role_txt, y0, y1, color, role in layers:
    ax.add_patch(Rectangle((1.2, y0), 7.6, y1 - y0, facecolor=color, edgecolor="black", lw=1.2, zorder=2))
    ax.text(2.55, (y0 + y1) / 2, name, fontsize=13, ha="center", va="center", zorder=4,
            color="white" if role in ("absorber", "ETL") else "#222222", weight="bold")

# role labels, left side
role_x = 0.42
for _, role_txt, y0, y1, _, role in layers:
    if role == "metal":
        ax.text(role_x, (y0 + y1) / 2, "Back\ncontact", fontsize=9.5, ha="right", va="center", style="italic", color="#333")
    elif role == "TCO":
        ax.text(role_x, (y0 + y1) / 2, "TCO", fontsize=9.5, ha="right", va="center", style="italic", color="#333")
    elif role == "absorber":
        ax.text(role_x, (y0 + y1) / 2, "Absorber", fontsize=9.5, ha="right", va="center", style="italic", color="#333")
    else:
        ax.text(role_x, (y0 + y1) / 2, role_txt, fontsize=9.5, ha="right", va="center", style="italic", color="#333")

# thickness labels, right side with leader dots
thick = {"Au": "100 nm", "CuI": "100 nm", "RbGeI$_3$": "700 nm", "TiO$_2$": "10 nm", "FTO": "500 nm"}
for name, _, y0, y1, _, role in layers:
    mid = (y0 + y1) / 2
    ax.text(9.62, mid, thick[name], fontsize=11, ha="right", va="center")

# bandgap labels
ax.text(6.55, 3.95, "$E_g$ = 1.4 eV", fontsize=11, ha="center", va="center", color="white", weight="bold")
ax.text(6.55, 3.02, "$E_g$ = 3.1 eV", fontsize=9.5, ha="center", va="center", color="#3d2a00")
ax.text(6.55, 4.67, "$E_g$ = 3.2 eV", fontsize=9, ha="center", va="center", color="white")
ax.text(6.55, 5.12, "$E_g$ = 3.2 eV", fontsize=9, ha="center", va="center", color="#123a5e")
ax.text(6.55, 5.18, "$E_g$ = 3.2 eV", fontsize=9, ha="center", va="center", color="#123a5e")

# sunlight
for yy in (5.85, 5.65):
    ax.add_patch(FancyArrowPatch((5.0, yy), (5.0, 5.45), arrowstyle="-|>", mutation_scale=20,
                                 color="#d4a017", lw=3, zorder=1))
ax.text(5.35, 5.70, "AM 1.5G", fontsize=11, ha="left", va="center", color="#8a6d00", style="italic")

# carriers
ax.add_patch(FancyArrowPatch((4.6, 4.30), (1.35, 4.62), arrowstyle="-|>", mutation_scale=22,
                             color="#1a5b8c", lw=2.6, zorder=3, shrinkA=2, shrinkB=2))
ax.text(3.05, 4.72, "$e^-$", fontsize=14, color="#1a5b8c", ha="center")
ax.add_patch(FancyArrowPatch((5.4, 3.55), (8.45, 3.10), arrowstyle="-|>", mutation_scale=22,
                             color="#7a2f2f", lw=2.6, zorder=3, shrinkA=2, shrinkB=2))
ax.text(7.05, 3.10, "$h^+$", fontsize=14, color="#7a2f2f", ha="center")

# band-offset annotations
ax.annotate("$\\Delta E_c \\approx$ 1.8 eV\n(electron blocker)",
            xy=(1.28, 3.33), xytext=(1.05, 1.95),
            fontsize=10, ha="left", va="top", color="#7a2f2f",
            arrowprops=dict(arrowstyle="->", color="#7a2f2f", lw=1.0))
ax.annotate("$\\Delta E_c \\approx$ 0.1 eV\n(electron extraction)",
            xy=(1.28, 4.57), xytext=(6.7, 5.28),
            fontsize=10, ha="left", va="top", color="#0d3d35",
            arrowprops=dict(arrowstyle="->", color="#0d3d35", lw=1.0))

fig.tight_layout(pad=0.4)
fig.savefig("figures/schematic_redraw.png", dpi=300, bbox_inches="tight", facecolor="white")
print("saved figures/schematic_redraw.png")
