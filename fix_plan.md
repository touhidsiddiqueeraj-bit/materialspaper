# Bandgap/Jsc Discrepancy — Correction Plan

## Root Cause (from data analysis)

1. **Table XI (bandgap sweep)** Jsc values at Eg=1.4 (27.42 mA/cm²) are inconsistent with the current `.def` file which produces Jsc≈30.32 at the same Eg. The sweep was run at a different point in the OAT sequence (Step 7) than the final device (after Steps 8–11).

2. **Thesis band diagram** says Eg=1.31 eV (the Table II initial value), contradicting Table 5.13 / Table XVI which state 1.4 eV. The final device simulation was run at the initial bandgap.

## Files to Create

### Modified .def files (from Final circuit.scaps via Python substitution)

| File | Changes from Final circuit.scaps |
|------|--------------------------------|
| `step7_params.def` | TiO₂ d=30nm, RbGeI₃ Nc=1.4e25/m³, Nv=2.8e25/m³ |
| `final_params.def` | None (copy of final) |
| `iso_D1.def` | Nc=1.4e25, Nv=2.8e25, TiO₂=30nm |
| `iso_D2.def` | Nc=1e23, Nv=1e23, TiO₂=10nm (final) |
| `iso_D3.def` | Nc=1.4e25, Nv=2.8e25, TiO₂=10nm |
| `iso_D4.def` | Nc=1e23, Nv=1e23, TiO₂=30nm |

### Sweeps (via scaps-runner)

| ID | Base def | Sweep | Values | Points |
|----|----------|-------|--------|--------|
| A-step7 | step7_params.def | Eg | 1.3, 1.35, 1.4, 1.45, 1.5, 1.6, 1.7 eV | 7 |
| B-final | final_params.def | Eg | 1.3, 1.35, 1.4, 1.45, 1.5, 1.6, 1.7 eV | 7 |
| C-eg131 | final_params.def | Eg | 1.31 eV | 1 |
| D-isolate | iso_D1–D4 | Eg=1.4 fixed | varied Nc/Nv/ETL | 4 |

### Output files (saved to `fix_results/`)

**Figures:**
- `fig_bandgap_sweep_corrected.png` — Jsc vs Eg: sweep A, sweep B, old Table XI, SQ limit
- `fig_jsc_diagnostic.png` — D1–D4 bar chart isolating the offset parameter
- `fig_pce_bandgap.png` — PCE vs Eg for sweeps A and B
- `fig_jv_final_device.png` — JV curves at Eg=1.31 vs Eg=1.4 with final params

**Tables:**
- `corrected_table_bandgap_sweep.md`
- `corrected_table_final_device.md`
- `diagnostic_table.md`

**Report:**
- `fix_report.md` — root cause summary + what to change in paper/thesis

## SQ Limit Check

SQ-limited Jsc at each Eg from the AM1.5G spectrum file, compared against both sweeps and old Table XI. Any Jsc > SQ limit = impossible (absorption model issue exposed).
