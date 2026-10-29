#!/usr/bin/env python3
"""r8_extras — bracketing extensions + flat-absorption-edge tests (reviewer 1,3).

E1/E2: flat grading (1240/Eg both endpoints) on endpoint deck (Eg 1.3) and
       Eg->1.4 variant: tests SQ-Jsc admissibility + eg choice on sharp edge.
E3/E4: eps 25/27 on post-nt deck (bracket eps=23.1 edge win).
E5:    eg 1.2 on post-nifC deck (bracket eg=1.3 edge win).
E6/E7: nc 3e17/5e17 cm-3 on post-htl deck (diagnostic: trend below lit floor).
E8/E9: nv 3e17/5e17 cm-3 on post-nc deck (same).
E10:   etl 40nm rerun on post-eg deck (pathology check: FF 70 vs 85 neighbors).
"""
import sys, os
sys.path.insert(0, '/home/touhid/Documents/materilaspaper')
sys.path.insert(0, '/home/touhid/Documents/materilaspaper/validation')
from r5_lib import DEF_DIR, OUT_DIR, write_def, run_set, edit_block
from r8_oat import apply_val, set_iface


def load(name):
    with open(os.path.join(DEF_DIR, name)) as f:
        return f.read()


def flat_edge(text, eg):
    e = f'{1240.0 / eg:.2f}'
    return edit_block(text, 'RbGeI3', 'absorption grading :',
                      {0: e, 1: e}, '[nm]')


variants = {}
# E1: endpoint deck, flat edge at 1.3 eV
t = flat_edge(load('r8_carry_s11.def'), 1.3)
write_def('r8x_flat13.def', t)
variants['r8x_flat13'] = 'r8x_flat13.def'
# E2: endpoint deck, Eg->1.4 + flat edge
t = load('r8_carry_s11.def')
t = edit_block(t, 'RbGeI3', 'Eg :', {0: '1.400000', 5: '1.400000', 6: '1.400000'}, '[eV]')
t = flat_edge(t, 1.4)
write_def('r8x_flat14.def', t)
variants['r8x_flat14'] = 'r8x_flat14.def'
# E3/E4: eps extension on post-nt deck
base = load('r8_carry_s02.def')
for e in (25, 27):
    t = edit_block(base, 'RbGeI3', 'eps :',
                   {0: f'{e:.6f}', 5: f'{e:.6f}', 6: f'{e:.6f}'}, '[-]')
    write_def(f'r8x_eps{e}.def', t)
    variants[f'r8x_eps{e}'] = f'r8x_eps{e}.def'
# E5: eg 1.2 on post-nifC deck
t = load('r8_carry_s06.def')
t = edit_block(t, 'RbGeI3', 'Eg :', {0: '1.200000', 5: '1.200000', 6: '1.200000'}, '[eV]')
t = edit_block(t, 'RbGeI3', 'absorption grading :', {0: '1033.33'}, '[nm]')
write_def('r8x_eg12.def', t)
variants['r8x_eg12'] = 'r8x_eg12.def'
# E6-E9: sub-floor DOS diagnostics
base = load('r8_carry_s09.def')
for lab, v in (('nc17a', 3e23), ('nc17b', 5e23)):
    t = edit_block(base, 'RbGeI3', 'Nc :',
                   {0: f'{v:.3e}', 5: f'{v:.3e}', 6: f'{v:.3e}'}, '[/m^3]')
    write_def(f'r8x_{lab}.def', t)
    variants[f'r8x_{lab}'] = f'r8x_{lab}.def'
base = load('r8_carry_s10.def')
for lab, v in (('nv17a', 3e23), ('nv17b', 5e23)):
    t = edit_block(base, 'RbGeI3', 'Nv :',
                   {0: f'{v:.3e}', 5: f'{v:.3e}', 6: f'{v:.3e}'}, '[/m^3]')
    write_def(f'r8x_{lab}.def', t)
    variants[f'r8x_{lab}'] = f'r8x_{lab}.def'
# E10: etl 40nm rerun
t = edit_block(load('r8_carry_s07.def'), 'TiO2', 'd :', {0: '4.000e-08'}, '[m]')
write_def('r8x_etl40b.def', t)
variants['r8x_etl40b'] = 'r8x_etl40b.def'

print(f'{len(variants)} extras')
from r8_oat import run_with_retry
res = run_with_retry(variants, os.path.join(OUT_DIR, 'r8_extras.json'),
                     {'start': 0, 'stop': 1.5, 'step': 0.02})
for k, v in sorted(res.items()):
    print(k, v)
