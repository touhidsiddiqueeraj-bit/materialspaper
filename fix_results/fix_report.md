# Fix Report -- Bandgap/Jsc Discrepancy

## Root Cause Summary

Two discrepancies identified:

1. **Table XI values are ~3 mA/cm2 lower** than current simulations at all Eg values.
   The `.def` file now includes absorption grading (front 885.7nm/1.4eV -> back 1033.3nm/1.2eV),
   which extends the effective absorption cutoff and raises Jsc. Table XI likely used
   a uniform absorption gap (no grading).

2. **Thesis band diagram states Eg=1.31 eV** but all simulations used Eg=1.4 eV.
   The published final-device Jsc (30.3156) matches our simulation at Eg=1.4 eV
   (30.3156) -- NOT at Eg=1.31 eV (33.274). The band diagram appears to come from an
   independent DFT/band-structure calculation, not the SCAPS simulation.

## Absorption Grading

The RbGeI3 layer has `absorption grading` from 885.7 nm (front, 1.4 eV) to
1033.3 nm (back, 1.2 eV) with 7 linear steps. This means:
- **Electrical Eg** = 1.4 eV throughout (determines Voc)
- **Absorption cutoff** varies from 1.4 eV (front) to 1.2 eV (back)
- Effective Jsc includes all photons above 1.2 eV, inflated by ~3 mA/cm2 vs uniform
- SQ Jsc at 1.4 eV = 29.0 mA/cm2; at 1.2 eV (grading back) = 34.5 mA/cm2

## Parameter Isolation at Eg=1.4 eV

All four D-series configurations give Jsc = 30.32 -- identical within rounding.
Nc/Nv/TiO2 thickness has NO effect on Jsc at fixed Eg. Jsc is entirely dominated
by the absorption model (with grading).

Nc/Nv and TiO2 DO affect Voc and FF:
- High Nc/Nv -> lower Voc (~0.93 vs ~1.13 V) due to higher recombination
- Thicker TiO2 -> slightly higher Voc (less interface recombination)

## Key Results

| Quantity | Value | Source |
|---------|-------|-------|
| Published final device Jsc | 30.3156 | Paper |
| Final params @ Eg=1.4 (our sim) | 30.3156 | Sweep B |
| Final params @ Eg=1.31 (our sim) | 33.274 | Sweep C |
| Table XI @ Eg=1.4 (Step-7) | 27.42 | Paper (published) |
| Step-7 params @ Eg=1.4 (our sim) | 30.3156 | Sweep A |

**The final device WAS simulated at Eg=1.4** (30.3156 matches 30.3156).
The thesis band diagram value of 1.31 eV is inconsistent with the simulation.

## Corrective Actions

### Paper
- **Table XI**: Add footnote stating OAT sweeps used uniform absorption (no grading)
  and Step-7 intermediate parameters (Nc=1.4e25, Nv=2.8e25, TiO2=30nm)
- **Table XVI / final device**: Verify Eg = 1.4 eV, not 1.31 eV
- **Band diagram / discussion**: Correct any reference to Eg=1.31. If DFT gave 1.31,
  state clearly that SCAPS used 1.4 for device simulation
- **Abstract / conclusion**: Update any implicit claim linking Eg=1.31 to device metrics

### Thesis
- **Band diagram section**: Reconcile Figure 5.x (1.31 eV) with Table 5.13 (1.4 eV)
- **Table 5.13**: Add column for absorption model (graded vs uniform)
- **Each OAT sweep**: Document which parameter set was used (Step-7 vs final)
- **Add disclosure**: Absorption model evolved between OAT and final simulation
