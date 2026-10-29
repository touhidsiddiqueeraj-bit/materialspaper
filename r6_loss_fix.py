#!/usr/bin/env python3
"""r6_loss_fix — correct K_rad/Auger index1 + optical derating via
illumination scaling (SCAPS ignores def Tfront under scripted working
point; illumination 90/85 = first-order 10/15% front-reflection loss,
consistent with the 0.1-1.5 sun linearity proven in round4_illum).
Also retries r6_rad_K16 (transient xvfb crash) and rebuilds realistic
waterfall nodes with corrected K/Auger + optical scaling.
"""
import sys, json, os
sys.path.insert(0, '/home/touhid/Documents/materilaspaper')
from r5_lib import BASE, DEF_DIR, write_def, edit_block, run_set

def set_krad(text, layer, val):
    return edit_block(text, layer, 'K_rad :',
                      {0: f'{val:.3e}', 1: f'{val:.3e}', 5: f'{val:.3e}', 6: f'{val:.3e}'},
                      '  1  0  [m^3/s]')

def set_auger(text, layer, val):
    t = edit_block(text, layer, 'c_n_auger :',
                   {0: f'{val:.3e}', 1: f'{val:.3e}', 5: f'{val:.3e}', 6: f'{val:.3e}'},
                   '  1  0  [m^6/s]')
    t = edit_block(t, layer, 'c_p_auger :',
                   {0: f'{val:.3e}', 1: f'{val:.3e}', 5: f'{val:.3e}', 6: f'{val:.3e}'},
                   '  1  0  [m^6/s]')
    return t

variants = {}
# corrected radiative @1e-16 (retry) + corrected combined realistic
t = set_krad(BASE, 'RbGeI3', 1e-16)
write_def('r6_rad_K16c.def', t)
variants['r6_rad_K16c'] = 'r6_rad_K16c.def'
t = set_krad(BASE, 'RbGeI3', 1e-16)
t = set_auger(t, 'RbGeI3', 1e-40)
write_def('r6_realistic_c.def', t)
variants['r6_realistic_c'] = 'r6_realistic_c.def'

def main():
    print(f'{len(variants)} native variants')
    run_set(variants, 'r6_loss_fix.json')

    # optical derating via illumination scaling (native SCAPS photon scaling)
    sys.path.insert(0, '/home/touhid/scaps-runner/src')
    from scaps_runner import SCAPSrunner
    from scaps_runner.script_gen import from_param_dict
    from r5_lib import op_summary_only
    OUT_DIR = '/home/touhid/Documents/materilaspaper/r5_results'
    r = SCAPSrunner(lambda p: from_param_dict(p), lambda p: op_summary_only(p), ncores=4)
    r.sync_parameters()
    inputs = {}
    for tag, illum in (('opt100', 100), ('opt90', 90), ('opt85', 85)):
        inputs[tag] = {'load': 'r6_realistic_c.def',
                       'workingpoint': {'temperature': 300, 'illumination': illum},
                       'iv': {'start': 0, 'stop': 1.5, 'step': 0.01}}
    out = r.run_inputs(inputs)
    print(out)
    prev = json.load(open(os.path.join(OUT_DIR, 'r6_loss_fix.json')))
    for k, v in out.items():
        sm = v.get('summary', v) if isinstance(v, dict) else {}
        prev[k] = sm if isinstance(sm, dict) else v
    json.dump(prev, open(os.path.join(OUT_DIR, 'r6_loss_fix.json'), 'w'), indent=2)
    print('saved r6_loss_fix.json with optical nodes')


if __name__ == '__main__':
    main()
