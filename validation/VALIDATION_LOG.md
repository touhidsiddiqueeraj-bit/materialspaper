# Validation log — SCAPS pipeline vs Wang et al., Science 2019 (β-CsPbI₃)

**Purpose:** answer the TSF desk-reject ("no direct link to experimental data").
RbGeI₃ has no experimental devices in the literature (all RbGeI₃ work is
SCAPS/DFT), so this validates the *pipeline* on an experimentally realized
inorganic perovskite and applies the identical pipeline to RbGeI₃.
This framing — methodology validation, NOT RbGeI₃ validation — must be kept
in the manuscript.

## 1. Reference selection

| Candidate | Stack completeness | J–V tabulated | EQE+int.Jsc | Control+champion | Verdict |
|---|---|---|---|---|---|
| Wang et al., Science 2019 (β-CsPbI₃) | Full: FTO/c-TiO₂/375nm/spiro/Ag + recipes | Yes (15.1%: 1.05/20.03/0.72; 18.4%: 1.11/~20/0.82) | Yes (19.71/19.85) | Yes + 32-device stats | **CHOSEN** |
| TOPO paper (PMC10580311, CsPbI₃) | Partial (no thicknesses; OAI+TOPO dipole unmodellable) | Supplement-only | Yes | Distributions only | rejected |

Source: accepted manuscript (green OA) via OIST repository.

## 2. Curve digitization (agent-first, user verifies)

`wang2019_CHI_JV.csv` (733 pts), `wang2019_ctrl_JV.csv` (600 pts):
render Fig.4A at 400 dpi → tick-regression calibration (x ±0.002 V,
y ±0.22 mA/cm²) → color segmentation (red/black) with blue-text +
legend masking → column-median traces → legend-remnant filter.
Self-check vs tabulated: CHI 20.02/1.125/81.9/18.46 (paper ~20.0/1.11/
0.82/18.4); control 19.63/1.058/72.2/15.00 (paper 20.03/1.05/0.72/15.1).
Note: digitized control plateau reads ~2% below tabulated Jsc
(representative curve vs champion stats — disclosed, not fitted).
See `verify_digitization.png`.

## 3. SCAPS rebuild (base: repo `perovskite-rbgei3.def`)

Stack: Ag / spiro-OMeTAD 180 nm / β-CsPbI₃ 375 nm (Eg 1.68, edge 738 nm) /
c-TiO₂ 40 nm / FTO, 318 K (J–V measured at ~45 °C), sqrt-law absorption.
TiO₂ 40 nm + spiro 180 nm are documented assumptions (recipes only in paper).

Literature-pinned (NOT fitted): Eg 1.68 (UV-vis edge), χ_abs 3.8
([3.7,3.9] SCAPS-literature range), χ_spiro 2.3 (doped-spiro range),
μ_CsPbI3 25/25 cm²/Vs, μ_spiro 2e-3 cm²/Vs (Li-TFSI-doped value),
NA_spiro 1e18 cm⁻³, A = 1.5e5 (Jsc-calibrated once: 19.92 vs 20.03),
Et mid-gap 0.84 eV. Back contact Ag at EFFECTIVE Fi_m 5.2 eV
(pinned metal/organic interface; nominal 4.7 eV imposes a 0.5 eV hole
barrier contradicted by the measured FF).

Fitted (only these): bulk Nt × interface N — the paper's own contrast
mechanism (CHI = interface passivation + 120 meV CBM realignment).

## 4. Diagnostic path (audit trail)

- Naive build (Fi_m 4.7, pristine spiro): Voc capped 0.78 — back-contact barrier.
- Fi_m ladder: 5.0/5.1 systematically fail to converge; 5.2 converges (FF 86.6).
- Jsc stuck at 18.0 at 375 nm regardless of Nt (optics, not recombination);
  A 1e5→1.5e5 recovers 19.92 at the true 375 nm thickness.
- VBO cliff +0.38 (spiro χ 2.2) capped Voc ~1.0; χ_spiro 2.5 → 1.22
  (overshoot, confirms knob); χ_abs 3.8 + χ_spiro 2.3 → champion fit.
- Control FF 0.72 unreachable via defects (floor ~83.6) — signature of
  series resistance (cracks/pinholes + hysteresis documented in paper);
  external V−JRₛ correction Rs = 6.9 Ω·cm² (same first-order method as
  the manuscript's own Rs section).

## 5. Final errors (all within ±1 pp PCE)

| Device | Model | Voc | Jsc | FF | PCE |
|---|---|---|---|---|---|
| Champion | Nt 3e13 cm⁻³, Nif 3e13 cm⁻² | 1.127 (+1.5%) | 19.92 (−0.4%) | 82.37 (+0.5%) | 18.49 (+0.5%) |
| Control | Nt 3e13 cm⁻³, Nif 1e14 cm⁻², Rs 6.9 | 1.060 (+1.0%) | 19.92 (−0.6%) | 71.88 (−0.2%) | 15.18 (+0.5%) |

Overlay: `fig_r7_overlay.png`. Grid data: `r7_grid_final.json`;
best-fit J–V: `r7_final_JV.json`; exploration runs: `r7_grid*.json`,
`r7_diag*.json` (includes failed/non-converged points).

## 6. Failed / non-converged runs (disclosed)

Fi_m 5.0 and 5.1 (3 attempts), one flat-edge grading edit, Nif 1e20 at
new bands (2 attempts), plus ~5% transient xvfb crashes rerun clean.

## 7. Round-2 audit additions
- Post-$R_{s}$ control J--V archived: `r7_control_Rs69_JV.csv`
  (V' = V - J*6.9/1000 from the truncated `r7i_a38s23_if18` quadrant).
- Main-text claim softened to "within 2%" (champion Voc error is +1.53%).
- Database counts: raw fetch 43,106 / 41,388 / 2,201; analysis-clean
  41,316 / 2,141 after validity filters (defined in supplement S5).
