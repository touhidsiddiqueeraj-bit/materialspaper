# Round-5 Report — Defect/Manufacturing Sweeps + Full CsGeI3 Mirror

Paper: `paper/round5/RbGeI3_Round5.docx/.pdf` (42 pp) from
`paper/round3/RbGeI3_Round4.docx` (35 pp). Backups in `backups_round5/`.

## Frozen baseline (all sweeps branch from this def)

`r5_baseline.def` = `perovskite-rbgei3.def` unchanged, 300 K / 1 sun:
**PCE 26.81% | Voc 1.1298 V | Jsc 30.3156 | FF 78.26%**
Headline: 26.81% / 1.13 V / 30.32 / 78.26.

## Harness fix (mid-campaign, load-bearing)

SCAPS workers share one `pythonresult.txt` per prefix; xvfb crashes (~15%)
left stale files that parsed as good data (caught: round-4 1.5-sun values
under 1-sun inputs). Fixed in `~/scaps-runner/.../runner.py` (unique
`pythonresult_<id>.txt` per input, pre-deleted) + `r5_lib.py`
(missing-file → FAILED; `Voc*Jsc*FF/100 = eta ± 0.6` arithmetic gate).
All tainted JSONs deleted and rerun; final JSONs are FAILED-free and
100% arithmetically consistent. Cross-validation: independent reruns
reproduce to 4 decimals (Cs ETL90 23.12/FF 88.26 twice; Cs ifC16 23.02 twice).

## Results (all hyperlinks = r5_results/*.json)

| Sweep | File | Headline |
|---|---|---|
| Baseline JV | r5_baseline.json | 26.81 / 1.1298 / 30.3156 / 78.26 |
| Et @Nt1e14 (flat 26.81-26.85) + @Nt1e21 U-curve 25.01→24.84→25.01; sigma 3x3 (21.45-27.23) | r5_et_sigma.json | mid-gap most lethal; e-trap 23.97 vs h-trap 26.71 at fixed product |
| NA 1e14→1e17 | r5_na.json | peak 26.82 @3e14; ≤0.1pp cost to 1e15; Jsc collapse past 1e16 |
| Rs 0→10 (external V−J·Rs) | r5_rs.json (+r5_rs.py) | ≥20% to Rs=8; ≥22% to Rs=6; FF 78.26→56.82 |
| mu 1→100 + 2D + 400nm | r5_mobility.json | 22.58→28.52 log-linear; e-mobility dominates; 700nm holds |
| T 280→400 | r5_temp.json | Ea=1.46eV≈Eg (bulk-limited); dVoc/dT=−1.10mV/K |
| CsGeI3 11-fam OAT (71/71) | r5_csgei3_oat.json | Eg1.4 control = 26.81 exact (isolation proven) |
| Cs final/Nt21/Nt22/etl90/ifC16 | r5_csfinal.json | 19.66 / 19.36 / 17.28; outliers confirmed by rerun |

Cs vs Rb: Voc +0.04 (Cs), Jsc +7.1 / FF +5.6 (Rb). VBO cliff 0.10 (Rb)
vs 0.30 eV (Cs) → CuI uniquely synergistic with RbGeI3.

## Paper deltas (all scripted in r5_assemble.py)

26.80→26.81 (14), 78.92→78.26 (7), 1.12V→1.13V (6), formula fixed;
V.C Et/sigma ext; new V.U/V.V/V.W; V.T Ea; VI.B + Table X; VII.A ladder;
conclusion; Figs 24–31; Table X subscripted; 42 pp, captions paired
(text audit; polaris/gemini vision backends down).
Physics note: σ·Nt product equivalence verified in-data
(sn1e17_sp1e17 ≡ r4_nt16 = 21.45%) — used (documented) for Rb Nt16 row.
Rs-combined ladder steps are first-order (flagged with * in Fig. 31).
