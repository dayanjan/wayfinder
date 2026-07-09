# Orthogonal check — NAB2 in DepMap (Cancer Dependency Map) · 2026-07-09

**Question asked:** does an orthogonal, independent experimental system — DepMap's genome-scale
CRISPR/RNAi *fitness* screens across ~1,200 cancer cell lines — support pursuing **NAB2** (a
transcriptional corepressor; the T-cell finding is NAB2 → Th1/Th2 → atopic eczema)?

**Source:** DepMap portal gene page for NAB2 (NGFI-A binding protein 2; MADER; 12q13.3;
ENSG00000166886; Entrez 4665), DepMap Public 26Q1+Score. Evidence screenshot:
`depmap-nab2_overview_screenshot.png` (captured 2026-07-09).

## Verdict: NEGATIVE for a cancer target; NON-CONTRADICTORY for the T-cell finding

### Evidence (read off the page)
| Axis | Value | Reading |
|---|---|---|
| **CRISPR dependency** | **4 / 1208** cell lines | Non-dependency; gene-effect distribution sits on 0, far from the −1 essential line |
| **RNAi dependency** | **1 / 710** cell lines | Non-dependency (orthogonal knockdown assay agrees) |
| **Lineage selectivity** | none evident (Other Solid / Other Heme ~0) | Not selectively essential in any tumor type |
| **Target tractability** (CanSAR) | Bioactive compounds **No** · Druggable structure **No** · Ligand-based **No** · Enzyme **No** | No classical druggable modality |
| **Predictability** | CRISPR 30.7th pct (acc 0.143), RNAi 2.29th pct (acc 0.063) | Dependency is poorly predictable = weak/uninformative |
| **Top CRISPR co-deps** | S100A7A 0.34, PLCD3 0.34, PLA2G2C 0.34, LYPLA1 0.26, BID 0.23 | Weak; **no EGR family** → no functional-network corroboration |
| **Top RNAi co-deps** | ANGPTL2 0.27, TRNAU1AP 0.25, PRC1 0.24, RHOB 0.23, ETFBKMT 0.23 | Weak; no coherent immune/Th program signal |
| **Mutations** | missense (~22 lines), stop/splice, frameshift (~7) | Background-level; no recurrent driver hotspot |

### Interpretation (calibrated)
1. **As a cancer drug target → do NOT pursue via DepMap.** NAB2 is not a fitness dependency (4/1208
   CRISPR, 1/710 RNAi), shows no lineage selectivity, and carries **no tractability flags**. Its known
   oncogenic context (the NAB2–STAT6 *fusion* in solitary fibrous tumor) is a rare mesenchymal tumor
   essentially absent from the DepMap panel, so it is not captured here — but the pan-cancer verdict is
   an unambiguous negative.
2. **This null does NOT refute the T-cell finding.** DepMap measures "is NAB2 required for cancer-cell
   proliferation"; our finding is "NAB2 regulates the Th1/Th2 program in CD4 T cells." Different assays —
   a gene can be a pivotal immune-state regulator without being a cancer fitness gene. A flat DepMap
   dependency is *expected* and *consistent* with an immune-regulator role. DepMap is simply the **wrong
   orthogonal validator** for a T-cell-state regulator (the right one is immune / primary-T-cell
   perturbation data, which we already have).
3. **No EGR-network corroboration.** NAB2's co-dependencies do not surface its known EGR partners
   (EGR1/2/3) — so DepMap offers no cross-context support for the NAB2→EGR→Th-program wiring either.
4. **One weak, honest curiosity:** the top CRISPR co-dependency is **S100A7A (psoriasin)** — a skin
   antimicrobial protein associated with atopic dermatitis/psoriasis — at r=0.34. Weak and likely
   coincidental; noted, not over-read.

### Why this matters for the drug-target framing
DepMap/CanSAR's "not druggable" is the concrete confirmation of the **regulator ≠ tractable drug target**
gap: NAB2 scores high novelty + high effect in our pipeline but **low tractability** here. This is the
strongest argument for adding a **tractability layer** (Open Targets / CanSAR) to the LBD output so
nominations are ranked by druggability, not just by novelty and effect. (See also: eczema is a skin-surface
disease, which reopens *non-classical* modalities — topical nucleic-acid knockdown — that a systemic
"undruggable" verdict does not consider.)
