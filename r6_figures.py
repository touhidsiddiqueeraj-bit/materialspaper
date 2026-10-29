#!/usr/bin/env python3
"""r6_figures — WP1/WP3/WP4/WP2 figures for Optical Materials submission. 300 dpi."""
import json, numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

OUT = '/home/touhid/Documents/materilaspaper/r5_results/'
D = json.load(open(OUT + 'r6_realistic_waterfall.json'))
B = json.load(open(OUT + 'r6_bsf_sweep.json'))
ML = json.load(open(OUT + 'r6_ml.json'))
GR = np.load(OUT + 'r6_GR.npz')

plt.rcParams.update({'font.size': 10, 'figure.dpi': 300})

# 1 waterfall
labels = ['Ideal\n26.81', '+rad/Auger\n26.79', '+10% refl\n24.08', '+bulk Nt15\n22.34', '+if Nt15\n20.80',
          'BSF ideal\n30.35', 'BSF full-real\n23.29']
vals = [26.81, D['R1_radAug100']['PCE_1sun'], D['R2_refl90']['PCE_1sun'],
        D['R3_bulk15']['PCE_1sun'], D['R4_bulkif15']['PCE_1sun'], 30.35,
        D['R5full']['PCE_1sun']]
cols = ['#1f77b4'] * 5 + ['#2ca02c'] * 2
fig, ax = plt.subplots(figsize=(7.5, 3.6))
ax.bar(labels, vals, color=cols)
ax.set_ylabel('PCE (% 1-sun norm.)')
ax.set_title('Loss waterfall: ideal to realistic, with BSF recovery')
for i, v in enumerate(vals):
    ax.text(i, v + 0.3, f'{v:.2f}', ha='center', fontsize=8)
fig.tight_layout(); fig.savefig(OUT + 'fig_r6_waterfall.png', dpi=300); plt.close(fig)

# 2 BSF heatmap (NA rows x thickness cols)
nas = ['NA17', 'NA18', 'NA19']; ds = [30, 50, 80, 100]
def _pce(r):
    return r.get('PCE', r.get('PCE_1sun'))
M = np.array([[_pce(B[f'r6_BSF{d}_{n}']) for d in ds] for n in nas])
fig, ax = plt.subplots(figsize=(5.2, 3.4))
im = ax.imshow(M, cmap='YlGn', aspect='auto', vmin=28, vmax=30.5)
ax.set_xticks(range(4), [f'{d}' for d in ds]); ax.set_yticks(range(3), ['1e17', '1e18', '1e19'])
ax.set_xlabel('BSF thickness (nm)'); ax.set_ylabel('BSF NA (/cm3)')
ax.set_title('BSF sweep PCE (%): doping dominates, thickness flat')
for i in range(3):
    for j in range(4):
        ax.text(j, i, f'{M[i, j]:.2f}', ha='center', fontsize=8)
fig.colorbar(im, label='PCE (%)')
fig.tight_layout(); fig.savefig(OUT + 'fig_r6_bsf.png', dpi=300); plt.close(fig)

# 3 ML parity (factorial main)
fig, ax = plt.subplots(figsize=(4.6, 4.2))
ax.scatter(ML['yte2'], ML['px2'], s=8, alpha=0.6)
lo, hi = min(ML['yte2']), max(ML['yte2'])
ax.plot([lo, hi], [lo, hi], 'r--', lw=1)
ax.set_xlabel('SCAPS PCE (%)'); ax.set_ylabel('XGBoost PCE (%)')
ax.set_title(f"Factorial surrogate R2={ML['xgb_factorial4']['R2']}")
fig.tight_layout(); fig.savefig(OUT + 'fig_r6_parity.png', dpi=300); plt.close(fig)

# 4 SHAP bar
rank = ML['shap_ranking']
feats = [r[0] for r in rank][::-1]; imp = [r[1] for r in rank][::-1]
fig, ax = plt.subplots(figsize=(5.4, 3.4))
ax.barh(feats, imp, color='#9467bd')
ax.set_xlabel('mean |SHAP| (PCE pts)')
ax.set_title('SHAP importance (UQ-8feat surrogate)')
fig.tight_layout(); fig.savefig(OUT + 'fig_r6_shap.png', dpi=300); plt.close(fig)

# 5 G-R + MS
fig, (a1, a2) = plt.subplots(1, 2, figsize=(8.5, 3.4))
a1.semilogy(GR['x_nm'], GR['G'], label='G(x) Beer-Lambert, SCAPS-Jsc norm.')
a1.semilogy(GR['x_nm'], GR['U'], label='U(x) SRH ~2% scale (illustrative)')
a1.set_xlabel('depth (nm)'); a1.set_ylabel('/m3/s'); a1.legend(fontsize=8); a1.set_title('Generation-recombination profile')
V = np.linspace(-0.5, 1.2, 50); Cinv2 = 9.399e4 * (1.457 - V) / 1e4  # scaled illustr.
a2.plot(V, Cinv2 / 1e8)
a2.set_xlabel('V (V)'); a2.set_ylabel('1/C2 (arb., slope from NA=1e18/cm3)')
a2.set_title('Mott-Schottky baseline (Vbi=1.457 V)')
fig.tight_layout(); fig.savefig(OUT + 'fig_r6_grms.png', dpi=300); plt.close(fig)
print('figures saved')
