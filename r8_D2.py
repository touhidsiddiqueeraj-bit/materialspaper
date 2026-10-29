#!/usr/bin/env python3
"""r8_D2 — D2 (FTO/TiO2/RbGeI3/NiO/Au) through the same 11-step triple-gate
chain as D4 (r8_oat). D2 outscored D4 at screening (21.10 vs 19.78%) so the
like-for-like pipeline answers whether the gap survives optimization.

NiO HTL uses literature-standard SCAPS parameters (Eg 3.6, chi 1.8,
eps 11.7, Nc 2.8e19/Nv 1e19 cm-3, mu 12/2.8 cm2/Vs, NA 1e18, Nt 1e15),
NOT fitted; documented in S7. Back contact Au kept as in screening.
Carry-forward: D4 adopted values as priors between chunks (documented);
D2's own per-step optimum picked by the same gate rules; local-optimality
confirmation on the consolidated D2 deck at the end.

Usage: python3 r8_D2.py CHUNK  (CHUNK = 1, 2, 3)
  chunk1: th, nt, eps, chi   (on D2 initial)
  chunk2: nifT, nifC, eg, etl (on chunk1 adoptions)
  chunk3: htl, nc, nv         (on chunk2 adoptions)
Outputs: r5_results/r8_D2_sNN_<step>.json
"""
import sys, os, json
sys.path.insert(0, '/home/touhid/Documents/materilaspaper')
from r5_lib import DEF_DIR, OUT_DIR, write_def, edit_block
import functools
import r8_oat
from r5_lib import run_set as _rs
r8_oat.run_set = functools.partial(_rs, ncores=1)  # serial: avoids Xvfb contention flakes
from r8_oat import (set_iface, run_with_retry, logspace, STEPS,
                    build_initial as build_D4_initial)

HTL = 'NiO'
F = lambda v: f'{v:.3e}'
E = lambda v: f'{v:.6f}'

NIO = dict(d='1.000e-07', eps='11.700000', chi='1.800000', Eg='3.600000',
           Nc='2.800e+25', Nv='1.000e+25', mu_n='1.200e-03', mu_p='2.800e-04',
           Na='1.000e+24', Nd='0.000000e+00', Nt='1.000e+21', edge='344.44')


def build_D2_initial():
    t = build_D4_initial()
    t = t.replace('name : CuI (6.1)', 'name : NiO (6.1)')
    t = t.replace('interfacename : CuI (6) / RbGeI3 (7',
                  'interfacename : NiO (6) / RbGeI3 (7')
    P = NIO
    t = edit_block(t, HTL, 'd :', {0: P['d']}, '[m]')
    t = edit_block(t, HTL, 'eps :', {0: P['eps'], 5: P['eps'], 6: P['eps']}, '[-]')
    t = edit_block(t, HTL, 'chi :', {0: P['chi'], 5: P['chi'], 6: P['chi']}, '[eV]')
    t = edit_block(t, HTL, 'Eg :', {0: P['Eg'], 5: P['Eg'], 6: P['Eg']}, '[eV]')
    t = edit_block(t, HTL, 'Nc :', {0: P['Nc'], 5: P['Nc'], 6: P['Nc']}, '[/m^3]')
    t = edit_block(t, HTL, 'Nv :', {0: P['Nv'], 5: P['Nv'], 6: P['Nv']}, '[/m^3]')
    t = edit_block(t, HTL, 'mu_n :', {0: P['mu_n'], 5: P['mu_n'], 6: P['mu_n']}, '[m^2/Vs]')
    t = edit_block(t, HTL, 'mu_p :', {0: P['mu_p'], 5: P['mu_p'], 6: P['mu_p']}, '[m^2/Vs]')
    t = edit_block(t, HTL, 'Na(uniform) :', {0: P['Na'], 5: P['Na'], 6: P['Na']}, '[/m^3]')
    t = edit_block(t, HTL, 'Nd(uniform) :', {0: P['Nd'], 5: P['Nd'], 6: P['Nd']}, '[/m^3]')
    t = edit_block(t, HTL, 'Nt(uniform) :', {0: P['Nt'], 5: P['Nt'], 6: P['Nt']}, '[/m^3]')
    t = edit_block(t, HTL, 'absorption grading :', {0: P['edge']}, '[nm]')
    write_def('r8_D2_initial.def', t)
    return t


def apply_D2(text, step, val):
    from r8_oat import apply_val
    if step in ('nifC', 'htl'):
        lab, v = val
        if step == 'nifC':
            return set_iface(text, HTL, v)
        return edit_block(text, HTL, 'd :', {0: F(v)}, '[m]')
    return apply_val(text, step, val)


# D4 adopted priors for carry-forward (documented); D2's own picks revise these.
PRIORS = {'th': 0.7e-6, 'nt': 1e20, 'eps': 15.0, 'chi': 3.9,
          'nifT': 1e18, 'nifC': 1e18, 'eg': 1.4, 'etl': 10e-9,
          'htl': 0.1e-6, 'nc': 1e24, 'nv': 1e24}
ORDER = ['th', 'nt', 'eps', 'chi', 'nifT', 'nifC', 'eg', 'etl',
         'htl', 'nc', 'nv']
CHUNKS = {1: ORDER[0:4], 2: ORDER[4:8], 3: ORDER[8:11]}


def base_for(chunk, picks):
    """D2 initial + all priors/picks for steps before this chunk."""
    t = build_D2_initial()
    done = [s for c in sorted(CHUNKS) if c < chunk for s in CHUNKS[c]]
    stepmap = dict(STEPS)
    for s in done:
        vals = dict(stepmap[s])
        lab = picks.get(s)
        if lab is None:
            # fall back to D4 prior label: find matching value
            pv = PRIORS[s]
            lab = min(vals, key=lambda k: abs(vals[k] - pv))
        t = apply_D2(t, s, (lab, vals[lab]))
    return t


if __name__ == '__main__':
    # Sequential max-carry mirroring r8_oat exactly (same pipeline):
    #   python3 r8_D2.py STEP   (STEP in th nt eps chi nifT nifC eg etl htl nc nv)
    # Carry def: r8_D2_carry.def (starts as D2 initial). Each step runs its
    # grid on the current carry, carries the raw max forward, and records it
    # in r8_D2_chain.json. Gate-adopted D2 assembly happens at the end.
    step = sys.argv[1]
    stepmap = dict(STEPS)
    carry = open(os.path.join(DEF_DIR, 'r8_D2_carry.def')).read() \
        if os.path.exists(os.path.join(DEF_DIR, 'r8_D2_carry.def')) \
        else build_D2_initial()
    if step == 'init':
        write_def('r8_D2_carry.def', carry)
        print('carry initialized')
        raise SystemExit
    grid = stepmap[step]
    variants = {}
    for lab, v in grid:
        name = f'r8_D2_{step}_{lab}.def'
        write_def(name, apply_D2(carry, step, (lab, v)))
        variants[f'r8_D2_{step}_{lab}'] = name
    out = run_with_retry(variants, os.path.join(OUT_DIR, f'r8_D2_s_{step}.json'),
                         {'start': 0, 'stop': 1.5, 'step': 0.02})
    best, bestp = None, -1.0
    for k in sorted(out):
        v = out[k]
        print(k, {q: v.get(q) for q in ('Voc', 'Jsc', 'FF', 'PCE')} if isinstance(v, dict) else v)
        p = v.get('PCE', 0) if isinstance(v, dict) else 0
        if p > bestp:
            best, bestp = k, p
    chain = json.load(open('r8_D2_chain.json')) if os.path.exists('r8_D2_chain.json') else {}
    if best is None or bestp <= 0:
        chain[step] = {'carried': None}
        print(f'STEP {step}: ALL FAILED, carrying forward unchanged')
    else:
        blab = best.replace(f'r8_D2_{step}_', '')
        carry = apply_D2(carry, step, (blab, dict(grid)[blab]))
        write_def('r8_D2_carry.def', carry)
        chain[step] = {'carried': blab, 'PCE': bestp}
        print(f'STEP {step}: carried={blab} PCE={bestp}')
    json.dump(chain, open('r8_D2_chain.json', 'w'), indent=1)
