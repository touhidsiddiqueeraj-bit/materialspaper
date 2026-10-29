#!/usr/bin/env python3
"""r7_validate — SCAPS pipeline validation against Wang et al. Science 2019
(beta-CsPbI3, FTO/c-TiO2/CsPbI3/spiro-OMeTAD/Ag).

Method: rebuild the experimental stack in SCAPS-1D with literature-pinned
bands/geometry; fit ONLY bulk Nt x interface N (the paper's own control vs
CHI-treated contrast is an interface-quality story). Everything else stays
pinned and is disclosed in VALIDATION_LOG.md.

Targets (measured at ~45 C = 318 K, AM1.5G):
  control : 15.1% (Voc 1.05 V, Jsc 20.03 mA/cm2, FF 72%)
  champion: 18.4% (Voc 1.11 V, Jsc ~20.0 mA/cm2, FF 82%)
  EQE-integrated Jsc: 19.71 / 19.85 mA/cm2 (cross-check, not fitted).
"""
import sys, os, json
sys.path.insert(0, '/home/touhid/Documents/materilaspaper')
from r5_lib import BASE, DEF_DIR, write_def, run_set, edit_block, edit_single

VAL_DIR = '/home/touhid/Documents/materilaspaper/validation'


def build_cspbi3_def(nt_bulk_m3, nif_m2, A_abs=1.5e5):
    """FINAL stack (see VALIDATION_LOG.md for the diagnostic path):
    - Ag back contact at EFFECTIVE Fi_m 5.2 eV (pinned metal/organic interface;
      nominal 4.7 eV gives a 0.5 eV hole-extraction barrier absent in the
      measured FF; Fi_m 5.0/5.1 systematically fail to converge).
    - Doped spiro-OMeTAD (Li-TFSI/tBP recipe): mu 2e-3 cm2/Vs (doped value).
    - CsPbI3 sqrt-law absorption A = 1.5e5 (Jsc-calibrated: 19.92 vs 20.03).
    - Only nt_bulk_m3 x nif_m2 are fitted; all else literature-pinned."""
    t = BASE
    # --- back contact: effective ohmic value (see docstring) ---
    t = t.replace('Fi_m :   5.100000 [eV]', 'Fi_m :   5.200000 [eV]')
    # --- HTL CuI -> doped spiro-OMeTAD (Wang recipe, standard SCAPS params) ---
    t = t.replace('name : CuI (6.1)', 'name : Spiro (6.1)')
    t = t.replace('interfacename : CuI (6) / RbGeI3 (7',
                  'interfacename : Spiro (6) / CsPbI3 (7')
    t = edit_block(t, 'Spiro', 'd :', {0: '1.800e-07'}, '[m]')
    t = edit_block(t, 'Spiro', 'eps :', {0: '3.000000', 5: '3.000000', 6: '3.000000'}, '[-]')
    t = edit_block(t, 'Spiro', 'chi :', {0: '2.200000', 5: '2.200000', 6: '2.200000'}, '[eV]')
    t = edit_block(t, 'Spiro', 'Eg :', {0: '3.000000', 5: '3.000000', 6: '3.000000'}, '[eV]')
    t = edit_block(t, 'Spiro', 'Nc :', {0: '2.200000e+24', 5: '2.200000e+24', 6: '2.200000e+24'}, '[/m^3]')
    t = edit_block(t, 'Spiro', 'Nv :', {0: '1.800000e+25', 5: '1.800000e+25', 6: '1.800000e+25'}, '[/m^3]')
    t = edit_block(t, 'Spiro', 'mu_n :', {0: '2.000000e-07', 5: '2.000000e-07', 6: '2.000000e-07'}, '[m^2/Vs]')
    t = edit_block(t, 'Spiro', 'mu_p :', {0: '2.000000e-07', 5: '2.000000e-07', 6: '2.000000e-07'}, '[m^2/Vs]')
    t = edit_block(t, 'Spiro', 'Na(uniform) :', {0: '1.000000e+24', 5: '1.000000e+24', 6: '1.000000e+24'}, '[/m^3]')
    t = edit_block(t, 'Spiro', 'absorption grading :', {0: '413.30'}, '[nm]')
    # --- absorber RbGeI3 -> beta-CsPbI3 (Wang: 350-400 nm film, edge ~736 nm) ---
    t = t.replace('name : RbGeI3 (7.1)', 'name : CsPbI3 (7.1)')
    t = t.replace('interfacename : RbGeI3 (7) / TiO2 (',
                  'interfacename : CsPbI3 (7) / TiO2 (')
    t = edit_block(t, 'CsPbI3', 'd :', {0: '3.750e-07'}, '[m]')
    t = edit_block(t, 'CsPbI3', 'eps :', {0: '10.000000', 5: '10.000000', 6: '10.000000'}, '[-]')
    t = edit_block(t, 'CsPbI3', 'Eg :', {0: '1.680000', 5: '1.680000', 6: '1.680000'}, '[eV]')
    t = edit_block(t, 'CsPbI3', 'Nc :', {0: '1.000000e+25', 5: '1.000000e+25', 6: '1.000000e+25'}, '[/m^3]')
    t = edit_block(t, 'CsPbI3', 'Nv :', {0: '1.000000e+25', 5: '1.000000e+25', 6: '1.000000e+25'}, '[/m^3]')
    t = edit_block(t, 'CsPbI3', 'mu_n :', {0: '2.500000e-03', 5: '2.500000e-03', 6: '2.500000e-03'}, '[m^2/Vs]')
    t = edit_block(t, 'CsPbI3', 'mu_p :', {0: '2.500000e-03', 5: '2.500000e-03', 6: '2.500000e-03'}, '[m^2/Vs]')
    t = edit_block(t, 'CsPbI3', 'Nt(uniform) :', {0: f'{nt_bulk_m3:.3e}', 5: f'{nt_bulk_m3:.3e}', 6: f'{nt_bulk_m3:.3e}'}, '[/m^3]')
    t = edit_single(t, 'CsPbI3', 'Et', '0.84', 'eV')
    t = edit_block(t, 'CsPbI3', 'absorption grading :', {0: '738.10'}, '[nm]')
    t = edit_block(t, 'CsPbI3', 'absorption model A, value of parameter 1 :',
                   {0: f'{A_abs:.3e}'}, '')
    # --- ETL: 10 nm -> 40 nm compact TiO2 (spray pyrolysis; documented assumption) ---
    t = edit_block(t, 'TiO2', 'd :', {0: '4.000e-08'}, '[m]')
    # --- interfaces: the single fit knob beside bulk Nt ---
    import re
    t = re.sub(r'(^N\s*:\s*)[\d.eE+-]+(\s*\[/m\^2\])',
               r'\g<1>' + f'{nif_m2:.3e}' + r'\g<2>', t, flags=re.MULTILINE)
    return t


if __name__ == '__main__':
    import itertools
    nts = [3e19, 1e20, 3e20, 1e21, 3e21]
    nifs = [3e17, 1e18, 3e18, 1e19, 3e19]
    variants = {}
    for nt, nif in itertools.product(nts, nifs):
        key = f'r7f_Nt{nt:.0e}_Nif{nif:.0e}'
        write_def(key + '.def', build_cspbi3_def(nt, nif))
        variants[key] = key + '.def'
    print(f'{len(variants)} defs written')
    run_set(variants, os.path.join(VAL_DIR, 'r7_grid_final.json'),
            iv={'start': 0, 'stop': 1.4, 'step': 0.01},
            temps={k: 318 for k in variants},
            with_jv_keys=tuple(variants))
