# Finding — a receipt-backed, near-novel T-cell → disease hypothesis the dataset itself proposed

**Method in one line:** the dataset came with no question, so we used literature-based discovery
(Swanson ABC) to *generate* the highest-value **untested** gene→program→disease questions it could
resolve, then had the deterministic **data-referee** answer each one against the four Perturb-seq
tables. LBD proposes; the referee culls. (Full method: `docs/lbd-proposer-spec.md`; build log:
`docs/lbd-build-log.md`.)

## The honest funnel (Stim8hr, CD4+ T-cell Perturb-seq)
The proposer is **answer-free**: the candidate gene set comes only from the knockdown-QC gate and
the DE effect tables (never from any disease answer or the referee's own output). Novelty comes
only from *external* literature (Europe PMC) and curated associations (Open Targets). The referee
runs *after* generation and can refute.

| Stage | Count |
|---|---|
| A universe (KD-gated, program-significant regulators) | 3,935 genes |
| Candidate (gene × disease) questions after literature/known gate | 22,039 |
| Referee **disease-C-supported** | 43 |
| Referee **CLEAN full-chain supported** (gate+effect+program+disease all hold, effect>0) | **30** |
| — of which empty-effect (excluded) / off-target-flagged / effect-refuted | 10 / 3 / 1 |
| Refuted for the specific disease (the cull) | 21,995 |

*The generate→cull ratio is the point:* 22,039 machine-generated questions, culled by real data
receipts to 30 clean supported. Nothing is asserted that a table value does not back.

## The standout: NAB2 → Th1/Th2 polarization → atopic eczema (@ Stim8hr)
A **near-novel** link (6 prior literature co-mentions; no curated Open Targets association,
score 0.038) that the data **supports with a receipt at every hop**:

| Hop | Status | Receipt |
|---|---|---|
| 0 · knockdown-QC gate | supported | 2/2 guides significant, best adj-p 1e-16 (guide expr 0.056 vs NTC 0.567) |
| 1 · effect | supported | on-target KD, effect −16.9, **301 downstream DE genes, no off-target flag** |
| 2 · program (Th1/Th2) | supported | Th1-associated in Ota 2021 (z 7.71, adj-p 1.96e-13); **not significant in Hollbacker 2021 (1 of 2 contrasts)** |
| 3 · disease (exact = atopic eczema) | supported | member of 2 atopic-eczema-enriched clusters: OR 3.90 FDR 0.0028; OR 3.43 FDR 0.0224 |

**Calibrated claim:** *consistent with a re-derived NAB2 → Th1/Th2 → atopic-eczema chain that the
literature has barely made.* Not "proven," not "discovered."

**Honest caveats (do not overclaim):**
- **Near-novel, not novel.** ac_lit=6 is a low, un-normalized Europe PMC count — it means *little
  prior literature*, not "well-established" and not "zero."
- **One of two program contrasts** is significant (Ota strong; Hollbacker n.s.) — reported, not hidden.
- **Mechanistic plausibility is a hypothesis-strengthener, not evidence:** NAB2 is the transcriptional
  corepressor of EGR2 (this project's independently-validated hero gene). That makes the hypothesis
  *interesting*; the *finding* is the receipt above, not the EGR2 relationship.

## The cull is real (honesty examples from the same run)
- **NUDT1 × type 1 diabetes** — the *only* pure-disjoint (zero-literature) supported hit, but a
  **trivial effect (4 downstream DEs)** and a borderline program shift. This is why we *rank* by a
  novelty+effect score rather than hard-gate on zero literature: strict literature-absence tracks
  obscurity, not importance.
- **DNAJB9 × type 1 diabetes** — supported chain but **off-target-flagged** at the effect hop (a caveat, surfaced).
- **SBF2** — effect **refuted**; correctly excluded from the supported set.
- **21,995** proposed questions refuted for the specific disease.

## Reproducibility
```
python -m pip install -r requirements.txt
PYTHONPATH=src python -m arbiter.lbd.verify_disease_ids     # re-verify disease→MONDO map
PYTHONPATH=src python -m arbiter.lbd.propose --condition Stim8hr   # regenerate the funnel + questions
```
Outputs: `data/lbd_out/sweep_Stim8hr.json` (full audit) + `lbd_questions_Stim8hr.json` (clean set).
The referee verdict for any triple: `arbiter.lbd.referee_triple.referee_triple(gene, disease, condition, data)`.

## Provenance / integrity
All code authored during the event (new-work-only; git history is the proof). Disease ids resolved
authoritatively against Open Targets + EBI OLS4 (MONDO, not EFO). The plan was hardened by a 3-round
repo-read Codex debate and the money-shot vetted by an independent Codex consult
(`docs/reviews/codex-debate_lbd-proposer-spec_2026-07-07.md`; consult logs in build log).
