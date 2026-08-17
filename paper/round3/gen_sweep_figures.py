#!/usr/bin/env python3
"""gen_sweep_figures.py - regenerate OAT sweep figures for the RbGeI3 paper
with a single shared legend at the bottom (outside axes, 4 columns), fixing
the PCE/Voc/Jsc/FF label clipping seen in the embedded figures.

Data: documents/thesis.docx tables 7, 9, 10, 11, 12, 14, 15, 16, 17.
Output: paper/round3/figs/figNN_*.png (replaces image5/7/8/9/10/12/13/14/15).
"""
import json
import re
import docx
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

L = '$V_{oc}$ (V) / $J_{sc}$ (mA/cm$^2$) / FF (%)'
FIG = [
    ('fig03_thickness', 'image5.png', 'T7',  'Effect of Absorber Layer Thickness',
     'Absorber Thickness ($\\mu$m)', 'linear'),
    ('fig05_dielectric', 'image7.png', 'T9', 'Effect of Absorber Dielectric Constant',
     'Absorber Dielectric Constant ($\\varepsilon_r$)', 'linear'),
    ('fig06_affinity', 'image8.png', 'T10', 'Effect of RbGeI$_3$ Electron Affinity',
     'RbGeI$_3$ Electron Affinity (eV)', 'linear'),
    ('fig07_tio2_iface', 'image9.png', 'T11', 'Effect of TiO$_2$/RbGeI$_3$ Interfacial Defect Density',
     'Interfacial Defect Density $N_t$ (cm$^{-2}$)', 'sci'),
    ('fig08_cui_iface', 'image10.png', 'T12', 'Effect of RbGeI$_3$/CuI Interfacial Defect Density',
     'Interfacial Defect Density $N_t$ (cm$^{-2}$)', 'sci'),
    ('fig10_tio2_thick', 'image12.png', 'T14', 'Effect of TiO$_2$ ETL Thickness',
     'TiO$_2$ ETL Thickness ($\\mu$m)', 'linear'),
    ('fig11_cui_thick', 'image13.png', 'T15', 'Effect of CuI HTL Thickness',
     'CuI HTL Thickness ($\\mu$m)', 'linear'),
    ('fig12_nc', 'image14.png', 'T16', 'Effect of Conduction-Band Effective DOS',
     'CB Effective DOS $N_c$ (cm$^{-3}$)', 'sci'),
    ('fig13_nv', 'image15.png', 'T17', 'Effect of Valence-Band Effective DOS',
     'VB Effective DOS $N_v$ (cm$^{-3}$)', 'sci'),
]
STYLE = [('PCE', 'r', 'o', '-'), ('$V_{oc}$', 'b', 's', '-'),
         ('$J_{sc}$', 'g', '^', '--'), ('FF', 'orange', 'd', '--')]
OUT = '/home/touhid/Documents/materilaspaper/paper/round3/figs'


def to_float(v, mode):
    v = v.strip().replace('×10', 'e')
    if mode == 'sci':
        m = re.fullmatch(r'10(\d+)', v)
        if m:
            return 10 ** int(m.group(1))
    return float(v)


def main():
    thesis = docx.Document('/home/touhid/Documents/materilaspaper/documents/thesis.docx')
    tables = {f'T{i}': t for i, t in enumerate(thesis.tables)}
    for name, media, tid, title, xlabel, mode in FIG:
        tbl = tables[tid]
        rows = [[c.text.strip() for c in r.cells] for r in tbl.rows[1:]]
        x = np.array([to_float(r[0], mode) for r in rows])
        pce = np.array([float(r[1]) for r in rows])
        voc = np.array([float(r[2]) for r in rows])
        jsc = np.array([float(r[3]) for r in rows])
        ff = np.array([float(r[4]) for r in rows])

        fig, ax = plt.subplots(figsize=(10, 5.6))
        ax2 = ax.twinx()
        ax.grid(alpha=0.3, which='both', ls=':')
        handles = []
        for label, color, marker, ls in STYLE:
            d = dict(zip(['PCE', '$V_{oc}$', '$J_{sc}$', 'FF'],
                         [pce, voc, jsc, ff]))[label]
            h, = (ax if label == 'PCE' else ax2).plot(
                x, d, color=color, marker=marker, ls=ls, lw=1.6, ms=5.5,
                label=label)
            handles.append(h)
        ax.set_xlabel(xlabel, fontsize=13)
        ax.set_ylabel('PCE (%)', fontsize=13)
        ax2.set_ylabel(L, fontsize=13)
        ax.set_title(title, fontsize=15)
        fig.legend(handles, [h.get_label() for h in handles],
                   loc='lower center', ncol=4, fontsize=12, frameon=False,
                   bbox_to_anchor=(0.5, -0.08))
        fig.tight_layout(rect=(0, 0.08, 1, 1))
        fig.savefig(f'{OUT}/{name}.png', dpi=300, bbox_inches='tight',
                    pad_inches=0.15)
        plt.close(fig)
        print(f'{name}.png  <- {tid} ({len(x)} pts, x {x[0]}..{x[-1]})')


if __name__ == '__main__':
    main()