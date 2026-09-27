#!/usr/bin/env python3
"""slim — split manuscript.tex into slim main + supplement.tex.
Moves OAT sweep detail (V.B,V.D-V.L) + illum/dark (V.R,V.S) to supplement.
Reletters kept subsections, renumbers main figures 1..19, S1..S12 in suppl.
Run from repo root. Backs up manuscript.tex -> manuscript_full.tex (once)."""
import re, os, shutil

TEX = 'solar_submission/manuscript.tex'
if not os.path.exists('solar_submission/manuscript_full.tex'):
    shutil.copy(TEX, 'solar_submission/manuscript_full.tex')
lines = open(TEX).read().split('\n')

# subsection key -> (supplement section, own old fig, S-label)
MOVE = [
    ('Effect of absorber layer thickness', 'S1', 3, 'S1'),
    ('Effect of absorber dielectric constant', 'S1', 5, 'S2'),
    ('Effect of absorber electron affinity', 'S1', 6, 'S3'),
    ('Effect of TiO2', 'S1', 7, 'S4'),
    ('Effect of RbGeI3/CuI interfacial', 'S1', 8, 'S5'),
    ('Effect of absorber bandgap', 'S1', 9, 'S6'),
    ('Effect of TiO2 ETL thickness', 'S1', 10, 'S7'),
    ('Effect of CuI HTL thickness', 'S1', 11, 'S8'),
    ('conduction-band effective density', 'S1', 12, 'S9'),
    ('valence-band effective density', 'S1', 13, 'S10'),
    ('Illumination dependence', 'S2', 18, 'S11'),
    ('Dark J--V characteristics', 'S2', 19, 'S12'),
]
MOVED_FIGS = {m[2]: m[3] for m in MOVE}
FIGMAP = {1: 1, 2: 2, 4: 3, 14: 4, 15: 5, 16: 6, 17: 7, 20: 8, 21: 9,
          22: 10, 23: 11, 24: 12, 25: 13, 26: 14, 27: 15, 28: 16, 29: 17,
          30: 18, 31: 19}
RELETTER = {'M': 'D', 'N': 'E', 'O': 'F', 'P': 'G', 'Q': 'H', 'T': 'I',
            'U': 'J', 'V': 'K', 'W': 'L'}
SECMAP = RELETTER  # Section V.X refs


def _onepass(text, smap):
    # single-pass: longest-first alternation, no cascade chains
    keys = '|'.join(str(k) for k in sorted(smap, reverse=True))
    def rep(m):
        n = int(m.group(2))
        return '%s%s' % (m.group(1), smap[n]) if n in smap else m.group(0)
    text = re.sub(r'((?:Figs?|Figure)\.\s*)(%s)\b' % keys, rep, text)
    text = re.sub(r'(Figure\s+)(%s)\b' % keys, rep, text)
    return text


def renumber_figs(text, smap):
    return _onepass(text, smap)


def renumber_figs_S(text):
    text = _onepass(text, MOVED_FIGS)
    return _onepass(text, FIGMAP)


def fix_sections(text):
    def rep(m):
        L = m.group(1)
        return 'Section V.%s' % SECMAP[L] if L in SECMAP else m.group(0)
    return re.sub(r'Section V\.([A-W])\b', rep, text)


# ---------- split into blocks ----------
# block boundaries: \section{, \subsection{, \begin{figure}, \begin{table}
bounds = []
for i, l in enumerate(lines):
    if (l.startswith('\\section{') or l.startswith('\\subsection{')
            or l.startswith('\\begin{figure}')
            or l.startswith('\\begin{table}')):
        bounds.append(i)
bounds.append(len(lines))


def block_kind(i):
    l = lines[i]
    if l.startswith('\\section{'):
        return ('sec', re.match(r'\\section\{(.*)\}', l).group(1))
    if l.startswith('\\subsection{'):
        m = re.match(r'\\subsection\{(.*)\}', l)
        return ('sub', m.group(1) if m else l)
    if l.startswith('\\begin{figure}'):
        return ('fig', None)
    if l.startswith('\\begin{table}'):
        return ('tab', None)
    return ('txt', None)


def fig_no(block_lines):
    m = re.search(r'figs/fig(\d+)\.(png|jpg)',
                  '\n'.join(block_lines))
    return int(m.group(1)) if m else None


# group lines into blocks
blocks = []
for bi in range(len(bounds) - 1):
    s, e = bounds[bi], bounds[bi + 1]
    blocks.append((block_kind(s), lines[s:e]))

main, suppl = [], []
suppl_S1, suppl_S2 = [], []
moved_sub_idx = set()
def norm(t):
    t = re.sub(r'\$_{[^}]*}\$', '', t)
    t = re.sub(r'\$[^$]*\$', '', t)
    return t


for bi, ((kind, title), blines) in enumerate(blocks):
    if kind == 'sub':
        nt = norm(title or '')
        hit = None
        for m in MOVE:
            key = m[0]
            if key in ('Effect of TiO2',):
                if 'TiO' in nt and 'interfacial' in nt:
                    hit = m
            elif key in ('Effect of RbGeI3/CuI interfacial',):
                if 'CuI' in nt and 'interfacial' in nt:
                    hit = m
            elif key in ('Effect of TiO2 ETL thickness',):
                if 'ETL thickness' in nt:
                    hit = m
            elif key in nt:
                hit = m
            if hit:
                break
        if hit:
            moved_sub_idx.add(bi)
            chunk = [l for l in blines]
            # retitle handled at emission
            (suppl_S1 if hit[1] == 'S1' else suppl_S2).append((hit, chunk))
            continue
    if kind == 'fig':
        fn = fig_no(blines)
        if fn in MOVED_FIGS:
            # stash figure for its subsection
            for container in (suppl_S1, suppl_S2):
                for si, (hit, Chunk) in enumerate(container):
                    if hit[2] == fn:
                        container[si] = (hit, Chunk + [''] + blines)
                        break
            continue
    main.append((kind, title, blines) if kind in ('sec', 'sub')
                else (kind, None, blines))

# ---------- build summary subsection, replace old V.B position ----------
SUMMARY = r'''\subsection{Optimization summary}
Eleven parameters were optimized one at a time on the screened
FTO/TiO$_{2}$/RbGeI$_{3}$/CuI/\allowbreak{}Au stack (absorber thickness, bulk
and interface defect densities, dielectric constant, electron affinity,
bandgap, transport-layer thicknesses, conduction- and valence-band densities
of states); each optimum was carried forward, giving the consolidated set in
Table VII. Full per-parameter traces (Figs.\ S1--S10) are given in
Supplementary Section~S1, and the illumination and dark characteristics
(Figs.\ S11--S12) in Section~S2. The defect-density step itself is retained
below (Section~V.C) together with its energy/asymmetry extension, since
Ge-related degradation is central to this work.'''

# insert summary where old V.B subsection was: find kept V.B? V.B header was
# moved (thickness) — insert summary right before V.C block in main.
out_main = []
inserted = False
for kind, title, blines in main:
    if (not inserted and kind == 'sub'
            and title.startswith('Effect of absorber defect density')):
        out_main.append(SUMMARY)
        inserted = True
    if kind == 'sub':
        m = re.match(r'([A-Z])\.\s*(.*)', title or '', re.DOTALL)
        if m and m.group(1) in RELETTER:
            newh = '\\subsection{%s. %s}' % (RELETTER[m.group(1)],
                                             m.group(2))
            bl2 = [''] + [l for l in blines]
            bl2[0] = newh
            out_main.append('\n'.join(bl2))
            continue
    out_main.append('\n'.join(blines))
main_text = '\n'.join(out_main)

# fix in-text Section refs + figure numbers in main
main_text = fix_sections(main_text)


def apply_figmap(text):
    # single-pass longest-first: no cascade chains (26->14->4->3)
    keys = '|'.join(str(k) for k in sorted(FIGMAP, reverse=True))
    def rep(m):
        return '%s%d' % (m.group(1), FIGMAP[int(m.group(2))])
    text = re.sub(r'(Figs?\.?\s*)(%s)\b' % keys, rep, text)
    text = re.sub(r'(Figure\s*)(%s)\b' % keys, rep, text)
    return text


# explicit range/pointer rewrites FIRST (they name moved figures)
main_text = main_text.replace(
    'reported in Figs. 3--13',
    'reported in Supplementary Figs.~S1--S10')
main_text = main_text.replace(
    '(Figs. 7 and 10)', '(Supplementary Figs.~S4 and S7)')
main_text = apply_figmap(main_text)
main_text = main_text.replace('FAPbI3', 'FAPbI$_{3}$')
# restore head (preamble/frontmatter/abstract/keywords) dropped by splitter
head = '\n'.join(lines[:bounds[0]])
head = head.replace(
    r'\setlength{\emergencystretch}{2em}',
    r'''\setlength{\emergencystretch}{2em}
\renewcommand{\thesection}{\Roman{section}}
\renewcommand{\thesubsection}{\thesection.\Alph{subsection}}
\renewcommand{\thetable}{\Roman{table}}''')
main_text = head + '\n' + main_text
open(TEX, 'w').write(main_text)
print('main written:', len(main_text.split()), 'words')

# ---------- supplement ----------
S = [r'''\documentclass[11pt]{article}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{amsmath,amssymb,graphicx,url,tabularx,booktabs}
\usepackage[margin=1in]{geometry}
\renewcommand{\thefigure}{S\arabic{figure}}
\title{Supplementary Material for ``Photovoltaic Performance Analysis of RbGeI3 Absorber Based Perovskite Solar Cell using SCAPS-1D Simulation''}
\author{Md.\ Abdul Malek Fahim and Hussain Touhid Siddiquee}
\begin{document}
\maketitle
''']
S.append(r'''\section*{S1.\ One-at-a-time sweep details}
Full per-parameter traces for the eleven sequential optimization steps summarized in Section~V.B of the main text.''')


def emit_suppl(container):
    for hit, Chunk in container:
        # Chunk[0] is the old \subsection header line; retitle plainly
        body = []
        for l in Chunk:
            if l.startswith('\\subsection{'):
                m = re.match(r'\\subsection\{(.*)\}\s*$', l)
                inner = m.group(1) if m else l
                inner = re.sub(r'^[A-Z]\.\s*', '', inner)
                body.append('\\subsection*{%s}' % inner)
            elif l.startswith('\\begin{figure}'):
                body.append(l)
            elif l.startswith('\\includegraphics'):
                body.append(l)
            elif l.startswith('\\caption{'):
                body.append(l)
            elif l.startswith('\\end{figure}'):
                body.append(l)
            else:
                body.append(l)
        S.append(renumber_figs_S('\n'.join(body)))


supp_text_fixups = [
    ('(Section V.G)', '(Supplementary Section S1.5)'),
    ('(Section V.F)', '(Supplementary Section S1.4)'),
    ('spectrum of Section V.M', 'spectrum of Section V.D of the main text'),
    ('Sections V.P and VII.A', 'Sections V.G and VII.A of the main text'),
]
emit_suppl(suppl_S1)
S.append(r'''\section*{S2.\ Illumination and dark characteristics}''')
emit_suppl(suppl_S2)
# bibliography subset for cited refs
full = open('solar_submission/manuscript_full.tex').read()
bibus = dict(re.findall(r'\\bibitem\{(r\d+)\}(.*)', full))
rawkeys = re.findall(r'\\cite\{([^}]*)\}', '\n'.join(S))
cited = sorted({k.strip() for grp in rawkeys for k in grp.split(',')},
               key=lambda x: int(x[1:]))
S.append(r'\begin{thebibliography}{99}')
for key in cited:
    for k in key.split(','):
        k = k.strip()
        if k in bibus:
            S.append('\\bibitem{%s}%s' % (k, bibus[k]))
S.append(r'\end{thebibliography}')
S.append(r'\end{document}')
supp = '\n'.join(S)
for a, b in supp_text_fixups:
    supp = supp.replace(a, b)
open('solar_submission/supplement.tex', 'w').write(supp)
print('supplement written')
print('moved subsections:', len(suppl_S1) + len(suppl_S2))
