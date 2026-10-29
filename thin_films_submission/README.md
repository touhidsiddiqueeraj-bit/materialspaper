# Thin Solid Films submission package — RbGeI₃ thin-film device engineering

> Status: ready to upload via Editorial Manager (Elsevier).
> Manuscript: `manuscript.tex` (editable elsarticle source) + `manuscript.pdf`.
> Base: combined Solar Energy baseline (OAT-11, GA, UQ, tolerances, Cs mirror)
> + new BSF / loss-waterfall / junction-baseline / ML-surrogate experiments,
> reframed for a thin-film devices audience.

## Upload checklist (EM item → file)

| EM item | File |
|---|---|
| Manuscript (PDF + editable source) | `manuscript.pdf` + `manuscript.tex` (10 figs, 3 tables, 50 refs) |
| Supplement (PDF + source) | `supplement.pdf` + `supplement.tex` (S1 OAT traces, S2 illum/dark, S3 tables) |
| Figures, 300 dpi (embed or separate) | `figs/*.png` (10 main + 12 supplement) |
| Graphical abstract (required by TSF) | `graphical_abstract.png` (2850×1260 px, 300 dpi) |
| Highlights (3–5 bullets, ≤85 chars each) | `highlights.txt` |
| Cover letter | `cover_letter.txt` |
| Title page (author details, declarations) | `titlepage.tex` / `titlepage.pdf` |

## Why Thin Solid Films

- Scope fit: thin-film synthesis, characterization and modelling; every result
  is a thin-film layer/interface result (10 nm TiO₂, 700 nm absorber,
  100 nm CuI, 30–100 nm BSF, interface defect densities).
- The SCAPS-1D simulator itself was introduced in this journal (Burgelman
  et al., Thin Solid Films 361–362, 527–532 (2000)).
- Keywords (6): lead-free perovskite; RbGeI₃ thin film; back surface field;
  SCAPS-1D; defect engineering; SHAP sensitivity analysis.

## Headline numbers (judge-verified, 3 rounds)

| Point | PCE | Evidence |
|---|---|---|
| Reference ideal | 26.81% | `r5_results/r5_baseline.json` |
| BSF optimum ideal | 30.35% | `r5_results/r6_bsf_sweep.json` (12/12) |
| No-BSF realistic | 20.80% | `r5_results/r6_realistic_waterfall.json` R4 |
| BSF full-realism | 23.29% (+2.49pp) | same file, R5full (gen: `r6_fix2.py`) |
| ML surrogate | R² 0.9999 | `r5_results/r6_ml.json` |

## Rebuild

```bash
pdflatex manuscript.tex   # twice for references
pdflatex supplement.tex
pdflatex titlepage.tex
```

Provenance of every number: `optical_submission/NOVELTY_MEMO.md`.
SCAPS scripts: repo root `r6_*.py`. Data: `r5_results/r6_*.json`.

## Prior-submission disclosure

Related baseline material was desk-rejected at Solar Energy for insufficient
novelty; this manuscript rebuilds the contribution around the BSF variant,
loss budget, junction baseline and ML surrogate, as stated in the cover
letter. Do not submit here in parallel with any other journal.
