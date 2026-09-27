#!/usr/bin/env python3
"""r5_figures2 — Et lethality at Nt21, sigma asymmetry, Cs-vs-Rb, waterfall."""
import json, os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

R = '/home/touhid/Documents/materilaspaper/r5_results'
plt.rcParams.update({'font.size': 9, 'figure.dpi': 300})
J = lambda f: json.load(open(os.path.join(R, f)))


def save(fig, name):
    fig.tight_layout()
    fig.savefig(os.path.join(R, name), dpi=300)
    plt.close(fig)
    print('wrote', name)


# ---- 1. Et lethality at Nt=1e21 (mid-gap worst) ----
d = J('r5_et_sigma.json')
pts = []
for k, v in d.items():
    if k.endswith('_Nt21') and 'PCE' in v and v.get('PCE', 0) > 0:
        pts.append((float(k.split('Et')[1].split('_')[0]), v['PCE']))
pts.append((0.7, d['r5_Nt21_Et0.7']['PCE']))
pts.sort()
fig, ax = plt.subplots(figsize=(5.25, 3.2))
ax.plot([p[0] for p in pts], [p[1] for p in pts], 'o-', ms=5, color='#B03030')
ax.set_xlabel('Defect energy Et (eV above Ev), Nt = 1e15 cm-3')
ax.set_ylabel('PCE (%)')
ax.grid(alpha=0.3)
save(fig, 'fig_r5_Et_Nt21.png')

# ---- 2. sigma asymmetry grouped bars ----
d = J('r5_et_sigma.json')
sn_vals = ['1e-21', '1e-19', '1e-17']
sp_vals = ['1e-21', '1e-19', '1e-17']
keys = {(sn, sp): f'r5_sn{sn[0]}e{sn[-2:]}_sp{sp[0]}e{sp[-2:]}'
        for sn in sn_vals for sp in sp_vals}
fig, ax = plt.subplots(figsize=(5.25, 3.2))
x = np.arange(3)
w = 0.22
for i, sn in enumerate(sn_vals):
    vals = [d[keys[(sn, sp)]]['PCE'] for sp in sp_vals]
    ax.bar(x + (i - 1) * w, vals, w, label=f'sigma_n={sn} m2')
ax.set_xticks(x)
ax.set_xticklabels([f'sigma_p={s}' for s in sp_vals])
ax.set_ylabel('PCE (%)')
ax.legend(fontsize=8)
ax.grid(alpha=0.3, axis='y')
save(fig, 'fig_r5_sigma.png')

# ---- 3. CsGeI3 vs RbGeI3: ideal / realistic / high-oxidation ----
csf = J('r5_csfinal.json')
rb_base = {'PCE': 26.81, 'Voc': 1.1294, 'Jsc': 30.3156}
rb_nt21 = d.get('r5_Nt21_Et0.7', {'PCE': 24.84, 'Voc': 1.1119,
                                  'Jsc': 30.3072})
rb_nt22 = {'PCE': 21.45, 'Voc': 1.0631, 'Jsc': 30.2236}  # sn1e17_sp1e17
# (sigma*Nt product-identical lifetime point; documented in text)
cats = ['Ideal\n(Nt=1e14)', 'Realistic\n(Nt=1e15)', 'High oxidation\n(Nt=1e16)']
rb = [rb_base['PCE'], rb_nt21['PCE'], rb_nt22['PCE']]
cs = [csf['r5_csf_final']['PCE'], csf['r5_csf_Nt21']['PCE'],
      csf['r5_csf_Nt22']['PCE']]
fig, ax = plt.subplots(figsize=(5.25, 3.4))
x = np.arange(3)
ax.bar(x - 0.2, rb, 0.4, label='RbGeI3 (Eg=1.4 eV)')
ax.bar(x + 0.2, cs, 0.4, label='CsGeI3 (Eg=1.6 eV)')
ax.set_xticks(x)
ax.set_xticklabels(cats)
ax.set_ylabel('PCE (%)')
ax.legend(fontsize=8)
ax.grid(alpha=0.3, axis='y')
for i, (a, b) in enumerate(zip(rb, cs)):
    ax.text(i - 0.2, a + 0.3, f'{a:.1f}', ha='center', fontsize=8)
    ax.text(i + 0.2, b + 0.3, f'{b:.1f}', ha='center', fontsize=8)
save(fig, 'fig_r5_Cs_vs_Rb.png')

# ---- 4. derating waterfall (RbGeI3 ideal -> realistic) ----
rs = J('r5_rs.json')
steps = ['Ideal\n26.81', 'Nt=1e15\n24.84', 'Nt=1e16\n21.45',
         '+Rs=4\n18.5*', '+Rs=8\n16.3*']
vals = [26.81, 24.84, 21.45,
        21.45 * rs['4']['PCE'] / rs['0']['PCE'],
        21.45 * rs['8']['PCE'] / rs['0']['PCE']]
fig, ax = plt.subplots(figsize=(5.25, 3.2))
ax.bar(range(len(steps)), vals, color='#2E6E4E')
ax.set_xticks(range(len(steps)))
ax.set_xticklabels(steps, fontsize=8)
ax.set_ylabel('PCE (%)')
ax.grid(alpha=0.3, axis='y')
save(fig, 'fig_r5_waterfall.png')
print('waterfall:', [round(v, 2) for v in vals])
