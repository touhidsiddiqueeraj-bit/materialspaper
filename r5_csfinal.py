#!/usr/bin/env python3
"""r5_csfinal — consolidated CsGeI3 final point (mirror of Rb recipe) +
realistic/high-oxidation derating + confirmation reruns of two outliers."""
import sys, re
sys.path.insert(0, '/home/touhid/Documents/materilaspaper')
from r5_lib import DEF_DIR, write_def, run_set, edit_block

CS = open(f'{DEF_DIR}/r5_cs_base.def').read()
variants = {}


def add(key, text):
    name = f'r5_csf_{key}.def'
    write_def(name, text)
    variants[f'r5_csf_{key}'] = name


add('final', CS)  # consolidated mirror-Rb point, explicit run
for tag, le in (('Nt21', 21), ('Nt22', 22)):
    add(tag, edit_block(CS, 'CsGeI3', 'Nt(uniform) :',
                        {i: f'{10.0 ** le:.6e}' for i in (0, 1, 2, 5, 6)},
                        '  0  2  [/m^3]'))
# confirm ETL-90nm outlier ( FF 88.26 in OAT )
add('etl90', edit_block(CS, 'TiO2', 'd :', {0: '9.000000e-08'}, ' [m]'))
# confirm CuI-side interface 1e16 point
blocks = CS.split('interface properties')
blocks[1] = re.sub(r'(^N\s*:\s*)[\d.eE+-]+(\s*\[/m\^2\])',
                   lambda m: m.group(1) + '1.000e+16' + m.group(2),
                   blocks[1], count=1, flags=re.MULTILINE)
add('ifC16', 'interface properties'.join(blocks))

print(f'{len(variants)} variants')
run_set(variants, 'r5_csfinal.json')
