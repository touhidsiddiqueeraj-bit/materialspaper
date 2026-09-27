#!/usr/bin/env python3
"""r5_figures — all Round-5 figures + markdown tables from result JSONs.
Reads r5_results/*.json, writes r5_results/fig_*.png + r5_tables.md.
Style: 300 dpi, ~5.25 in wide to match paper figures."""
import json, os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

R = '/home/touhid/Documents/materilaspaper/r5_results'
plt.rcParams.update({'font.size': 9, 'figure.dpi': 300})


def save(fig, name):
    fig.tight_layout()
    fig.savefig(os.path.join(R, name), dpi=300)
    plt.close(fig)
    print('wrote', name)


J = lambda f: json.load(open(os.path.join(R, f)))
tables = []

# ---- 1. Et lethality curve ----
d = J('r5_et_sigma.json')
ets, pces, vocs = [], [], []
for k, v in sorted(d.items()):
    if k.startswith('r5_Et') and 'PCE' in v and v.get('PCE', 0) > 0:
        ets.append(float(k.split('Et')[1].split('_')[0]))
        pces.append(v['PCE'])
        vocs.append(v['Voc'])
fig, ax = plt.subplots(figsize=(5.25, 3.2))
ax.plot(ets, pces, 'o-', ms=5)
ax.set_xlabel('Defect energy Et (eV above Ev)')
ax.set_ylabel('PCE (%)')
ax.grid(alpha=0.3)
save(fig, 'fig_r5_Et.png')
tables.append(('Et sweep (Nt=1e14 cm-3)',
               ['Et (eV)', 'PCE (%)', 'Voc (V)'],
               [[e, p, v] for e, p, v in zip(ets, pces, vocs)]))

# ---- 2. sigma asymmetry heat table (text table only) ----
sigs = {k: v for k, v in d.items() if '_sp' in k}
if sigs:
    rows = []
    for k in sorted(sigs):
        v = sigs[k]
        rows.append([k, v.get('PCE'), v.get('Voc'), v.get('FF')])
    tables.append(('sigma_n x sigma_p at Et=0.6 eV (PCE %)',
                   ['case', 'PCE', 'Voc', 'FF'], rows))

# ---- 3. NA doping ----
d = J('r5_na.json')
x, p, vo, js = [], [], [], []
for k in sorted(d, key=lambda k: float(k[5:])):
    v = d[k]
    x.append(float(k[5:]) - 6)  # log10 in /cm^3
    p.append(v['PCE'])
    vo.append(v['Voc'])
    js.append(v['Jsc'])
fig, ax = plt.subplots(figsize=(5.25, 3.2))
ax.plot(x, p, 's-', ms=5, label='PCE')
ax.set_xlabel('log10 NA (cm-3)')
ax.set_ylabel('PCE (%)')
ax.grid(alpha=0.3)
save(fig, 'fig_r5_NA.png')
tables.append(('NA sweep', ['logNA (/cm3)', 'PCE', 'Voc', 'Jsc'],
               [[a, b, c, e] for a, b, c, e in zip(x, p, vo, js)]))

# ---- 4. Rs tolerance ----
d = J('r5_rs.json')
rs = sorted(d, key=float)
pr = [d[k]['PCE'] for k in rs]
fr = [d[k]['FF'] for k in rs]
fig, ax = plt.subplots(figsize=(5.25, 3.2))
ax.plot([float(k) for k in rs], pr, 'o-', ms=5, label='PCE')
ax.plot([float(k) for k in rs], fr, 's--', ms=4, label='FF')
ax.axhline(20, color='r', ls=':', lw=1)
ax.set_xlabel('Rs (ohm.cm2)')
ax.set_ylabel('%')
ax.legend()
ax.grid(alpha=0.3)
save(fig, 'fig_r5_Rs.png')

# ---- 5. mobility ----
d = J('r5_mobility.json')
m1 = sorted([(int(k[5:]), d[k]['PCE']) for k in d if k.startswith('r5_mu')
             and '_th' not in k and '_mup' not in k and 'mun' not in k])
fig, ax = plt.subplots(figsize=(5.25, 3.2))
ax.semilogx([m for m, _ in m1], [p for _, p in m1], 'o-', ms=5)
ax.set_xlabel('mu_n = mu_p (cm2/Vs)')
ax.set_ylabel('PCE (%)')
ax.grid(alpha=0.3, which='both')
save(fig, 'fig_r5_mu.png')
tables.append(('mobility 1D (700 nm)', ['mu', 'PCE'], m1))

# ---- 6. Ea fit ----
d = J('r5_temp.json')
Ts = sorted([int(k[4:]) for k in d if k.startswith('r5_T')])
Vo = [d[f'r5_T{T}']['Voc'] for T in Ts]
coef = np.polyfit(Ts, Vo, 1)  # Voc = a*T + b; Ea = q*b
Ea = coef[1]  # eV
fig, ax = plt.subplots(figsize=(5.25, 3.2))
ax.plot(Ts, Vo, 'o', ms=5)
xx = np.array([0, 420])
ax.plot(xx, coef[0] * xx + coef[1], 'r--', lw=1)
ax.set_xlabel('T (K)')
ax.set_ylabel('Voc (V)')
ax.grid(alpha=0.3)
save(fig, 'fig_r5_Ea.png')
print(f'Ea = {Ea:.3f} eV, dVoc/dT = {coef[0]*1000:.2f} mV/K')
tables.append(('temperature (Ea fit)', ['T (K)', 'Voc', 'PCE'],
               [[T, d[f'r5_T{T}']['Voc'], d[f'r5_T{T}']['PCE']] for T in Ts]))

# ---- 7. CsGeI3 OAT summary ----
try:
    d = J('r5_csgei3_oat.json')
    fams = {}
    for k, v in d.items():
        fam = ''.join(c for c in k[6:] if not c.isdigit() and c not in '.-')
        fams.setdefault(fam, []).append((k, v.get('PCE', 0)))
    print('CsGeI3 families:', {k: len(v) for k, v in fams.items()})
    best = max(d.items(), key=lambda kv: kv[1].get('PCE', 0))
    print('CsGeI3 OAT best point:', best)
except FileNotFoundError:
    print('CsGeI3 OAT not ready yet')

with open(os.path.join(R, 'r5_tables.md'), 'w') as f:
    for title, hdr, rows in tables:
        f.write(f'## {title}\n\n| ' + ' | '.join(hdr) + ' |\n')
        f.write('|' + '|'.join(['---'] * len(hdr)) + '|\n')
        for r in rows:
            f.write('| ' + ' | '.join(str(c) for c in r) + ' |\n')
        f.write('\n')
print('wrote r5_tables.md')
