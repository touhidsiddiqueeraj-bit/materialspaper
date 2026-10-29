# Review fix ledger — major-revision response (built Oct 2026)
Reviewer verdict: major revision. Builder verdicts: ACCEPT (fix), PARTIAL (fix subset),
REBUT (disagree with evidence), STALE (targets older version).

## Major concerns
1. Ideal results at/above DB limit; low NC/NV drives it — ACCEPT.
   Rebase absorber NC/NV 1e17→1e18 (literature-standard), keep K_rad=1e-10 and
   REPORT radiative J0 vs DB explicitly, SQ limits beside every ideal number,
   "mathematical maximum"→"best found (62 evals)". Table IV paradox resolved
   by re-optimizing on rebased deck (Phase 1). GA genes audited
   (ga_results.json: eg 1.33, Nt 1e12/cm3, NV 2.6e16/cm3 — as reviewer said).
2. Junction baseline (Vbi/W/Mott-Schottky) — ACCEPT with attempt.
   GUI C-V attempt first (user decision); drop to lifetime/diffusion-only on failure.
3. Provenance (deck versions, QE, edge optima, OAT audit) — ACCEPT.
   Frozen-deck full OAT re-run + QE from same deck + extended edge sweeps +
   main-text per-step table (Phase 1). 10 nm TiO2 kept with pinhole caveat.
4. Three window definitions + tolerance contradictions — ACCEPT.
   One stacked definition, tolerances recomputed on stacked point, Rsh sentence
   from r6_rsh.json data (exists, unreported), TRPL-1e17 tension stated.
5. Oxidation fab spec as re-expression — PARTIAL.
   Verified: NA 1e16 costs only 0.35pp (r5_na.json) → "collapse" language GOES.
   Keep Ef→Nt quantitative core; separate V_Ge doping vs Cs_I recombination
   roles; exposure bands marked illustrative; Ef not lab-settable stated.
6. UQ/SHAP inconsistency — ACCEPT.
   Verified: code samples Eg/Nt/NC/NV/mu_n/mu_p/Nint1-2 (uq_and_dark_results.json
   N=200), NOT thickness/eps as text claims. Rewrite V.H to code. ML numbers
   check out (factorial n=193 →127 failed ✓; 80/20 held-out ✓; R² 0.9999 test /
   0.68 test). Disclose all; soften range-dependent claims; no Sobol (disclose why).
7. Validation/database overstated — PARTIAL.
   Strengthen methodology-vs-material caveat, date-stamp DB; results stand
   (fits within 1.5% on both devices are solver+pipeline evidence as claimed).
8. BSF mechanism + Cs confound — ACCEPT.
   Band/recombination-profile diagnostics decide reflection vs cliff-removal;
   Cu2O feasibility paragraph; Eg/χ confound admitted; SHAP Eg-dominance hedged.

## Specific errors (all ACCEPT unless noted)
- Fig.13 "beat" reversal — fix caption+body. Eq.(5) phantom — renumber PCE eq.
- CsSnI3 26.40→26.38 (table value rules). dPCE/dT −0.0304 — STALE (absent from
  current text; only −0.0302 present; note in response).
- Ea=1.46>Eg=1.4 — add extrapolation-artifact caveat (T-dependent NC/NV).
- D4 lowest PCE — soften to selection rationale with CuI refs (already cited).
- BSF 30.35 = Sb2S3 30.35 — verified independent (r6_bsf_sweep.json 12/12 vs
  Rahman stack); state coincidence explicitly.
- Refs: r10 DOI→10.1126; r6 authors; r15/r16 re-cited (thermal-stability claim
  keeps r14 only); [43]-[46]→ expand stubs; [23] preprint hedged.
- Abstract de-numbering; audit-log → reproducibility appendix; I.D rewrite.

## Presentation
- Title/abstract trim; split declined (user: single revision).
- Fix order per reviewer with Phase 1→6 dependency chain (see todos).
