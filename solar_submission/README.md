# Solar Energy submission package — RbGeI3 SCAPS-1D study

> **Status (Oct 2026, referee-response revision): D2 like-for-like pipeline
> (28.16% adopted — gap survives, D4 kept on stability/cost); BSF mechanism
> corrected by controlled attribution (offset-removal dominates, field
> minority; 19.65/24.36/21.33 matrix); oxidation budget with anneal
> freeze-in bounds + 15.53% current-state rung; validation→calibration,
> NOMAD→frozen-context; QE section dropped; 25 figs after Fig.1/QE removal;
> findings-first voice; data-availability statement added.**

> **Status (Oct 2026): merged revision — thin-films novelties (BSF, loss
> waterfall, junction baseline, XGBoost/SHAP) backfilled into the Solar
> package; both prior submissions rejected, nothing under review elsewhere.**
> Title: *Defect-Tolerant Design of Lead-Free RbGeI₃ Solar Cells:
> Back-Surface-Field Enhancement, Realistic Loss Budgeting and SHAP
> Sensitivity From SCAPS-1D Optimization to Manufacturing Tolerances,
> Benchmarked Against CsGeI₃*.
>
> **Numbers (r8 frozen-deck rebase, current): H1 adopted 27.06%
> (1.0613 V, 30.3161 mA/cm², 84.11%); BSF optimum 28.01% (NA 1e19);
> GA best-found 28.30%; stacked window S3 20.78% (S4-BSF 21.76%);
> waterfall W1 24.28% / W2 21.93% (`r8_waterfall_JV.json`); UQ mean
> 24.86±1.77 (N=200); XGB R² 0.9074. Junction claims withdrawn to
> lifetime-only (1000 ns, 8.6 µm); scripted QE/C-V header-only limits
> disclosed; Ea 1.48 eV reported as artifact.**

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
| `manuscript.pdf` | Review PDF (44 pp, compiled with pdfLaTeX, no errors) |
| `supplement.tex` / `supplement.pdf` | Supplementary material S1–S7 (S4 = BSF/lifetime/ML notes; Tables S1–S6; S7 = reproducibility appendix) |
| `titlepage.tex` / `titlepage.pdf` | Standalone title page upload (authors, affiliation, contact, counts) |
| `figs/*.png` | 38 figures, 300 dpi (fig32–39 = BSF/waterfall/G-profile/parity/SHAP/validation/database/oxidation) |
| `graphical_abstract.png` | Graphical abstract (ported from thin-films package) |
| `highlights.txt` | 5 highlights, ≤85 chars each (BSF + waterfall + SHAP blended) |
| `cover_letter.txt` | Draft cover letter (with prior-rejection disclosure) |
| `README.md` | This file |

## Merge provenance (Oct 2026)

Backfilled from `thin_films_submission/`: BSF §, loss waterfall §,
lifetime-baseline §, XGBoost/SHAP §, honesty-protocol paragraph,
bibliography entries, graphical abstract. All solar-only depth kept:
OAT + tolerances, GA/UQ, CsGeI₃ mirror, methods prose.
`thin_films_submission/` left frozen.

**Superseded by the r8 frozen-deck rebase (same sections, new runs):**
BSF grid `r8_bsf.json` 12/12 via `r8_bsf.py` (opt 28.01%);
stacked waterfall S1/S2/S3/S4 + W1/W2 (`r8_stack.json`,
`r8_S3_JV.json`, `r8_s490_JV.json`, `r8_waterfall_JV.json`;
20.78% / 21.76% BSF); lifetime-only baseline (1000 ns, 8.6 µm;
Vbi/W/M-S withdrawn); ML `r8_ml.json` (XGB R² 0.9074, 8 feats).

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
- **Main (current)**: 25 figures, 8 tables (Arabic numerals).
Files `figs/fig32` (BSF), `fig34-36` (G-profile, parity, SHAP) render as
Figs. 18, 20-22; `fig37-39` (calibration overlay, database context, oxidation) render
as Figs. 23-25, referenced as such in text.
- **Word count (verified)**: ~5,714 strict (prose ~5,004 + tables ~710;
captions/refs excluded) — inside the 4,000–6,000 guide.
- **Oxidation-budget reframing (Oct 2026)**: retitled; new Section VI.I +
Fig. 27 (PCE vs V_Ge formation energy, `validation/r8_oxidation_fig.py`);
N_A subsection absorbed as oxidation corollary; 7 new DFT/experimental refs
(rMing, rThirumal, rZhang24, rZhangPRX, rPCCMAI, rGeDope, rKino);
supplement S6 derivation; case file `validation/oxidation_case.md`.
- **Dual-judge review, oxidation round (passed round 3)**: content
[9,9,9,9,8], visuals [9,9,9,9,9]. Fixed: supplement title/bib placement,
TRPL real citation (Jang et al., Commun. Mater. 7 (2026)), fig39 arrow
semantics + fonts, S5 margin overflow, supplement Samaki row (zero orphans
both files), Fig. 20–24 pointer corrections.
- **Independent dual-judge review (3 rounds max, passed round 3)**:
content [9,8,9,8,8], visuals [9,8,8,9,8] — scale 1–10 vs published
literature, 8+ pass on all 5 criteria each. Fixed: Table IV rounding
footnote, NOMAD raw-vs-clean counts, post-Rs control JV archive,
fig25 math labels, fig37/38 fonts + widths, Table VI width, full
rMA/rML40 citations, supplement S-table numbering, zero orphan refs.
- **Count (strict reading, tables included, captions/refs excluded): ~5,940
words** — inside the 4,000–6,000 guide. Prose-only ~5,250.
- **Experimental anchoring (Oct 2026, `validation/`)**: SCAPS rebuild of
Wang et al. Science 2019 β-CsPbI₃ (control 15.18 vs 15.10%, champion
18.49 vs 18.40%; `r7_validate.py`, overlay Fig. 37, error Table VII) +
NOMAD Perovskite-DB benchmark (41,316 one-sun entries; window tops 100%
of 2,141 inorganic; Fig. 38, supplement S5). Answers the TSF
desk-reject on experimental grounding.
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
