#!/usr/bin/env python3
"""trim — prose condensation on solar_submission/manuscript.tex (claims kept).
Run ONCE (guard aborts if already applied)."""
import re

TEX = 'solar_submission/manuscript.tex'
m = open(TEX).read()
assert 'slow-trim-marker-absent' not in m
assert 'TRIMMED-V2' not in m, 'already trimmed!'

P = []
# ---- rationale: 5 paras -> compact ----
P.append(('Fluorine-doped tin oxide (FTO) is the front transparent conducting electrode. It has high optical transparency in the visible spectrum together with excellent electrical conductivity, allowing incident sunlight to reach the absorber layer while simultaneously collecting the generated electrons with minimal resistive loss',
          'Fluorine-doped tin oxide (FTO, 500 nm) is the front electrode for its transparency, conductivity, and thermal/chemical stability'))
P.append(('FTO was preferred over alternative transparent conducting oxides (such as indium tin oxide, ITO) for its superior thermal and chemical stability, its compatibility with the TiO$_{2}$ ETL deposition process, and its lower cost. The thickness of the FTO layer was fixed at 500 nm, consistent with values commonly reported for perovskite solar cells',
          'It was preferred over ITO for stability, process compatibility, and cost'))
P.append(('Titanium dioxide (TiO$_{2}$) is the electron transport layer. The primary function of the ETL is to extract photogenerated electrons from the absorber layer and transport them toward the FTO electrode while effectively blocking holes. TiO$_{2}$ is an n-type semiconductor with a wide bandgap of approximately 3.2 eV in its anatase phase, providing excellent transparency throughout the visible region of the solar spectrum. Its conduction-band minimum lies slightly below that of most iodide-based perovskites, providing an energetically downhill path for photogenerated electrons to transfer from the absorber into the ETL, while its deep valence band acts as an effective barrier against hole transport',
          'Titanium dioxide (TiO$_{2}$) is the electron transport layer: its 3.2 eV gap passes visible light, its conduction-band minimum lies slightly below typical iodide-perovskite levels for downhill electron transfer, and its deep valence band blocks holes'))
P.append(('Although its intrinsic electron mobility is lower than that of ZnO and SnO$_{2}$, TiO$_{2}$ provides sufficiently fast electron transport when fabricated with appropriate morphology and crystallinity, and it forms chemically stable interfaces with perovskite materials',
          'Despite lower mobility than ZnO/SnO$_{2}$, it transports adequately and forms stable perovskite interfaces'))
P.append(('Rubidium germanium iodide (RbGeI$_{3}$) is the photoactive absorber. Compared with conventional lead-based perovskites, RbGeI$_{3}$ is environmentally friendly because germanium replaces toxic lead while keeping the optoelectronic properties an absorber needs. RbGeI$_{3}$ adopts the ABX$_{3}$ perovskite structure with rubidium at the A-site, germanium at the B-site, and iodine at the X-site. Its direct bandgap in the 1.3--1.4 eV range, strong optical absorption coefficient (reported to be comparable to that of MAPbI$_{3}$ by first-principles calculations',
          'Rubidium germanium iodide (RbGeI$_{3}$, ABX$_{3}$) is the absorber: replacing lead with germanium keeps the needed optoelectronics, with a direct 1.3--1.4 eV gap and strong absorption (comparable to MAPbI$_{3}$ by first-principles calculations'))
P.append(('The initial absorber thickness used for device screening was 400 nm, and the bandgap was initially set to 1.4 eV, consistent with values reported in the experimental literature',
          'Screening used 400 nm and 1.4 eV from experimental literature'))
P.append(('Copper iodide (CuI) is our hole transport layer, chosen for its excellent hole conductivity, high optical transparency, appropriate valence-band alignment with RbGeI$_{3}$, and comparatively low fabrication cost',
          'Copper iodide (CuI) is the hole transport layer for its conductivity, transparency, close valence alignment with RbGeI$_{3}$, and low cost'))
P.append(('The HTL extracts photogenerated holes efficiently from the absorber layer while preventing electron back-transfer toward the rear electrode. CuI is a wide-gap ($E_{\\mathrm{g}}$ $\\approx$ 3.1 eV) p-type transparent conductor whose valence-band maximum aligns closely with that of RbGeI$_{3}$ (giving a small valence-band offset of approximately 0.10 eV as quantified in Section V.E), supporting efficient hole extraction. Reported single-crystal hole mobilities of CuI exceed 100 cm$^{2}$ V$^{-1}$ s$^{-1}$, and its solution-processability at low temperatures makes it attractive for large-area fabrication',
          'CuI is a wide-gap ($E_{\\mathrm{g}}$ $\\approx$ 3.1 eV) p-type conductor whose valence maximum aligns with RbGeI$_{3}$ (0.10 eV offset, Section V.E); single-crystal hole mobilities exceed 100 cm$^{2}$ V$^{-1}$ s$^{-1}$ and it processes from solution at low temperature'))
P.append(('The initial CuI thickness was set to 100 nm.\nGold (Au) forms the rear metal contact because of its high work function, excellent electrical conductivity, and superior chemical stability. A high-work-function metal establishes an ohmic contact with the hole transport layer, thereby reducing contact resistance and improving hole collection efficiency',
          'Screening used 100 nm CuI. Gold (Au) is the back contact: its high work function gives an ohmic contact to CuI without a parasitic Schottky barrier'))
P.append(('The choice of Au over lower-work-function alternatives such as Ag or Al ensures that the back contact does not introduce a parasitic Schottky barrier at the CuI/\\allowbreak{}Au interface, which would otherwise degrade the fill factor and open-circuit voltage of the device.',
          ''))
# ---- band diagram: merge paras 1+2, trim ----
P.append(('The CuI/\\allowbreak{}RbGeI$_{3}$ interface exhibits a pronounced conduction-band discontinuity. Based on the electron-affinity values of CuI ($\\chi$ = 2.1 eV) and RbGeI$_{3}$ ($\\chi$ = 3.9 eV), the conduction-band offset is $\\Delta E_{\\mathrm{c}}$ $\\approx$ |2.1 $-$ 3.9| = 1.8 eV, which acts as an effective electron-blocking barrier. The corresponding valence-band offset, computed using $E_{\\mathrm{v}}$ = $-($E_{\\mathrm{g}}$ + $\\chi$), is $\\Delta E_{\\mathrm{v}}$ $\\approx$ |($-$5.30) $-$ ($-$5.20)| $\\approx$ 0.10 eV, indicating that the valence bands of CuI and RbGeI$_{3}$ are nearly aligned. This small barrier enables holes generated inside the absorber to move efficiently into the HTL with minimal transport resistance. Within the 700 nm RbGeI$_{3}$ absorber layer, both $E_{\\mathrm{c}}$ and $E_{\\mathrm{v}}$ remain nearly constant, indicating a relatively uniform electrostatic potential throughout the bulk absorber. The energy difference between $E_{\\mathrm{c}}$ and $E_{\\mathrm{v}}$ corresponds to the absorber bandgap of 1.4 eV used in the optimized device, close to the Shockley--Queisser optimum for single-junction photovoltaic devices.\nA second band discontinuity appears at the RbGeI$_{3}$/TiO$_{2}$ interface located approximately 800 nm from the back contact. Because the electron affinities of RbGeI$_{3}$ and TiO$_{2}$ are 3.9 eV and 4.0 eV respectively, the conduction-band offset is only about 0.10 eV, forming a 0.10 eV downward step at the interface that assists electron extraction and suppresses interfacial recombination. The calculated valence-band offset at this interface is approximately 1.90 eV (using $E_{\\mathrm{v}}$(RbGeI$_{3}$) = $-$5.30 eV and $E_{\\mathrm{v}}$(TiO$_{2}$) = $-$(4.0+3.2) = $-$7.2 eV, giving $\\Delta E_{\\mathrm{v}}$ = |$-$5.30 $-$ ($-$7.2)| = 1.90 eV), creating a substantial energetic barrier that effectively blocks holes from entering the TiO$_{2}$ layer.\nUnder illumination, the quasi-Fermi levels split apart across the device, with the electron quasi-Fermi level $F_{\\mathrm{n}}$ lying close to the conduction band in the absorber and ETL and the hole quasi-Fermi level $F_{\\mathrm{p}}$ following the valence band. The $F_{\\mathrm{n}}$ $-$ $F_{\\mathrm{p}}$ splitting sets the photovoltage (V$_{\\mathrm{OC}}$ $\\approx$ 1.13 V) and is consistent with the high open-circuit voltage of the optimized device. Slight band bending near both heterojunctions reflects the built-in electric field established after contact formation, which drives photogenerated electrons toward the TiO$_{2}$/FTO electrode and holes toward the CuI HTL.',
          'From affinities ($\\chi$ = 2.1 vs 3.9 eV) the conduction offset is $\\Delta E_{\\mathrm{c}}$ $\\approx$ 1.8 eV (electron-blocking), while $E_{\\mathrm{v}}$ = $-$($E_{\\mathrm{g}}$ + $\\chi$) gives $\\Delta E_{\\mathrm{v}}$ $\\approx$ 0.10 eV, so holes cross freely; both band edges stay flat across the 700 nm absorber, consistent with the 1.4 eV gap near the Shockley--Queisser optimum. At RbGeI$_{3}$/TiO$_{2}$ ($\\approx$800 nm from the back contact) a 0.10 eV downward conduction step assists extraction while a 1.90 eV valence offset blocks holes. Under illumination the quasi-Fermi levels split, $F_{\\mathrm{n}}$ tracking the conduction band and $F_{\\mathrm{p}}$ the valence band; the splitting sets V$_{\\mathrm{OC}}$ $\\approx$ 1.13 V, with slight bending at the heterojunctions from the built-in field.'))
P.append(('A second band discontinuity appears at the RbGeI$_{3}$/TiO$_{2}$ interface located approximately 800 nm from the back contact. Because the electron affinities of RbGeI$_{3}$ and TiO$_{2}$ are 3.9 eV and 4.0 eV respectively, the conduction-band offset is only about 0.10 eV, forming a 0.10 eV downward step at the interface that assists electron extraction and suppresses interfacial recombination. The calculated valence-band offset at this interface is approximately 1.90 eV (using $E_{\\mathrm{v}}$(RbGeI$_{3}$) = $-$5.30 eV and $E_{\\mathrm{v}}$(TiO$_{2}$) = $-$(4.0+3.2) = $-$7.2 eV, giving $\\Delta E_{\\mathrm{v}}$ = |$-$5.30 $-$ ($-$7.2)| = 1.90 eV), creating a substantial energetic barrier that effectively blocks holes from entering the TiO$_{2}$ layer.',
          'At RbGeI$_{3}$/TiO$_{2}$ ($\\chi$ = 3.9 vs 4.0 eV, \\approx800 nm from the back contact) a 0.10 eV downward conduction step assists extraction while a 1.90 eV valence offset ($E_{\\mathrm{v}}$ = $-$5.30 vs $-$7.2 eV) blocks holes.'))
P.append(('Slight band bending near both heterojunctions reflects the built-in electric field established after contact formation, which drives photogenerated electrons toward the TiO$_{2}$/FTO electrode and holes toward the CuI HTL.',
          'Slight bending at the heterojunctions reflects the built-in field driving electrons to FTO and holes to CuI.'))
# ---- benchmarking ----
P.append(('The performance is competitive with the best tin-based lead-free devices (including the 26.40\\% CsSnI$_{3}$ device of Park et al. \\cite{r40} and the 25.98\\% MASnI$_{3}$ device of Islam et al. \\cite{r41}), while avoiding the Sn$^{2+}$ $\\rightarrow$ Sn$^{4+}$ oxidation that limits the long-term stability of tin-based absorbers. The proposed PCE also exceeds that of CZTS-HTL lead-free devices reported by Piñón Reyes et al. \\cite{r42}, confirming the competitiveness of the all-inorganic CuI HTL approach adopted here.',
          'The performance is competitive with the best tin-based devices (26.40\\% CsSnI$_{3}$ \\cite{r40}, 25.98\\% MASnI$_{3}$ \\cite{r41}) while avoiding Sn$^{2+}$ $\\rightarrow$ Sn$^{4+}$ oxidation, and exceeds CZTS-HTL devices \\cite{r42}.'))
P.append(('All comparator values in Table V were cross-checked against the primary sources; where an entry was internally inconsistent, the efficiency consistent with its reported V$_{\\mathrm{OC}}$, J$_{\\mathrm{SC}}$, and FF was adopted. All entries are SCAPS-1D simulation studies, including the Pindolia et al. entry (not an experimental study, despite occasional mischaracterization); the Loumachi et al. device string is ITO/\\allowbreak{}C$_{60}$/RbGeI$_{3}$/CBTS/\\allowbreak{}Ag (Section II).',
          'All comparator values were cross-checked against primary sources (adopting the efficiency implied by reported V$_{\\mathrm{OC}}$, J$_{\\mathrm{SC}}$, FF where inconsistent); all entries are SCAPS-1D simulations, and the Loumachi string is ITO/\\allowbreak{}C$_{60}$/RbGeI$_{3}$/CBTS/\\allowbreak{}Ag (Section II).'))
# ---- lit review ----
P.append(('highlighting the device structure, the photovoltaic performance, and the principal limitation of each work.',
          'highlighting structure, performance, and limitations.'))
P.append((' In particular, the entries for Pindolia et al. (2022), Loumachi et al. (2024), and Pathak et al. (2026) are quoted verbatim from the corresponding primary sources.',
          ''))
P.append(('Two structural details deserve explicit clarification to prevent citation-propagation errors. First, the ETL in the Loumachi et al. device \\cite{r22} is C$_{60}$ (buckminsterfullerene), frequently rendered ``C$_{60}$\'\' in the literature, and the subscript matters because ``C6\'\' is a different species. Second, the back contact is silver (Ag), not gold (Au), as stated in the primary source \\cite{r22}.',
          'Two details prevent citation-propagation errors: the Loumachi ETL is C$_{60}$ (not ``C6\'\') and its back contact is Ag, not Au \\cite{r22}.'))
# ---- contributions ----
P.append(('We first screen eight ETL--HTL combinations to identify the FTO/\\allowbreak{}TiO$_{2}$/RbGeI$_{3}$/CuI/\\allowbreak{}Au architecture as a promising candidate for inorganic-HTL optimization, and then run an eleven-step sequential optimization covering absorber thickness, absorber defect density, dielectric constant, electron affinity, bandgap, conduction- and valence-band effective density of states, ETL and HTL thicknesses, and the two interfacial defect densities.',
          'We first screen eight ETL--HTL combinations, then run an eleven-step sequential optimization of absorber, interface, and transport-layer parameters.'))
P.append(('Section II surveys recent literature. Section III describes the device structure and material selection. Section IV presents the methodology and optimization procedure. Section V reports and discusses the results, Section VI compares with prior literature, and Sections VII and VIII cover limitations and conclusions.',
          'Section II surveys literature; Sections III--IV describe device and methods; Section V reports results; Section VI benchmarks; VII--VIII close.'))
# ---- research gap ----
P.append(('SCAPS-1D solves the Poisson equation together with the electron and hole continuity equations self-consistently across the device stack \\cite{r19}, capturing carrier generation, transport, and recombination under either dark or illuminated conditions. The software allows the user to vary material and interface parameters independently, which makes it possible to disentangle their individual contributions to device performance. Figure 1 shows the graphical user interface of SCAPS-1D version 3.3.10 used in this study.',
          'SCAPS-1D solves Poisson, continuity, and drift-diffusion equations self-consistently \\cite{r19}, disentangling individual parameter contributions (Figure 1).'))
P.append(('The Pindolia study is broader than its shorthand citation in the secondary literature suggests. The paper systematically studied the effect of various HTL and ETL materials, layer thicknesses, doping concentrations, defect densities, back-contact work functions, and operating temperature in a broad multi-parameter sweep \\cite{r14}.',
          'That study swept HTLs, ETLs, thicknesses, doping, defects, contacts, and temperature broadly \\cite{r14}.'))
# ---- perovskite problem ----
P.append(('Lead raises contamination concerns at every stage of the device life cycle, from fabrication through operation to disposal \\cite{r9,r10}, and the search for benign substitutes based on tin (Sn), germanium (Ge), bismuth (Bi), and antimony (Sb) is now a central research direction \\cite{r11,r12}.',
          'Lead contamination concerns across the device life cycle drive the search for Sn, Ge, Bi, and Sb substitutes \\cite{r9,r10,r11,r12}.'))
P.append(('Recent density-functional-theory (DFT) calculations confirm a direct bandgap and a high optical absorption coefficient comparable to that of MAPbI$_{3}$ \\cite{r13,r17,r18}. The material is well suited to single-junction photovoltaics.',
          'DFT confirms a direct gap with MAPbI$_{3}$-comparable absorption \\cite{r13,r17,r18}.'))
# ---- QE ----
P.append(('Figure 4 tracks the quantum efficiency of the optimized cell, that is, how many collected carriers each incident photon yields. QE climbs from 34.52\\% at 300 nm to 49.18\\% at 350 nm and levels out near 100\\% at 400 nm. The suppressed ultraviolet response is surface recombination: high-energy photons are absorbed so close to the front that some carriers die before collection \\cite{r21,r38}.',
          'Figure 4 tracks the quantum efficiency: QE climbs from 34.52\\% at 300 nm to near 100\\% at 400 nm, the suppressed ultraviolet response being surface recombination of near-front absorption \\cite{r21,r38}.'))
P.append(('The integral shortfall is a deck-version difference, not physics: the QE spectrum was archived from the earlier sweep-campaign deck (the same deck generation that produced the the Section V.B sweep record offset discussed in Section V.H), whereas the J--V metrics come from the consolidated deck. Re-simulation with the consolidated deck gives identical J--V with flat or graded absorption endpoints ($\\Delta$JSC = 0.00 mA/cm$^{2}$), so no absorption-model difference can account for the gap.',
          'The shortfall is a deck-version difference, not physics: the QE spectrum comes from the earlier sweep deck while J--V uses the consolidated deck (flat/graded endpoints give identical J--V, $\\Delta$JSC = 0.00).'))
# ---- future ----
P.append(('with Ge$^{2+}$-stabilizing measures: GeI2-excess or hydrazine-type reducing additives, Lewis-base trap passivation (pyridine/thiourea routes reported for Ge/Sn perovskites), A-site alloying, and encapsulation, followed by long-term stability testing of the RbGeI$_{3}$/CuI stack.',
          'with Ge$^{2+}$ stabilization (reducing additives, trap passivation, alloying, encapsulation) and stability testing.'))
# ---- conclusion ----
P.append(('We started from eight configurations spanning two ETLs (TiO$_{2}$, PCBM) and four HTLs (NiO, CuI, CBTS, Spiro-OMeTAD). FTO/\\allowbreak{}TiO$_{2}$/RbGeI$_{3}$/CuI/\\allowbreak{}Au won the screening on durability, cost, and hole mobility rather than raw efficiency; its initial PCE was not the best of the eight, and it then held its gains through optimization. Its edge traces to band alignment, efficient charge extraction, low recombination, and clean transport at the interfaces. The choice is explicitly stability- and cost-constrained (CuI durability and cost, TiO$_{2}$ processing), not raw-efficiency-led: D2 (TiO$_{2}$/NiO, 21.10\\%) outscored D4 (19.78\\%) at screening.',
          'From eight ETL--HTL combinations, FTO/\\allowbreak{}TiO$_{2}$/RbGeI$_{3}$/CuI/\\allowbreak{}Au was selected on durability, cost, and alignment rather than raw efficiency (D2 outscored it 21.10\\% to 19.78\\% at screening).'))
P.append(('RbGeI$_{3}$ at 1.4 eV, in short, is a computationally promising absorber candidate subject to the realism bounds above. Joint',
          'Joint'))
P.append(('(Sections V.C, V.U-W, VI.B)',
          '(Sections V.C, V.J--V.L, VI.B)'))
# ---- GA tail decode compress ----
P.append(('(SCAPS SI-unit genes lognt = 18.14, lognif = 17.82, lognc = 23.03, lognv = 22.42 decode as $10^{18.14}$/m$^{3}$ = 1.37$\\times$10$^{12}$/cm$^{3}$, $10^{17.82}$/m$^{2}$ = 6.63$\\times$10$^{13}$/cm$^{2}$, $10^{23.03}$/m$^{3}$ = 1.08$\\times$10$^{17}$/cm$^{3}$, $10^{22.42}$/m$^{3}$ = 2.64$\\times$10$^{16}$/cm$^{3}$; best deck archived as round4\\_results/ga\\_best.def), giving',
          '(gene values and best deck archived), giving'))
P.append(('Jointly, N$_{\\mathrm{C}}$ = N$_{\\mathrm{V}}$ = 10$^{18}$ cm$^{-3}$ reaching 27.13\\% above the 26.81\\% headline is a direct OPAT interaction failure: the sequential 10$^{17}$ cm$^{-3}$ per-step optima do not survive joint evaluation, so Table III is retained as the documented reference, not as a claimed optimum.',
          ''))
# ---- stale affinity ref (V.E moved to Supplementary S1.3) ----
P.append(('whose valence maximum aligns with RbGeI$_{3}$ (0.10 eV offset, Section V.E);',
          'whose valence maximum aligns with RbGeI$_{3}$ (0.10 eV offset, Supplementary Section S1.3);'))
# ---- defect merge ----
P.append(('In the bulk, defects shorten carrier lifetimes and cut collection efficiency by acting as Shockley-Read-Hall (SRH) recombination centers. We swept the RbGeI$_{3}$ defect density from 10$^{12}$ to 10$^{18}$ cm$^{-3}$ with all else fixed.\nThe device tolerates defects up to 10$^{14}$ cm$^{-3}$ without visible loss; above that, PCE collapses from 20.40\\% to 7.58\\% as the density reaches 10$^{18}$ cm$^{-3}$, mostly through falling V$_{\\mathrm{OC}}$ (0.848 to 0.550 V). The sweep settles at 10$^{14}$ cm$^{-3}$, the bulk density SCAPS studies typically assume for lead-free absorbers.',
          'Bulk defects act as SRH recombination centers: swept from 10$^{12}$ to 10$^{18}$ cm$^{-3}$, the device holds to 10$^{14}$ cm$^{-3}$ without loss, then PCE collapses from 20.40\\% to 7.58\\% at 10$^{18}$ cm$^{-3}$ through falling V$_{\\mathrm{OC}}$ (0.848 to 0.550 V). The sweep settles at 10$^{14}$ cm$^{-3}$, the standard lead-free assumption.'))

P.append(('shows the energy alignment across the device: the 1.8 eV conduction-band offset at CuI/\\allowbreak{}RbGeI$_{3}$ blocks electron leakage to the back contact, while the 0.1 eV offset at RbGeI$_{3}$/TiO$_{2}$ aids electron extraction; both interfaces are thus electronically well passivated.',
          'shows clean extraction paths at both heterojunctions; both interfaces are thus electronically well passivated.'))
P.append(('Section II surveys literature; Sections III--IV describe device and methods; Section V reports results; Section VI benchmarks; VII--VIII close.',
          ''))
P.append(('supports a direct and tunable bandgap, and is less toxic \\cite{r13}.',
          '\\cite{r13}.'))
n = 0
for a, b in P:
    if a in m:
        m = m.replace(a, b)
        n += 1
    else:
        print('MISS:', repr(a[:90]))
        # fallback: normalize double-space/newline differences
        ax = re.sub(r'\s+', ' ', a)
        found = False
        for mm in re.finditer(re.escape(ax[:60]), re.sub(r'\s+', ' ', m)):
            print('  near-miss at', mm.start())
            found = True
            break
        if not found:
            print('  no anchor at all')
print('applied %d/%d' % (n, len(P)))
m = m.replace('TRIMMED-V2-MARK', '')
m += '\n% TRIMMED-V2\n'
open(TEX, 'w').write(m)
