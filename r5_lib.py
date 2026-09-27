#!/usr/bin/env python3
"""r5_lib — shared def-edit + runner boilerplate for Round-5 sweeps.
Base: perovskite-rbgei3.def (OPAT final point). All edits are block-scoped to
the RbGeI3 layer block (between 'name : RbGeI3' and next 'interface properties').
SI units throughout: /m^3, /m^2, m^2/Vs, m, eV.
"""
import sys, os, json, re
sys.path.insert(0, '/home/touhid/scaps-runner/src')
from scaps_runner import SCAPSrunner, parse_jv_curve
from scaps_runner.script_gen import from_param_dict

DEF_DIR = '/home/touhid/.scaps-runner/scaps_dat/def'
OUT_DIR = '/home/touhid/Documents/materilaspaper/r5_results'
os.makedirs(OUT_DIR, exist_ok=True)

BASE = open(os.path.join(DEF_DIR, 'perovskite-rbgei3.def')).read()


def edit_block(text, layer, key, fields, suffix, first_only=True):
    """Replace numeric fields (by index) of a colon line inside layer block."""
    lines = text.split('\n')
    ni = next(i for i, l in enumerate(lines)
              if l.strip().startswith('name :') and layer in l)
    end = len(lines)
    for i in range(ni + 1, len(lines)):
        s = lines[i].strip()
        if s.startswith('name :') or s.startswith('interface properties'):
            end = i
            break
    for i in range(ni, end):
        if lines[i].strip().startswith(key):
            parts = lines[i].split(':')
            nums = re.findall(r'[\d.eE+-]+', parts[1])
            for idx, v in fields.items():
                nums[idx] = v
            n_keep = 7 if len(nums) >= 7 else len(nums)
            lines[i] = parts[0] + ':  ' + '  '.join(nums[:n_keep]) + suffix
            if first_only:
                break
    return '\n'.join(lines)


def edit_single(text, layer, key, value, unit):
    """Replace single-value line (Et, sigma_n/p) inside layer block."""
    lines = text.split('\n')
    ni = next(i for i, l in enumerate(lines)
              if l.strip().startswith('name :') and layer in l)
    end = len(lines)
    for i in range(ni + 1, len(lines)):
        s = lines[i].strip()
        if s.startswith('name :') or s.startswith('interface properties'):
            end = i
            break
    for i in range(ni, end):
        if lines[i].strip().startswith(key):
            lines[i] = f'{key} :  {value}\t[{unit}]'
            break
    return '\n'.join(lines)


F7 = {0: None, 5: None, 6: None}  # fields 1,6,7 keep-pattern


def set7(text, layer, key, val, suffix):
    return edit_block(text, layer, key, {0: val, 5: val, 6: val}, suffix)


def set_interfaces(text, n_m2):
    def repl(m):
        return m.group(1) + f'{n_m2:.3e}' + m.group(2)
    return re.sub(r'(^N\s*:\s*)[\d.eE+-]+(\s*\[/m\^2\])', repl,
                  text, flags=re.MULTILINE)


def write_def(name, content):
    with open(os.path.join(DEF_DIR, name), 'w') as f:
        f.write(content)
    return name


def parse_summary(path):
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
    return sm


def arith_ok(sm, tol=0.6):
    """Fail-closed: Voc*Jsc*FF/100 must reproduce eta (Pin=100 mW/cm2).
    Catches stale-file parses (e.g. 1.5-sun file under a 1-sun input)."""
    try:
        return abs(sm['Voc'] * abs(sm['Jsc']) * sm['FF'] / 100
                   - sm['eta']) <= tol
    except KeyError:
        return False


def op_summary_only(path):
    import os as _os
    if not _os.path.exists(path):
        return {'PCE': 0, 'FAILED': 'missing-result-file'}
    sm = parse_summary(path)
    if 'eta' in sm and arith_ok(sm):
        return {'Voc': round(sm['Voc'], 4), 'Jsc': round(abs(sm['Jsc']), 4),
                'FF': round(sm['FF'], 2), 'PCE': round(sm['eta'], 2)}
    return {'PCE': 0, 'FAILED': 'inconsistent-or-empty'}


def op_with_jv(path):
    import os as _os
    if not _os.path.exists(path):
        return {'FAILED': 'missing-result-file', 'J': [], 'V': []}
    J, V = parse_jv_curve(path)
    r = {'J': J.tolist(), 'V': V.tolist()}
    sm = parse_summary(path)
    if sm and arith_ok(sm):
        r['summary'] = {k: (round(v, 4) if k != 'FF' else round(v, 2))
                        for k, v in sm.items()}
    else:
        r['summary'] = {}
        r['FAILED'] = 'inconsistent-or-empty'
    return r


def run_set(variants, out_json, iv=None, temps=None, with_jv_keys=(),
            ncores=4):
    """variants: {run_key: def_filename}. Builds inputs, runs, saves JSON."""
    r = SCAPSrunner(lambda p: from_param_dict(p),
                    op_with_jv if with_jv_keys else
                    (lambda p: op_summary_only(p)), ncores=ncores)
    r.sync_parameters()
    inputs = {}
    for k, d in variants.items():
        wp = {'temperature': (temps[k] if temps else 300),
              'illumination': 100}
        ivp = iv or {'start': 0, 'stop': 1.5, 'step': 0.02}
        inputs[k] = {'load': d, 'workingpoint': wp, 'iv': ivp}
    out = r.run_inputs(inputs)
    results = {}
    for k, v in out.items():
        if with_jv_keys and k in with_jv_keys:
            results[k] = v
            sm = v.get('summary', {})
            if sm:
                print(f"{k}: Voc={sm.get('Voc')} Jsc={sm.get('Jsc')} "
                      f"FF={sm.get('FF')} eta={sm.get('eta')}")
            else:
                print(f"{k}: NO SUMMARY (failed?)")
        else:
            sm = v.get('summary', v) if isinstance(v, dict) else {}
            if isinstance(sm, dict) and 'eta' in sm:
                results[k] = {
                    'Voc': round(sm['Voc'], 4),
                    'Jsc': round(abs(sm['Jsc']), 4),
                    'FF': round(sm['FF'], 2), 'PCE': round(sm['eta'], 2)}
            else:
                results[k] = (v if isinstance(v, dict) else
                              {'PCE': 0, 'FAILED': True})
            print(f"{k}: {results[k]}")
    with open(os.path.join(OUT_DIR, out_json), 'w') as f:
        json.dump(results, f, indent=2)
    print(f'saved {out_json}')
    return results
