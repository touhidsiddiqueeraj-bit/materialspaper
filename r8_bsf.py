#!/usr/bin/env python3
"""r8_bsf — BSF 4x3 grid on the REBASED H1-adopted deck (reviewer Phase 2/3).
Reuses build_bsf() from r6_bsf_sweep with base = r8_H1_adopted.def text.
Grid: d = 30/50/80/100 nm x NA = 1e17/18/19 /cm3 = 12 runs.
Plus: eps23-cost (pin cost), etl20-cost (caveat cost), H1 JV save.
"""
import sys, os
sys.path.insert(0, '/home/touhid/Documents/materilaspaper')
from r5_lib import DEF_DIR, OUT_DIR, write_def, run_set, edit_block
from r6_bsf_sweep import build_bsf
from r8_oat import run_with_retry


def load(name):
    with open(os.path.join(DEF_DIR, name)) as f:
        return f.read()


H1 = load('r8_H1_adopted.def')
variants = {}
for dnm in (30, 50, 80, 100):
    for na, natag in ((1e23, '17'), (1e24, '18'), (1e25, '19')):
        t = build_bsf(H1, dnm * 1e-9, na)
        name = f'r8_BSF{dnm}_NA{natag}.def'
        write_def(name, t)
        variants[f'r8_BSF{dnm}_NA{natag}'] = name
# eps pin cost on H1
t = edit_block(H1, 'RbGeI3', 'eps :',
               {0: '23.100000', 5: '23.100000', 6: '23.100000'}, '[-]')
write_def('r8_eps23cost.def', t)
variants['r8_eps23cost'] = 'r8_eps23cost.def'
# etl 20nm cost on H1
t = edit_block(H1, 'TiO2', 'd :', {0: '2.000e-08'}, '[m]')
write_def('r8_etl20cost.def', t)
variants['r8_etl20cost'] = 'r8_etl20cost.def'

print(f'{len(variants)} variants')
res = run_with_retry(variants, os.path.join(OUT_DIR, 'r8_bsf.json'),
                     {'start': 0, 'stop': 1.5, 'step': 0.02})
for k, v in sorted(res.items()):
    print(k, v)
# H1 JV save (for Rsh/Rs post-processing + overlay figures)
run_with_retry({'r8_H1_JV': 'r8_H1_adopted.def'},
               os.path.join(OUT_DIR, 'r8_H1_JV.json'),
               {'start': 0, 'stop': 1.5, 'step': 0.01},
               with_jv_keys=('r8_H1_JV',))
