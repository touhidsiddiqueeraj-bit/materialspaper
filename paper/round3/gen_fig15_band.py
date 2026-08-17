#!/usr/bin/env python3
"""Regenerate Fig. 15: equilibrium energy band diagram of the optimized
FTO/TiO2/RbGeI3/CuI cell, in the style of the original SCAPS-1D diagram
(interface step connectors, Fn/Fp quasi-Fermi pair, layer labels above with
thicknesses). All numbers come from the manuscript itself.

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
EC = '#1f4e79'
EV = '#c0392b'
BOUND = '#8c8c8c'

fig, ax = plt.subplots(figsize=(10.5, 6.6), dpi=200)
for name, x0, x1, ec, ev in LAYERS:
    ax.plot([x0, x1], [ec, ec], color=EC, lw=2.4, zorder=3)
    ax.plot([x0, x1], [ev, ev], color=EV, lw=2.4, zorder=3)

# vertical step connectors at the interfaces (both bands) so the band edges
# read as continuous curves rather than floating segments
for xb in (500, 510, 1210):
    for y in (-4.00, -7.20, -3.90, -5.30, -2.10, -5.20):
        ax.plot([xb, xb], [y, y], color='#666666', lw=1.2, zorder=2,
                solid_capstyle='butt')

# dotted boundary lines between layers
for xb in (500, 510, 1210):
    ax.axvline(xb, color=BOUND, ls=':', lw=1.4, zorder=1)

# Fn/Fp quasi-Fermi levels (coincident at equilibrium)
for dy in (-0.015, 0.015):
    ax.plot([0, 1310], [EF + dy, EF + dy], ls='--', color='#2e7d32',
            lw=1.6, zorder=4, solid_capstyle='butt')
ax.text(1315, EF, 'F$_n$, F$_p$ (E$_f$)', fontsize=12.5, color='#2e7d32',
        ha='left', va='center')

def dlabel(x, y, txt, dx=0, dy=0.0, ha='center', fs=13):
    ax.annotate(txt, xy=(x, y), xytext=(x + dx, y + dy), ha=ha, fontsize=fs,
                color='black', arrowprops=dict(arrowstyle='-', lw=1.2))

dlabel(509, -3.78, r'$\Delta E_c \approx 0.1$ eV')              # TiO2/RbGeI3, Ec
dlabel(509, -6.32, r'$\Delta E_v \approx 1.9$ eV')              # TiO2/RbGeI3, Ev
dlabel(1209, -2.52, r'$\Delta E_c \approx 1.8$ eV', dx=20)      # CuI/RbGeI3, Ec
dlabel(1209, -5.72, r'$\Delta E_v \approx 0.1$ eV', dx=60)      # CuI/RbGeI3, Ev

ax.set_xlim(0, 1370)
ax.set_ylim(-7.6, -1.0)
ax.set_xlabel('Device Thickness (nm)', fontsize=14)
ax.set_ylabel('Energy (eV)', fontsize=14)
ax.set_xticks([0, 500, 1210, 1310])
ax.set_xticklabels(['0', '500', '1210', '1310'], fontsize=11)
ax.set_yticks(range(-7, 0))
ax.tick_params(axis='y', labelsize=12)
for name, x0, x1, ec, ev in LAYERS:
    label = name if name in ('FTO', 'CuI') else (name + r' (ETL)' if name == 'TiO$_2$' else r' (Absorber)')
    ax.text((x0 + x1) / 2, -1.22, name, ha='center', fontsize=14)
ax.text(1050, -1.48, '(Absorber)', ha='center', fontsize=11.5, color='#444444')
ax.text(520, -1.48, '(ETL)', ha='center', fontsize=11.5, color='#444444')
ax.text(250, -1.48, '(500 nm)', ha='center', fontsize=11.5, color='#444444')
ax.text(1260, -1.48, '(100 nm)', ha='center', fontsize=11.5, color='#444444')
ax.text(860, -1.48, '(700 nm)', ha='center', fontsize=11.5, color='#444444')
ax.legend([ax.plot([], [], color=EC, lw=2.4)[0],
           ax.plot([], [], color=EV, lw=2.4)[0],
           ax.plot([], [], ls='--', color='#2e7d32', lw=1.6)[0]],
          [r'$E_c$', r'$E_v$', r'$F_n$, $F_p$ ($E_f$)'],
          loc='lower right', fontsize=13, frameon=False)
ax.set_title('Equilibrium Energy Band Diagram of the Optimized '
             r'FTO/TiO$_2$/RbGeI$_3$/CuI Solar Cell', fontsize=16)
plt.tight_layout()
out = '/home/touhid/Documents/materilaspaper/paper/round3/figs/fig15_band.png'
plt.savefig(out)
print('saved', out)
