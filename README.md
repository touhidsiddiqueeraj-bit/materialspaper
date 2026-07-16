# RbGeI₃ Perovskite Solar Cell — SCAPS-1D Simulation

Numerical simulation and optimisation of a lead-free RbGeI₃ perovskite solar cell with **FTO/TiO₂/RbGeI₃/CuI/Au** architecture using SCAPS-1D. The optimised device achieves **26.69% PCE**.

## Repository Structure

```
├── paper/                          # Manuscript (DOCX + PDF)
│   ├── RbGeI3_Perovskite_JournalPaper_fixed.docx
│   └── RbGeI3_Perovskite_JournalPaper_fixed.pdf
├── documents/                      # Supporting documents
│   ├── thesis.docx                 # Full thesis
│   ├── defense_slides.pptx         # Defense presentation
│   └── reference_masnbr3.pdf       # Reference paper
├── scaps/
│   ├── scripts/                    # SCAPS-1D batch scripts (.scr)
│   │   ├── run_all.scr             # Master orchestrator
│   │   ├── 01_cv_mott_schottky.scr # C-V / Mott-Schottky
│   │   ├── 02_resistance_sweep.scr # Series & shunt resistance
│   │   ├── 03_workfunction_sweep.scr# Back contact work function
│   │   ├── 04_intensity_sweep.scr  # Light intensity dependence
│   │   └── 05_gr_profiles.scr      # Generation-recombination
│   ├── analysis/
│   │   └── analyze_results.py      # Parse output → figures + report
│   ├── data/                       # SCAPS output (gitignored)
│   └── figures/                    # Thesis figures + generated plots
├── .gitignore
├── VERIFICATION_REPORT.md          # Reference validation
└── README.md
```

## Optimised Parameters

| Parameter | Value |
|-----------|-------|
| Absorber thickness | 700 nm |
| Bandgap | 1.4 eV |
| Defect density | 1×10¹⁴ cm⁻³ |
| Dielectric constant (εᵣ) | 15 |
| N_C / N_V | 1×10¹⁷ cm⁻³ |
| **PCE** | **26.69%** |
| V_OC | 1.1127 V |
| J_SC | 30.32 mA/cm² |
| FF | 79.13% |

## SCAPS-1D Simulation Status

**All 5 batch scripts are not yet run.** SCAPS-1D was never successfully installed in the Wine environment. The data directories (`scaps/data/*/`) are empty and `results_report.txt` contains placeholder data.

### Scripts

| Script | Analysis | Sweep Details | Status |
|--------|----------|--------------|--------|
| `01_cv_mott_schottky.scr` | C-V / Mott-Schottky | 1 MHz, 100 kHz, 10 kHz + C-f at V=0 | ❌ Not run |
| `02_resistance_sweep.scr` | Series & shunt resistance | Rₛ: 0–20 Ω·cm², Rₛₕ: 10²–10⁶ Ω·cm² | ❌ Not run |
| `03_workfunction_sweep.scr` | Back contact work function | 4.0–6.0 eV (12 steps) | ❌ Not run |
| `04_intensity_sweep.scr` | Light intensity dependence | 0.01–10 suns (7 steps) | ❌ Not run |
| `05_gr_profiles.scr` | G-R depth profiles | At V=0 and V=V_mp | ❌ Not run |

### How to Run

1. **Install SCAPS-1D**: Register at [scaps.elis.ugent.be](https://scaps.elis.ugent.be) (email Marc.Burgelman@ugent.be), download the installer, then:
   ```bash
   WINEPREFIX=~/.wine_scaps wine SCAPS3311_setup.exe
   ```
2. Create the optimised device definition file `FTO_TiO2_RbGeI3_CuI_Au.def` in SCAPS with parameters from Table XVI.
3. Copy all `.scr` scripts from `scaps/scripts/` into the SCAPS working directory.
4. In SCAPS: **Actions → Run script → select `run_all.scr`** (takes ~15–30 min).
5. After completion:
   ```bash
   python scaps/analysis/analyze_results.py
   ```
   This parses all output files and generates figures as PDFs in `scaps/figures/` and a text report in `scaps/data/results_report.txt`.

## Authors

- Md. Abdul Malek Fahim
- Hussain Touhid Siddiquee
- Rafiqul Islam (Supervisor)
- Ishmam Ahmed Chowdhury (Co-supervisor)

**Leading University, Sylhet**
