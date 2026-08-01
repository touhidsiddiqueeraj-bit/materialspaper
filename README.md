# RbGeI₃ Perovskite Solar Cell — SCAPS-1D Simulation

Numerical simulation and optimisation of a lead-free RbGeI₃ perovskite solar cell with an **FTO/TiO₂/RbGeI₃/CuI/Au** planar heterojunction architecture, carried out with SCAPS-1D (v3.3.10) under Wine. The optimised device reaches **26.69% PCE**.

## Final Device Results

| Parameter | Value |
|-----------|-------|
| PCE | 26.69% |
| V_OC | 1.1127 V |
| J_SC | 30.3156 mA/cm² |
| FF | 79.13% |
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
├── paper/
│   └── RbGeI3_JournalPaper_Corrected_2026-07-29.docx / .pdf   # Manuscript (current version)
├── documents/
│   ├── thesis.docx                 # Companion thesis
│   ├── defense_slides.pptx         # Defense presentation
│   └── reference_masnbr3.pdf       # Reference paper
├── figures/                        # Simulation campaign figures
│   ├── temperature_sweep.png
│   ├── illumination_sweep.png
│   ├── dark_jv.png
│   ├── convergence_check.png
│   ├── sensitivity_tornado.png
│   ├── uncertainty_quantification.png
│   ├── factorial_by_eg.png
│   └── heatmap_Eg{1.3,1.45,1.6}.png
├── fix_results/                    # Bandgap/Jsc discrepancy analysis outputs
│   ├── fix_report.md
│   ├── corrected_table_bandgap_sweep.md
│   ├── diagnostic_table.md
│   ├── raw_results.json
│   └── fig_*.png                   # Diagnostic figures
├── factorial_sweep.json            # 320-point joint factorial grid (Eg × Nt × NC × NV)
├── factorial_sweep_results.json    # Summarised factorial results
├── uq_and_dark_results.json        # 200-sample UQ + dark J–V
├── dark_and_conv_results.json      # Convergence study + J–V curves
├── heatmap_data.json               # 2D PCE matrices (Nt×NC, Nt×NV, NC×NV)
├── run_fix.py                      # Re-runs discrepancy sweeps via scaps-runner
├── gen_figures.py                  # Regenerates fix_results figures/tables from raw_results.json
├── Final circuit.scaps             # SCAPS circuit file
├── fix_plan.md                     # Discrepancy analysis plan
├── discrepency.txt                 # Discrepancy documentation
├── todolist.txt                    # Full simulation campaign log
├── VERIFICATION_REPORT.md          # Reference/citation verification (50 refs)
└── WORKLOG.md                      # Work log
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
