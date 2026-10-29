# Novelty memo — answering the Solar Energy desk-reject

**Reject text:** "presents largely well-established methods and lacks sufficient
novelty relative to existing literature."

## What was already in the rejected manuscript (kept, not re-claimed)
OAT-11 optimization, GA joint optimum, LHS-UQ N=200, Et/sigma asymmetry, NA/Rs/mu
sweeps, Ea diagnostic, same-stack CsGeI3 mirror. These stay as background.

## What is new in this submission (all executed, all in r5_results/)
| # | Claim | Evidence file | Runs |
|---|---|---|---|
| N1 | Cu2O-like p+ BSF on this exact stack: 26.79→30.35% ideal; NA dominates, thickness flat | r6_bsf_sweep.json (12/12 + refill) | 13 |
| N2 | BSF under full realism (bulk+if 1e15 @0.9-sun): 20.80→23.29% (+2.49pp, like-for-like) | r6_realistic_waterfall.json R5full (gen: r6_fix2.py) | 1 |
| N3 | Native radiative bound: K=1e-16 → -0.02pp; K=1e-14 → -1.15pp | r6_loss.json | 4 |
| N4 | Auger null at 1-sun (1e-41..1e-39 → ±0.00pp) | r6_loss.json | 4 |
| N5 | Reflection by native photon scaling: -2.71pp; bulk -1.74; interface -1.54 → 20.80% | r6_realistic_waterfall.json R1-R4 (+src tags) | 4 |
| N6 | Rsh target ≥1e3 Ω·cm² (JV-derived); Rs ≥20% to 8 Ω·cm² | r6_rsh.json, r5_rs.json | analytic+archived |
| N7 | XGB surrogate R² 0.9999 (factorial) + SHAP ranking Eg>interface>mu_n | r6_ml.json | 0 new (reuse 520) |
| N8 | Junction baseline Vbi 1.457V, W 171nm, tau 1000ns, L 8.6um + MS/G-R figs | r6_junction.json, r6_GR.npz | analytic |
| N9 | All Jsc below SQ@1.4eV; arithmetic gate on every reported node | all r6 JSONs | — |

## Honesty log (disclosed in manuscript Methods)
- Tfront def-edit ignored under scripting → reflection via 0.9-sun photon scaling.
- `save results.cv` header-only (3 probes) → analytical junction baseline.
- Sub-1-sun SCAPS eta is self-normalized → PCE_1sun recomputed explicitly.
- BSF defs branch from K=0 base (bounded -0.02pp inconsistency).
- UQ-surrogate R² is 0.68 (flat landscape); the 0.9999 is the factorial block
  (320 simulated, 193 valid rows) — both reported; SHAP comes from the UQ model.
- r6_loss.json K15 FAILED node replaced by guarded rerun r6_fix2.py (F1: 26.62).
- R5 (bulk-only) superseded by R5full (bulk+interfaces, like-for-like vs R4).
- All run-scripts now import-safe (`if __name__ == '__main__'` guards verified):
  r6_loss.py, r6_loss_fix.py, r6_real.py, r6_bsf_sweep.py, r6_fix2.py, r6_rsh.py,
  r6_ml.py, r6_junction.py, r6_figures.py (repo root, run, not git-staged —
  no commit without author request).
  The waterfall JSON (r6_realistic_waterfall.json) is FAILED-free. Retained
  annotated FAILED nodes (transient xvfb crashes, rerun elsewhere): r6_loss.json
  K16-single (superseded by K16c in r6_loss_fix.json). All reported numbers come
  from converged nodes only.

## Provenance
Scripts (repo root): r6_loss.py, r6_loss_fix.py, r6_real.py, r6_bsf.py,
r6_bsf_sweep.py, r6_ml.py, r6_junction.py, r6_figures.py, r6_fix2.py, r6_rsh.py.
Figures: r5_results/fig_r6_*.png (300 dpi).
Manuscript: optical_submission/manuscript.tex → manuscript.pdf (12 pp, pdflatex clean, 10 labeled figs).
