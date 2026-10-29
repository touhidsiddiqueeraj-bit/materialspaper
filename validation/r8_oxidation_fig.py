#!/usr/bin/env python3
"""r8_oxidation_fig — PCE vs V_Ge formation energy (oxidation-budget figure).

Data: consolidated-device Nt ladder from archived runs
  Nt=1e14 -> 27.06 (H1), 1e15 -> 24.40 (S1), 1e16 -> 20.76 (H1-Nt16),
  plus current-state rung Nt=1e17 -> 15.53 (r8_budget_check.json).
Mapping: E^f = -kT*ln(Nt/Nsites), Nsites = 4.87e21 cm-3 (a = 5.9 A), 300 K.
Anchors: TRPL sub-ns -> Nt >= 1e17 (E^f <= 0.28); N_A-collapse onset 1e16.
Output: solar_submission/figs/fig39.png
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

plt.rcParams.update({'font.size': 11})
kT = 0.025851
NS = 1 / (5.9e-8) ** 3

# archived CONSOLIDATED points on the rebased H1 deck (Nt cm-3, PCE).
# Dashed extension is schematic (reviewer: equilibrium bounds kinetics).
pts = [(1e14, 27.06), (1e15, 24.40), (1e16, 20.76)]
ef = [-kT * np.log(n / NS) for n, _ in pts]

fig, ax = plt.subplots(figsize=(6.4, 4.6))
xs = np.linspace(ef[-1], ef[0], 200)
ns = NS * np.exp(-np.array(xs) / kT)
ax.plot(xs, np.interp(np.log10(ns), [14, 15, 16],
                      [p for _, p in pts]), 'k-', lw=1.8)
ax.plot(ef, [p for _, p in pts], 'ko', ms=6, label='SCAPS consolidated Nt ladder')
ax.plot(-kT * np.log(1e17 / NS), 15.53, 'rs', ms=7, label='current-state rung (Nt=1e17)')
ax.plot([ef[-1], 0.15], [20.76, 2.0], 'k--', lw=1.2)
ax.annotate('metallic short-circuit\n(Ming et al.)', (0.15, 2.0), xytext=(6, 12),
            textcoords='offset points', fontsize=9,
            arrowprops=dict(arrowstyle='->', lw=0.8))

# processing-condition bands (staggered labels)
for (a, b, c, lab, yy) in [(0.46, 0.58, '#c8e6c9', 'glovebox, Ge-rich', 4.0),
                            (0.38, 0.46, '#fff9c4', 'marginal', 8.0),
                            (0.32, 0.38, '#ffe0b2', 'brief air', 4.0),
                            (0.12, 0.32, '#ffcdd2', 'ambient / metallic', 26.0)]:
    ax.axvspan(a, b, color=c, alpha=0.55)
    ax.text((a + b) / 2, yy, lab, ha='center', fontsize=8.5, style='italic')

ax.annotate('headline 27.06%', (ef[0], 27.06), xytext=(-72, -10),
            textcoords='offset points', fontsize=9,
            arrowprops=dict(arrowstyle='->', lw=0.8))
ax.annotate('reported sub-ns TRPL\nimplies Nt>=1e17', (0.26, 11.5),
            xytext=(-86, 26), textcoords='offset points', fontsize=9,
            arrowprops=dict(arrowstyle='->', lw=0.8))
ax.annotate(r'$N_A$ soft-penalty onset ($10^{16}$, $-0.3$pp)',
            (0.338, 20.76), xytext=(8, 10),
            textcoords='offset points', fontsize=9,
            arrowprops=dict(arrowstyle='->', lw=0.8))
ax.set_xlabel(r'V$_{\mathregular{Ge}}$ formation energy $E^f$ (eV)  $\longleftarrow$  increasing oxidation', fontsize=12)
ax.set_ylabel('PCE (%)', fontsize=12)
ax.tick_params(labelsize=11)
ax.set_xlim(0.12, 0.58)
ax.set_ylim(0, 29)
ax.grid(alpha=0.3)
fig.savefig('/home/touhid/Documents/materilaspaper/solar_submission/figs/fig39.png',
            dpi=300, bbox_inches='tight')
print('fig39 saved')
