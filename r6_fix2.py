#!/usr/bin/env python3
"""r6_fix2 — judge-mandated gap closure (generating script on record).
 F1: r6_rad_K15 rerun (transient crash in r6_loss.py left it FAILED).
 F2: full-realism BSF node R5full = BSF50/NA1e19 + bulk Nt1e21 + interfaces
     1e19 @90 illum — like-for-like comparator to R4 (bulk+if 1e15 @90).
Writes into r6_loss.json (F1) and r6_realistic_waterfall.json (F2, key R5full).
"""
import sys, json, os, re
sys.path.insert(0, '/home/touhid/Documents/materilaspaper')


def main():
    from r5_lib import BASE, write_def, edit_block, run_set
    sys.path.insert(0, '/home/touhid/scaps-runner/src')
    from scaps_runner import SCAPSrunner
    from scaps_runner.script_gen import from_param_dict
    from r6_real import parse_pin_aware  # noqa: run-script import; guarded here
    from r6_bsf_sweep import build_bsf

    # F1
    t = edit_block(BASE, 'RbGeI3', 'K_rad :',
                   {0: '1.000e-15', 1: '1.000e-15', 5: '1.000e-15', 6: '1.000e-15'},
                   '  1  0  [m^3/s]')
    write_def('r6_rad_K15b.def', t)
    run_set({'r6_rad_K15': 'r6_rad_K15b.def'}, 'r6_loss_F1.json')

    # F2
    t2 = build_bsf(BASE, 50e-9, 1e25)
    t2 = edit_block(t2, 'RbGeI3', 'Nt(uniform) :',
                    {0: '1.000e+21', 1: '1.000e+21', 2: '1.000e+21',
                     5: '1.000e+21', 6: '1.000e+21'}, '  0  2  [/m^3]')

    def set_if(text, n_m2):
        return re.sub(r'(^N\s*:\s*)[\d.eE+-]+(\s*\[/m\^2\])',
                      lambda m: m.group(1) + f'{n_m2:.3e}' + m.group(2),
                      text, flags=re.MULTILINE)
    t2 = set_if(t2, 1e19)
    write_def('r6_BSF50_NA19_full15.def', t2)
    r = SCAPSrunner(lambda p: from_param_dict(p), lambda p: parse_pin_aware(p), ncores=2)
    r.sync_parameters()
    out = r.run_inputs({
        'R5full': {'load': 'r6_BSF50_NA19_full15.def',
                   'workingpoint': {'temperature': 300, 'illumination': 90},
                   'iv': {'start': 0, 'stop': 1.5, 'step': 0.01}}})
    print(out)
    wf = json.load(open('/home/touhid/Documents/materilaspaper/r5_results/r6_realistic_waterfall.json'))
    wf.update(out)
    json.dump(wf, open('/home/touhid/Documents/materilaspaper/r5_results/r6_realistic_waterfall.json', 'w'), indent=2)
    print('R5full saved')


if __name__ == '__main__':
    main()
