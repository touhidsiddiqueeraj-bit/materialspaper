#!/usr/bin/env python3
"""mk_latex — Round5 docx -> solar_submission/manuscript.tex (elsarticle)."""
import docx, re, os, shutil, hashlib, zipfile
from collections import Counter

DOCX = 'paper/round5/RbGeI3_Round5.docx'
OUT = 'solar_submission'
FIGD = os.path.join(OUT, 'figs')
os.makedirs(FIGD, exist_ok=True)
d = docx.Document(DOCX)
W = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'

SUPMAP = {'⁰': '0', '¹': '1', '²': '2', '³': '3', '⁴': '4', '⁵': '5',
          '⁶': '6', '⁷': '7', '⁸': '8', '⁹': '9', '⁻': '-', '⁺': '+'}
SUBMAP = {'₂': '2', '₃': '3'}


def protect_carets(t):
    t = re.sub(r'(\d)x10\^(-?[\d.]+)', r'$\1\\times10^{\2}$', t)
    t = re.sub(r'10\^(-?[\d.]+)', r'$10^{\1}$', t)
    return t


def group_supsub(t):
    t = re.sub('([⁰¹²³⁴⁵⁶⁷⁸⁹⁻⁺]+)',
               lambda m: '$^{%s}$' % ''.join(SUPMAP[c] for c in m.group(1)),
               t)
    t = re.sub('([₂₃]+)',
               lambda m: '$_{%s}$' % ''.join(SUBMAP[c] for c in m.group(1)),
               t)
    return t


FORMULAS = [
    (r'\bVOC\b', r'V$_{\mathrm{OC}}$'),
    (r'\bJSC\b', r'J$_{\mathrm{SC}}$'),
    (r'\bdVOC\b', r'dV$_{\mathrm{OC}}$'),
    (r'\bNC\b', r'N$_{\mathrm{C}}$'),
    (r'\bNV\b', r'N$_{\mathrm{V}}$'),
    (r'\bND\b', r'$N_{\mathrm{D}}$'),
    (r'\bNa\b', r'$N_{\mathrm{A}}$'),
    (r'\bNA\b', r'$N_{\mathrm{A}}$'),
    (r'\bNt\b', r'$N_{\mathrm{t}}$'),
    (r'\bEt\b', r'$E_{\mathrm{t}}$'),
    (r'\bEg\b', r'$E_{\mathrm{g}}$'),
    (r'\bEa\b', r'$E_{\mathrm{a}}$'),
    (r'\bVbi\b', r'$V_{\mathrm{bi}}$'),
    (r'\bRs\b', r'$R_{\mathrm{s}}$'),
    (r'\bRsh\b', r'$R_{\mathrm{sh}}$'),
    (r'\bJn\b', r'$J_{\mathrm{n}}$'),
    (r'\bEc\b', r'$E_{\mathrm{c}}$'),
    (r'\bEv\b', r'$E_{\mathrm{v}}$'),
    (r'\bJp\b', r'$J_{\mathrm{p}}$'),
    (r'\bFn\b', r'$F_{\mathrm{n}}$'),
    (r'\bFp\b', r'$F_{\mathrm{p}}$'),
    (r'\bmun\b', r'$\mu_{\mathrm{n}}$'),
    (r'\bmup\b', r'$\mu_{\mathrm{p}}$'),
    (r'\bmu\b', r'$\mu$'),
    (r'sigma_([np])', 'SIGMA'),
    (r'RbGeI3', r'RbGeI$_{3}$'),
    (r'CsGeI3', r'CsGeI$_{3}$'),
    (r'MAPbI3', r'MAPbI$_{3}$'),
    (r'MASnI3', r'MASnI$_{3}$'),
    (r'MASnBr3', r'MASnBr$_{3}$'),
    (r'CsSnI3', r'CsSnI$_{3}$'),
    (r'MAGeI3', r'MAGeI$_{3}$'),
    (r'FAPbI3', r'FAPbI$_{3}$'),
    (r'FAGeI3', r'FAGeI$_{3}$'),
    (r'CsGeX3', r'CsGeX$_{3}$'),
    (r'RbGeX3', r'RbGeX$_{3}$'),
    (r'ABX3', r'ABX$_{3}$'),
    (r'TiO2', r'TiO$_{2}$'),
    (r'SnO2', r'SnO$_{2}$'),
    (r'C60', r'C$_{60}$'),
    (r'Ge2\+', r'Ge$^{2+}$'),
    (r'Ge4\+', r'Ge$^{4+}$'),
    (r'Sn2\+', r'Sn$^{2+}$'),
    (r'Sn4\+', r'Sn$^{4+}$'),
    (r'Pb2\+', r'Pb$^{2+}$'),
    (r'ΔE([cv])', 'DELTAE'),
]


def conv_text(t, cites=True):
    """Plain-text -> LaTeX (no bold/italic)."""
    t = t.replace('_', r'\_')
    t = re.sub(r'sigma\\_([np])',
               lambda m: '$\\sigma_{%s}$' % m.group(1), t)
    t = re.sub(r'\$([^$]+)\$\s*x\s*\$([^$]+)\$',
               lambda m: '$%s\\times%s$' % (m.group(1), m.group(2)), t)
    t = protect_carets(t)
    t = t.replace('√(hν − Eg)', r'$\sqrt{h\nu-E_{\mathrm{g}}}$')
    t = group_supsub(t)
    for pat, rep in FORMULAS:
        if rep == 'SIGMA':
            continue  # handled above (pre-escape)
        elif rep == 'DELTAE':
            t = re.sub(pat,
                       lambda m: '$\\Delta E_{\\mathrm{%s}}$' % m.group(1),
                       t)
        else:
            t = re.sub(pat, lambda m, r=rep: r, t)
    greek = {'Δ': r'$\Delta$', 'ε': r'$\epsilon$', 'ψ': r'$\psi$',
             'ρt': r'$\rho_{\mathrm{t}}$', 'ρ': r'$\\rho$',
             'χ': r'$\chi$', 'λ': r'$\lambda$', 'α': r'$\alpha$',
             'ν': r'$\nu$', 'µ': r'$\mu$', 'μ': r'$\mu$'}
    for k, v in greek.items():
        t = t.replace(k, v)
    t = t.replace('×', r'$\times$').replace('->', r'$\rightarrow$')
    t = t.replace('≈', r'$\approx$')
    t = t.replace('→', r'$\rightarrow$').replace('−', '$-$')
    t = t.replace('±', r'$\pm$').replace('∞', r'$\infty$')
    t = t.replace('≤', r'$\leq$').replace('°', r'$^{\circ}$')
    t = re.sub(r'\b(cm|m|nm)-(\d)\b', r'\1$^{-\2}$', t)
    t = t.replace('cm2/Vs', r'cm$^{2}$/Vs').replace('m2/Vs', r'm$^{2}$/Vs')
    t = t.replace('mA/cm2', r'mA/cm$^{2}$')
    t = t.replace('ohm.cm2', r'$\Omega\cdot$cm$^{2}$')
    t = re.sub(r'(FTO|ITO|PCBM|NiO|CuI|CBTS|Spiro-OMeTAD|PEDOT:PSS|'
               r'CsSn0\.5Ge0\.5I3|Au|Ag|Al|ZnO|TiO\$_{2}\$|RbGeI\$_{3}\$|'
               r'CsGeI\$_{3}\$|C\$_{60}\$|MASnI\$_{3}\$|CsSnI\$_{3}\$)/',
               r'\1/\\allowbreak{}', t)
    t = t.replace('–', '--').replace('“', '``').replace('”', "''")
    t = t.replace('’', "'").replace('★', '').replace('~', r'$\sim$')
    t = t.replace('&', r'\&').replace('%', r'\%')
    if cites:
        def rng(m):
            a, b = int(m.group(1)), int(m.group(2))
            return '\\cite{%s}' % ','.join('r%d' % i for i in range(a, b + 1))
        t = re.sub(r'\[(\d+)[–-](\d+)\]', rng, t)
        t = re.sub(r'\[(\d+(?:\s*,\s*\d+)*)\]',
                   lambda m: '\\cite{%s}' % ','.join(
                       'r%s' % x.strip()
                       for x in m.group(1).split(',')), t)
    return t


def conv_para(p):
    """docx paragraph -> LaTeX, preserving bold/italic runs."""
    # If no bold/italic, convert the joined text: formula tokens (TiO2,
    # RbGeI3, ...) are often split across subscript-styled runs, which
    # per-run conversion would miss (leaving raw tokens behind).
    if not any((r.bold or r.italic) and (r.text or '').strip()
               for r in p.runs):
        return conv_text(''.join(r.text or '' for r in p.runs))
    out = []
    for r in p.runs:
        t = conv_text(r.text or '')
        if not t.strip():
            out.append(t)
            continue
        if r.bold:
            t = r'\textbf{%s}' % t
        if r.italic:
            t = r'\textit{%s}' % t
        out.append(t)
    return ''.join(out)


def conv_cell(cell):
    return ' '.join(conv_para(p) for p in cell.paragraphs)


# ---------- image <-> caption association ----------
REL_EMBED = '{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed'
NS = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
body = d.element.body
els = list(body)
img_at = {}   # element index -> blip embed id
for i, e in enumerate(els):
    if e.tag.endswith('}p'):
        for b in e.findall('.//{http://schemas.openxmlformats.org/drawingml/2006/main}blip'):
            rid = b.get(REL_EMBED)
            if rid:
                img_at.setdefault(i, []).append(rid)
rels = d.part.rels
rid2bytes = {}
for r in rels.values():
    if 'image' in (r.reltype or ''):
        rid2bytes[r.rId] = r.target_part.blob
cap_at = {}   # element index -> figure number
for i, e in enumerate(els):
    if e.tag.endswith('}p'):
        m = re.match(r'Fig\. (\d+)\.\s*(.*)', ''.join(
            t.text or '' for t in e.findall(f'.//{W}t')),
            re.DOTALL)
        if m:
            cap_at[i] = (int(m.group(1)), m.group(2).strip())
paired = {}   # figno -> (img_indices, caption)
used = set()
for ci in sorted(cap_at):
    best, bd = None, 1e9
    for ii in img_at:
        if ii in used:
            continue
        dist = abs(ii - ci) + (0 if ii < ci else 0.5)
        if dist < bd:
            bd, best = dist, ii
    if best is not None:
        used.add(best)
        paired[cap_at[ci][0]] = (best, cap_at[ci][1])
print('paired figures:', sorted(paired))
# save images
for fn, (ii, cap) in sorted(paired.items()):
    rids = img_at[ii]
    blob = rid2bytes[rids[0]]
    ext = '.png' if blob[:4] == b'\x89PNG' else '.jpg'
    open(os.path.join(FIGD, 'fig%d%s' % (fn, ext)), 'wb').write(blob)
print('saved', len(paired), 'figures')

# ---------- emit ----------
L = []
L.append(r'''\documentclass[review]{elsarticle}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{amsmath,amssymb}
\usepackage{tabularx,booktabs}
\usepackage{url}
\usepackage{textcomp}
\usepackage{graphicx}
\usepackage{lineno}
\setlength{\emergencystretch}{2em}
\renewcommand{\thesection}{\Roman{section}}
\renewcommand{\thesubsection}{\thesection.\Alph{subsection}}
\renewcommand{\thetable}{\Roman{table}}
\journal{Solar Energy}
\begin{document}
\begin{frontmatter}
''')
title = conv_text(d.paragraphs[0].text.strip() + ': ' +
                  d.paragraphs[1].text.strip())
L.append(r'\title{%s}' % title)
L.append(r'''\author[lus]{Md.\ Abdul Malek Fahim\fnref{fn1}}
\author[lus]{Hussain Touhid Siddiquee\corref{cor1}\fnref{fn2}}
\address[lus]{Department of Electrical and Electronic Engineering, Leading University, Sylhet, Bangladesh}
\cortext[cor1]{Corresponding author.}
\fntext[fn1]{E-mail: mdabdulmalekfahim@gmail.com; fahim.eee@lus.ac.bd}
\fntext[fn2]{E-mail: touhidsiddiqueeraj@gmail.com}
\begin{abstract}''')
L.append(conv_para(d.paragraphs[7]))
L.append(r'''\end{abstract}
\begin{keyword}''')
kw = d.paragraphs[8].text
kw = re.sub(r'^Keywords:\s*', '', kw).rstrip('.')
L.append(conv_text(kw))
L.append(r'''\end{keyword}
\end{frontmatter}
''')

EQ = (r'''\begin{equation}\label{eq:poisson}
\frac{d}{dx}\left(\epsilon\frac{d\psi}{dx}\right) =
-q\left(p-n+N_{D}-N_{A}+\rho_{t}\right)
\end{equation}
\begin{equation}\label{eq:electron}
\frac{dJ_{n}}{dx} = q\,(R-G)
\end{equation}
\begin{equation}\label{eq:hole}
\frac{dJ_{p}}{dx} = q\,(G-R)
\end{equation}''')

skip_tables = set()
tbl_counter = [0]


def emit_table(tb):
    rows = [[conv_cell(c).strip() for c in r.cells] for r in tb.rows]
    n = len(rows[0])

    def numeric(col):
        for r in rows[1:]:
            s = re.sub(r'\$[^$]*\$', '0', r[col])
            s = re.sub(r'\\[a-zA-Z]+', '', s)
            if not re.fullmatch(r'[\d.\-+±–\s,×x/]*', s.strip()):
                return False
        return True

    spec = ''.join('c' if numeric(j) else 'X' for j in range(n))
    size = r'\footnotesize' if n >= 5 else r'\small'
    L.append(r'{%s\setlength{\tabcolsep}{3pt}' % size)
    if 'X' in spec:
        L.append(r'\begin{tabularx}{\textwidth}{%s}' % spec)
    else:
        L.append(r'\begin{tabular}{%s}' % spec)
    L.append(r'\hline')
    L.append(' \\\\\n'.join(' & '.join(r) for r in [rows[0]]))
    L.append(r'\\\hline')
    for r in rows[1:]:
        L.append(' & '.join(r) + r'\\')
    L.append(r'\hline')
    L.append(r'\end{tabular%s}' % ('x' if 'X' in spec else ''))
    L.append('}')


BARE_CAPTIONS = {
    8: ('Comparison of the proposed device with recently reported lead-free '
        'perovskite solar cells. All entries are SCAPS-1D simulation studies.'),
}


def nearest_table(from_idx):
    best, bd = None, 1e9
    for k, tb in enumerate(d.tables):
        if k in skip_tables:
            continue
        for j, e in enumerate(els):
            if e is tb._tbl:
                dist = abs(j - from_idx)
                if dist < bd:
                    bd, best = dist, k
    return best
for i, e in enumerate(els):
    if e.tag.endswith('}tbl'):
        for k, tb in enumerate(d.tables):
            if tb._tbl is e and k not in skip_tables and k in BARE_CAPTIONS:
                L.append('\n\\begin{table}[htbp]\n\\centering')
                emit_table(tb)
                skip_tables.add(k)
                L.append('\\caption{%s}\n\\end{table}' %
                         conv_text(BARE_CAPTIONS[k]))
        continue
    if not e.tag.endswith('}p'):
        continue
    from docx.text.paragraph import Paragraph
    p = Paragraph(e, d)
    txt = p.text.strip()
    if not txt:
        continue
    style = p.style.name if p.style is not None else 'Normal'
    if i < 9:
        continue  # front matter handled
    if txt.startswith('References'):
        break
    if style == 'Heading 1':
        t = re.sub(r'^[IVX]+\.\s*', '', txt)
        L.append('\n\\section{%s}' % conv_text(t))
        continue
    if style == 'Heading 2':
        t = re.sub(r'^[A-Z]\.\s*', '', txt)
        L.append('\n\\subsection{%s}' % conv_text(t))
        continue
    # Normal-style subsection headers added in R5 (U/V/W, VI.B, VII.A)
    if re.match(r'^[UVW]\.\s', txt) and len(txt) < 60 and 'Fig' not in txt:
        L.append('\n\\subsection{%s}' % conv_text(txt))
        continue
    if txt.startswith('B. A-site cation influence'):
        L.append('\n\\subsection{%s}' %
                 conv_text('A-site cation influence: RbGeI3 versus CsGeI3'))
        L.append(conv_para(p))
        continue
    if txt.startswith('A. Limitations of the present study'):
        L.append('\n\\subsection{Limitations of the present study}')
        L.append(conv_para(p))
        continue
    m = re.match(r'(Table (X|IX|VIII|VII|VI|V|IV|III|II|I))\.\s*(.*)', txt,
                 re.DOTALL)
    if m and len(txt) < 400:
        k = nearest_table(i)
        if k is None:
            L.append(conv_para(p))
            continue
        L.append('\n\\begin{table}[htbp]\n\\centering')
        emit_table(d.tables[k])
        skip_tables.add(k)
        cap = conv_text(m.group(3))
        L.append('\\caption{%s}\n\\end{table}' % cap)
        continue
    m2 = re.match(r'Fig\. (\d+)\.\s*(.*)', txt, re.DOTALL)
    if m2 and int(m2.group(1)) in paired:
        fn = int(m2.group(1))
        ext = '.png'
        if not os.path.exists(os.path.join(FIGD, 'fig%d%s' % (fn, ext))):
            ext = '.jpg'
        L.append('\n\\begin{figure}[htbp]\n\\centering')
        L.append('\\includegraphics[width=0.85\\linewidth]{figs/fig%d%s}' %
                 (fn, ext))
        L.append('\\caption{%s}\n\\end{figure}' % conv_text(m2.group(2)))
        continue
    if 'summarized below; further details' in txt:
        L.append(conv_para(p))
        L.append(EQ)
        continue
    L.append(conv_para(p))

# ---------- references ----------
L.append('\n\\begin{thebibliography}{99}')
for p in d.paragraphs:
    t = p.text.strip()
    m = re.match(r'\[(\d+)\]\s*(.*)', t, re.DOTALL)
    if m:
        ref = conv_text(m.group(2), cites=False)
        ref = re.sub(r'(doi:\s*)(\S+)', r'\1\\url{\2}', ref)
        ref = re.sub(r'(https?://\S+)', r'\\url{\1}', ref)
        L.append('\\bibitem{r%s} %s' % (m.group(1), ref))
L.append('\\end{thebibliography}\n\\end{document}')

open(os.path.join(OUT, 'manuscript.tex'), 'w').write('\n'.join(L))
print('wrote manuscript.tex (%d lines)' % len(L))
print('tables emitted:', len(skip_tables), '/', len(d.tables))
