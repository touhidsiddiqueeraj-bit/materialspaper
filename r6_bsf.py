#!/usr/bin/env python3
"""r6_bsf — WP3 pilot: p+ Cu2O-like BSF (50 nm) inserted between RbGeI3 and CuI.
File order is back->front (back contact ... CuI, RbGeI3, TiO2, FTO ... front).
Insert BSF block + split CuI/RbGeI3 interface into CuI/BSF + BSF/RbGeI3.
BSF params (Cu2O literature: Eg~2.1, chi~3.2, eps~7.5, NA 1e18cm-3=1e24m-3).
Pilot: 1 variant vs base. Expand only if it converges.
"""
import sys, re, json, os
sys.path.insert(0, '/home/touhid/Documents/materilaspaper')
from r5_lib import BASE, DEF_DIR, write_def, run_set

cuI_start = BASE.index('name : CuI')
rb_start = BASE.index('name : RbGeI3')
cui_block = BASE[cuI_start:rb_start]
# cui_block = layer CuI + its srh + interface CuI/RbGeI3 + interface recombination
assert cui_block.count('interface properties') == 1, 'expected 1 interface in CuI block'
assert 'CuI (6) / RbGeI3 (7' in cui_block

# Build BSF layer block: copy CuI layer part (up to 'srhrecombination'), retune
layer_part = cui_block[:cui_block.index('srhrecombination')]
bsf = layer_part.replace('name : CuI (6.1)', 'name : BSF (Cu2O)')
bsf = bsf.replace('d : 1.000e-07 [m]', 'd : 5.000e-08 [m]')
bsf = re.sub(r'(eps :\s+)6\.500000', r'\g<1>7.500000', bsf)
bsf = re.sub(r'(chi :\s+)2\.100000', r'\g<1>3.200000', bsf)
bsf = re.sub(r'(Eg :\s+)3\.100000', r'\g<1>2.100000', bsf)
bsf = re.sub(r'(Na\(uniform\) :\s+)1\.000000e\+24', r'\g<1>1.000000e+24', bsf)  # keep 1e18cm-3
# srh part for BSF: reuse CuI srh (Nt 1e20/m3 neutral)
srh_part = cui_block[cui_block.index('srhrecombination'):cui_block.index('interface properties')]
# interfaces: duplicate CuI/RbGeI3 interface block, rename
if_part = cui_block[cui_block.index('interface properties'):]
if_bsf_cuI = if_part.replace('CuI (6) / RbGeI3 (7', 'CuI (6) / BSF (8')
if_bsf_rb = if_part.replace('CuI (6) / RbGeI3 (7', 'BSF (8) / RbGeI3 (7')
new_chunk = layer_part + srh_part + if_bsf_cuI + bsf + srh_part + if_bsf_rb
new_def = BASE[:cuI_start] + new_chunk + BASE[rb_start:]
assert new_def.count('interface properties') == BASE.count('interface properties') + 1, \
    f"interface count {new_def.count('interface properties')}"
assert 'name : BSF (Cu2O)' in new_def
write_def('r6_BSF50.def', new_def)
print('layers:', new_def.count('\nname :'), 'interfaces:', new_def.count('interface properties'))
print('wrote r6_BSF50.def')

run_set({'r6_BSF50': 'r6_BSF50.def', 'r6_base_ref': 'r6R_base.def'}, 'r6_bsf_pilot.json')
