# Journal of Applied Physics submission package — RbGeI₃ SCAPS-1D study

Source: `aip_advances/manuscript.tex` (already a REVTeX 4.2 AIP conversion of
`solar_submission/manuscript.tex`, r8 frozen-deck rebase), re-tagged and
recompiled for the Journal of Applied Physics. JAP is single-blind
(anonymous reviewers, named authors), so authors appear throughout.

Three changes from the AIP Advances build:

1. `\documentclass[aip,amsmath,...]` → `\documentclass[aip,jap,amsmath,...]`
   (selects the JAP substyle, drops the running title).
2. **Cross-reference fix.** In the AIP Advances `.tex`, every `\label{fig:…}` /
   `\label{tab:…}` sat *before* its `\caption`, so LaTeX picked up the
   enclosing section counter instead of the float counter. The compiled PDF
   cited "Fig. V V.C" 27 times and "Table V V" 16 times. All 32 labels are now
   placed after `\caption{…}`, and references resolve to Fig. 1–24 and
   Table I–VIII. Rebuild-verified: 0 undefined, 0 multiply-defined labels.
3. **Displayed equations punctuated.** All four (`eq:poisson`–`eq:pce`) ended
   bare; AIP style requires punctuation. The lead-in now ends with a colon and
   the equations carry commas, so they read as part of the sentence
   ("…for details): (1), (2), (3), where ε is the permittivity…").

Everything else in the `.tex` already satisfies AIP's general guidelines.

## Content audit (referee-style) and the fixes applied

A content referee pass over `manuscript.pdf` + `supplementary.pdf` raised
scope, consistency and arithmetic points. Each was re-verified against the
source before anything was changed; the fixes below are the ones that were
confirmed, the rest are recorded as open risks.

**Fixed (verified in the source):**

| # | Defect | Fix |
|---|---|---|
| 1 | Table VI printed **2025** for `\cite{r42}`, whose own `\bibitem` is Micromachines **12**(12), 1508 (**2021**) | year → 2021 |
| 2 | Conclusion cited "Sections V.C, V.J–V.L" — §V has only eleven subsections (A–K), so **V.L does not exist**; the doping/resistance/mobility trio is really V.I–V.K | → "V.I–V.K" |
| 3 | §III.C: "the optimized 700 nm (Section V.G)" — V.G is Uncertainty quantification; the thickness step is in V.B | → "Section V.B" |
| 4 | §IV.D: "Section V.G reports a genetic-algorithm joint search" — the GA result is `fig:ga` | → cited `Fig. 7` directly |
| 5 | Cover letter claimed the same-stack CsGeI₃ control "isolat[es] the **A-site cation effect**" — the manuscript says the opposite (Table VII caption and §VII.B: "evidence about gap-plus-alignment, not A-site chemistry proper") | → "isolating a band-gap effect at fixed electron affinity rather than A-site chemistry" |
| 6 | Cover letter claimed Supplementary S1–S7 "give the SCAPS decks, run scripts, and archived result files" — the supplement *names* them; the Data Availability Statement says "upon reasonable request" | → cover letter now matches the Data Availability Statement |
| 7 | Cover letter presented the β-CsPbI₃ calibration without the manuscript's own qualifier that it tests the *solver*, not the device | qualifier added |
| 8 | Cover letter presented the oxidation thermodynamics without the manuscript's own "CsGeI₃ DFT transferred by framework analogy / equilibrium is a lower bound" caveats | caveats added |
| 9 | `alt_text.txt` Figure 5 said efficiency had "a spread under 2 percentage points"; the manuscript reports mean 24.86 ± 1.77 % with a 5th/95th range of 22.23–27.79 % (5.6 pp) | → "a standard deviation of 1.8 percentage points" |
| 10 | `supplementary.pdf` S6 pointed at "main-text **Fig. 25**" — the main text has 24 figures; the oxidation figure is 24 | → `Fig. 24` (source `solar_submission/supplement.tex`, rebuilt) |
| 11 | `supplementary.pdf` Table S4 sourced initial parameters to "Table II"/"Table IV" — those are the main text's screening and optimized-parameter tables; the initial-parameter tables are the supplement's own S2/S3 | → `Table S2` / `Table S3` |

**Raised but not fixed — these are yours to decide:**

1. **Scope (the referee's headline objection).** 27.06 % is within 0.15 pp of
   the best prior RbGeI₃ simulation (27.21 %, Loumachi et al.) and the study is
   a one-at-a-time sweep on an already-swept material, which is close to what
   JAP's Articles policy disclaims. The paper's defence is the BSF interface
   attribution, the thermodynamic→process-spec translation and the stacked
   loss budget, which is also what the cover letter now leads with. No edit
   can fix this; it is an editor's call.
2. **Printed-Row arithmetic.** The referee reported that 5 of ~25 printed
   (V_OC, J_SC, FF, PCE) rows fail recomputation. Re-checking with a
   display-rounding tolerance (V_OC ±0.005 V alone allows ±0.12 pp in PCE)
   leaves **one** genuine outlier: the Table VIII "Wang champion (measured)"
   row, whose printed PCE of 18.40 % needs V_OC ≈ 1.122 V while the table
   prints 1.11 V. That row is a digitized literature value and its J_SC is
   already printed as "~20.0", so the most likely reading is that the source
   rounds differently — but the paper does not say so. Table V already carries
   "PCEs are unrounded SCAPS outputs (displayed inputs rounded)"; Table II does
   not. Adding that half-sentence to Table II's caption would close the point
   without touching any number.
3. **Adopted-device disclosure.** The referee asked for the interface electron
   and hole thermal velocities (E_t/σ inputs) actually used for the adopted
   device. Not found in the manuscript; the referee could not check it either.
4. **Novelty/positioning.** Every listed contribution is a documented sweep
   plus a control; the abstract does not name a novelty claim, which JAP
   requires, but it also does not clearly state what is new. Reframing the
   abstract's last sentence is an authorial decision.

## Journal facts (verified Oct 2026)

- **Journal of Applied Physics** (AIP Publishing), ISSN 0021-8979 print /
  1089-7550 web, weekly. Scope: important new experimental *and theoretical*
  results in applied physics; the relevant coverage lines are **photovoltaics**,
  **physics of devices and sensors**, **physics of semiconductors**, and
  **thin films, interfaces, and surfaces**.
- **Article types**: Articles, Methods, Reviews, Perspectives, Tutorials.
  This manuscript is submitted as an **Article** (original research study).
- **Length**: no main-text word or page cap for Articles; JAP has **eliminated
  all page charges**, including excess page charges, and "the editors will
  decide whether the manuscript's length is appropriate". Ours: **40 pp**.
- **Abstract**: one paragraph, approximately 250 words, no displayed equations,
  footnotes, references, graphics or tables. Ours: **206 words** (a stricter
  whitespace count gives 201; both well under the cap), 0 `\cite`.
- **Order**: Title, authors, affiliations, abstract, text, conclusion,
  supplementary-material section, acknowledgments, author declarations
  (conflict of interest, ethics, author contributions), data availability,
  appendixes, references. All met.
- **Initial submission**: a single compiled manuscript **PDF** with figures
  embedded (AIP explicitly asks you *not* to upload separate figure files at
  initial submission) plus a separate **supplementary PDF**. Alt text is a
  revision-stage requirement.
- **Editorial policy checks passed**: JAP says "routine experiments or
  calculations that simply extend previous methods to a new system are not
  appropriate unless the results are used to significantly advance the solution
  of an important problem", and asks authors to **avoid novelty claims**
  ("novel", "for the first time", …). The manuscript contains no such claims
  (grep-verified), and its stated contribution is mechanism plus a process spec,
  not a parameter sweep. See the risk note below.
- **Open access**: hybrid. Standard publication is subscription-funded (no
  mandatory APC); JAP is also part of AIP's **Subscribe to Open** pilot.
- **Submission portal**: Peer X-Press — `jap.peerx-press.org` (same system as
  the AIP Advances package).
- **Roman section/table numbering kept**: AIP style numbers tables with Roman
  numerals (I, II, III, …) and figures with Arabic numerals. REVTeX renders
  both, so all in-text cross-refs (V.B, Table VI, Fig. 12, …) stay valid.

### Format audit (measured, not assumed)

| Check | Result |
|---|---|
| Length | 40 pp single-column `preprint`. JAP publishes **no page or word cap** for Articles (0 page charges), but "the editors will decide whether the manuscript's length is appropriate" — 40 preprint pp ≈ 20 two-column pp, long for JAP's norm. Nothing violated; norm risk only. |
| Abstract | **206 words**, one paragraph, 0 `\cite`, no equations/graphics/tables. ✓ (≤ ~250) |
| References | 56 `\bibitem`, **56 distinct citations**, 0 never-cited, 0 cited-but-undefined. ✓ |
| Figures | 24, cited in text in order 1–24, Arabic numerals, every one captioned. ✓ |
| Tables | 8, Roman numerals I–VIII, cited in text. ✓ |
| Text footnotes | none (the 6 `\footnote` grep hits are `\footnotesize` inside tables). ✓ |
| Page numbers | consecutively numbered to 40. ✓ |
| Novelty claims | none ("novel", "for the first time", …) — JAP explicitly forbids them. ✓ |
| **Figure resolution** | AIP wants 300 dpi for colour online. At the **one-column width (3.37 in) every figure is 440–926 dpi ✓. At the two-column width (6.69 in) all but fig32 and fig38 fall to 222–287 dpi ✗.** `fig2.png` is stored at 150 dpi and `fig15.png` carries no DPI tag at all. → Place figures one-column, or re-export any two-column candidate at ≥ 2000 px wide. |
| **Embedded widths** | Figures are embedded at 0.70–1.0 `\linewidth` ≈ 4.5–6.5 in in the single-column preprint — i.e. **neither** AIP's 3.37 in (1-col) **nor** 6.69 in (2-col). Production will rescale; not a submission blocker, but it is not "sized precisely as you want them to appear". |
| **Equations** | 4 displayed equations, numbered on the right and now **punctuated** (comma after each, colon before the block). ✓ |
| **Alt text** | 32 entries (24 figures + 8 tables), `Figure N:`/`Table N:` labels with no file names, every description **25–50 words**, ends with a period. ✓ (script-verified) |
| Class option | `preprint` (inherited from the AIP Advances build). AIP's Overleaf template default was **not** verified; both `preprint` and `reprint` are accepted for initial submission. |

### Deliberate deviations from the Elsevier version (inherited from the AIP build)

Abstract citation removed (AIP rule); three orphan references (r5, r6, r38)
cited in place; `tabularx`/`X`-columns → `tabular*` (revtex4-2 clash);
sentence-case title per the AIP Style Manual.

## Contents

| File | Role |
|---|---|
| `manuscript.tex` | REVTeX 4.2 source, `aip,jap` substyle (compiles clean: 0 errors, 0 undefined citations) |
| `manuscript.pdf` | Compiled review PDF, 40 pp, figures embedded |
| `figures/*.png` | 24 PNGs, flat, bare filenames (PXP-safe) |
| `supplementary.pdf` | Supplement S1–S7 (18 pp; cross-references to the main text corrected — see the content audit below) |
| `cover_letter.txt` | Cover letter (JAP does not require one; provided anyway) |
| `alt_text.txt` | Alt text for 24 figures + 8 tables (required at revision). AIP format: `Figure N:` / `Table N:` labels, no file names, one to two sentences each, all 32 entries in the 25–50-word band. |
| `highlight_image.png` | **Does not meet the highlight-image spec:** 2850 × 1260 px (aspect 2.26 vs the required 8.0139 × 6.2739 in, aspect 1.28) and PNG, but AIP accepts only EPS, TIFF or JPEG here. Replace before the revision stage. |
| `JAP_upload.zip` | One-file upload bundle (tex + figures) |

## Build (reproduce the PDF)

```bash
cd jap_submission
pdflatex -interaction=nonstopmode manuscript.tex   # 3 passes for natbib
pdflatex -interaction=nonstopmode manuscript.tex
pdflatex -interaction=nonstopmode manuscript.tex
```

## Upload checklist (Peer X-Press)

1. Manuscript file → `manuscript.tex` (+ `figures/*.png`, or the zip).
2. Author-generated review PDF → `manuscript.pdf` (overrides the system PDF).
3. Supplementary → `supplementary.pdf`.
4. Cover letter → paste `cover_letter.txt` (optional for JAP).
5. Article type → **Article**.
6. Declarations to enter in PXP: COI none; no funding; no human/animal
   subjects (no ethics statement needed); ORCID iDs if available.
7. Alt text → at revision (compliant, prepared here). Highlight image → at
   revision, and it **needs replacing first** (see Contents).

## ⚠️ Confirm before submitting

1. **Duplicate-submission risk — confirmed, act first.** `solar_submission/SOLMAT-D-26-02796.pdf`
   is a *Solar Energy Materials and Solar Cells* manuscript draft of this same
   paper, and `solar_submission/revision/SOLMAT-D-26-02796_latex.zip` is the
   uploaded source bundle; it was submitted 2026-10-12, four days ago, and no
   decision is recorded in the repo. The cover letter asserts the work "is not
   under consideration elsewhere". Submitting to JAP while SOLMAT holds the
   manuscript is duplicate submission, and it sinks both. Withdraw from SOLMAT
   (or wait for the decision) before using this package.
2. **Fit risk (desk-reject).** JAP's Articles policy explicitly disclaims
   calculations that only extend known methods to a new system. The cover
   letter therefore leads with the BSF attribution, the oxidation thermodynamics
   → process-spec translation, the stacked loss budget and the experimental
   calibration, not with the 27.06% number. If an editor pushes back on scope,
   the realistic fallbacks are *Journal of Renewable and Sustainable Energy*
   (AIP, same template) or *Solar Energy Materials and Solar Cells*.
3. **Author Contributions (CRediT)** in `manuscript.tex` is a best-effort
   draft written during the AIP conversion — verify the roles against what
   Fahim and Siddiquee actually did.
4. PXP author order/metadata must match the manuscript (Fahim first,
   Siddiquee corresponding).
5. Verify at submission time: the PXP URL, and whether AIP currently asks for
   alt text at initial submission or only at revision.
