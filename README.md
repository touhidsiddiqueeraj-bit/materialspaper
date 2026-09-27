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
- **Joint factorial sweep**: 320-point grid (E_g × N_t × N_C × N_V); global optimum 31.70% at E_g = 1.3 eV, N_t = 10¹⁸ m⁻³.
- **Uncertainty quantification**: Latin hypercube, 200 samples over 8 parameters (±25%) → PCE = 25.92 ± 1.78%.
- **Temperature sweep**: 280–400 K; dV_OC/dT = −1.08 mV/K.
- **Illumination sweep**: 0.1–1.5 suns; ideality factor n ≈ 1.2.
- **Dark J–V**: rectification ratio 1.8×10¹⁰, J₀ ≈ 7.1×10⁻¹⁸ A/cm².
- **Convergence check**: tighter numerical settings change results by < 0.02% relative.
- **Band diagram**: equilibrium energy band diagram of the final device, with ΔE_c and ΔE_v quantified at both heterojunctions.

## Device Definition

The simulation input is `perovskite-rbgei3.def` (SCAPS definition file). Layer parameters (χ = electron affinity, E_g = bandgap, ε_r = relative permittivity):

| Layer | Thickness | χ (eV) | E_g (eV) | ε_r |
|-------|-----------|--------|----------|-----|
| CuI (back) | 100 nm | 2.1 | 3.1 | 6.5 |
| RbGeI₃ (absorber) | 700 nm | 3.9 | 1.4 | 15 |
| TiO₂ | 10 nm | 4.0 | 3.2 | 9 |
| FTO (front) | 500 nm | 4.4 | 3.2 | 9 |

The absorber uses graded absorption (front 1.4 eV → back 1.2 eV, 7 linear steps) with a uniform electrical bandgap of 1.4 eV.

## Reproduction

SCAPS-1D 3.3.10 runs under Wine via `scaps-runner` (4 worker prefixes in `~/.scaps-runner/`).

```bash
scaps-runner status                          # check setup
scaps-runner sweep params.json               # parameter sweep from JSON
scaps-runner script band.script              # run a raw SCAPS script
```

- Device definition: `~/.scaps-runner/scaps_dat/def/perovskite-rbgei3.def`
- Re-run the discrepancy sweeps: `python run_fix.py`
- Regenerate fix figures/tables: `python gen_figures.py`
- Band diagram export uses the SCAPS script command `save results.eb`

## Contributions

- **Md. Abdul Malek Fahim** — idea and initial execution
- **Hussain Touhid Siddiquee** — paper writing and simulations
- **Rafiqul Islam** — supervisor
- **Ishmam Ahmed Chowdhury** — co-supervisor

**Leading University, Sylhet**
