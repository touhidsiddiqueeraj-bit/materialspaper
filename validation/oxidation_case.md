# Oxidation-constrained design case — RbGeI₃ (built Oct 2026)

**Thesis:** the paper's new headline niche is not another efficiency number but
an *oxidation budget*: how much Ge²⁺→Ge⁴⁺ a RbGeI₃ fab can tolerate, derived by
mapping DFT vacancy thermodynamics onto our SCAPS defect ladder. No lab needed;
every number below is published DFT/experiment + our archived runs.

## 1. DFT/experimental anchors (all published)

- **Ming et al., JMCA 2016 (CsGeI₃ DFT):** V_Ge is the DOMINANT native defect,
  shallow acceptor with LOW formation enthalpy → very high hole density,
  especially Ge-poor. Ge-poor/I-rich limit → degenerate, metallic, short-circuit
  behavior (no compensating donors). Ge-rich/Cs-rich/I-poor limit → V_Ge
  suppressed, Fermi level pinned at εv+0.43 eV → usable p-type absorber, but
  V_I deep traps appear. There is a narrow Goldilocks chemical-potential window.
- **Zhang et al., Molecules 2024 (CsBX₃ systematics):** Ge hosts carry
  low-E^f deep defects (Cs_I in CsGeI₃); CsGeI₃/CsGeBr₃ more tolerant than
  CsGeCl₃ but still afflicted. Sn analog: V_Sn E^f NEGATIVE (Sn→+4) — Ge is the
  same oxidation story, one row down.
- **Zhang et al., PRX Energy 2023 (HSE+SOC):** V_I in CsGeI₃ has Ctot =
  3.2×10⁻¹⁹ cm³/s (5 orders below CsSnI₃) → V_I is NOT the killer; focus stays
  on V_Ge (doping/metallicity) + Cs_I (deep). Nuance disclosed: V_I role is
  functional-dependent (Ming/PBE says deep trap; HSE+SOC says benign).
- **Yang et al. 2026 (ML discovery):** ordered-vacancy compounds destabilize
  CsGeI₃ → intrinsic vacancy-driven performance limit. Fresh support.
- **Thirumal et al., JMCA 2015 (experiment):** Ge-iodide perovskites oxidize
  rapidly; poor PV. The reason zero RbGeI₃ devices exist.
- **PCCMAI passivation (Ge–Pb, 2025, experiment):** 16.85→20.14% via Ge-defect
  passivation = Nt-reduction in our waterfall language. Calibration anchor.
- **Ge-doped CsPb(I,Br)₃ (JMCA 2025, experiment):** 1% Ge optimal (19.70%);
  more Ge hurts → V_Ge proliferation threshold. Dose-response anchor.
- **TRPL lifetimes (review 2026):** 1.12 ns → <0.70 ns with Ge content.
  Our SRH check: τ=1000/100/10/1/0.1 ns at Nt=1e14–1e18 → measured sub-ns
  films sit at Nt ≳ 1e17, i.e. 100–1000× above our ≤1e15 tolerance target.
- **Kino et al., PCCP 2025 (DFT):** Lewis base removes deep levels on MAGeI₃
  surfaces → molecular-passivation lever with computed mechanism.

## 2. Quantitative mapping (N = N_sites·exp(−E^f/kT), N_sites = 4.87e21 cm⁻³)

| Processing condition | E^f(V_Ge) | [V_Ge] (cm⁻³) | p≈2N | SCAPS analog → PCE |
|---|---|---|---|---|
| Inert, Ge-rich (passivated) | 0.55 | 2.8e12 | 5.6e12 | below headline |
| Good glovebox | 0.45 | 1.3e14 | 2.7e14 | **headline 26.81%** |
| Marginal glovebox | 0.40 | 9.3e14 | 1.9e15 | **realistic 24.84%** |
| Brief air exposure | 0.35 | 6.4e15 | 1.3e16 | ~22% (N_A-collapse onset) |
| Ambient processing | 0.30 | 4.4e16 | 8.9e16 | worse than high-ox 21.45% |
| Ge-poor limit | 0.15 | 1.5e19 | 2.9e19 | metallic/short (Ming) |

Cross-checks already in our data: N_A sweep collapses above 1e16 (p hits
1e16 at E^f≈0.35 ✓); 1e18 row gives 7.58% (collapse ✓); Cs-mirror control
supports A-site insensitivity (Cs→Rb transfer assumption).

## 3. Disclosures required in manuscript
- Numbers are CsGeI₃ DFT; RbGeI₃ assumed analogous (same Ge–I framework,
  A-site has no band-edge weight).
- Equilibrium thermodynamics = bounds; real oxidation is kinetic (present
  air-exposure axis as chemical-potential shift, Nt axis as quantitative).
- V_I role functional-dependent; claim rests on V_Ge + Cs_I only.

## 4. Recommended paper surgery (when authorized)
New headline section "Oxidation budget" + 1 figure family (PCE vs Ge⁴⁺
fraction + passivation-lever ranking vs PCCMAI/Kino anchors); retitle toward
oxidation tolerance; cover letter leads with the budget table. Replaces the
"0.40 pp from best simulation" framing, which Sept-2026 papers already beat.
