# AIP Advances submission package — RbGeI₃ SCAPS-1D study

Source: `solar_submission/manuscript.tex` (r8 frozen-deck rebase) converted
to the official AIP REVTeX template (`revtex4-2`, `aip`, `preprint`).
AIP Advances uses single-blind review — authors appear throughout.

## Journal facts (verified Oct 2026)

- **AIP Advances** (AIP Publishing, online ISSN 2158-3226), broad
  physical-sciences scope, soundness-based review (technical correctness,
  not impact). Submission via **Peer X-Press**:
  aipadvances.peerx-press.org.
- **No strict page limit** for Regular Articles (cf. MMM contributed
  3500-word / APL 3000-word caps, which do not apply here).
- **APC $1,800** on acceptance, CC BY, authors retain copyright. Ability
  to pay is not visible to editors/reviewers and does not affect the
  decision (pcr@aip.org).
- **Abstract**: one paragraph, ≤250 words, no refs/equations/graphics
  (ours: 193 words, citation-free).
- **Order**: Title, authors, affiliations, abstract, text, conclusion,
  supplementary-material section, acknowledgments, author declarations
  (COI + CRediT), data availability, appendixes, references. All met.
- **Initial submission**: single compiled manuscript PDF (figures
  embedded) + separate supplementary PDF.
- **Figures**: embedded via `\includegraphics`; 1-column max 3.37 in,
  2-column 6.69 in; PNG accepted. Tables numbered with Roman numerals
  (kept), figures Arabic. Roman section numbering kept so all in-text
  cross-refs (V.B, Table VI, …) stay valid.
- **Deliberate deviations from the Elsevier version**: abstract citation
  removed (AIP rule); 3 orphan references (r5, r6, r38) cited in place;
  `tabularx/X-columns` → `tabular*` (revtex4-2 clash); sentence-case
  title per AIP Style Manual.

## Contents

| File | Role |
|---|---|
| `manuscript.tex` | REVTeX source (compiles clean: 0 errors, 41 pp) |
| `manuscript.pdf` | Compiled review PDF (figures embedded) |
| `figures/*.png` | 24 PNGs, flat, bare filenames (PXP-safe) |
| `supplementary.pdf` | Supplement S1–S7 (18 pp, from solar package) |
| `alt_text.txt` | Alt text for 25 figs + 8 tables (required at revision) |
| `highlight_image.png` | Candidate highlight image (2850×1260 @300 dpi; spec is 8.0139×6.274 in — production may crop) |
| `cover_letter.txt` | Cover letter |
| `AIP_Advances_upload.zip` | One-file upload bundle (tex + figures) |

## Upload checklist (Peer X-Press)

1. Manuscript file → `manuscript.tex` (+ `figures/*.png`, or the zip).
2. Review PDF → `manuscript.pdf` (author-generated PDF overrides system PDF).
3. Supplementary → `supplementary.pdf`.
4. Cover letter → paste `cover_letter.txt`.
5. Alt text + highlight image → at revision (prepared here).
6. Declarations to enter in PXP: COI none; no funding; no human/animal
   subjects (no ethics statement needed); ORCID iDs if available.

## ⚠️ Confirm before submitting

1. **Author Contributions (CRediT)** in `manuscript.tex` is a best-effort
   draft (`% TODO`) — verify roles for Fahim/Siddiquee.
2. PXP author order/metadata must match the manuscript (Fahim first,
   Siddiquee corresponding).
3. APC $1,800 readiness.
