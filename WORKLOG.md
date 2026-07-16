# Worklog — SCAPS-1D Additions to RbGeI₃ Paper

**Paper**: SCAPS-1D numerical optimization of a lead-free RbGeI₃ perovskite solar cell with TiO₂/CuI charge transport layers  
**Author**: Md. Abdul Malek Fahim  
**Baseline device**: FTO/TiO₂/RbGeI₃/CuI/Au | PCE: 26.69% | V_OC: 1.1127 V | J_SC: 30.32 mA/cm² | FF: 79.13%

---

## Optimized Baseline Parameters (Table XVI)

| Parameter | Value |
|-----------|-------|
| Absorber thickness | 700 nm |
| Absorber bandgap | 1.4 eV |
| Absorber defect density | 1×10¹⁴ cm⁻³ |
| Electron affinity (RbGeI₃) | 3.9 eV |
| Dielectric constant | 15 |
| N_C | 1×10¹⁷ cm⁻³ |
| N_V | 1×10¹⁷ cm⁻³ |
| ETL (TiO₂) thickness | 10 nm |
| HTL (CuI) thickness | 100 nm |
| Interface N_t (both) | 1×10¹⁴ cm⁻² |

**Layer stack**: FTO (500 nm) | TiO₂ (10 nm) | RbGeI₃ (700 nm) | CuI (100 nm) | Au

---

## Task List

### [x] 1. Ref [26] — Fix reference in PDF
- [x] DOCX fixed → `_fixed.docx`
- [x] PDF generated from fixed DOCX via LibreOffice → `_fixed.pdf`
- [x] Change: wrong Saikia CsSnI₃ title/DOI → correct Saikia CsGeI₃ paper (Opt. Mater. 123, 111839, 2022, doi:10.1016/j.optmat.2021.111839)

### [x] 2. C–V / Mott-Schottky Analysis
**Script**: `01_cv_mott_schottky.scr` ✓  
**Parser**: `analyze_results.py` → `analyze_cv()` ✓  
**Figures**: `fig_cv_mott_schottky.pdf` (2-panel: C-V + 1/C²) ✓

Runs C-V at 1 MHz, 10 kHz, 100 kHz to extract V_bi, N_A, W.
Also runs C-f at V=0 (100 Hz – 10 MHz).

### [x] 3. Series & Shunt Resistance Sweep
**Script**: `02_resistance_sweep.scr` ✓  
**Parser**: `analyze_results.py` → `analyze_resistance_sweep()` ✓  
**Figures**: `fig_resistance.pdf` (2-panel: PCE vs Rs, PCE vs Rsh) ✓

R_s: 0, 1, 2, 5, 10, 15, 20 Ω·cm²  
R_sh: 10², 10³, 10⁴, 10⁵, 10⁶ Ω·cm²

### [x] 4. Back Contact Work Function Optimization
**Script**: `03_workfunction_sweep.scr` ✓  
**Parser**: `analyze_results.py` → `analyze_workfunction_sweep()` ✓  
**Figures**: `fig_workfunction.pdf` (4-panel: PCE/Voc/Jsc/FF vs WF) ✓

Sweep 4.0–6.0 eV, step 0.2 eV. Also annotates real metals (Au, Cu, Ni, C, Ag, Pt).

### [x] 5. Light Intensity Dependence
**Script**: `04_intensity_sweep.scr` ✓  
**Parser**: `analyze_results.py` → `analyze_intensity_sweep()` ✓  
**Figures**: `fig_intensity.pdf` (PCE vs intensity + Voc vs ln(I) with ideality factor) ✓

7 intensities from 0.01 to 10 suns. Extracts ideality factor n from Voc–ln(I) slope.

### [x] 6. G–R (Generation–Recombination) Profiles
**Script**: `05_gr_profiles.scr` ✓ (manual profile save step noted)  
**Parser**: Placeholder in `analyze_results.py` — needs .prf file from SCAPS GUI

### [ ] 7. Run SCAPS scripts & generate figures
- [x] Scripts written: `run_all.scr` orchestrates all 5
- [x] Analysis script: `analyze_results.py` parses all outputs, makes figures + tables
- [ ] Run `run_all.scr` in SCAPS (needs SCAPS installed)
- [ ] Run `python analyze_results.py` to generate figures
- [ ] Write new subsections O–R in paper
- [ ] Update TOC, references, section numbering

---

## File Reference

| File | Purpose |
|------|---------|
| `RbGeI3_Perovskite_JournalPaper_2026-07-11 (5).docx` | Original DOCX |
| `RbGeI3_Perovskite_JournalPaper_2026-07-11 (5)_fixed.docx` | DOCX with ref [26] corrected |
| `RbGeI3_Perovskite_JournalPaper_2026-07-11 (8).pdf` | Original PDF (needs ref [26] fix) |
| `VERIFICATION_REPORT.md` | Reference verification results |
| `WORKLOG.md` | This file |

## Data Files to Create

All outputs from SCAPS simulation scripts will go in:
```
/home/touhid/Documents/materilaspaper/scaps_data/
├── cv_mott_schottky/
│   ├── cv_1mhz.csv
│   └── mott_schottky.csv
├── resistance/
│   ├── rs_sweep.csv
│   └── rsh_sweep.csv
├── workfunction/
│   └── wf_sweep.csv
├── intensity/
│   └── intensity_sweep.csv
└── gr_profiles/
    ├── gr_sc.csv
    └── gr_mpp.csv
```
