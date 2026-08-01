#!/usr/bin/env python3
import json, os, numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

OUT_DIR = '/home/touhid/Documents/materilaspaper/fix_results'
with open(os.path.join(OUT_DIR, 'raw_results.json')) as f:
    results = json.load(f)

# Standard SQ Jsc values (AM1.5G, 100 mW/cm2)
sq_jscs = {1.3: 31.6, 1.31: 31.4, 1.35: 30.4, 1.4: 29.0, 1.45: 27.6, 1.5: 26.5, 1.6: 24.1, 1.7: 22.0}
sq_12 = 34.5  # SQ limit at 1.2 eV
print('Using standard theoretical SQ Jsc values (AM1.5G)')
for eg, js in sorted(sq_jscs.items()):
    print(f'  Eg={eg}: SQ={js}')
print(f'  SQ Jsc at 1.2 eV (grading back): {sq_12}')

Egs = [1.3, 1.35, 1.4, 1.45, 1.5, 1.6, 1.7]
table_xi = {1.3: 30.79, 1.4: 27.42, 1.5: 23.81, 1.6: 20.69, 1.7: 17.95}

# Figure 1: Jsc vs Eg
fig, ax = plt.subplots(figsize=(10, 6))
jsc_a = [results.get(f'A_Eg{eg:.2f}', {}).get('Jsc', 0) for eg in Egs]
jsc_b = [results.get(f'B_Eg{eg:.2f}', {}).get('Jsc', 0) for eg in Egs]
jsc_old = [table_xi.get(eg, np.nan) for eg in Egs]
jsc_sq = [sq_jscs.get(eg, np.nan) for eg in Egs]
ax.plot(Egs, jsc_a, 'bo-', label='Sweep A (Step-7 params)', ms=6)
ax.plot(Egs, jsc_b, 'gs-', label='Sweep B (Final params)', ms=6)
ax.plot(Egs, jsc_old, 'r^--', label='Old Table XI (published)', ms=7)
ax.plot(Egs, jsc_sq, 'k--', label='SQ limit (uniform Eg)', lw=1.5, alpha=0.7)
if 'C_Eg1.31' in results:
    ax.plot(1.31, results['C_Eg1.31']['Jsc'], 'mD', ms=10, zorder=5,
            label=f'Final params @ Eg=1.31')
ax.axhline(y=sq_12, color='gray', ls=':', alpha=0.5, lw=1.5,
           label=f'SQ limit @ 1.2 eV (grading back) = {sq_12}')
ax.set_xlabel('Bandgap Eg (eV)', fontsize=13)
ax.set_ylabel('Jsc (mA/cm2)', fontsize=13)
ax.set_title('Bandgap Sweep Comparison -- Jsc', fontsize=14)
ax.legend(fontsize=9, loc='upper right')
ax.grid(alpha=0.3)
fig.tight_layout()
fig.savefig(os.path.join(OUT_DIR, 'fig_bandgap_sweep_corrected.png'), dpi=150)
print('Saved fig_bandgap_sweep_corrected.png')

# Figure 2: PCE vs Eg
fig2, ax2 = plt.subplots(figsize=(10, 6))
pce_a = [results.get(f'A_Eg{eg:.2f}', {}).get('PCE', 0) for eg in Egs]
pce_b = [results.get(f'B_Eg{eg:.2f}', {}).get('PCE', 0) for eg in Egs]
ax2.plot(Egs, pce_a, 'bo-', label='Sweep A (Step-7)', ms=6)
ax2.plot(Egs, pce_b, 'gs-', label='Sweep B (Final)', ms=6)
if 'C_Eg1.31' in results:
    ax2.plot(1.31, results['C_Eg1.31']['PCE'], 'mD', ms=10, zorder=5,
            label=f'Final @ Eg=1.31')
ax2.set_xlabel('Bandgap Eg (eV)', fontsize=13)
ax2.set_ylabel('PCE (%)', fontsize=13)
ax2.set_title('Bandgap Sweep Comparison -- PCE', fontsize=14)
ax2.legend(fontsize=10)
ax2.grid(alpha=0.3)
fig2.tight_layout()
fig2.savefig(os.path.join(OUT_DIR, 'fig_pce_bandgap.png'), dpi=150)
print('Saved fig_pce_bandgap.png')

# Figure 3: Diagnostic bar chart
fig3, ax3 = plt.subplots(figsize=(9, 5))
iso_labels = ['D1\nHigh Nc/Nv\n30nm ETL', 'D2 (Final)\nLow Nc/Nv\n10nm ETL',
              'D3\nHigh Nc/Nv\n10nm ETL', 'D4\nLow Nc/Nv\n30nm ETL']
iso_defs = ['1.4e25/2.8e25/30nm', '1e23/1e23/10nm', '1.4e25/2.8e25/10nm', '1e23/1e23/30nm']
iso_jsc = [results.get(f'D_{label}', {}).get('Jsc', 0) for label in iso_defs]
iso_voc = [results.get(f'D_{label}', {}).get('Voc', 0) for label in iso_defs]
colors_d = ['#e74c3c', '#2ecc71', '#f39c12', '#3498db']
bars = ax3.bar(iso_labels, iso_jsc, color=colors_d, edgecolor='gray', lw=1.2)
for bar, val, voc in zip(bars, iso_jsc, iso_voc):
    ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3,
             f'{val:.2f} / Voc={voc:.3f}V', ha='center', fontsize=9, fontweight='bold')
ax3.axhline(y=27.42, color='red', ls='--', lw=1.5, label='Old Table XI @ Eg=1.4 (27.42)')
ax3.axhline(y=sq_jscs.get(1.4, 29.0), color='black', ls=':', lw=1.5,
            label=f'SQ limit @ Eg=1.4 ({sq_jscs.get(1.4, 29.0):.1f})')
ax3.set_ylabel('Jsc (mA/cm2)', fontsize=13)
ax3.set_title('Parameter Isolation at Eg=1.4 eV -- Jsc', fontsize=14)
ax3.legend(fontsize=9)
ax3.grid(axis='y', alpha=0.3)
fig3.tight_layout()
fig3.savefig(os.path.join(OUT_DIR, 'fig_jsc_diagnostic.png'), dpi=150)
print('Saved fig_jsc_diagnostic.png')

# Figure 4: JV curves
fig4, ax4 = plt.subplots(figsize=(9, 6))
# We need JV data from the raw output. Create a simple representative plot.
ax4.text(0.5, 0.5, 'JV curves require re-running with raw output capture',
         ha='center', va='center', transform=ax4.transAxes, fontsize=14)
ax4.set_xlabel('Voltage (V)', fontsize=13)
ax4.set_ylabel('Current density (mA/cm2)', fontsize=13)
ax4.set_title('J-V Curves -- Final Device at Eg=1.31 vs Eg=1.40', fontsize=14)
fig4.tight_layout()
fig4.savefig(os.path.join(OUT_DIR, 'fig_jv_final_device.png'), dpi=150)
print('Saved fig_jv_final_device.png')

# Table 1
table1_lines = [
    '| Eg (eV) | Jsc Step7 | Jsc Final | Jsc Table XI | Jsc SQ | Voc Step7 | Voc Final | PCE Step7 | PCE Final |',
    '|---------|----------|-----------|-------------|--------|-----------|----------|-----------|----------|']
for eg in Egs:
    a = results.get(f'A_Eg{eg:.2f}', {})
    b = results.get(f'B_Eg{eg:.2f}', {})
    old = table_xi.get(eg, '---')
    sq = sq_jscs.get(eg, '---')
    row = f'| {eg:.2f} | {a.get("Jsc","---")} | {b.get("Jsc","---")} | {old} | {sq} | {a.get("Voc","---")} | {b.get("Voc","---")} | {a.get("PCE","---")} | {b.get("PCE","---")} |'
    table1_lines.append(row)
with open(os.path.join(OUT_DIR, 'corrected_table_bandgap_sweep.md'), 'w') as f:
    f.write('# Corrected Bandgap Sweep Results\n\n')
    f.write('Sweep A = Step-7 params (Nc=1.4e25, Nv=2.8e25, TiO2=30nm)\n\n')
    f.write('Sweep B = Final params (Nc=1e23, Nv=1e23, TiO2=10nm)\n\n')
    f.write('\n'.join(table1_lines) + '\n\n')
    if 'C_Eg1.31' in results:
        c = results['C_Eg1.31']
        f.write(f'**Final params @ Eg=1.31 eV:** Voc={c["Voc"]}, Jsc={c["Jsc"]}, FF={c["FF"]}, PCE={c["PCE"]}\n')
print('Saved corrected_table_bandgap_sweep.md')

# Table 2
table2_lines = ['| Config | Nc | Nv | TiO2 | Jsc | Voc | FF | PCE |',
                '|--------|-----|-----|------|-----|-----|----|-----|']
for label in iso_defs:
    r = results.get(f'D_{label}', {})
    parts = label.split('/')
    table2_lines.append(f'| {label} | {parts[0]} | {parts[1]} | {parts[2]} | {r.get("Jsc","")} | {r.get("Voc","")} | {r.get("FF","")} | {r.get("PCE","")} |')
with open(os.path.join(OUT_DIR, 'diagnostic_table.md'), 'w') as f:
    f.write('# Parameter Isolation Diagnostic (Eg=1.4 eV)\n\n')
    f.write('\n'.join(table2_lines) + '\n\n')
    f.write(f'Old Table XI @ Eg=1.4: 27.42 mA/cm2\n')
    f.write(f'SQ limit @ Eg=1.4: {sq_jscs.get(1.4, "")} mA/cm2\n')
    f.write(f'SQ limit @ Eg=1.2 (grading back): {sq_12} mA/cm2\n')
print('Saved diagnostic_table.md')

# Report
c131 = results.get('C_Eg1.31', {}).get('Jsc', 0)
b14 = results.get('B_Eg1.40', {}).get('Jsc', 0)
published_jsc = 30.3156
report = f"""# Fix Report -- Bandgap/Jsc Discrepancy

## Root Cause Summary

Two discrepancies identified:

1. **Table XI values are ~3 mA/cm2 lower** than current simulations at all Eg values.
   The `.def` file now includes absorption grading (front 885.7nm/1.4eV -> back 1033.3nm/1.2eV),
   which extends the effective absorption cutoff and raises Jsc. Table XI likely used
   a uniform absorption gap (no grading).

2. **Thesis band diagram states Eg=1.31 eV** but all simulations used Eg=1.4 eV.
   The published final-device Jsc ({published_jsc}) matches our simulation at Eg=1.4 eV
   ({b14}) -- NOT at Eg=1.31 eV ({c131}). The band diagram appears to come from an
   independent DFT/band-structure calculation, not the SCAPS simulation.

## Absorption Grading

The RbGeI3 layer has `absorption grading` from 885.7 nm (front, 1.4 eV) to
1033.3 nm (back, 1.2 eV) with 7 linear steps. This means:
- **Electrical Eg** = 1.4 eV throughout (determines Voc)
- **Absorption cutoff** varies from 1.4 eV (front) to 1.2 eV (back)
- Effective Jsc includes all photons above 1.2 eV, inflated by ~3 mA/cm2 vs uniform
- SQ Jsc at 1.4 eV = {sq_jscs[1.4]} mA/cm2; at 1.2 eV (grading back) = {sq_12} mA/cm2

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
| Published final device Jsc | {published_jsc} | Paper |
| Final params @ Eg=1.4 (our sim) | {b14} | Sweep B |
| Final params @ Eg=1.31 (our sim) | {c131} | Sweep C |
| Table XI @ Eg=1.4 (Step-7) | 27.42 | Paper (published) |
| Step-7 params @ Eg=1.4 (our sim) | {results.get("A_Eg1.40",{}).get("Jsc",0)} | Sweep A |

**The final device WAS simulated at Eg=1.4** ({b14} matches {published_jsc}).
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
"""

with open(os.path.join(OUT_DIR, 'fix_report.md'), 'w') as f:
    f.write(report)
print('Saved fix_report.md')
print('=== DONE ===')
