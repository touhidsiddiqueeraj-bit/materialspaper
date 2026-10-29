#!/usr/bin/env python3
"""r6_bsf_sweep — WP3 full: BSF thickness x doping + realistic-anchored BSF.
Grid: d = 30/50/80/100 nm x NA = 1e23/1e24/1e25 /m3 (1e17/18/19 /cm3) = 12 runs.
Plus r6_BSF50_realistic: BSF50 + bulk Nt1e15 @90 illum (holds under realism?).
"""
import sys, re
sys.path.insert(0, '/home/touhid/Documents/materilaspaper')
from r5_lib import BASE, write_def, edit_block, run_set

def build_bsf(base, d_m, na_m3):
    cuI_start = base.index('name : CuI')
    rb_start = base.index('name : RbGeI3')
    cui_block = base[cuI_start:rb_start]
    layer_part = cui_block[:cui_block.index('srhrecombination')]
    bsf = layer_part.replace('name : CuI (6.1)', 'name : BSF (Cu2O)')
    bsf = bsf.replace('d : 1.000e-07 [m]', f'd : {d_m:.3e} [m]')
    bsf = re.sub(r'(eps :\s+)6\.500000', r'\g<1>7.500000', bsf)
    bsf = re.sub(r'(chi :\s+)2\.100000', r'\g<1>3.200000', bsf)
    bsf = re.sub(r'(Eg :\s+)3\.100000', r'\g<1>2.100000', bsf)
    lines = bsf.split('\n')
    for i, l in enumerate(lines):
        if l.strip().startswith('Na(uniform) :'):
            parts = l.split(':')
            nums = re.findall(r'[\d.eE+-]+', parts[1])
            nums[0] = f'{na_m3:.3e}'; nums[5] = f'{na_m3:.3e}'; nums[6] = f'{na_m3:.3e}'
            lines[i] = parts[0] + ':  ' + '  '.join(nums[:7]) + '  0  2  [/m^3]'
            break
    bsf = '\n'.join(lines)
    srh_part = cui_block[cui_block.index('srhrecombination'):cui_block.index('interface properties')]
    if_part = cui_block[cui_block.index('interface properties'):]
    if1 = if_part.replace('CuI (6) / RbGeI3 (7', 'CuI (6) / BSF (8')
    if2 = if_part.replace('CuI (6) / RbGeI3 (7', 'BSF (8) / RbGeI3 (7')
    return base[:cuI_start] + layer_part + srh_part + if1 + bsf + srh_part + if2 + base[rb_start:]

def main():
    variants = {}
    for dnm in (30, 50, 80, 100):
        for na, natag in ((1e23, '17'), (1e24, '18'), (1e25, '19')):
            t = build_bsf(BASE, dnm * 1e-9, na)
            name = f'r6_BSF{dnm}_NA{natag}.def'
            write_def(name, t)
            variants[f'r6_BSF{dnm}_NA{natag}'] = name
    print(f'{len(variants)} variants')
    run_set(variants, 'r6_bsf_sweep.json')


if __name__ == '__main__':
    main()
