#!/usr/bin/env python3
"""r8_uq — UQ LHS re-run on the REBASED H1 deck (reviewer concern 6).
Replicates the round-5 sampling design (N=200, same 8 features and ranges),
centered identically (ranges still bracket H1). Differences, all disclosed:
- base deck = r8_H1_adopted.def (NC/NV=1e18, K_rad=1e-16);
- Eg moves co-move chi (3.9+0.5*(Eg-1.4), as in GA) + absorption edge, so SHAP
  measures gap physics, not misalignment (reviewer Eg/chi confound);
- LHS seed fixed (11); stratified uniform (linear: Eg, mu; log10: rest).
Plus: dark JV (illumination 0) + illumination sweep (0.1-1.5 suns) on H1
for supplement S2 figures.
Outputs: r8_uq.json (same schema as uq_and_dark_results.json subset).
"""
import sys, os, json
import numpy as np
sys.path.insert(0, '/home/touhid/Documents/materilaspaper')
from r5_lib import DEF_DIR, OUT_DIR, write_def, run_set, edit_block, set7
from r8_oat import set_iface, run_with_retry

rng = np.random.default_rng(11)
N = 200
MU_SFX = '  1  0  [m^2/Vs]'


def lhs(n, lo, hi, log=False):
    u = (np.arange(n) + rng.random(n)) / n
    rng.shuffle(u)
    if log:
        return 10 ** (np.log10(lo) + u * (np.log10(hi) - np.log10(lo)))
    return lo + u * (hi - lo)


def load(name):
    with open(os.path.join(DEF_DIR, name)) as f:
        return f.read()


H1 = load('r8_H1_adopted.def')
S = {
    'Eg': lhs(N, 1.35, 1.45),
    'Nt': lhs(N, 5e19, 5e21, log=True),
    'NC': lhs(N, 5e22, 5e23, log=True),
    'NV': lhs(N, 5e22, 5e23, log=True),
    'mu_n': lhs(N, 0.0015, 0.005),
    'mu_p': lhs(N, 0.0015, 0.005),
    'Nint1': lhs(N, 5e17, 5e18, log=True),
    'Nint2': lhs(N, 5e17, 5e18, log=True),
}
variants = {}
rows = []
for i in range(N):
    t = H1
    eg = float(S['Eg'][i])
    t = edit_block(t, 'RbGeI3', 'Eg :', {0: f'{eg:.6f}', 5: f'{eg:.6f}', 6: f'{eg:.6f}'}, '[eV]')
    chi = 3.9 + 0.5 * (eg - 1.4)
    t = edit_block(t, 'RbGeI3', 'chi :', {0: f'{chi:.6f}', 5: f'{chi:.6f}', 6: f'{chi:.6f}'}, '[eV]')
    t = edit_block(t, 'RbGeI3', 'absorption grading :', {0: f'{1240.0 / eg:.2f}'}, '[nm]')
    t = edit_block(t, 'RbGeI3', 'Nt(uniform) :',
                   {0: f'{S["Nt"][i]:.3e}', 5: f'{S["Nt"][i]:.3e}', 6: f'{S["Nt"][i]:.3e}'}, '[/m^3]')
    t = edit_block(t, 'RbGeI3', 'Nc :',
                   {0: f'{S["NC"][i]:.3e}', 5: f'{S["NC"][i]:.3e}', 6: f'{S["NC"][i]:.3e}'}, '[/m^3]')
    t = edit_block(t, 'RbGeI3', 'Nv :',
                   {0: f'{S["NV"][i]:.3e}', 5: f'{S["NV"][i]:.3e}', 6: f'{S["NV"][i]:.3e}'}, '[/m^3]')
    t = set7(t, 'RbGeI3', 'mu_n :', f'{S["mu_n"][i]:.6e}', MU_SFX)
    t = set7(t, 'RbGeI3', 'mu_p :', f'{S["mu_p"][i]:.6e}', MU_SFX)
    t = set_iface(t, 'TiO2', float(S['Nint1'][i]))
    # CuI-side interface: marker 'CuI' matches only the non-BSF CuI/RbGeI3 block
    t2 = t
    lines = t2.split('\n')
    marks = [j for j, l in enumerate(lines) if 'interfacename :' in l and 'CuI' in l]
    assert len(marks) == 1, f'expected 1 CuI block, got {len(marks)}'
    t = set_iface(t, 'CuI', float(S['Nint2'][i]))
    key = f'r8uq_{i:03d}'
    write_def(key + '.def', t)
    variants[key] = key + '.def'

print(f'{len(variants)} UQ variants')
res = run_with_retry(variants, os.path.join(OUT_DIR, 'r8_uq.json'),
                     {'start': 0, 'stop': 1.5, 'step': 0.02})
rows = []
for i in range(N):
    key = f'r8uq_{i:03d}'
    v = res.get(key, {})
    row = {'Eg': float(S['Eg'][i]), 'Nt': float(S['Nt'][i]), 'NC': float(S['NC'][i]),
           'NV': float(S['NV'][i]), 'mu_n': float(S['mu_n'][i]), 'mu_p': float(S['mu_p'][i]),
           'Nint1': float(S['Nint1'][i]), 'Nint2': float(S['Nint2'][i])}
    row.update({k: v.get(k) for k in ('Voc', 'Jsc', 'FF', 'PCE')})
    rows.append(row)
ok = [r for r in rows if r.get('PCE', 0) > 0]
print(f'converged {len(ok)}/{N}')
json.dump({'uq': rows}, open(os.path.join(OUT_DIR, 'r8_uq.json'), 'w'), indent=1)

# dark JV + illumination sweep on H1 (supplement S2; custom illumination)
import sys as _s
_s.path.insert(0, '/home/touhid/scaps-runner/src')
from scaps_runner import SCAPSrunner as _R, parse_jv_curve as _pjv
from scaps_runner.script_gen import from_param_dict as _fp
from r5_lib import op_summary_only as _op


def _opjv(path):
    J, V = _pjv(path)
    return {'J': J.tolist(), 'V': V.tolist()}


_r = _R(lambda p: _fp(p), _opjv, ncores=2)
_r.sync_parameters()
_di = {'r8_dark': {'load': 'r8_H1_adopted.def',
                   'workingpoint': {'temperature': 300, 'illumination': 0},
                   'iv': {'start': -0.5, 'stop': 1.3, 'step': 0.02}}}
for _suns in (0.1, 0.3, 0.5, 0.8, 1.0, 1.5):
    _di[f'r8_ill{_suns}'] = {'load': 'r8_H1_adopted.def',
                             'workingpoint': {'temperature': 300,
                                              'illumination': int(100 * _suns)},
                             'iv': {'start': 0, 'stop': 1.5, 'step': 0.01}}
_dout = _r.run_inputs(_di)
json.dump({k: v for k, v in _dout.items()},
          open(os.path.join(OUT_DIR, 'r8_darkillum.json'), 'w'))
print('dark/illum saved:', sorted(_dout))
