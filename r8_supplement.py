#!/usr/bin/env python3
"""r8_supplement — temperature / defect-energy / sigma-asymmetry / CsGeI3
re-runs on the REBASED H1 deck (reviewer: stale-deck figures).
- temp: 280-400K (8) fine IV for Ea fit.
- Et: 0.2-1.2 step 0.2 (7) at Nt=1e14 + Nt=1e15 x Et 0.2/0.7 (2).
- sigma 3x3 at Et=0.6 (9).
- CsGeI3: H1 with Eg->1.6 only (original protocol; confound admitted in
  text), +Nt15, +Nt16 variants + Eg->1.4 control (4).
Outputs: r8_temp.json, r8_etsigma.json, r8_cs.json.
"""
import sys, os
sys.path.insert(0, '/home/touhid/Documents/materilaspaper')
from r5_lib import DEF_DIR, OUT_DIR, write_def, run_set, edit_block, edit_single
from r8_oat import run_with_retry


def load(name):
    with open(os.path.join(DEF_DIR, name)) as f:
        return f.read()


H1 = load('r8_H1_adopted.def')

# ---- temperature (Ea fit needs fine IV) ----
temps = [280, 297, 314, 331, 348, 365, 382, 400]
run_with_retry({f'r8_T{T}': 'r8_H1_adopted.def' for T in temps},
               os.path.join(OUT_DIR, 'r8_temp.json'),
               {'start': 0, 'stop': 1.5, 'step': 0.01},
               temps={f'r8_T{T}': T for T in temps})

# ---- defect energy + sigma asymmetry ----
v = {}
for et in (0.2, 0.4, 0.6, 0.8, 1.0, 1.2):
    t = edit_single(H1, 'RbGeI3', 'Et', f'{et:.3f}', 'eV')
    write_def(f'r8_Et{et:.1f}.def', t)
    v[f'r8_Et{et:.1f}'] = f'r8_Et{et:.1f}.def'
v['r8_Et0.6_base'] = 'r8_H1_adopted.def'
sigs = ['1e-21', '1e-19', '1e-17']
for sn in sigs:
    for sp in sigs:
        t = edit_single(H1, 'RbGeI3', 'Et', '0.600', 'eV')
        t = edit_single(t, 'RbGeI3', 'sigma_n', f'1.000{sn[1:]}', 'm^2')
        t = edit_single(t, 'RbGeI3', 'sigma_p', f'1.000{sp[1:]}', 'm^2')
        tag = f'sn{sn[0]}e{sn[-2:]}_sp{sp[0]}e{sp[-2:]}'
        write_def(f'r8_{tag}.def', t)
        v[f'r8_{tag}'] = f'r8_{tag}.def'
for et in (0.2, 0.7):
    t = edit_single(H1, 'RbGeI3', 'Et', f'{et:.3f}', 'eV')
    t = edit_block(t, 'RbGeI3', 'Nt(uniform) :',
                   {0: '1.000e+21', 5: '1.000e+21', 6: '1.000e+21'}, '[/m^3]')
    write_def(f'r8_Nt21_Et{et:.1f}.def', t)
    v[f'r8_Nt21_Et{et:.1f}'] = f'r8_Nt21_Et{et:.1f}.def'
run_with_retry(v, os.path.join(OUT_DIR, 'r8_etsigma.json'),
               {'start': 0, 'stop': 1.5, 'step': 0.02})

# ---- CsGeI3 mirror (Eg-only protocol, confound admitted) ----
c = {}
t = edit_block(H1, 'RbGeI3', 'Eg :', {0: '1.600000', 5: '1.600000', 6: '1.600000'}, '[eV]')
t = edit_block(t, 'RbGeI3', 'absorption grading :', {0: '775.00'}, '[nm]')
write_def('r8_cs_ideal.def', t)
c['r8_cs_ideal'] = 'r8_cs_ideal.def'
for nt, tag in ((1e21, 'Nt15'), (1e22, 'Nt16')):
    t2 = edit_block(t, 'RbGeI3', 'Nt(uniform) :',
                    {0: f'{nt:.3e}', 5: f'{nt:.3e}', 6: f'{nt:.3e}'}, '[/m^3]')
    write_def(f'r8_cs_{tag}.def', t2)
    c[f'r8_cs_{tag}'] = f'r8_cs_{tag}.def'
t3 = edit_block(H1, 'RbGeI3', 'Eg :', {0: '1.400000', 5: '1.400000', 6: '1.400000'}, '[eV]')
write_def('r8_cs_ctrl14.def', t3)
c['r8_cs_ctrl14'] = 'r8_cs_ctrl14.def'
run_with_retry(c, os.path.join(OUT_DIR, 'r8_cs.json'),
               {'start': 0, 'stop': 1.5, 'step': 0.02})
print('supplement runs done')
