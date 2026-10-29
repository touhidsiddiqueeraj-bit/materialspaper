#!/usr/bin/env python3
"""r6_real — realistic waterfall nodes with Pin-aware parsing.
Nodes (all on corrected realistic_c base = K1e-16 + Auger1e-40):
 R0 ideal 1-sun (ref r5_baseline 26.81)
 R1 +radiative/Auger (r6_realistic_c @100 = 26.79)
 R2 +10% reflection (realistic_c @90 -> PCE_1sun ~24.08)
 R3 +realistic bulk Nt=1e15 (Nt15 def @90)
 R4 +interface Nt=1e15 (Nt15 bulk+interface @90)
Rs/Rsh external budgeting applied in r6_rsh.py (first-order, flagged).
SCAPS eta at reduced illumination is normalized to that illumination,
so PCE_1sun = Voc*Jsc*FF/100 is computed explicitly (Pin=100).
"""
import sys, json, os, re
sys.path.insert(0, '/home/touhid/Documents/materilaspaper')
from r5_lib import BASE, write_def, edit_block
sys.path.insert(0, '/home/touhid/scaps-runner/src')
from scaps_runner import SCAPSrunner
from scaps_runner.script_gen import from_param_dict

OUT_DIR = '/home/touhid/Documents/materilaspaper/r5_results'

def set_krad_auger(text):
    t = edit_block(text, 'RbGeI3', 'K_rad :',
                   {0: '1.000e-16', 1: '1.000e-16', 5: '1.000e-16', 6: '1.000e-16'}, '  1  0  [m^3/s]')
    t = edit_block(t, 'RbGeI3', 'c_n_auger :',
                   {0: '1.000e-40', 1: '1.000e-40', 5: '1.000e-40', 6: '1.000e-40'}, '  1  0  [m^6/s]')
    t = edit_block(t, 'RbGeI3', 'c_p_auger :',
                   {0: '1.000e-40', 1: '1.000e-40', 5: '1.000e-40', 6: '1.000e-40'}, '  1  0  [m^6/s]')
    return t

def set_bulk_nt(text, layer, n_m3):
    return edit_block(text, layer, 'Nt(uniform) :',
                      {0: f'{n_m3:.3e}', 1: f'{n_m3:.3e}', 2: f'{n_m3:.3e}',
                       5: f'{n_m3:.3e}', 6: f'{n_m3:.3e}'}, '  0  2  [/m^3]')

def set_interfaces(text, n_m2):
    def repl(m):
        return m.group(1) + f'{n_m2:.3e}' + m.group(2)
    return re.sub(r'(^N\s*:\s*)[\d.eE+-]+(\s*\[/m\^2\])', repl, text, flags=re.MULTILINE)

base = set_krad_auger(BASE)
write_def('r6R_base.def', base)
t = set_bulk_nt(base, 'RbGeI3', 1e21)
write_def('r6R_Nt15.def', t)
t2 = set_interfaces(set_bulk_nt(base, 'RbGeI3', 1e21), 1e19)  # 1e15 cm-2 interfaces
write_def('r6R_Nt15if15.def', t2)

def parse_pin_aware(path):
    sm = {}
    with open(path) as f:
        for line in f:
            ls = line.strip()
            for k in ('Voc', 'Jsc', 'FF', 'eta'):
                if ls.startswith(k + ' ='):
                    try:
                        sm[k] = float(ls.split('=')[1].strip().split()[0])
                    except ValueError:
                        pass
    if not all(k in sm for k in ('Voc', 'Jsc', 'FF')):
        return {'PCE': 0, 'FAILED': 'empty'}
    pce1 = round(sm['Voc'] * abs(sm['Jsc']) * sm['FF'] / 100, 2)
    return {'Voc': round(sm['Voc'], 4), 'Jsc': round(abs(sm['Jsc']), 4),
            'FF': round(sm['FF'], 2), 'eta_illum': round(sm.get('eta', 0), 2),
            'PCE_1sun': pce1}

def main():
    base = set_krad_auger(BASE)
    write_def('r6R_base.def', base)
    t = set_bulk_nt(base, 'RbGeI3', 1e21)
    write_def('r6R_Nt15.def', t)
    t2 = set_interfaces(set_bulk_nt(base, 'RbGeI3', 1e21), 1e19)
    write_def('r6R_Nt15if15.def', t2)
    r = SCAPSrunner(lambda p: from_param_dict(p), lambda p: parse_pin_aware(p), ncores=4)
    r.sync_parameters()
    inputs = {
        'R1_radAug100': {'load': 'r6R_base.def', 'workingpoint': {'temperature': 300, 'illumination': 100}, 'iv': {'start': 0, 'stop': 1.5, 'step': 0.01}},
        'R2_refl90': {'load': 'r6R_base.def', 'workingpoint': {'temperature': 300, 'illumination': 90}, 'iv': {'start': 0, 'stop': 1.5, 'step': 0.01}},
        'R3_bulk15': {'load': 'r6R_Nt15.def', 'workingpoint': {'temperature': 300, 'illumination': 90}, 'iv': {'start': 0, 'stop': 1.5, 'step': 0.01}},
        'R4_bulkif15': {'load': 'r6R_Nt15if15.def', 'workingpoint': {'temperature': 300, 'illumination': 90}, 'iv': {'start': 0, 'stop': 1.5, 'step': 0.01}},
    }
    out = r.run_inputs(inputs)
    json.dump(out, open(os.path.join(OUT_DIR, 'r6_realistic_waterfall.json'), 'w'), indent=2)
    for k, v in out.items():
        print(k, v)
    print('saved r6_realistic_waterfall.json')


if __name__ == '__main__':
    main()
