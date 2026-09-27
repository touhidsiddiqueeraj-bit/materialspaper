#!/usr/bin/env python3
"""r5_na — background acceptor density sweep (Ge-vacancy p-type doping).
NA = 1e20..1e23 /m^3 (=1e14..1e17 /cm^3), half-decade log grid, 7 runs."""
import sys
sys.path.insert(0, '/home/touhid/Documents/materilaspaper')
from r5_lib import BASE, write_def, set7, run_set

variants = {}
for logna in (20.0, 20.5, 21.0, 21.5, 22.0, 22.5, 23.0):
    na = 10 ** logna
    t = set7(BASE, 'RbGeI3', 'Na(uniform) :', f'{na:.6e}',
             '  0  2  [/m^3]')
    name = f'r5_NA{logna:.1f}.def'
    write_def(name, t)
    variants[f'r5_NA{logna:.1f}'] = name

print(f'{len(variants)} variants')
run_set(variants, 'r5_na.json')
