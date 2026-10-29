# Optical Materials submission package — BSF-enhanced RbGeI₃/CuI study

> Status: ready to upload via Editorial Manager (Elsevier).
> Manuscript: `manuscript.tex` (editable source, elsarticle) + `manuscript.pdf` (12 pp).

## Upload checklist (EM item → file)

| EM item | File |
|---|---|
| Manuscript (PDF + editable source) | `manuscript.pdf` + `manuscript.tex` (17 pp, 50 refs) |
| Supplement (PDF + source) | `supplement.pdf` + `supplement.tex` (9 pp: S1 OAT traces S1–S10, S2 illum/dark S11–S12, S3 tables S1–S4) |
| Figures, 300 dpi (embed or separate) | `figs/*.png` (22: 10 main + 12 supplement) + `graphical_abstract.png` |
| Highlights (≤85 chars each) | `highlights.txt` |
| Cover letter | `cover_letter.txt` |
| Graphical abstract (optional, encouraged) | `graphical_abstract.png` |
| Internal only (DO NOT upload) | `NOVELTY_MEMO.md` |

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
pdflatex manuscript.tex   # twice for references (none external — single pass is fine)
```

Provenance of every number: `NOVELTY_MEMO.md`. SCAPS scripts: repo root `r6_*.py`
(all import-safe). Data: `r5_results/r6_*.json`.
