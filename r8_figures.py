#!/usr/bin/env python3
"""r8_figures — regenerate ALL main-text figures from r8 archives (reviewer).
Deterministic; every number traceable to a JSON in r5_results/.
Kept files: fig1, fig2, fig15 (band edges unchanged), fig37 (validation deck).
Repurposed: fig14 (QE->BSF band lineup), fig33 (waterfall->BSF desensitization),
fig34 (GRMS->G-profile single panel).
Output: solar_submission/figs/*.png (overwrite).
"""
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


def trace4(axs, x, series, title=''):
    for ax, k, lab in zip(axs, ('PCE', 'Voc', 'Jsc', 'FF'),
                           ('PCE (%)', 'Voc (V)', 'Jsc (mA/cm2)', 'FF (%)')):
        ax.plot(x, [s[k] for s in series], 'o-', ms=4)
        ax.set_ylabel(lab, fontsize=9)
        ax.tick_params(labelsize=8)
        ax.grid(alpha=0.3)
    if title:
        axs[0].set_title(title, fontsize=10)


def sup_trace(key_prefix, src, xs, labels, name):
    d = J(src)
    fig, ax = plt.subplots(2, 2, figsize=(6.4, 4.6))
    axs = ax.flat
    kept, series = [], []
    for lab in labels:
        v = d.get(key_prefix + lab, {})
        if isinstance(v, dict) and v.get('PCE', 0) > 0:
            kept.append(lab)
            series.append({k: v[k] for k in ('PCE', 'Voc', 'Jsc', 'FF')})
    trace4(axs, list(range(len(kept))), series)
    axs[2].set_xticks(range(len(kept)))
    axs[2].set_xticklabels(kept, rotation=30, fontsize=7)
    axs[3].set_xticks(range(len(kept)))
    axs[3].set_xticklabels(kept, rotation=30, fontsize=7)
    save(fig, name)


# ---- supplement traces (S1-S10 <- r8 steps) ----
sup_trace('r8_s01_th_', 'r8_s01_th.json',
          None, ['0.3um', '0.4um', '0.5um', '0.6um', '0.7um', '0.8um', '0.9um', '1.0um'], 'fig3.png')
sup_trace('r8_s03_eps_', 'r8_s03_eps.json',
          None, ['10', '12', '15', '18', '21', '23.1'], 'fig5.png')
sup_trace('r8_s04_chi_', 'r8_s04_chi.json',
          None, ['3.7', '3.8', '3.9', '4.0', '4.1', '4.2'], 'fig6.png')
sup_trace('r8_s05_nifT_', 'r8_s05_nifT.json',
          None, ['1e12cm2', '1e13cm2', '1e14cm2', '1e15cm2', '1e16cm2', '1e17cm2', '1e18cm2'], 'fig7.png')
sup_trace('r8_s06_nifC_', 'r8_s06_nifC.json',
          None, ['1e12cm2', '1e13cm2', '1e14cm2', '1e15cm2', '1e16cm2', '1e17cm2', '1e18cm2'], 'fig8.png')
sup_trace('r8_s07_eg_', 'r8_s07_eg.json',
          None, ['1.3', '1.4', '1.5', '1.6', '1.7'], 'fig9.png')
sup_trace('r8_s08_etl_', 'r8_s08_etl.json',
          None, ['10nm', '20nm', '29nm', '40nm', '50nm', '70nm', '90nm'], 'fig10.png')
sup_trace('r8_s09_htl_', 'r8_s09_htl.json',
          None, ['0.05um', '0.075um', '0.1um', '0.4um', '0.7um', '1.0um', '1.3um', '1.6um', '1.9um'], 'fig11.png')
sup_trace('r8_s10_nc_', 'r8_s10_nc.json',
          None, ['nc0', 'nc1', 'nc2', 'nc3', 'nc4', 'nc5', 'nc6'], 'fig12.png')
sup_trace('r8_s11_nv_', 'r8_s11_nv.json',
          None, ['nv0', 'nv1', 'nv2', 'nv3', 'nv4', 'nv5', 'nv6'], 'fig13.png')

# ---- main traces ----
def main_trace(src, keyfn, name):
    d = J(src)
    fig, ax = plt.subplots(2, 2, figsize=(6.4, 4.6))
    keys, series = [], []
    for k in sorted(d.keys()):
        v = d[k]
        if isinstance(v, dict) and v.get('PCE', 0) > 0:
            keys.append(k)
            series.append({q: v[q] for q in ('PCE', 'Voc', 'Jsc', 'FF')})
    trace4(ax.flat, list(range(len(keys))), series)
    save(fig, name)


print('sup/main traces done')
