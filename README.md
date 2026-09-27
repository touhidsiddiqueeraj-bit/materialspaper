# RbGeI₃ Perovskite Solar Cell — SCAPS-1D Simulation

> **Status (Sep 2026): under review at *Solar Energy* (Elsevier) as a Regular Paper** —
> *Defect-Tolerant Design of Lead-Free RbGeI₃ Solar Cells: From SCAPS-1D Optimization
> to Manufacturing Tolerances, Benchmarked Against CsGeI₃*.
> Submission package: [`solar_submission/`](solar_submission/).

Numerical simulation and optimisation of a lead-free RbGeI₃ perovskite solar cell with an **FTO/TiO₂/RbGeI₃/CuI/Au** planar heterojunction architecture, carried out with SCAPS-1D (v3.3.10) under Wine. The optimised device reaches **26.81% PCE**.

## Final Device Results

| Parameter | Value |
|-----------|-------|
| PCE | 26.81% |
| V_OC | 1.13 V |
| J_SC | 30.32 mA/cm² |
| FF | 78.26% |
| Absorber thickness | 700 nm |
| Absorber bandgap | 1.4 eV |
| Absorber defect density | 1×10¹⁴ cm⁻³ |
| Electron affinity (RbGeI₃) | 3.9 eV |
| Dielectric constant | 15 |
| N_C / N_V | 1×10¹⁷ cm⁻³ |
| ETL (TiO₂) thickness | 10 nm |
| HTL (CuI) thickness | 100 nm |
| Interface N_t (both junctions) | 1×10¹⁴ cm⁻² |

**Layer stack**: FTO (500 nm) / TiO₂ (10 nm) / RbGeI₃ (700 nm) / CuI (100 nm) / Au, simulated under AM 1.5G, 100 mW/cm², 300 K.

## Repository Structure

```
├── solar_submission/               # Solar Energy (Elsevier) submission package
│   ├── manuscript.tex / .pdf       # Main paper, elsarticle review mode (36 pp)
│   ├── supplement.tex / .pdf       # Supplementary S1–S3 (11 pp)
│   ├── titlepage.tex / .pdf        # Standalone title page upload
│   ├── cover_letter.txt            # Draft cover letter (+ word count)
│   ├── highlights.txt              # 5 highlights (≤85 chars)
│   ├── figs/fig{1..31}.png         # All figures, 300 dpi
│   └── README.md                   # Journal facts + package checklist
├── paper/round5/
│   └── RbGeI3_Round5.docx / .pdf   # Full-record Word master (42 pp)
├── r5_results/                     # Round-5 simulation results (JSON + figures)
│   ├── r5_baseline.json            # Frozen headline device (26.81%)
│   ├── r5_et_sigma.json            # Defect energy + capture asymmetry
│   ├── r5_na.json                  # Background doping sweep
│   ├── r5_rs.json                  # Series-resistance tolerance map
│   ├── r5_mobility.json            # Mobility sweep (+ thin checks)
│   ├── r5_temp.json                # Temperature sweep (Ea extraction)
│   ├── r5_csgei3_oat.json          # Full 11-family CsGeI3 mirror (71 runs)
│   ├── r5_csfinal.json             # Consolidated CsGeI3 + derating
│   └── R5_REPORT.md                # Full provenance + harness-fix notes
├── r5_*.py, mk_latex.py,           # Reproducibility scripts (sweeps →
│   slim.py, slim2.py, trim.py      # LaTeX → slim/split → submission)
├── Final circuit.scaps             # SCAPS circuit file (device definition)
├── fix_plan.md / discrepency.txt   # Bandgap/Jsc discrepancy audit trail
├── todolist.txt                    # Full simulation campaign log
└── VERIFICATION_REPORT.md          # Reference/citation verification
```

## Simulation Campaign

- **Device screening**: 8 ETL/HTL configurations (TiO₂/PCBM × NiO/CuI/CBTS/Spiro-OMeTAD) screened; FTO/TiO₂/RbGeI₃/CuI/Au selected on band-alignment grounds (initial PCE 19.79%).
- **OAT optimisation**: 11 parameters swept sequentially (absorber thickness, defect density, dielectric constant, electron affinity, bandgap, N_C, N_V, ETL/HTL thicknesses, both interface defect densities) — 71 runs total.
- **Joint factorial sweep**: 320-point grid (E_g × N_t × N_C × N_V); grid optimum 31.70% at E_g = 1.3 eV, N_t = 10¹⁸ m⁻³.
- **Genetic-algorithm joint optimum**: 6-gene search (62 evaluations) → 31.78% at E_g = 1.33 eV, N_t ≈ 10¹² cm⁻³ — reported as the mathematical maximum, not the device claim.
- **Uncertainty quantification**: Latin hypercube, 200 samples over 8 parameters (±25%) → PCE = 25.92 ± 1.78% (median 25.85%).
- **Temperature sweep**: 280–400 K; dV_OC/dT = −1.10 mV/K; V_OC(T) extrapolates to E_a = 1.46 eV ≈ E_g (bulk-limited recombination).
- **Illumination sweep**: 0.1–1.5 suns; J_SC linear, ideality factor n ≈ 1.17.
- **Dark J–V**: rectification ratio 1.8×10¹⁰ (−0.5…+1.3 V window); ideality n ≈ 1.5, J₀ ≈ 5×10⁻¹¹ A/cm².
- **Convergence check**: tighter numerical settings change results by < 0.02% relative.
- **Band diagram**: illuminated energy band diagram of the final device, with ΔE_c and ΔE_v quantified at both heterojunctions plus quasi-Fermi splitting.

### Round-5 additions (new in this revision)

All branched from the frozen baseline (`r5_baseline.json`: 26.81% / 1.13 V / 30.32 mA/cm² / 78.26%):

- **Defect energy + capture asymmetry**: Et sweep (0.2–1.2 eV above E_v) at N_t = 10¹⁵ cm⁻³ shows a symmetric mid-gap minimum (25.01 → 24.84 → 25.01%); at fixed σ_n·σ_p, electron-dominated traps limit PCE to 23.97% vs 26.71% hole-dominated.
- **Background doping**: N_A = 10¹⁴–10¹⁷ cm⁻³; peak 26.82% near 3×10¹⁴, ≤0.1 pp cost up to 10¹⁵; J_SC collapses past 10¹⁶. Synthetic target: N_A ≤ 10¹⁵ cm⁻³.
- **Series resistance**: external V − J·R_s correction, 0–10 Ω·cm²; PCE ≥ 20% to R_s = 8, ≥ 22% to R_s = 6. Manufacturing tolerance threshold: R_s ≈ 8 Ω·cm².
- **Mobility**: μ = 1–100 cm²/Vs, log-linear PCE 22.58 → 28.52%; electron mobility dominates; 700 nm holds over 400 nm. Crystallization target: μ ≥ 15 cm²/Vs.
- **CsGeI₃ mirror**: full 11-family OAT (71 runs) in the identical TiO₂/CuI stack, changing only E_g (1.4 → 1.6 eV). Consolidated CsGeI₃: 19.66% (V_OC 1.17 V, J_SC 23.18, FF 72.65); RbGeI₃ leads at every defect level. Control rerun at E_g = 1.4 eV reproduces RbGeI₃ exactly (26.81%), proving A-site isolation.

## Device Definition

The simulation input is `perovskite-rbgei3.def` (SCAPS definition file). Layer parameters (χ = electron affinity, E_g = bandgap, ε_r = relative permittivity):

| Layer | Thickness | χ (eV) | E_g (eV) | ε_r |
|-------|-----------|--------|----------|-----|
| CuI (back) | 100 nm | 2.1 | 3.1 | 6.5 |
| RbGeI₃ (absorber) | 700 nm | 3.9 | 1.4 | 15 |
| TiO₂ | 10 nm | 4.0 | 3.2 | 9 |
| FTO (front) | 500 nm | 4.4 | 3.2 | 9 |

Absorption uses the SCAPS square-root law at the uniform electrical bandgap (1.4 eV). A front-to-back grading variant was tested and found inert (ΔJ_SC = 0.00 mA/cm²), so the headline device is reported with uniform absorption.

## Reproduction

SCAPS-1D 3.3.10 runs under Wine via `scaps-runner` (4 worker prefixes in `~/.scaps-runner/`).

```bash
scaps-runner status                          # check setup
python3 r5_baseline.py                       # frozen headline device
python3 r5_et_sigma.py r5_na.py r5_mobility.py r5_temp.py   # tolerance sweeps
python3 r5_csgei3.py && python3 r5_csfinal.py # CsGeI3 mirror + consolidation
python3 r5_figures.py r5_figures2.py         # figures + tables from JSONs
python3 mk_latex.py && python3 slim.py && python3 slim2.py && python3 trim.py  # docx → submission
```

- Device definition: `~/.scaps-runner/scaps_dat/def/perovskite-rbgei3.def` (backed up as `backups_round5/r5_base.def` — local only, git-ignored)
- Results parsers fail closed: unique per-input result files plus a `V_OC·J_SC·FF/100 = PCE` arithmetic gate (see `r5_lib.py` and `r5_results/R5_REPORT.md`)
- Build the submission PDFs: `pdflatex manuscript.tex` (×2) and `pdflatex supplement.tex` (×2) inside `solar_submission/`

## Contributions

- **Md. Abdul Malek Fahim** (first author) — idea and initial execution
- **Hussain Touhid Siddiquee** (second and corresponding author) — paper writing and simulations
- **Rafiqul Islam** — supervisor
- **Ishmam Ahmed Chowdhury** — co-supervisor

**Leading University, Sylhet**
