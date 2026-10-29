#!/usr/bin/env python3
"""r8_figB — bespoke main/supplement figures from r8 archives (reviewer)."""
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

R = '/home/touhid/Documents/materilaspaper/r5_results'
F = '/home/touhid/Documents/materilaspaper/solar_submission/figs'
J = lambda f: json.load(open(f'{R}/{f}'))
plt.rcParams.update({'font.size': 10})


def save(fig, name):
    fig.tight_layout()
    fig.savefig(f'{F}/{name}', dpi=300)
    plt.close(fig)
    print('wrote', name)


def quad(jv):
    V = np.array(jv['V'])
    Ja = np.abs(np.array(jv['J']))
    o = np.argsort(V)
    V, Ja = V[o], Ja[o]
    i = Ja.argmin()
    return V[:i + 1], Ja[:i + 1]


def rs_post(Vt, Jt, Rs):
    Vp = Vt - Jt * Rs / 1000.0
    m = Vp > 0.001
    return Vp[m], Jt[m]


def rsh_post(Vt, Jt, Rsh):
    Jp = Jt - Vt / Rsh * 1000.0
    m = Jp > 0
    return Vt[m], Jp[m]


def mpp(V, JJ):
    P = V * JJ
    i = P.argmax()
    voc = float(np.interp(0, JJ[::-1], V[::-1]))
    return voc, float(JJ[0]), P[i] / (voc * JJ[0]) * 100, float(P[i])


# ---- fig16: H1 JV ----
d = J('r8_H1_JV.json')['r8_H1_JV']
V, Ja = quad(d)
voc, jsc, ff, pce = mpp(V, Ja)
fig, ax = plt.subplots(figsize=(6.4, 4.4))
ax.plot(V, Ja, 'k-', lw=1.6)
i = (V * Ja).argmax()
ax.plot(V[i], Ja[i], 'ro', ms=6)
ax.text(0.04, 0.94, f'Voc={voc:.2f} V\nJsc={jsc:.2f}\nFF={ff:.1f}%\nPCE={pce:.2f}%',
        transform=ax.transAxes, va='top', fontsize=9,
        bbox=dict(fc='white', alpha=0.8, ec='0.7'))
ax.set_xlabel('Voltage (V)', fontsize=11)
ax.set_ylabel('Current density (mA/cm2)', fontsize=11)
ax.set_xlim(0, 1.25)
ax.grid(alpha=0.3)
save(fig, 'fig16.png')

# ---- fig4: bulk Nt trace (main) ----
d = J('r8_s02_nt.json')
order = ['1e12cm', '1e13cm', '1e14cm', '1e15cm', '1e16cm', '1e17cm', '1e18cm']
fig, ax = plt.subplots(2, 2, figsize=(6.4, 4.6))
for a, k, lab in zip(ax.flat, ('PCE', 'Voc', 'Jsc', 'FF'),
                      ('PCE (%)', 'Voc (V)', 'Jsc (mA/cm2)', 'FF (%)')):
    a.semilogx([1e12, 1e13, 1e14, 1e15, 1e16, 1e17, 1e18],
               [d[f'r8_s02_nt_{o}'][k] for o in order], 'o-', ms=4)
    a.set_ylabel(lab, fontsize=9)
    a.tick_params(labelsize=8)
    a.grid(alpha=0.3)
save(fig, 'fig4.png')

# ---- fig14 NEW: analytic rear band lineup, no-BSF vs BSF ----
# Ev/Ec depths (eV): absorber 5.30/3.90, CuI 5.20/2.10, Cu2O 5.30/3.20
fig, ax = plt.subplots(1, 2, figsize=(7.2, 4.0), sharey=True)
for a, title, layers in zip(ax,
                             ['no BSF: RbGeI3 / CuI', 'with BSF: RbGeI3 / Cu2O / CuI'],
                             [[('RbGeI3', 5.30, 3.90), ('CuI', 5.20, 2.10)],
                              [('RbGeI3', 5.30, 3.90), ('Cu2O', 5.30, 3.20), ('CuI', 5.20, 2.10)]]):
    x = 0
    for name, ev, ec in layers:
        w = 1.0
        a.hlines([-ec, -ev], x, x + w, colors=['b', 'r'], lw=2.5)
        a.text(x + w / 2, -ev + 0.12, name, ha='center', fontsize=9)
        a.vlines([x + w], -7.4, -2.0, colors='0.7', lw=0.8, ls='--')
        x += w
    a.set_xlim(0, x)
    a.set_title(title, fontsize=10)
    a.set_ylabel('electron energy (eV)', fontsize=10)
    a.tick_params(labelsize=8)
    a.grid(alpha=0.2, axis='y')
ax[0].annotate('', xy=(1.0, -5.2), xytext=(1.0, -5.3),
               arrowprops=dict(arrowstyle='<->', lw=1.2))
ax[0].text(1.08, -5.25, '0.10 eV cliff', fontsize=8, va='center')
save(fig, 'fig14.png')

# ---- fig17: UQ histograms ----
u = J('r8_uq.json')['uq']
u = [r for r in u if r.get('PCE', 0) > 0]
fig, ax = plt.subplots(2, 2, figsize=(6.4, 4.6))
for a, k, lab in zip(ax.flat, ('PCE', 'Voc', 'Jsc', 'FF'),
                      ('PCE (%)', 'Voc (V)', 'Jsc (mA/cm2)', 'FF (%)')):
    vals = [r[k] for r in u]
    a.hist(vals, bins=25, color='0.45', edgecolor='white', linewidth=0.4)
    a.axvline(np.median(vals), color='r', ls='--', lw=1.2)
    a.set_xlabel(lab, fontsize=9)
    a.tick_params(labelsize=8)
save(fig, 'fig17.png')

# ---- fig20: temperature traces ----
d = J('r8_temp.json')
T = [280, 297, 314, 331, 348, 365, 382, 400]
fig, ax = plt.subplots(2, 2, figsize=(6.4, 4.6))
for a, k, lab in zip(ax.flat, ('PCE', 'Voc', 'Jsc', 'FF'),
                      ('PCE (%)', 'Voc (V)', 'Jsc (mA/cm2)', 'FF (%)')):
    a.plot(T, [d[f'r8_T{t}'][k] for t in T], 'o-', ms=4)
    a.set_ylabel(lab, fontsize=9)
    a.tick_params(labelsize=8)
    a.grid(alpha=0.3)
save(fig, 'fig20.png')

# ---- fig21: GA history ----
g = J('r8_ga_results.json')
fig, ax = plt.subplots(figsize=(6.4, 3.6))
ax.plot(range(6), g['history'], 'o-', ms=5)
ax.set_xlabel('generation', fontsize=10)
ax.set_ylabel('best PCE (%)', fontsize=10)
ax.tick_params(labelsize=9)
ax.grid(alpha=0.3)
save(fig, 'fig21.png')

# ---- fig22: defect tolerance bars ----
fig, ax = plt.subplots(figsize=(6.4, 4.0))
x = np.arange(3)
ax.bar(x - 0.2, [27.06, 24.40, 20.76], 0.4, label='bulk Nt 1e14/1e15/1e16')
ax.bar(x + 0.2, [27.06, 24.10, 18.04], 0.4, label='interface Nt 1e14/1e15/1e16')
ax.set_xticks(x)
ax.set_xticklabels(['1e14', '1e15', '1e16'])
ax.set_xlabel('defect density (cm-3 bulk / cm-2 interface)', fontsize=10)
ax.set_ylabel('PCE (%)', fontsize=10)
ax.legend(fontsize=9)
ax.grid(alpha=0.3, axis='y')
save(fig, 'fig22.png')

# ---- fig23: stacked waterfall ----
fig, ax = plt.subplots(figsize=(6.4, 4.0))
vals = [27.06, 24.28, 21.93, 20.78, 21.76]
labs = ['R0\nideal', 'R1\n+optics', 'R2\n+bulk', 'R3\n+interfaces', 'R4\n+BSF']
cols = ['0.3', '0.45', '0.55', '0.65', 'tab:red']
ax.bar(labs, vals, color=cols)
for i, v in enumerate(vals):
    ax.text(i, v + 0.3, f'{v:.2f}%', ha='center', fontsize=9)
ax.set_ylabel('PCE$_{1-sun}$ (%)', fontsize=10)
ax.set_ylim(0, 30)
ax.grid(alpha=0.3, axis='y')
save(fig, 'fig23.png')

# ---- fig24: Et ----
d = J('r8_etsigma.json')
ets = [0.2, 0.4, 0.6, 0.8, 1.0, 1.2]
fig, ax = plt.subplots(figsize=(6.4, 4.0))
ax.plot(ets, [d[f'r8_Et{e:.1f}']['PCE'] for e in ets], 'o-', ms=5, label='Nt=1e14')
ax.plot([0.2, 0.7], [d['r8_Nt21_Et0.2']['PCE'], d['r8_Nt21_Et0.7']['PCE']],
        's--', ms=5, label='Nt=1e15')
ax.set_xlabel('Et (eV above Ev)', fontsize=10)
ax.set_ylabel('PCE (%)', fontsize=10)
ax.legend(fontsize=9)
ax.grid(alpha=0.3)
save(fig, 'fig24.png')

# ---- fig25: sigma (new data, mathtext labels) ----
d = J('r8_sigma.json')
snv = ['1e-21', '1e-19', '1e-17']
spv = ['1e-21', '1e-19', '1e-17']
fmt = lambda s: r'$10^{%d}$' % int(s.split('e')[1])
fig, ax = plt.subplots(figsize=(5.25, 3.9))
x = np.arange(3)
w = 0.22
for i, sn in enumerate(snv):
    vals = [d[f'r8_sn{sn[0]}e{sn[-2:]}_sp{sp[0]}e{sp[-2:]}']['PCE'] for sp in spv]
    ax.bar(x + (i - 1) * w, vals, w, label=r'$\sigma_n$=' + fmt(sn) + r' m$^2$')
ax.set_xticks(x)
ax.set_xticklabels([r'$\sigma_p$=' + fmt(s) + r' m$^2$' for s in spv])
ax.set_ylabel('PCE (%)', fontsize=10)
ax.legend(fontsize=9, loc='upper center', bbox_to_anchor=(0.5, -0.18), ncol=3)
ax.grid(alpha=0.3, axis='y')
save(fig, 'fig25.png')

# ---- fig26: NA on stacked ----
d = J('r8_stack.json')
fig, ax = plt.subplots(figsize=(6.4, 4.0))
xs = [20.0, 20.5, 21.0, 21.5, 22.0, 22.5, 23.0]
sm = lambda k: d[f'r8_NA{k:.1f}']
ax.semilogx([10.0**x / 1e6 for x in xs], [sm(k).get('PCE', sm(k).get('eta')) for k in xs], 'o-', ms=5)
ax.set_xlabel('NA (cm-3)', fontsize=10)
ax.set_ylabel('PCE (%)', fontsize=10)
ax.grid(alpha=0.3)
save(fig, 'fig26.png')

# ---- fig27/fig31: Rs/Rsh post on S3 ----
d = J('r8_S3_JV.json')
Vt, Jt = quad(d)
voc = float(np.interp(0, Jt[::-1], Vt[::-1]))
jsc = float(Jt[0])
rs_vals, rsh_vals = [], []
for Rs in (0, 2, 4, 6, 8, 10):
    Vp, Jp = rs_post(Vt, Jt, Rs)
    rs_vals.append(mpp(Vp, Jp))
for Rsh in (100, 500, 1000, 10000):
    Vp, Jp = rsh_post(Vt, Jt, Rsh)
    rsh_vals.append(mpp(Vp, Jp))
fig, ax = plt.subplots(figsize=(6.4, 4.0))
ax.plot([0, 2, 4, 6, 8, 10], [v[2] for v in rs_vals], 'o-', ms=5, label='FF')
ax.plot([0, 2, 4, 6, 8, 10], [v[3] for v in rs_vals], 's--', ms=5, label='PCE')
ax.set_xlabel('Rs (ohm.cm2)', fontsize=10)
ax.legend(fontsize=9)
ax.grid(alpha=0.3)
save(fig, 'fig27.png')
fig, ax = plt.subplots(figsize=(6.4, 4.2))
labs = ['S3\n20.78'] + [f'Rs{r}\n{v[3]:.1f}' for r, v in zip((2, 4, 8), rs_vals[1::2])] + \
       [f'Rsh{r}\n{v[3]:.1f}' for r, v in zip((100, 500, 1000), rsh_vals[:3])]
vals = [20.78] + [v[3] for v in rs_vals[1::2]] + [v[3] for v in rsh_vals[:3]]
ax.bar(labs, vals, color='0.5')
ax.axhline(20.0, color='r', ls='--', lw=1.2)
ax.set_ylabel('PCE (%)', fontsize=10)
ax.grid(alpha=0.3, axis='y')
save(fig, 'fig31.png')

# ---- fig28: mobility on stacked ----
d = J('r8_stack.json')
fig, ax = plt.subplots(figsize=(6.4, 4.0))
mus = [1, 5, 15, 30, 100]
sm = lambda k: d[k]
ax.semilogx(mus, [sm(f'r8_mu{m}').get('PCE', sm(f'r8_mu{m}').get('eta')) for m in mus], 'o-', ms=5)
ax.set_xlabel('mu_n = mu_p (cm2/Vs)', fontsize=10)
ax.set_ylabel('PCE (%)', fontsize=10)
ax.grid(alpha=0.3)
save(fig, 'fig28.png')

# ---- fig29: Ea fit ----
d = J('r8_temp.json')
T = np.array([280, 297, 314, 331, 348, 365, 382, 400])
V = np.array([d[f'r8_T{t}']['Voc'] for t in T])
sv, iv = np.polyfit(T, V, 1)
fig, ax = plt.subplots(figsize=(6.4, 4.0))
ax.plot(T, V, 'o', ms=5)
ax.plot([0, 400], [iv, iv + sv * 400], 'r--', lw=1.2)
ax.text(30, iv - 0.04, f'Ea = {iv:.2f} eV', fontsize=10)
ax.set_xlabel('T (K)', fontsize=10)
ax.set_ylabel('Voc (V)', fontsize=10)
ax.grid(alpha=0.3)
save(fig, 'fig29.png')

# ---- fig30: Rb vs Cs ----
fig, ax = plt.subplots(figsize=(6.4, 4.0))
x = np.arange(3)
ax.bar(x - 0.2, [27.06, 24.40, 20.76], 0.4, label='RbGeI3')
ax.bar(x + 0.2, [19.65, 19.31, 17.07], 0.4, label='CsGeI3')
ax.set_xticks(x)
ax.set_xticklabels(['ideal', 'Nt 1e15', 'Nt 1e16'])
ax.set_ylabel('PCE (%)', fontsize=10)
ax.legend(fontsize=9)
ax.grid(alpha=0.3, axis='y')
save(fig, 'fig30.png')

# ---- fig32: BSF heatmap ----
d = J('r8_bsf.json')
grid = [[d[f'r8_BSF{dnm}_NA{na}']['PCE'] for na in ('17', '18', '19')] for dnm in (30, 50, 80, 100)]
fig, ax = plt.subplots(figsize=(5.4, 4.0))
im = ax.imshow(grid, cmap='YlOrRd', aspect='auto')
ax.set_xticks([0, 1, 2])
ax.set_xticklabels(['1e17', '1e18', '1e19'])
ax.set_yticks([0, 1, 2, 3])
ax.set_yticklabels(['30 nm', '50 nm', '80 nm', '100 nm'])
ax.set_xlabel('BSF NA (cm-3)', fontsize=10)
ax.set_ylabel('BSF thickness', fontsize=10)
for i in range(4):
    for j in range(3):
        ax.text(j, i, f"{grid[i][j]:.2f}", ha='center', va='center', fontsize=9)
fig.colorbar(im, label='PCE (%)')
save(fig, 'fig32.png')

# ---- fig33 REPURPOSED: BSF interface desensitization ----
d = J('r8_nifsens.json')
fig, ax = plt.subplots(figsize=(6.4, 4.0))
x = np.arange(3)
ax.bar(x - 0.2, [27.06, d['r8_Nnif15']['PCE'], d['r8_Nnif16']['PCE']], 0.4, label='no BSF')
ax.bar(x + 0.2, [28.00, d['r8_Bnif15']['PCE'], d['r8_Bnif16']['PCE']], 0.4, label='BSF50-NA19')
ax.set_xticks(x)
ax.set_xticklabels(['Nif 1e14', 'Nif 1e15', 'Nif 1e16 (cm-2)'])
ax.set_ylabel('PCE (%)', fontsize=10)
ax.legend(fontsize=9)
ax.grid(alpha=0.3, axis='y')
save(fig, 'fig33.png')

# ---- fig34: G-profile single panel (analytic, H1 Jsc) ----
A = 1e5
lam = np.linspace(300, 900, 300)
E = 1240.0 / lam
alpha = np.where(E > 1.4, A * np.sqrt(E - 1.4), 0.0)
G = alpha / alpha.max()
fig, ax = plt.subplots(figsize=(6.4, 4.0))
ax.plot(lam, G * 100, 'k-', lw=1.6)
ax.axvline(886, color='r', ls='--', lw=1.2)
ax.text(890, 50, 'edge 886 nm (1.4 eV)', fontsize=9)
ax.set_xlabel('wavelength (nm)', fontsize=10)
ax.set_ylabel('normalized generation (%)', fontsize=10)
ax.grid(alpha=0.3)
save(fig, 'fig34.png')

# ---- fig35: parity (UQ, R2=0.907) ----
d = J('r8_ml.json')
fig, ax = plt.subplots(figsize=(5.2, 5.2))
ax.plot(d['yte'], d['pxgb'], 'o', ms=4, alpha=0.7)
lo = min(min(d['yte']), min(d['pxgb']))
hi = max(max(d['yte']), max(d['pxgb']))
ax.plot([lo, hi], [lo, hi], 'r--', lw=1.2)
ax.text(0.05, 0.95, "R2 = 0.907 (held-out 20%)", transform=ax.transAxes, fontsize=10, va='top')
ax.set_xlabel('simulated PCE (%)', fontsize=10)
ax.set_ylabel('predicted PCE (%)', fontsize=10)
ax.grid(alpha=0.3)
save(fig, 'fig35.png')

# ---- fig36: SHAP new ranking ----
d = J('r8_ml.json')
rk = d['shap_ranking']
fig, ax = plt.subplots(figsize=(6.0, 3.8))
ax.barh([r[0] for r in rk][::-1], [r[1] for r in rk][::-1])
ax.set_xlabel('mean |SHAP|', fontsize=10)
ax.grid(alpha=0.3, axis='x')
save(fig, 'fig36.png')

# ---- supplement S11/S12: illum + dark ----
d = J('r8_darkillum.json')
fig, ax = plt.subplots(figsize=(6.4, 4.0))
for k in sorted(d.keys()):
    if k.startswith('r8_ill'):
        V = np.array(d[k]['V'])
        Ja = np.abs(np.array(d[k]['J']))
        ax.plot(V, Ja, '-', lw=1.2, label=k.replace('r8_ill', ''))
ax.set_xlabel('Voltage (V)', fontsize=10)
ax.set_ylabel('Current density (mA/cm2)', fontsize=10)
ax.legend(title='suns', fontsize=8)
ax.grid(alpha=0.3)
save(fig, 'fig18.png')
d = J('r8_dark_JV.json')['r8_dark']
V = np.array(d['V'])
Ja = np.abs(np.array(d['J']))
fig, ax = plt.subplots(figsize=(6.4, 4.0))
ax.semilogy(V, Ja, 'k-', lw=1.4)
ax.set_xlabel('Voltage (V)', fontsize=10)
ax.set_ylabel('|J| (mA/cm2)', fontsize=10)
ax.grid(alpha=0.3)
save(fig, 'fig19.png')
print('ALL BESPOKE DONE')
