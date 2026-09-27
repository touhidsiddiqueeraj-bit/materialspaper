#!/usr/bin/env python3
"""r5_retry — rerun all FAILED points + Et sweep at Nt=1e21 (lethality regime).
Merges results into existing JSONs. Defs already in DEF_DIR (or made here)."""
import sys, json, os
sys.path.insert(0, '/home/touhid/Documents/materilaspaper')
from r5_lib import (BASE, OUT_DIR, write_def, edit_single, edit_block,
                    run_set)

RETRIES = {  # json -> [(run_key, def_file)]
    'r5_et_sigma.json': [('r5_Et0.6', 'r5_Et0.6.def')],
    'r5_na.json': [(f'r5_NA{x:.1f}', f'r5_NA{x:.1f}.def')
                   for x in (20.0, 20.5, 21.5)],
    'r5_mobility.json': [(f'r5_mu{m}', f'r5_mu{m}.def') for m in (1, 5)],
}

# Et-at-Nt21 lethality sweep (7 new defs)
for et in (0.2, 0.4, 0.6, 0.8, 1.0, 1.2):
    t = edit_single(BASE, 'RbGeI3', 'Et', f'{et:.3f}', 'eV')
    t = edit_block(t, 'RbGeI3', 'Nt(uniform) :',
                   {i: '1.000000e+21' for i in (0, 1, 2, 5, 6)},
                   '  0  2  [/m^3]')
    name = f'r5_Et{et:.1f}_Nt21.def'
    write_def(name, t)
    RETRIES.setdefault('r5_et_sigma.json', []).append(
        (f'r5_Et{et:.1f}_Nt21', name))
# Nt21 Et=0.7 exists from main sweep (r5_Nt21_Et0.7) as 7th point

for jf, pairs in RETRIES.items():
    variants = {k: d for k, d in pairs}
    print(f'--- {jf}: {len(variants)} runs ---')
    fresh = run_set(variants, '_r5_tmp.json')
    os.remove(os.path.join(OUT_DIR, '_r5_tmp.json'))
    p = os.path.join(OUT_DIR, jf)
    d = json.load(open(p))
    d.update(fresh)
    json.dump(d, open(p, 'w'), indent=2)
    nfail = sum(1 for v in fresh.values() if 'FAILED' in v)
    print(f'{jf}: {nfail} still FAILED')
    for k, v in fresh.items():
        print(f'  {k}: {v}')
