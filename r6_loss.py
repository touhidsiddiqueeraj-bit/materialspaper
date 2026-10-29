#!/usr/bin/env python3
"""r6_loss — WP1 realistic loss budget (Round-6 novelty campaign).
Native SCAPS def-edits (no post-processing except Rs/Rsh which SCAPS
scripting does not expose — flagged as first-order estimate):
 L1 radiative K_rad in RbGeI3: 0 / 1e-16 / 1e-15 / 1e-14 m3/s
 L2 Auger c_n=c_p in RbGeI3: 0 / 1e-41 / 1e-40 / 1e-39 m6/s
 L3 front transmission Tfront: 1.0 / 0.95 / 0.90 / 0.85
 L4 combined realistic: K=1e-16 + Auger=1e-40 + T=0.90 (+Nt=1e15cm-3 variant)
Literature anchors: perovskite K_rad~1e-10 cm3/s=1e-16 m3/s (Stranks/MAPbI3);
 Auger~1e-28 cm6/s=1e-40 m6/s; 10% air/FTO reflection (n~1.93 Fresnel).
SI units in def (/m3, m2, m3/s, m6/s).
"""
import sys, re
sys.path.insert(0, '/home/touhid/Documents/materilaspaper')
from r5_lib import BASE, write_def, edit_block, run_set

def set_krad(text, layer, val):
    return edit_block(text, layer, 'K_rad :', {0: f'{val:.3e}', 5: f'{val:.3e}', 6: f'{val:.3e}'}, '  1  0  [m^3/s]')

def set_auger(text, layer, val):
    t = edit_block(text, layer, 'c_n_auger :', {0: f'{val:.3e}', 5: f'{val:.3e}', 6: f'{val:.3e}'}, '  1  0  [m^6/s]')
    t = edit_block(t, layer, 'c_p_auger :', {0: f'{val:.3e}', 5: f'{val:.3e}', 6: f'{val:.3e}'}, '  1  0  [m^6/s]')
    return t

def set_tfront(text, val):
    return re.sub(r'(internal Tfront\s*:\s*)[\d.eE+-]+', lambda m: m.group(1) + f'  {val:.4e}', text)

def set_bulk_nt(text, layer, n_m3):
    return edit_block(text, layer, 'Nt(uniform) :',
                      {0: f'{n_m3:.3e}', 1: f'{n_m3:.3e}', 2: f'{n_m3:.3e}',
                       5: f'{n_m3:.3e}', 6: f'{n_m3:.3e}'}, '  0  2  [/m^3]')

variants = {}
# L1 radiative
for tag, kval in (('K0', 0.0), ('K16', 1e-16), ('K15', 1e-15), ('K14', 1e-14)):
    t = set_krad(BASE, 'RbGeI3', kval)
    name = f'r6_rad_{tag}.def'
    write_def(name, t)
    variants[f'r6_rad_{tag}'] = name
# L2 Auger
for tag, aval in (('A0', 0.0), ('A41', 1e-41), ('A40', 1e-40), ('A39', 1e-39)):
    t = set_auger(BASE, 'RbGeI3', aval)
    name = f'r6_aug_{tag}.def'
    write_def(name, t)
    variants[f'r6_aug_{tag}'] = name
# L3 reflection
for tag, tf in (('T100', 1.0), ('T95', 0.95), ('T90', 0.90), ('T85', 0.85)):
    t = set_tfront(BASE, tf)
    name = f'r6_refl_{tag}.def'
    write_def(name, t)
    variants[f'r6_refl_{tag}'] = name
# L4 combined realistic (native, no Rs — Rs/Rsh done in r6_rsh.py post-proc)
t = set_krad(BASE, 'RbGeI3', 1e-16)
t = set_auger(t, 'RbGeI3', 1e-40)
t = set_tfront(t, 0.90)
write_def('r6_realistic.def', t)
variants['r6_realistic'] = 'r6_realistic.def'
t2 = set_bulk_nt(t, 'RbGeI3', 1e21)  # Nt=1e15 cm-3 realistic defect
write_def('r6_realistic_Nt15.def', t2)
variants['r6_realistic_Nt15'] = 'r6_realistic_Nt15.def'

def main():
    print(f'{len(variants)} variants')
    run_set(variants, 'r6_loss.json')


if __name__ == '__main__':
    main()
