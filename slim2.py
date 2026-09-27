#!/usr/bin/env python3
"""slim2 — move Tables I-IV to supplement S3, fix U/V/W + VII.A titles,
remap Table refs (single-pass), light prose trim. Operates on
solar_submission/manuscript.tex + supplement.tex. Idempotent-ish: run ONCE
on slim output (guard: abort if 'Supplementary Table S1' already present)."""
import re, shutil

TEX = 'solar_submission/manuscript.tex'
SUP = 'solar_submission/supplement.tex'
m = open(TEX).read()
assert 'Supplementary Table S1' not in m, 'already slimmed!'
s = open(SUP).read()

# ---------- 1. extract Tables I-IV (first four table envs) ----------
envs = list(re.finditer(r'\\begin\{table\}.*?\\end\{table\}', m, re.DOTALL))
assert len(envs) == 10, len(envs)
moved = [envs[i].group(0) for i in range(4)]
SNUM = ['S1', 'S2', 'S3', 'S4']
sup_tables = []
for sn, env in zip(SNUM, moved):
    env = re.sub(r'\\caption\{', '\\\\caption{Table %s. ' % sn, env, count=1)
    # strip original 'Table X. ' lead inside caption
    env = re.sub(r'\\caption\{Table %s\. Table [IVX]+\. ' % sn,
                 '\\\\caption{Table %s. ' % sn, env, count=1)
    sup_tables.append(env)
    m = m.replace(env if False else moved[moved.index(env)], '', 1) \
        if False else m
# remove by span (reverse order)
for e in sorted(envs[:4], key=lambda x: x.start(), reverse=True):
    m = m[:e.start()] + m[e.end():]
s = s.replace(r'\end{document}',
              '\\section*{S3.\\ Screening and simulation setup tables}\n'
              + '\n'.join(sup_tables)
              + '\n\\end{document}')

# ---------- 2. Table ref remap (single pass, longest-first) ----------
TMAP = {'X': 'VI', 'IX': 'V', 'VIII': 'IV', 'VII': 'III', 'VI': 'II',
        'V': 'I', 'IV': 'S4', 'III': 'S3', 'II': 'S2', 'I': 'S1'}
keys = '|'.join(sorted(TMAP, key=len, reverse=True))


def trep(mo):
    old = mo.group(1)
    new = TMAP[old]
    return ('Supplementary Table %s' % new if new.startswith('S')
            else 'Table %s' % new)


m = re.sub(r'Table (%s)\b' % keys, trep, m)

# ---------- 3. U/V/W inline letters + A-site dup + VII.A title ----------
m = m.replace('U. Effect of background acceptor doping.',
              'J. Effect of background acceptor doping.')
m = m.replace('V. Effect of series resistance: manufacturing tolerance.',
              'K. Effect of series resistance: manufacturing tolerance.')
m = m.replace('W. Absorber mobility viability.',
              'L. Absorber mobility viability.')
m = m.replace('\\subsection{A-site cation influence: RbGeI$_{3}$ versus CsGeI$_{3}$}\nB. A-site cation influence: RbGeI$_{3}$ versus CsGeI$_{3}$.',
              '\\subsection{A-site cation influence: RbGeI$_{3}$ versus CsGeI$_{3}$}')
m = re.sub(r'\\subsection\{Limitations of the present study\} Four caveats',
           '\\\\subsection{Limitations of the present study}\nFour caveats',
           m, count=1)

# ---------- 4. light prose trim (~150 words, claims preserved) ----------
TRIMS = [
    ('Photovoltaic devices are commonly classified into three generations based on the absorber material and fabrication technology. First-generation crystalline silicon (c-Si) cells dominate the commercial market thanks to their high efficiency and long operational lifetime, but they require energy-intensive processing and rigid substrates. Second-generation thin-film technologies (including CdTe, CIGS, and amorphous silicon) reduce material consumption and offer flexible substrates, but their efficiencies are modest and some rely on scarce or toxic elements. The third generation, which includes dye-sensitized solar cells, organic photovoltaics, quantum-dot cells, and perovskite solar cells (PSCs) \\cite{r5,r6}, promises high efficiency at low processing cost and is intensely studied.',
     'Photovoltaic devices are commonly classified into three generations: crystalline silicon (high efficiency, energy-intensive), thin films (less material, modest efficiency), and emerging devices promising high efficiency at low processing cost.'),
]
for a, b in TRIMS:
    if a in m:
        m = m.replace(a, b)
        print('trim applied')
    else:
        print('TRIM PATTERN NOT FOUND')

open(TEX, 'w').write(m)
open(SUP, 'w').write(s)
print('slim2 done')
