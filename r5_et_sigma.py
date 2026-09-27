#!/usr/bin/env python3
"""r5_et_sigma — defect energy level + capture cross-section asymmetry.
Base Nt = 1e20 /m^3 (=1e14 /cm^3). Et in eV above Ev (ref 0).
A: Et = 0.2..1.2 step 0.2 (7 runs).
B: at worst Et from A -> use mid-gap 0.6 eV fallback: sigma_n x sigma_p grid
   {1e-21, 1e-19, 1e-17}^2 = 9 runs.
C: Nt = 1e21 /m^3 at Et = 0.2 (band-edge) and 0.7 (near mid-gap) (2 runs)."""
import sys
sys.path.insert(0, '/home/touhid/Documents/materilaspaper')
from r5_lib import BASE, write_def, edit_single, edit_block, run_set

variants = {}
# A: Et sweep
for et in (0.2, 0.4, 0.6, 0.8, 1.0, 1.2):
    t = edit_single(BASE, 'RbGeI3', 'Et', f'{et:.3f}', 'eV')
    name = f'r5_Et{et:.1f}.def'
    write_def(name, t)
    variants[f'r5_Et{et:.1f}'] = name
# Et=0.6 is the base file itself
variants['r5_Et0.6_base'] = 'r5_baseline.def'

# B: sigma asymmetry at Et=0.6 (mid-gap worst case)
for sn in ('1.000000e-21', '1.000000e-19', '1.000000e-17'):
    for sp in ('1.000000e-21', '1.000000e-19', '1.000000e-17'):
        t = edit_single(BASE, 'RbGeI3', 'sigma_n', sn, 'm^2')
        t = edit_single(t, 'RbGeI3', 'sigma_p', sp, 'm^2')
        tag = f'sn{sn[0]}e{sn[-2:]}_sp{sp[0]}e{sp[-2:]}'
        name = f'r5_{tag}.def'
        write_def(name, t)
        variants[f'r5_{tag}'] = name

# C: high-Nt at band-edge vs mid-gap Et
for et in (0.2, 0.7):
    t = edit_single(BASE, 'RbGeI3', 'Et', f'{et:.3f}', 'eV')
    t = edit_block(t, 'RbGeI3', 'Nt(uniform) :',
                   {0: '1.000000e+21', 1: '1.000000e+21',
                    2: '1.000000e+21', 5: '1.000000e+21',
                    6: '1.000000e+21'}, '  0  2  [/m^3]')
    name = f'r5_Nt21_Et{et:.1f}.def'
    write_def(name, t)
    variants[f'r5_Nt21_Et{et:.1f}'] = name

print(f'{len(variants)} variants')
run_set(variants, 'r5_et_sigma.json')
