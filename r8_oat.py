#!/usr/bin/env python3
"""r8_oat — MAJOR-REVISION frozen-deck sequential OAT redo (reviewer concern 3).

Starts from the INITIAL deck (Table S2 values) on ONE frozen deck generation,
runs the 11 steps in order with carry-forward, bracketing former edge optima:
eps extended low (10,12), chi extended low (3.7,3.8), CuI extended thin
(0.05,0.075 um), NC/NV REBASED to literature range 1e18-1e20 (reviewer
concern 1). Per-interface N sweeps (steps 5,6) edit only their own block.
Eg steps rescale the absorption edge (1240/Eg).
Outputs: r8_sNN.json per step + r8_oat_summary.json + r8 defs in def dir.
"""
import sys, os, json, re
sys.path.insert(0, '/home/touhid/Documents/materilaspaper')
from r5_lib import BASE, DEF_DIR, OUT_DIR, write_def, run_set, edit_block

F = lambda v: f'{v:.3e}'
E = lambda v: f'{v:.6f}'


def set_iface(text, marker, n_m2):
    """Set N ([/m^2]) inside EVERY interface block whose interfacename contains
    marker (BSF decks have two BSF blocks: CuI/BSF and BSF/absorber)."""
    lines = text.split('\n')
    starts = [i for i, l in enumerate(lines)
              if 'interfacename :' in l and marker in l]
    if not starts:
        raise ValueError(f'no interface block matches {marker!r}')
    for si in starts:
        end = len(lines)
        for i in range(si + 1, len(lines)):
            s = lines[i].strip()
            if s.startswith('interfacename :') or s.startswith('layer'):
                end = i
                break
        for i in range(si, end):
            if re.match(r'^N\s*:', lines[i].strip()):
                lines[i] = re.sub(r'[\d.eE+-]+', f'{n_m2:.3e}', lines[i], count=1)
                break
    return '\n'.join(lines)


def build_initial():
    t = BASE
    t = edit_block(t, 'RbGeI3', 'd :', {0: '4.000e-07'}, '[m]')
    t = edit_block(t, 'RbGeI3', 'Nt(uniform) :',
                   {0: '1.000e+21', 5: '1.000e+21', 6: '1.000e+21'}, '[/m^3]')
    t = edit_block(t, 'RbGeI3', 'eps :',
                   {0: '23.010000', 5: '23.010000', 6: '23.010000'}, '[-]')
    t = edit_block(t, 'RbGeI3', 'Nc :',
                   {0: '1.400e+25', 5: '1.400e+25', 6: '1.400e+25'}, '[/m^3]')
    t = edit_block(t, 'RbGeI3', 'Nv :',
                   {0: '2.800e+25', 5: '2.800e+25', 6: '2.800e+25'}, '[/m^3]')
    t = edit_block(t, 'RbGeI3', 'Na(uniform) :',
                   {0: '1.000e+15', 5: '1.000e+15', 6: '1.000e+15'}, '[/m^3]')
    t = edit_block(t, 'RbGeI3', 'Nd(uniform) :',
                   {0: '1.000e+15', 5: '1.000e+15', 6: '1.000e+15'}, '[/m^3]')
    t = edit_block(t, 'TiO2', 'd :', {0: '3.000e-08'}, '[m]')
    return t


def apply_val(text, step, val):
    """Return new def text with step's value applied. val is (label, SI float/str)."""
    lab, v = val
    if step == 'th':
        return edit_block(text, 'RbGeI3', 'd :', {0: F(v)}, '[m]')
    if step == 'nt':
        return edit_block(text, 'RbGeI3', 'Nt(uniform) :',
                           {0: F(v), 5: F(v), 6: F(v)}, '[/m^3]')
    if step == 'eps':
        return edit_block(text, 'RbGeI3', 'eps :',
                           {0: E(v), 5: E(v), 6: E(v)}, '[-]')
    if step == 'chi':
        return edit_block(text, 'RbGeI3', 'chi :',
                           {0: E(v), 5: E(v), 6: E(v)}, '[eV]')
    if step == 'nifT':
        return set_iface(text, 'TiO2', v)
    if step == 'nifC':
        return set_iface(text, 'CuI', v)
    if step == 'eg':
        t = edit_block(text, 'RbGeI3', 'Eg :',
                       {0: E(v), 5: E(v), 6: E(v)}, '[eV}')
        return edit_block(t, 'RbGeI3', 'absorption grading :',
                          {0: f'{1240.0 / v:.2f}'}, '[nm]')
    if step == 'etl':
        return edit_block(text, 'TiO2', 'd :', {0: F(v)}, '[m]')
    if step == 'htl':
        return edit_block(text, 'CuI', 'd :', {0: F(v)}, '[m]')
    if step == 'nc':
        return edit_block(text, 'RbGeI3', 'Nc :',
                           {0: F(v), 5: F(v), 6: F(v)}, '[/m^3]')
    if step == 'nv':
        return edit_block(text, 'RbGeI3', 'Nv :',
                           {0: F(v), 5: F(v), 6: F(v)}, '[/m^3]')
    raise ValueError(step)


def logspace(lo, hi, n):
    import numpy as np
    return [10 ** v for v in np.linspace(lo, hi, n)]


STEPS = [
    ('th', [(f'{t}um', t * 1e-6) for t in [0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]]),
    ('nt', [(f'1e{i}cm', 10.0 ** (i + 6)) for i in range(12, 19)]),
    ('eps', [(str(e), float(e)) for e in [10, 12, 15, 18, 21, 23.1]]),
    ('chi', [(str(c), c) for c in [3.7, 3.8, 3.9, 4.0, 4.1, 4.2]]),
    ('nifT', [(f'1e{i}cm2', 10.0 ** (i + 6)) for i in range(12, 19)]),
    ('nifC', [(f'1e{i}cm2', 10.0 ** (i + 6)) for i in range(12, 19)]),
    ('eg', [(str(e), e) for e in [1.3, 1.4, 1.5, 1.6, 1.7]]),
    ('etl', [(f'{int(t * 1e9)}nm', t) for t in [1e-8, 2e-8, 3e-8, 4e-8, 5e-8, 7e-8, 9e-8]]),
    ('htl', [(f'{t}um', t * 1e-6) for t in [0.05, 0.075, 0.1, 0.4, 0.7, 1.0, 1.3, 1.6, 1.9]]),
    ('nc', [(f'nc{i}', v) for i, v in enumerate(logspace(24, 26, 7))]),
    ('nv', [(f'nv{i}', v) for i, v in enumerate(logspace(24, 26, 7))]),
]

def run_with_retry(variants, out_path, iv, tries=3, with_jv_keys=(), temps=None):
    """Run variants; re-run FAILED keys up to `tries` attempts. Uses run_set's
    return values (it overwrites the file per call); writes merged JSON once."""
    merged, remaining = {}, dict(variants)
    for attempt in range(tries):
        if not remaining:
            break
        got = run_set(remaining, os.path.basename(out_path), iv=iv,
                      with_jv_keys=tuple(k for k in remaining if k in with_jv_keys),
                      temps={k: temps[k] for k in remaining} if temps else None)
        merged.update(got)

        def _ok(v):
            if not isinstance(v, dict):
                return False
            if v.get('PCE', 0) > 0:
                return True
            sm = v.get('summary', {})
            return isinstance(sm, dict) and sm.get('eta') is not None
        remaining = {k: v for k, v in variants.items() if not _ok(merged.get(k))}
        if remaining:
            print(f'  retry {attempt + 1}: {len(remaining)} failed -> {sorted(remaining)}')
    json.dump(merged, open(out_path, 'w'), indent=2)
    return merged


if __name__ == '__main__':
    cur = build_initial()
    write_def('r8_initial.def', cur)
    summary = []
    for si, (step, grid) in enumerate(STEPS, 1):
        variants = {}
        for lab, v in grid:
            key = f'r8_s{si:02d}_{step}_{lab}'
            write_def(key + '.def', apply_val(cur, step, (lab, v)))
            variants[key] = key + '.def'
        out = f'r8_s{si:02d}_{step}.json'
        opath = os.path.join(OUT_DIR, out)
        if os.path.exists(opath):
            os.remove(opath)
        res = run_with_retry(variants, opath,
                             {'start': 0, 'stop': 1.5, 'step': 0.02})
        best, bestp = None, -1.0
        for k, vv in res.items():
            p = vv.get('PCE', 0) if isinstance(vv, dict) else 0
            if p > bestp:
                best, bestp = k, p
        if best is None or bestp <= 0:
            summary.append({'step': step, 'best': None, 'metrics': {}})
            print(f'STEP {si} {step}: ALL FAILED, carrying forward unchanged')
            write_def(f'r8_carry_s{si:02d}.def', cur)
            continue
        blab = best.replace(f'r8_s{si:02d}_{step}_', '')
        bval = dict(grid)[blab]
        cur = apply_val(cur, step, (blab, bval))
        write_def(f'r8_carry_s{si:02d}.def', cur)
        summary.append({'step': step, 'best': blab,
                        'metrics': res[best]})
        print(f'STEP {si} {step}: best={blab} PCE={bestp}')
    json.dump(summary, open(os.path.join(OUT_DIR, 'r8_oat_summary.json'), 'w'), indent=1)
    print('saved r8_oat_summary.json')
