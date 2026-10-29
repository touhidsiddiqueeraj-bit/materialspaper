#!/usr/bin/env python3
"""r8_stack — ONE stacked realistic window on H1 + tolerances recomputed on it.
S1: H1 + bulk Nt 1e15/cm3.
S2: S1 + interfaces 1e15/cm2 (JV saved for Rs/Rsh post-processing).
S3: S2 at 90 mW/cm2 (photon-scaling optics; PCE_1sun = VJFF/100 reported).
S4: BSF50-NA19 inserted on S2 deck (BSF under full realism).
BSFJV: BSF50-NA19 on H1 (ideal-BSF JV for overlay).
NAx7: background doping sweep on S2 deck (tolerance on stacked point).
MUx5: joint mobility 1D sweep on S2 deck (tolerance on stacked point).
"""
import sys, os, re
sys.path.insert(0, '/home/touhid/Documents/materilaspaper')
from r5_lib import DEF_DIR, OUT_DIR, write_def, edit_block, set_interfaces
from r5_lib import SCAPSrunner, op_summary_only
from r6_bsf_sweep import build_bsf
from r8_oat import run_with_retry, set_iface


def load(name):
    with open(os.path.join(DEF_DIR, name)) as f:
        return f.read()


H1 = load('r8_H1_adopted.def')
MU_SFX = '  1  0  [m^2/Vs]'


def set_mu(text, mu_cm):
    from r5_lib import set7
    t = set7(text, 'RbGeI3', 'mu_n :', f'{mu_cm * 1e-4:.6e}', MU_SFX)
    return set7(t, 'RbGeI3', 'mu_p :', f'{mu_cm * 1e-4:.6e}', MU_SFX)


# S1/S2 decks
s1 = edit_block(H1, 'RbGeI3', 'Nt(uniform) :',
                {0: '1.000e+21', 5: '1.000e+21', 6: '1.000e+21'}, '[/m^3]')
write_def('r8_S1_Nt15.def', s1)
s2 = set_interfaces(s1, 1e19)
write_def('r8_S2_full15.def', s2)
# S4: BSF on S2 deck (interfaces already 1e19 -> duplicated correctly)
s4 = build_bsf(s2, 50e-9, 1e25)
write_def('r8_S4_BSFreal.def', s4)

variants = {'r8_S1_Nt15': 'r8_S1_Nt15.def',
            'r8_S2_full15': 'r8_S2_full15.def',
            'r8_S4_BSFreal': 'r8_S4_BSFreal.def'}
# NA sweep on S2
for logna in (20.0, 20.5, 21.0, 21.5, 22.0, 22.5, 23.0):
    na = 10 ** logna
    t = edit_block(s2, 'RbGeI3', 'Na(uniform) :',
                   {0: f'{na:.3e}', 5: f'{na:.3e}', 6: f'{na:.3e}'}, '[/m^3]')
    name = f'r8_NA{logna:.1f}.def'
    write_def(name, t)
    variants[f'r8_NA{logna:.1f}'] = name
# mobility 1D on S2
for mu in (1, 5, 15, 30, 100):
    name = f'r8_mu{mu}.def'
    write_def(name, set_mu(s2, mu))
    variants[f'r8_mu{mu}'] = name

print(f'{len(variants)} variants')
res = run_with_retry(variants, os.path.join(OUT_DIR, 'r8_stack.json'),
                     {'start': 0, 'stop': 1.5, 'step': 0.02},
                     with_jv_keys=('r8_S2_full15', 'r8_S4_BSFreal'))
for k, v in sorted(res.items()):
    sm = v.get('summary', v) if isinstance(v, dict) else {}
    print(k, {q: sm.get(q) for q in ('Voc', 'Jsc', 'FF', 'PCE', 'eta')})

# S3: S2 deck at 90 mW/cm2 (custom illumination; PCE_1sun reported)
r = SCAPSrunner(lambda p: __import__('scaps_runner').script_gen.from_param_dict(p),
                op_summary_only, ncores=2)
r.sync_parameters()
out = r.run_inputs({'r8_S3_90sun': {'load': 'r8_S2_full15.def',
                                    'workingpoint': {'temperature': 300, 'illumination': 90},
                                    'iv': {'start': 0, 'stop': 1.5, 'step': 0.02}}})
print('S3-90sun:', out)
# BSF ideal JV save
run_with_retry({'r8_BSF_JV': 'r8_BSF50_NA19.def'},
               os.path.join(OUT_DIR, 'r8_BSF_JV.json'),
               {'start': 0, 'stop': 1.5, 'step': 0.01},
               with_jv_keys=('r8_BSF_JV',))
