#!/usr/bin/env python3
"""r8_ga — MAJOR-REVISION GA re-run on rebased deck (reviewer concern 1).
Base: r8_H1_adopted.def (NC/NV=1e18, K_rad=1e-16 DB-consistent).
Genes: Eg, log10(Nt_bulk /m3), log10(N_if /m2, both tied), log10(NC), log10(NV), d_abs(um).
NC/NV bounds rebased to [24,26] (literature floor); chi follows Eg.
Pop 10 x 6 gen + 2 seeds = ~62 SCAPS evals. Seeds fixed (random.seed(7)).
Framing: reports best-found joint point, NOT a global maximum.
"""
import sys, os, json, re, random
sys.path.insert(0, '/home/touhid/scaps-runner/src')
from scaps_runner import SCAPSrunner, parse_jv_curve
from scaps_runner.script_gen import from_param_dict
import numpy as np

random.seed(7)
np.random.seed(7)

BASE_DEF = '/home/touhid/.scaps-runner/scaps_dat/def/r8_H1_adopted.def'
DEF_DIR = '/home/touhid/.scaps-runner/scaps_dat/def'
OUT_DIR = '/home/touhid/Documents/materilaspaper/r5_results'
os.makedirs(OUT_DIR, exist_ok=True)
BASE = open(BASE_DEF).read()

BOUNDS = {  # (lo, hi); NC/NV rebased to literature floor 1e18/cm3 (review)
    'eg': (1.30, 1.60),
    'lognt': (18.0, 22.0),     # Nt bulk /m3  (1e12..1e16 /cm3)
    'lognif': (16.0, 20.0),    # interface N /m2 both (1e12..1e16 /cm2)
    'lognc': (24.0, 26.0),     # NC /m3
    'lognv': (24.0, 26.0),     # NV /m3
    'dabs': (0.40, 1.00),      # absorber thickness um
}
GENES = list(BOUNDS.keys())
# adopted-H1 seed + low-gap seed (base already carries K_rad=1e-16 + NC/NV=1e18)
SEEDS = [
    {'eg': 1.40, 'lognt': 20.0, 'lognif': 18.0, 'lognc': 24.0, 'lognv': 24.0, 'dabs': 0.70},
    {'eg': 1.30, 'lognt': 18.0, 'lognif': 18.0, 'lognc': 24.0, 'lognv': 24.0, 'dabs': 0.70},
]

def build_def(g):
    lines = BASE.split('\n')
    name_idx = next(i for i, l in enumerate(lines) if l.strip().startswith('name :') and 'RbGeI3' in l)
    # find block end: next 'name :' or 'interface properties'
    end = len(lines)
    for i in range(name_idx + 1, len(lines)):
        ss = lines[i].strip()
        if ss.startswith('name :') or ss.startswith('interface properties'):
            end = i
            break
    eg, chi = g['eg'], 3.9 + 0.5 * (g['eg'] - 1.4)
    for i in range(name_idx, end):
        s = lines[i].strip()
        if s.startswith('d :') and 'm]' in s:
            lines[i] = re.sub(r'^(\s*d\s*:\s*)[\d.eE+-]+', r'\g<1>' + f'{g["dabs"] * 1e-6:.6e}', lines[i], count=1)
            break
    for i in range(name_idx, end):
        s = lines[i].strip()
        def setfields(prefix, vals, suffix):
            parts = lines[i].split(':')
            nums = re.findall(r'[\d.eE+-]+', parts[1])
            for idx, v in vals.items():
                nums[idx] = v
            lines[i] = parts[0] + ':  ' + '  '.join(nums[:7]) + suffix
        if s.startswith('Eg :'):
            e = f'{eg:.6f}'
            setfields('Eg', {0: e, 1: e, 5: e, 6: e}, '  1  0  [eV]')
        elif s.startswith('chi :'):
            c = f'{chi:.6f}'
            setfields('chi', {0: c, 5: c, 6: c}, '  1  0  [eV]')
        elif s.startswith('Nc :'):
            v = f'{10 ** g["lognc"]:.6e}'
            setfields('Nc', {0: v, 5: v, 6: v}, '  1  0  [/m^3]')
        elif s.startswith('Nv :'):
            v = f'{10 ** g["lognv"]:.6e}'
            setfields('Nv', {0: v, 5: v, 6: v}, '  1  0  [/m^3]')
        elif s.startswith('Nt(uniform) :'):
            v = f'{10 ** g["lognt"]:.6e}'
            setfields('Nt', {0: v, 1: v, 2: v, 5: v, 6: v}, '  0  2  [/m^3]')
    text = '\n'.join(lines)
    nif = 10 ** g['lognif']
    text = re.sub(r'(^N\s*:\s*)[\d.eE+-]+(\s*\[/m\^2\])',
                  r'\g<1>' + f'{nif:.3e}' + r'\g<2>', text, flags=re.MULTILINE)
    return text

def individual_tag(g):
    return (f"eg{g['eg']:.2f}_nt{g['lognt']:.1f}_nif{g['lognif']:.1f}_"
            f"nc{g['lognc']:.1f}_nv{g['lognv']:.1f}_d{g['dabs']:.2f}".replace('.', 'p'))

# validate one def before launching
sample = build_def(SEEDS[0])
open(os.path.join(DEF_DIR, 'r4_ga_sample.def'), 'w').write(sample)
blk = sample.split('name : RbGeI3')[1].split('interface properties')[0]
for key in ('d :', 'Eg :', 'chi :', 'Nc :', 'Nv :', 'Nt(uniform) :'):
    print('SAMPLE', [l.strip()[:110] for l in blk.split('\n') if l.strip().startswith(key)][:1])

def op(path):
    try:
        J, V = parse_jv_curve(path)
    except Exception:
        return {'PCE': 0.0, 'FAILED': True}
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
    if 'eta' in sm:
        return {'PCE': round(sm['eta'], 2), 'Voc': round(sm['Voc'], 4),
                'Jsc': round(abs(sm['Jsc']), 4), 'FF': round(sm['FF'], 2)}
    return {'PCE': 0.0, 'FAILED': True}

runner = SCAPSrunner(lambda p: from_param_dict(p), op, ncores=4)
runner.sync_parameters()

def evaluate(pop):
    defs = {}
    for g in pop:
        tag = 'r8ga_' + individual_tag(g)
        with open(os.path.join(DEF_DIR, tag + '.def'), 'w') as f:
            f.write(build_def(g))
        defs[tag] = g
    runner.sync_parameters()
    inputs = {t: {'load': t + '.def', 'workingpoint': {'temperature': 300, 'illumination': 100},
                    'iv': {'start': 0, 'stop': 1.5, 'step': 0.02}} for t in defs}
    out = runner.run_inputs(inputs)
    res = []
    for t, g in defs.items():
        r = out.get(t, {'PCE': 0.0})
        res.append((g, float(r.get('PCE', 0.0)), r))
    return res

def rand_gene():
    return {k: random.uniform(*BOUNDS[k]) for k in GENES}

def crossover(a, b):
    alpha = np.random.uniform(0.3, 0.7)
    return {k: alpha * a[k] + (1 - alpha) * b[k] for k in GENES}

def mutate(g, rate=0.25, scale=0.12):
    g = dict(g)
    for k in GENES:
        if random.random() < rate:
            lo, hi = BOUNDS[k]
            g[k] = float(np.clip(g[k] + random.gauss(0, scale * (hi - lo)), lo, hi))
    return g

POP, NGEN, ELITE = 10, 6, 2
history, log = [], []
pop = [dict(s) for s in SEEDS] + [rand_gene() for _ in range(POP - len(SEEDS))]
for gen in range(NGEN):
    res = evaluate(pop)
    res.sort(key=lambda x: -x[1])
    best = res[0]
    history.append(best[1])
    for g, fit, det in res:
        log.append({'gen': gen, 'fit': fit, 'genes': g, 'detail': det})
    print(f'GEN {gen}: best={best[1]:.2f} {individual_tag(best[0])} {best[2]}', flush=True)
    # select: elites + tournament children + immigrants
    nxt = [dict(res[i][0]) for i in range(ELITE)]
    while len(nxt) < POP - 2:
        a, b = random.choice(res[:6])[0], random.choice(res[:6])[0]
        nxt.append(mutate(crossover(a, b)))
    nxt += [rand_gene() for _ in range(2)]
    pop = nxt

res = sorted(log, key=lambda x: -x['fit'])
print('TOP5:')
for r in res[:5]:
    print(f"  {r['fit']:.2f} gen{r['gen']} {individual_tag(r['genes'])} {r['detail']}")
with open(os.path.join(OUT_DIR, 'r8_ga_results.json'), 'w') as f:
    json.dump({'history': history, 'top': res[:15], 'bounds': BOUNDS}, f, indent=2)
print('saved r8_ga_results.json, history:', history)
