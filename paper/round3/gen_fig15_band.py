#!/usr/bin/env python3
"""Regenerate Fig. 15: equilibrium energy band diagram of the optimized
FTO/TiO2/RbGeI3/CuI cell, redrawn from the manuscript's own numbers.

Levels (eV, vacuum-referenced):
  CuI:    Eg 3.1, chi 2.1 -> Ec -2.10, Ev -5.20
  RbGeI3: Eg 1.4, chi 3.9 -> Ec -3.90, Ev -5.30
  TiO2:   Eg 3.2, chi 4.0 -> Ec -4.00, Ev -7.20
  FTO:    degenerate n-type, aligned with the TiO2 ETL (-4.00/-7.20)
Offsets: CuI/RbGeI3 dEc 1.8, dEv 0.10; RbGeI3/TiO2 dEc 0.1, dEv 1.90.
Layer spans (nm): FTO 0-500, TiO2 500-510, RbGeI3 510-1210, CuI 1210-1310.
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

LAYERS = [('FTO', 0, 500, -4.00, -7.20), ('TiO$_2$', 500, 510, -4.00, -7.20),
          ('RbGeI$_3$', 510, 1210, -3.90, -5.30), ('CuI', 1210, 1310, -2.10, -5.20)]
EF = -4.5

fig, ax = plt.subplots(figsize=(10.5, 6.6), dpi=200)
for name, x0, x1, ec, ev in LAYERS:
    if name == 'CuI':
        ax.axvspan(x0, x1, color='#f3d9b8', alpha=0.30, zorder=0)
    else:
        ax.axvspan(x0, x1, color='#c9daf8', alpha=0.35, zorder=0)
    ax.plot([x0, x1], [ec, ec], color='#1f4e79', lw=2.6, zorder=3)
    ax.plot([x0, x1], [ev, ev], color='#c0392b', lw=2.6, zorder=3)
ax.plot([0, 1310], [EF, EF], ls='--', color='#333333', lw=1.6, zorder=3)

def dlabel(x, y, txt, dx=0, dy=0.0, ha='center'):
    ax.annotate(txt, xy=(x, y), xytext=(x + dx, y + dy), ha=ha, fontsize=13,
                color='black', arrowprops=dict(arrowstyle='-', lw=1.2))

dlabel(510, -3.55, r'$\Delta E_c \approx 0.1$ eV')              # TiO2/RbGeI3, Ec
dlabel(510, -6.30, r'$\Delta E_v \approx 1.9$ eV')              # TiO2/RbGeI3, Ev
dlabel(1210, -2.45, r'$\Delta E_c \approx 1.8$ eV')             # CuI/RbGeI3, Ec
dlabel(1208, -5.85, r'$\Delta E_v \approx 0.1$ eV', dx=210)     # CuI/RbGeI3, Ev

ax.set_xlim(0, 1310)
ax.set_ylim(-9.2, -0.6)
ax.set_xlabel('Position (nm)', fontsize=14)
ax.set_ylabel('Energy (eV)', fontsize=14)
ax.set_xticks([0, 500, 1210, 1310])
ax.set_xticklabels(['0', '500', '1210', '1310'], fontsize=11)
ax.tick_params(axis='y', labelsize=12)
for name, x0, x1, ec, ev in LAYERS:
    ax.text((x0 + x1) / 2, -8.4, name, ha='center', fontsize=15,
            fontstyle='italic')
ax.legend([ax.plot([], [], color='#1f4e79', lw=2.6)[0],
           ax.plot([], [], color='#c0392b', lw=2.6)[0],
           ax.plot([], [], ls='--', color='#333333')[0]],
          [r'$E_c$', r'$E_v$', r'$E_f$'], loc='upper left', fontsize=13,
          frameon=False)
ax.set_title('Equilibrium Energy Band Diagram of the Optimized '
             r'FTO/TiO$_2$/RbGeI$_3$/CuI Solar Cell', fontsize=16)
plt.tight_layout()
out = '/home/touhid/Documents/materilaspaper/paper/round3/figs/fig15_band.png'
plt.savefig(out)
print('saved', out)