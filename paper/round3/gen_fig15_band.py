#!/usr/bin/env python3
"""Regenerate Fig. 15 in the style of figuresample.jpeg (sample band diagram):
Ec solid green, Ev solid red, and coincident equilibrium Fn/Fp at EF; legend
Ec(eV) Fn(eV) Fp(eV) Ev(eV) top-right; stacked per-layer labels inside the
plot (role / material / thickness) with per-layer Eg annotations; numeric
interface annotations; vertical band connectors at interfaces.

Layer order follows the sample (HTL first, FTO last): CuI | RbGeI3 | TiO2 | FTO.
Levels (eV, vacuum-referenced, same as in the manuscript):
  CuI:    Eg 3.1, chi 2.1 -> Ec -2.10, Ev -5.20
  RbGeI3: Eg 1.4, chi 3.9 -> Ec -3.90, Ev -5.30
  TiO2:   Eg 3.2, chi 4.0 -> Ec -4.00, Ev -7.20
  FTO:    Eg 3.2, chi 4.4 -> Ec -4.40, Ev -7.60
Offsets: CuI/RbGeI3 dEc 1.8, dEv 0.10; RbGeI3/TiO2 dEc 0.1, dEv 1.90.
Layer spans (nm): CuI 0-100, RbGeI3 100-800, TiO2 800-810, FTO 810-1310.
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# left-to-right: HTL first, FTO last (sample orientation)
LAYERS = [('HTL', 'CuI', 0, 100, -2.10, -5.20, 3.1, '(100 nm)'),
          ('Absorber', 'RbGeI$_3$', 100, 800, -3.90, -5.30, 1.4, '(700 nm)'),
          ('ETL', 'TiO$_2$', 800, 810, -4.00, -7.20, 3.2, '(10 nm)'),
          ('FTO', '', 810, 1310, -4.40, -7.60, 3.2, '(500 nm)')]
EF = -4.5
EC_C = '#0f7a11'   # solid green
EV_C = '#b5080a'   # solid red
FN_C = '#0f7a11'   # dashed green
FP_C = '#0f7a11'   # dotted green

fig, ax = plt.subplots(figsize=(10.0, 6.2), dpi=200)

# band lines: continuous across boundaries inside the plot, steps at interfaces
def draw_band(x0, x1, y, color, style, lw):
    ax.plot([x0, x1], [y, y], color=color, lw=lw, ls=style,
            solid_capstyle='butt', zorder=3)

for i, (_, _, x0, x1, ec, ev, *_) in enumerate(LAYERS):
    draw_band(x0, x1, ec, EC_C, 'solid', 2.2)
    draw_band(x0, x1, ev, EV_C, 'solid', 2.2)
    # This is an equilibrium, zero-bias diagram: Fn = Fp = EF. Real
    # illuminated splitting requires a SCAPS band-profile export.
    draw_band(x0, x1, EF, FN_C, 'dashed', 1.2)
    draw_band(x0, x1, EF, FP_C, 'dotted', 1.4)

# vertical connectors at each interface, using the actual adjacent band edges
for left, right in zip(LAYERS, LAYERS[1:]):
    xb = right[2]
    ax.plot([xb, xb], [left[4], right[4]], color=EC_C, lw=1.6,
            solid_capstyle='butt', zorder=2)
    ax.plot([xb, xb], [left[5], right[5]], color=EV_C, lw=1.6,
            solid_capstyle='butt', zorder=2)

# stacked labels inside each layer, kept clear of the band lines
LABELS = [
    ('CuI',    [('HTL', -2.55), ('CuI', -3.05), ('(100 nm)', -3.55), ('3.1 eV', -2.15)]),
    ('RbGeI3', [('Absorber', -3.10), ('RbGeI$_3$', -3.38), ('(700 nm)', -3.66), ('1.4 eV', -2.60)]),
    ('TiO2',   [('ETL', -3.35), ('TiO$_2$', -3.65), ('(10 nm)', -3.95)]),  # 3.2 eV shown on FTO line? skip
    ('FTO',    [('3.2 eV', -4.15), ('FTO', -5.65), ('(500 nm)', -6.10)]),
]
CX = {'CuI': 50, 'RbGeI3': 450, 'TiO2': 805, 'FTO': 1060}
for name, texts in LABELS:
    xc = CX[name]
    for txt, y in texts:
        ax.text(xc, y, txt, ha='center', va='center', fontsize=13,
                bbox=dict(boxstyle='round,pad=0.15', fc='white', ec='white', alpha=0.85))

# interface annotations (offsets) - clear of lines
ax.annotate('$\\Delta$E$_c$ = 1.8 eV', xy=(100, -2.9), xytext=(265, -2.3),
            fontsize=12, ha='center', color='k',
            arrowprops=dict(arrowstyle='-', color='k', lw=0.8))
ax.annotate('$\\Delta$E$_v$ = 0.1 eV', xy=(100, -5.25), xytext=(265, -5.8),
            fontsize=12, ha='center', color='k',
            arrowprops=dict(arrowstyle='-', color='k', lw=0.8))
ax.annotate('$\\Delta$E$_c$ = 0.1 eV', xy=(800, -3.95), xytext=(650, -2.3),
            fontsize=12, ha='center', color='k',
            arrowprops=dict(arrowstyle='-', color='k', lw=0.8))
ax.annotate('$\\Delta$E$_v$ = 1.9 eV', xy=(800, -6.3), xytext=(620, -6.8),
            fontsize=12, ha='center', color='k',
            arrowprops=dict(arrowstyle='-', color='k', lw=0.8))

ax.set_xlim(0, 1310)
ax.set_ylim(-8.0, -1.05)
ax.set_xlabel('Device Thickness (nm)', fontsize=15)
ax.set_ylabel('Energy (eV)', fontsize=15)
ax.set_xticks(range(0, 1201, 200))
ax.set_yticks(range(-7, 0))
ax.tick_params(labelsize=12)

# legend: Ec, Fn, Fp, Ev (sample order and placement: upper right)
legend_handles = [
    ax.plot([], [], color=EC_C, lw=2.2, ls='solid')[0],
    ax.plot([], [], color=FN_C, lw=1.2, ls='dashed')[0],
    ax.plot([], [], color=FP_C, lw=1.4, ls='dotted')[0],
    ax.plot([], [], color=EV_C, lw=2.2, ls='solid')[0],
]
ax.legend(legend_handles, ['Ec(eV)', 'Fn(eV)', 'Fp(eV)', 'Ev(eV)'],
          loc='upper right', fontsize=13, frameon=True, borderaxespad=0.5)

plt.tight_layout()
out = '/home/touhid/Documents/materilaspaper/paper/round3/figs/fig15_band.png'
plt.savefig(out)
print('saved', out)
