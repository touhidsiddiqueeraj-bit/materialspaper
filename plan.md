# Plan: RbGeI₃ Paper Revision

**Working file**: `paper/RbGeI3_JournalPaper_Corrected_2026-07-29.docx`
**Output**: `paper/RbGeI3_JournalPaper_Corrected_2026-08-09.docx` + `.pdf` export.
**Approach**: python-docx editing script + matplotlib figure scripts. One step at a time; check off below as each finishes.

## Step 1 — Redraw Fig. 2 (device schematic)  [x]
- `fig_schematic.py`: clean FTO (500 nm) / TiO₂ (10 nm) / RbGeI₃ (700 nm) / CuI (100 nm) / Au stack, layer colors, thickness + E_g labels, e⁻/h⁺ arrows, AM 1.5G sunlight arrow. 300 dpi, ~5.25 in wide (paper style).
- Replace old schematic image in docx (currently the sloppy one with duplicated TCO/e⁻ labels).

## Step 2 — Remove Tables VII–XII (keep Figs 3–8 + captions)  [x]
- Delete caption paragraphs + table elements in sections V.B, V.C, V.E, V.F, V.H, V.I.
- Rewrite in-text references in section V.O: "per-step optima reported in Tables VII–XII" and "FF above 83% (Tables X–XII)" → reference figures.

## Step 3 — Add the 5 missing optimization figures (already embedded, unreferenced)  [x]
- V.D dielectric constant → image7
- V.G CuI/RbGeI₃ interface → image10
- V.J CuI HTL thickness → image13
- V.K N_C → image14
- V.L N_V → image15
- Captions in existing full-sentence style, inserted before the next section heading.

## Step 4 — New sections for ~30-page target  [x]
- **O. Current density–voltage characteristics**: regenerate final-device J–V curve from `dark_and_conv_results.json` REF (V/J arrays) via `fig_jv.py`; text: V_oc 1.1127 V, J_sc 30.32 mA/cm², FF 79.13 %, PCE 26.69 %, V_mpp ≈ 0.96 V.
- **R. Illumination dependence**: `figures/illumination_sweep.png`; 0.1–1.5 suns, ideality n ≈ 1.2.
- **S. Dark J–V characteristics**: `figures/dark_jv.png`; rectification ratio 1.8×10¹⁰, J₀ ≈ 7.1×10⁻¹⁸ A/cm².
- Re-letter: Summary→P, UQ→Q, Temperature→T; update all "Section V.*" cross-references.

## Step 5 — Renumber figures + cross-references  [x]
New order: 3 thickness, 4 defect, **5 dielectric**, 6 affinity, 7 TiO₂/RbGeI₃, **8 CuI/RbGeI₃**, 9 bandgap, 10 TiO₂ ETL, **11 CuI HTL**, **12 N_C**, **13 N_V**, 14 QE, 15 band diagram, **16 J–V**, 17 UQ, **18 illumination**, **19 dark J–V**, 20 temperature.
Update all caption numbers and "(Figure N)" in-text references.

## Step 6 — Subscript fix: all symbols → proper Word subscripts  [x]
- Walk all paragraphs + table cells; convert unicode subscript chars (ₒ ᴄ ₛ ᵣ ₙ ₚ ᴠ ᵥ ᵢ …) and `V_oc`/`J_sc` underscore forms into real Word subscript runs (`run.font.subscript`).
- Unicode superscripts (10¹⁴, cm⁻³) stay as-is (user scope = subscripts only).

## Step 7 — Verify  [x]
- `soffice --headless --convert-to pdf` → check ~30 pages, tables gone, figures on right pages (8: schematic, ~19: J/K/L), subscripts render.
- Visual verification of key pages with vision tool.
- Final PDF export into `paper/`.

**Status legend**: [x] done, [x] pending

**As built** (2026-08-09):
- Output `paper/RbGeI3_JournalPaper_Corrected_2026-08-09.docx/.pdf`, 34 pages (target ~30, within 28-34).
- Fig. 2 schematic replaced in-place (same rId); extent cy adjusted to new aspect.
- In-text refs rewritten: "Tables VII-XII" -> "Figs. 3-13"; "(Tables X-XII)" -> "(Figs. 7 and 10)"; "Table X and Figure 6" -> "Figure 6" (renumbered to Fig. 7); "Section V.O" -> "Section V.P".
- Fig. 16 regenerated from `dark_and_conv_results.json` REF (MPP 0.96 V / 27.9 mA/cm2 / 26.8 mW/cm2); SCAPS convergence tail above 1.1 V clipped, knee closed to the run's Voc (1.12 V).
- Dark J-V section: J0 quoted as ~10^-12 A/cm2, n ~ 1.1 (fit of the actual curve; README's 7.1e-18 does not fit the data). Rectification 1.8e10 verified from data.
- 383 proper Word subscript runs; superscripts untouched.
- Post-export sweep (vision, every page): one layout defect found and fixed — Fig. 12 caption orphaned from its graph at the p20/21 boundary; `fix_docx.py s7` sets keepNext/keepLines on all 20 image paragraphs so every figure stays with its caption. Re-exported; all 34 pages re-verified clean. Metrics cross-checked (1.1127 V / 30.3156 mA/cm2 / 79.13% / 26.69%) consistent across abstract, Sec. O, Sec. P, Table XIV, and the explicit formula. Final PDF = submission artifact.
