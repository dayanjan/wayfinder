# Manuscript critical review + resolution — 2026-07-11 (overnight)

Five-reviewer critical pass on the revised Wayfinder manuscript (after figures + related-work + evidence-
strengthening + genomics correction), then a consolidated fix pass. Reviewers: **4 Claude agents** (skeptical
journal referee; T-cell immunology & statistical genetics; LBD/methods & related-work; applied statistics &
figure-JSON consistency) + **1 Codex** (gpt-5.6-sol, read-only adversarial). Raw Codex review:
`codex-adv_manuscript_2026-07-11.md`. Verdict across the board: unusually candid manuscript; a few real
lapses **against** its own calibration standard, one arithmetic P0. All P0s + substantive P1s fixed below.

## P0 (blocking) — all CONVERGED across reviewers, all FIXED
| # | Finding | Fix applied |
|---|---------|-------------|
| P0-1 | §4.1 funnel: "43 … 30 + 10 + 3 + 1" enumerates **44 ≠ 43**; prose contradicted Fig 2 | Rewrote §4.1 + §3.2: **43 supported = 30 clean + 10 weak + 3 flagged; +1 refuted-effect; +21,995 refuted-disease = 22,039**. Matches Fig 2 + gate_grid JSON (disease_c_supported_total=43). |
| P0-2 | §4.1 "referee supports **395**/47,220" vs §4.1b "disease hop supports **406**" — unreconciled | Added clause: of the 406 whose disease hop passes, 395 also clear QC/effect/program; gate culls 395→43. |
| P0-3 | §4.2 "confident, receipt-backed no" showcased on SLC1A5, a **borderline FDR miss (0.054)** + substrate-inherited | Added calibration: SLC1A5's no sits at the substrate FDR boundary and is substrate-inherited; the referee's *own* confident-no is located in the QC gate (IL2; ~1-in-6 out-of-funnel). |

## P1 (important) — FIXED
- **§4.1b vs §4.2b count clash (2,430 vs 1,914):** reconciled — 1,914 = identifier-resolved subset of the 2,430 failed-KD genes (11,415 of 12,539 in T4 have a resolvable ID). Verified against `hard_negatives.py:14`.
- **§2.4 overgeneralization** (Codex): softened "what none of them does" → "we are not aware of"; fixed "receipts are citations or model confidence" to be system-specific (Robin/Coscientist run *new* experiments; the real axis is *held, pre-existing* substrate). Methods reviewer independently verified every §2.4 competitor claim as **fair/accurate, no strawman**.
- **§4.4 cis-effect** (Codex + immunology converged): the corrected ~43 kb promoter separation makes promoter cis-spread *a priori* weak → the STAT6-unmoved result is confirmatory; dropped "overlapping 3′ ends" as a promoter-repression mechanism (it's 3′ read-through, not promoter spread); softened "refuted" → **"no detectable STAT6-expression cis-effect at Stim8hr"** with explicit scope (aggregate null ≠ all cis channels).
- **§4.3 "not a 12q13 locus artifact"** → qualified: "not a *locally colocated* gene-set artifact; LD provenance of the label remains open (§4.4b)."
- **§4.3 "found zero papers"** (LLM audit stated as fact) → "surfaced no papers … a targeted agent search, not an exhaustive review; novelty in the surfaced literature, not proven absence."
- **§4.6 "strongest evidence the finding is a property of the data"** → softened to computational reproducibility (not biological validity).
- **Abstract** now names the un-dischargeable 12q13 confounder, not only the falsified cis one.
- **§5.2 direction/"brake"** (Codex + immunology): added data provenance (exploratory public-expression mining, accessions in project record, outside the substrate) + hedged the brake reading on the **sign** of the Th2 shift under NAB2-KD (the substrate doesn't settle it → advanced as the directional *question*).
- **§5.3** adds a "one flagship worked to depth; the rest nominated" limitation (pre-empts the n=1 objection).
- **Moreau 2023 misapplied** to the obscurity claim (Methods reviewer): re-pointed the obscurity sentence to **Stoeger 2018** ("ignorome"); kept Moreau for the evaluation sentence.
- **Genomics** verified base-pair-exact against Ensembl by the immunology reviewer (72 bp 3′ overlap; 43,096 bp TSS-TSS); no stale "1.9 kb" in the `.tex`.
- **Bib quality:** fixed `\&amp;` → `\&` (cheng2021); added stoeger2018, collins2008, lensch2022, etc. (all DOIs resolved-verified).

## Deferred / submission TODOs (low priority; not blocking on the paper's own terms)
- `plausibility2026` (arXiv:2606.01042) byline unverifiable headlessly → placeholder "Byline pending"; fill before journal submission.
- Frontiers author-year bib style + article template at submission (README).
- Optional polish not applied: trim the CS $6.41/scriptability detail to supplementary (§4.5); one-line PerTurboAgent cite; 12q13→12q13.3 once; a fully-worked second survivor (EGR2) — handled instead by the n=1 limitation.
- Frozen markdown source (`docs/manuscript/sections/*.md`) still carries the old "1.9 kb"/"Figure 5"; the `.tex` is authoritative (README says so). Sync or delete the markdown before release if desired.

Build after fixes: **32 pages, 0 errors, 0 undefined citations, 0 bibtex warnings.**
