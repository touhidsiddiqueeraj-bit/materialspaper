# Solar Energy submission package — RbGeI3 SCAPS-1D study

## Journal facts (verified 2026-09-27)

- **Solar Energy** (Elsevier, ISSN 0038-092X), official journal of ISES.
  IF 7.9, CiteScore 13.0. Submission via Editorial Manager.
- **Regular Papers: 4000–6000 words** (excl. captions + references).
- **LaTeX: standard `elsarticle` class** (`\documentclass[review]` used here —
  single column + line numbers for referees). No strict reference format at
  submission (numbered `\bibitem` list included inline).
- Figures: 300 dpi minimum (all PNGs here are 300 dpi); editable source
  (`manuscript.tex`) + PDF both included, as required for production.

## Contents

| File | Role |
|---|---|
| `manuscript.tex` | Editable source (elsarticle, review mode) |
| `manuscript.pdf` | Review PDF (36 pp, compiled with pdfLaTeX, no errors) |
| `supplement.tex` / `supplement.pdf` | Supplementary material S1–S3 (11 pp) |
| `titlepage.tex` / `titlepage.pdf` | Standalone title page upload (authors, affiliation, contact, counts) |
| `figs/fig1.png` … `fig31.png` | All 31 figures, 300 dpi |
| `highlights.txt` | 5 highlights, ≤85 chars each |
| `cover_letter.txt` | Draft cover letter |
| `README.md` | This file |

Build: `python3 ../mk_latex.py` (repo root) regenerates `manuscript.tex`
from `paper/round5/RbGeI3_Round5.docx`; compile with
`pdflatex manuscript.tex` twice.

## Status after independent judge review (2026-09-27) — all fixable items fixed

Judge verdict was NEEDS-FIX; the following were corrected, recompiled
(main exit 0, 36 pp; supplement exit 0, 11 pp; no errors/undefined refs):

1. **FF-peak sentence** now 331 K / 80.17% (was stale 340 K / 80.27%),
   dPCE/dT −0.0302 %/K; verified against `r5_temp.json`.
2. **pp-deltas** corrected: 0.40 (Loumachi), 0.34 (Pathak), 8.21 (Raj).
3. **Title-page emails**: explicit `fntext` footnotes — Hussain Touhid
   Siddiquee (second author) is corresponding author; Fahim (first author)
   holds both his mails. Mirrored in docx, supplement (`\thanks`), title
   page, and cover letter sign-off.
4. **Funding / declaration** (author-confirmed): no funding received; no
   competing interests — finalized on the title page.
4. **Abstract trimmed 325 → 199 words** (all claims preserved).
5. **Keywords trimmed 9 → 6.**
6. **Author order**: Md. Abdul Malek Fahim first, Hussain Touhid Siddiquee
   second (docx + tex + cover letter + supplement).

## Word-count compliance (the big one) — DONE via supplement split

Solar Energy's guide **explicitly accepts supplementary files** ("Electronic
Annexes ... published online alongside the article on ScienceDirect").
Split executed (`slim.py`, `slim2.py`):

- **Supplement** (`supplement.tex/.pdf`, 11 pp): S1 = ten OAT sweep details
  (Figs. S1–S10), S2 = illumination + dark characteristics (Figs. S11–S12),
  S3 = screening/setup tables (Tables S1–S4), with its own mini-bibliography.
- **Main**: 19 figures (auto-numbered 1–19), 6 tables (auto-numbered I–VI in
  Roman, matching in-text refs), full hierarchy V.A–V.L → VI.A–VI.B →
  VII.A–VII.B verified in reading order in the PDF.
- **Count (strict reading, tables included, captions/refs excluded): ~5,940
  words** — inside the 4,000–6,000 guide. Prose-only ~5,250.
- Prose condensation (`trim.py`, claims preserved): materials rationale,
  band diagram, benchmarking, lit review, contributions, gap, QE, future
  work, conclusion, defect, GA gene-decode + five micro-cuts.

## Build pipeline (all scripted, rerunnable)

`mk_latex.py` (docx→tex) → `slim.py` (main/supplement split, reletter,
renumber) → `slim2.py` (Tables I–IV→S1–S4, title fixes) → `trim.py`
(condensation) → small hand-fixes → `pdflatex ×2` each file.
`manuscript_full.tex` = pre-slim backup. The docx remains the full-record
master (42 pp); the tex pair is the submission master.

## ⚠️ Residual notes

1. Graphical abstract not included (optional but encouraged).
2. 12 minor overfull lines in main (cosmetic only).
3. Rs-combined derating steps are first-order estimates (flagged in Fig. 19
   caption — formerly Fig. 31).
4. Section/figure/table numbers in the PDF are LaTeX-auto (Roman sections,
   V.A–V.L, VI.A–VI.B) and were verified to match every in-text reference.
