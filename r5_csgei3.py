#!/usr/bin/env python3
"""r5_csgei3 — FULL OAT sweep mirror for CsGeI3 in the identical TiO2/CuI stack.
A-site isolation: ONLY the absorber Eg changes (1.4 -> 1.6 eV); chi, eps,
Nc/Nv, mu, doping, defects stay at the RbGeI3 baseline values. Rationale: the
A-site cation is electronically inert (no weight at CBM/VBM, Ge-4s/I-5p
derived); its effect is structural (tolerance factor -> octahedral tilt -> Eg).
Absorption: flat uniform endpoints at 775 nm / 1.60 eV (grading proved inert
in Round 4: flat 885.7/885.7 == graded run).
11 sweeps from the Cs baseline (independent, same grids as the RbGeI3 OAT):
 thickness(8) Nt(7) eps(5) chi(4) if-TiO2(7) if-CuI(7) Eg(5) ETL(7) HTL(7)
 NC(7) NV(7) = 71 runs. Consolidation follows in r5_csgei3_final.py after
 per-sweep optima are read off.
"""
import sys, re
sys.path.insert(0, '/home/touhid/Documents/materilaspaper')
from r5_lib import BASE, write_def, run_set, edit_block, set7

CS_EG = 1.6
CS_ABS_NM = 1240.0 / CS_EG  # 775.0


def cs_base():
    t = BASE
    # absorber Eg fields 0,1,5,6 -> 1.6
    t = edit_block(t, 'RbGeI3', 'Eg :',
                   {0: f'{CS_EG:.6f}', 1: f'{CS_EG:.6f}',
                    5: f'{CS_EG:.6f}', 6: f'{CS_EG:.6f}',
                    2: '0.500000', 3: '1.000000', 4: '1.000000'},
                   '  1  0  [eV]')
    # rename layer tag for provenance (comment-safe: SCAPS name line)
    t = t.replace('name : RbGeI3 (7.1)', 'name : CsGeI3 (7.1)')
    # flat absorption endpoints in the CsGeI3 block only
    lines = t.split('\n')
    out, incs = [], False
    for line in lines:
        s = line.strip()
        if s.startswith('name :'):
            incs = 'CsGeI3' in s
        if incs and s.startswith('absorption grading :') and '885.70' in line:
            line = (f'absorption grading :\t  {CS_ABS_NM:.2f}\t  '
                    f'{CS_ABS_NM:.2f}\t  250.00\t  250.00\t    0.00\t    '
                    f'{CS_EG:.2f}\t    {CS_EG:.2f}\t 7\t 0\t[nm]')
        out.append(line)
    return '\n'.join(out)


CSBASE = cs_base()
write_def('r5_cs_base.def', CSBASE)
# sanity: confirm Eg + abs lines
blk = CSBASE.split('name : CsGeI3')[1].split('interface properties')[0]
print([l.strip()[:80] for l in blk.split('\n')
       if l.strip().startswith(('Eg :', 'absorption grading'))])


def set_iface(text, n_m2, side):
    """Set interface N [/m^2] for one side: side='CuI' (iface1) or 'TiO2'."""
    blocks = text.split('interface properties')
    for i in range(1, len(blocks)):
        head = blocks[i][:400]
        if side == 'CuI' and 'CuI' not in head:
            continue
        if side == 'TiO2' and not ('TiO2' in head and 'CuI' not in
                                   head.split('interfacename')[1][:60]):
            # second interface block is RbGeI3/TiO2; first contains CuI
            if 'CuI' in head:
                continue
        blocks[i], n = re.subn(r'(^N\s*:\s*)[\d.eE+-]+(\s*\[/m\^2\])',
                               lambda m: m.group(1) + f'{n_m2:.3e}' +
                               m.group(2),
                               blocks[i], count=1, flags=re.MULTILINE)
    return 'interface properties'.join(blocks)


variants = {}


def add(key, text):
    name = f'r5_cs_{key}.def'
    write_def(name, text)
    variants[f'r5_cs_{key}'] = name


# 1. thickness 0.3..1.0 um (8)
for d in (0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0):
    add(f'th{d:.1f}', edit_block(CSBASE, 'CsGeI3', 'd :',
                                {0: f'{d * 1e-6:.6e}'}, ' [m]'))
# 2. Nt 1e18..1e24 /m^3 (7)
for le in range(18, 25):
    add(f'nt{le}', edit_block(
        CSBASE, 'CsGeI3', 'Nt(uniform) :',
        {i: f'{10.0 ** le:.6e}' for i in (0, 1, 2, 5, 6)},
        '  0  2  [/m^3]'))
# 3. eps 15..23.1 (5)
for ep in (15.0, 17.0, 19.0, 21.0, 23.1):
    add(f'ep{ep}', set7(CSBASE, 'CsGeI3', 'eps :', f'{ep:.6f}',
                        '  1  0  [-]'))
# 4. chi 3.9..4.2 (4) — tests CuI/TiO2 alignment for the wider gap
for ch in (3.9, 4.0, 4.1, 4.2):
    add(f'chi{ch}', set7(CSBASE, 'CsGeI3', 'chi :', f'{ch:.6f}',
                         '  1  0  [eV]'))
# 5/6. interface Nt per side 1e16..1e22 /m^2 (7+7)
for le in range(16, 23):
    add(f'ifT{le}', set_iface(CSBASE, 10.0 ** le, 'TiO2'))
    add(f'ifC{le}', set_iface(CSBASE, 10.0 ** le, 'CuI'))
# 7. Eg 1.3..1.7 (5)
for eg in (1.3, 1.4, 1.5, 1.6, 1.7):
    add(f'eg{eg}', edit_block(
        CSBASE, 'CsGeI3', 'Eg :',
        {0: f'{eg:.6f}', 1: f'{eg:.6f}', 5: f'{eg:.6f}', 6: f'{eg:.6f}',
         2: '0.500000', 3: '1.000000', 4: '1.000000'}, '  1  0  [eV]'))
# 8. ETL thickness 0.01..0.09 um (7)
for dnm in (10, 20, 30, 40, 50, 70, 90):
    add(f'etl{dnm}', edit_block(CSBASE, 'TiO2', 'd :',
                               {0: f'{dnm * 1e-9:.6e}'}, ' [m]'))
# 9. HTL thickness 0.1..1.9 um (7)
for dum in (0.1, 0.4, 0.7, 1.0, 1.3, 1.6, 1.9):
    add(f'htl{dum}', edit_block(CSBASE, 'CuI', 'd :',
                               {0: f'{dum * 1e-6:.6e}'}, ' [m]'))
# 10/11. NC, NV 1e23..1e26 /m^3 (7+7)
for le in range(23, 27):
    v = 10.0 ** le
    add(f'nc{le}', set7(CSBASE, 'CsGeI3', 'Nc :', f'{v:.6e}',
                        '  1  0  [/m^3]'))
    add(f'nv{le}', set7(CSBASE, 'CsGeI3', 'Nv :', f'{v:.6e}',
                        '  1  0  [/m^3]'))
# extra half-decade points for NC/NV (match RbGeI3 7-pt log grids better)
for tag, v in (('nc23h', 3.16e23), ('nc24h', 3.16e24), ('nc25h', 3.16e25),
               ('nv23h', 3.16e23), ('nv24h', 3.16e24), ('nv25h', 3.16e25)):
    key = 'Nc :' if tag.startswith('nc') else 'Nv :'
    add(tag, set7(CSBASE, 'CsGeI3', key, f'{v:.6e}', '  1  0  [/m^3]'))

print(f'{len(variants)} CsGeI3 variants')
run_set(variants, 'r5_csgei3_oat.json')
