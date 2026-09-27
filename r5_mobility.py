#!/usr/bin/env python3
"""r5_mobility — absorber carrier mobility sweep.
1D joint (mun=mup): 1, 5, 15, 30, 100 cm^2/Vs (5 runs, 700 nm).
2D cross at {5, 15, 30}^2 minus center dup (8 runs, 700 nm).
Thin check: mu = 5, 15 cm^2/Vs at 400 nm absorber (2 runs)."""
import sys
sys.path.insert(0, '/home/touhid/Documents/materilaspaper')
from r5_lib import BASE, write_def, set7, edit_block, run_set

MU_SFX = '  1  0  [m^2/Vs]'


def set_mu(text, mu_cm):
    mu = mu_cm * 1e-4
    t = set7(text, 'RbGeI3', 'mu_n :', f'{mu:.6e}', MU_SFX)
    return set7(t, 'RbGeI3', 'mu_p :', f'{mu:.6e}', MU_SFX)


variants = {}
for mu in (1, 5, 15, 30, 100):
    name = f'r5_mu{mu}.def'
    write_def(name, set_mu(BASE, mu))
    variants[f'r5_mu{mu}'] = name

for mun in (5, 15, 30):
    for mup in (5, 15, 30):
        if mun == 15 and mup == 15:
            continue  # covered by 1D (mu15 both)
        t = set7(BASE, 'RbGeI3', 'mu_n :', f'{mun * 1e-4:.6e}', MU_SFX)
        t = set7(t, 'RbGeI3', 'mu_p :', f'{mup * 1e-4:.6e}', MU_SFX)
        name = f'r5_mun{mun}_mup{mup}.def'
        write_def(name, t)
        variants[f'r5_mun{mun}_mup{mup}'] = name

for mu in (5, 15):
    t = set_mu(BASE, mu)
    t = edit_block(t, 'RbGeI3', 'd :', {0: '4.000000e-07'}, ' [m]')
    name = f'r5_mu{mu}_th04.def'
    write_def(name, t)
    variants[f'r5_mu{mu}_th04'] = name

print(f'{len(variants)} variants')
run_set(variants, 'r5_mobility.json')
