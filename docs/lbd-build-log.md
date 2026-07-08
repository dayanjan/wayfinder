# LBD proposer — build log & process doc

Running record of building the LBD question-proposer (`docs/lbd-proposer-spec.md` v2).
Document-as-we-go: every tool, decision, and verification lands here as it happens.

## Compliance stance (read first)
**NEW WORK ONLY** — every file under `src/arbiter/lbd/` is authored during the event
(started 2026-07-07); git history is the compliance proof. Sibling projects
(`2026-03-05-LightsOut-R01/tools/`, `2026-06-13 Health Informatics Textbook/`) informed the
**pattern only** — deterministic `.env`-keyed API clients with on-disk caching. **Zero file
copy.** Prefer direct API/SDK tools over MCP (user doctrine §19); all clients are plain REST/
GraphQL keyed off `.env`.

## Tool inventory (`src/arbiter/lbd/`, all fresh)
| File | Role | Source / API | Key |
|---|---|---|---|
| `entity_maps.py` | Pinned A/B/C maps: 12 eligible + 2 umbrella diseases → **MONDO** ids; Th1/Th2 keyword arms | (static, API-verified) | — |
| `_http.py` | Shared cached GET/POST → `data/lbd_cache/` (gitignored); `.env` loader; politeness sleep | — | — |
| `sources.py` | `cooccur_count` (Europe PMC), `opentargets_disease_targets`/`opentargets_known` (A–C known set), `mygene_ensembl` | Europe PMC · Open Targets GraphQL · MyGene | none (keyless) |
| `entities.py` | `build_a_universe()` (KD gate ∩ effect, answer-free), `load_c()`, program constants | local CSVs (T1/T2/T4) | — |
| `verify_disease_ids.py` | Reproducible provenance: re-resolve the pinned ids vs Open Targets + OLS4; assert match | Open Targets · EBI OLS4 | none |
| `resolve_efo.py` *(scratch)* | one-off resolver that seeded the map; graduated into `verify_disease_ids.py` | — | — |

`.env` keys available: `NCBI_API_KEY`, `OPENALEX_API_KEY`, `SEMANTIC_SCHOLAR_API_KEY`,
`ZOTERO_*`, `ANTHROPIC_API_KEY`. v1 needs **none** (Europe PMC / Open Targets / MyGene are
keyless); NCBI/OpenAlex are optional fallbacks/politeness upgrades. Deps: `requirements.txt`
(`pandas`, `requests`).

## Pinned entity maps — how we know they're right
- **C (disease → id):** resolved all 14 CSV disease names against the **Open Targets search
  API** (the exact service the A–C exclusion queries) + cross-checked **EBI OLS4**, 2026-07-08.
  All 14 names exact-matched. **Every canonical id is a MONDO id, not EFO** — my memory-drafted
  EFO ids were the wrong id system. Pinning EFO would have made Open Targets return "no known
  association" for every gene → falsely inflate novelty everywhere. Caught by authoritative
  resolution, not memory. Provenance regenerable via `python -m arbiter.lbd.verify_disease_ids`.
- **Verified usable:** `disease(efoId:"MONDO_0004979")` (asthma) is accepted by the association
  query → 7403 targets with scores (FLG/IL4R/IL33/TSLP ~0.72–0.74). **Query the disease side**
  (`disease(id).associatedTargets`); the target-side `associatedDiseases(efoIds:[...])` filter
  returned empty for the known GATA3×asthma pair.
- **B (program → keywords):** Th1/Th2 arms + umbrella pinned. A–B bridge uses **process terms
  only** (no marker genes, stricter); B–C bridge **keeps markers** (disease lit cites them).
  Flip via `PROGRAM["ab_use_markers"]`.

## A-universe definition — decision record
Spec v2 §1 estimated "~200–450 genes"; the real substrate is far larger. Measured 2026-07-08:
| Definition | Unique genes |
|---|---|
| loose: KD-gate ∩ (ontarget_significant OR n_downstream>0) — `build_a_universe()` default | **9,471** |
| ontarget_significant only | 7,913 |
| **program-significant: loose ∩ Th1/Th2 T2 adj_p<0.05 — `build_a_universe(program_significant=True)`** | **4,373** |
| ontarget_significant ∩ program-significant | 3,702 |

**Decision:** the A universe is intentionally large; the **novelty ranking narrows it**, not a
hard gene cap. Default to `program_significant=True` (4,373 = "regulators OF the program",
matching spec intent and staying answer-free since T2 is program-level, not disease-level).
The "~200–450" line in the spec is an artifact of the absent `*_regulator_coefficients.csv`
and should be read as "the ranked shortlist," not the universe.

## Call-volume strategy (keeps API load bounded)
- **A–B** (Europe PMC): one query per A gene (~4.4k, cached once). 
- **B–C** (Europe PMC): one query per disease (12).
- **A–C known** (Open Targets): **prefetch each disease's associated-target map (12 calls)**,
  then look up every A gene in the map — O(12) calls, not O(genes×diseases).
- **A–C literature** (Europe PMC): computed **only for candidates that survive** the program
  bridges + known-exclusion — a few hundred, not ~52k.

## Running log
- **2026-07-08** — 3-round repo-read codex-debate hardened the spec v1→v2 (9→3→0 findings,
  build-ready; record in `docs/reviews/codex-debate_lbd-proposer-spec_2026-07-07.md`). Fable-5
  sub-agent independently confirmed build-ready + same top risk (disjoint-survivor existence).
  Pinned + API-verified the disease/program maps (MONDO catch). Authored the fresh tool layer
  (`_http`, `sources`, `entities`, `entity_maps`, `verify_disease_ids`) + `requirements.txt`;
  smoke-tested: A universe builds (9,471 loose / 4,373 program-significant), C=12, B=Th1/Th2.
  Live client smoke: Europe PMC (GATA3×Th2 = 10,177 co-mentions) + MyGene (GATA3→ENSG00000107485)
  worked first try; the Open Targets client had a bug — `associatedTargets` page size is capped
  at **3000** (size>3000 errors → 0 rows). Fixed with score-DESC pagination that early-stops
  below the novelty floor. Re-verified: asthma known-map=2,999; IL4R 0.744 / GATA3 0.559 /
  TSLP 0.718 known, **SLC1A5 = 0.0** (correct — the metabolic non-asthma gene is the novelty
  signal, and matches the referee's SLC1A5-refuted demo). Tool layer complete + tested.

## Preflight result — go/no-go = **GO** (with a quality caveat)
`cooccur.py::preflight_sample` ran over an 18-gene sample × 12 diseases (216 triples,
Stim8hr), 2026-07-08:
- **Disjoint survivors exist: 10 / 216.** `ac_lit==0` in 4.6% of triples; `ac_known≤τ(0.1)`
  in 91%. The pipeline runs end-to-end and produces candidate novel A→C hypotheses. **The
  load-bearing unknown (does a disjoint survivor exist?) resolves positively.**
- **Caveat — quality, not count.** The sample was the first 18 *alphabetical* genes (ABCD2,
  AAMDC, AAK1, ABC-transporters…), so these survivors are "novel because *understudied*"
  (ac_lit=0 is trivially true for obscure genes), not because of a compelling biological
  bridge. All top survivors have low ab/bc → negative novelty scores. This is expected for a
  weak alphabetical slice and is exactly why we **rank** rather than hard-gate (F-007).
- **Two method risks logged:** (1) short gene symbols (AAK1, ABCD2) can produce false-positive
  Europe PMC matches — the real run should use the ENSG-aware / quoted-symbol query or a
  gene-name synonym guard; (2) ac_lit=0 is trivially satisfied by understudied genes, so the
  demo candidate must be chosen from the **ranked top**, and must PASS THE REFEREE — a disjoint
  flag alone is not the money-shot.

## Codex independent consult (2026-07-08) — verdict + actions
Ran a repo-read Codex consult on the tool code + preflight (`.claude/scratch/lbd-debate/
codex_consult*.txt`). **Bottom line: LBD worth building, but the current novelty score +
query layer will systematically confuse "interesting disjoint" with "barely studied or badly
queried" — fix ranking before any full sweep.** Agreed on all points. Actions taken:
- **Scoring flaw (accepted):** `bc` is constant per disease across genes (a disease-popularity
  axis, not a gene signal) and `ac_lit=0` is too cheap. → rewrote as a **gated/balanced
  objective**: gate on `ab` above a universe percentile + `bc≥min_bc` + `ac_known≤τ`; rank by
  `min(z(log1p ab), z(log1p bc)) + β·z(log1p effect) − w·log1p(ac_lit) − w2·ac_known`.
- **"Not obscure" prior (the biggest miss):** *novelty ≠ absence of literature* — the compelling
  story is "understudied in literature BUT strong in the data." → added **dataset effect strength
  (`n_downstream`)** as the prior (already answer-free; EGR2=854).
- **Symbol-query bug (accepted):** `_phrase()` left bare gene symbols (AAK1/IL2/JUN) → false
  positives. → always-quote terms in the Europe PMC queries (fielded gene-annotation queries
  logged as future hardening).
- **Reorder (accepted):** built `referee_triple` FIRST (done + verified — EGR2 supported for
  11/12 diseases, **refuted-for-C for Hashimoto's**, i.e. it discriminates; SLC1A5 refuted;
  IL2 gate-fail untested), then a ranked pilot, then the full sweep.
- **Strategic (accepted):** keep LBD **subordinate to the referee demo**; the submission is the
  receipt-backed referee + 1–2 LBD examples *if they survive*; always show generated→culled
  counts and be honest when the proposer emits junk. Don't bet the demo on a pristine money shot.

## Ranked pilot result (2026-07-08) — pipeline + cull verified end-to-end
`referee_triple` built + verified (EGR2 supported 11/12, **refuted-for-C for Hashimoto's** =
discriminates; SLC1A5 refuted; IL2 gate-fail untested). Ranked pilot (15 effect-ranked genes +
5 controls × 12 diseases, Stim8hr) after fixing the scoring:
- **First run: 0 disjoint** — my bug: I still hard-gated `ac_lit<=0`. Well-studied strong
  regulators almost always have *some* disease literature, so that gate leaves nothing. Fixed
  per the spec's own F-007: `ac_lit` is a **rank penalty, not a gate** (gate = ab-percentile +
  bc + not-known).
- **Second run funnel: generated 240 → disjoint 75 → top-culled 12 → referee-supported 0.**
  The pipeline generates and the referee **honestly culls** (all 12 top candidates refuted-for-C).
- **Bias found:** ranking genes by `n_downstream` surfaces **pan-essential TCR genes** (CD3E,
  ZAP70, CD247, ITK) — huge global effect, but NOT in specific disease clusters, so the referee
  refutes them. `n_downstream` rewards "kills the cell," not "shifts the program." Ranking
  refinement to consider: use T2 program-shift magnitude (|zscore|) as the effect prior instead
  of/with n_downstream. Does NOT block the full sweep (which uses ALL genes, not a top-effect
  sample), only reorders survivors.

## FULL SWEEP result (Stim8hr, 2026-07-08) — the honest funnel + the money-shot
`propose.py` full sweep over all program-significant genes. A **Codex judgment consult** then
found a real bug (the triple answer was set from the disease hop ALONE, so effect-refuted/flagged/
empty rows were mislabelled "supported"). **Fixed:** `referee_triple.answer` is now a FULL-CHAIN
verdict. Corrected honest funnel (matches Codex's independent rerun, stricter on empty-effect):

**a_genes 3,935 → eligible pairs 22,039 → disease-C-supported 43 →**
- **CLEAN full-chain supported: 30** (gate+effect+program+disease-C all hold, effect>0)
- supported_weak 10 (effect=0 downstream — empty effect, excluded from clean)
- supported_flagged 3 (off-target caveat)
- refuted_effect 1 (SBF2 — effect refuted; correctly excluded)
- refuted_for_c 21,995 (the cull)
Artifacts: `data/lbd_out/sweep_Stim8hr.json` + `lbd_questions_Stim8hr.json` (clean set; gitignored).

- **The one pure-disjoint clean** (NUDT1 × T1D) has a **trivial effect (4 DEs)** + borderline
  program shift — *strict literature-absence correlates with weak/obscure*, why we rank not
  hard-gate (F-007).
- **Headline money-shot — NAB2 × atopic eczema @ Stim8hr.** Codex verdict: **keep-with-caveat** —
  frame as *"near-novel, receipt-backed, Ota-supported,"* NOT pristine-novel or replicated.
  Clean full-chain, receipts verified by Codex against the CSVs:
  - GATE supported (2/2 guides, best adj-p 1e-16; guide expr 0.056 vs NTC 0.567)
  - EFFECT supported, **on-target, NO off-target flag**, effect −16.9, **301 downstream DEs**
  - PROGRAM supported, Th1-associated (Ota 2021 zscore 7.71, adj-p 1.96e-13; **Hollbacker n.s.
    — only 1 of 2 contrasts significant, state this**)
  - DISEASE supported for the **specific** disease: atopic-eczema clusters OR 3.90 FDR 0.0028
    **and** OR 3.43 FDR 0.0224 (2 clusters)
  - ac_lit=6 is a **low/noisy count, NOT "established/curated literature"** (not gene-normalized);
    say "near-novel," never "known." EGR2-NAB2 corepressor is a **hypothesis-strengthener, NOT
    part of the referee evidence** — subordinate it to the receipt (Codex caution).
- **Honesty examples for the demo:** NUDT1 pure-disjoint-but-weak; DNAJB9 supported-but-off-target-
  flagged; SBF2 refuted-effect; and the 21,995 refuted-for-C = the cull. Show the full class breakdown.
- **Codex on conditions:** Stim8hr is **sufficient** for the demo; run Rest/Stim48hr only as a
  bonus/appendix if time remains — do NOT spend demo-critical time chasing them first.

The story: *the LBD engine generated 22,039 candidate questions from a dataset that came with none;
the data-referee culled to 30 clean receipt-backed supported; the standout is a near-novel,
mechanistically-plausible gene→program→specific-disease link (NAB2→Th1/Th2→atopic eczema).*

## Independent NAB2 literature audit (2026-07-08) — novelty verified + a confounder caught
Built a fresh multi-source literature tool (`src/arbiter/lit/search.py` — Europe PMC + OpenAlex +
Semantic Scholar, cached, direct-API per §19), pulled a 155-paper NAB2 corpus, and ran a **4-agent
independent team** (molecular / immunology / disease / genetics). Synthesis:
`docs/nab2_knowledge_synthesis_2026-07-08.md`. Key results:
- **NAB2→Th1/Th2 and NAB2→atopic eczema are BOTH genuinely novel — 0 direct papers each** (more
  novel than the noisy ac_lit=6). NAB2's known T-cell role is *activation* (co-activates IL-2), not
  lineage polarization; its Th-axis footprint runs through EGR2/EGR3.
- **Confounder caught: STAT6 adjacency.** NAB2 is ~1.9 kb from STAT6 (master Th2/atopic gene; they
  fuse in solitary fibrous tumor). The atopic-eczema link may be STAT6's shadow.
  *Our-data check (partial defense):* NAB2 & STAT6 sit in **different** atopic-eczema clusters
  (NAB2 74/90 FDR 0.0028/0.0224; STAT6 30 FDR 0.0005), and the KD is NAB2-specific → the functional
  effect is real NAB2 biology. STAT6 itself is also referee-supported (positive control).
- **EGR-mediation** mechanism caveat logged. Finding writeup + framing updated accordingly.
- **Net:** the audit *strengthens* the submission — catching the STAT6 confounder is the project's
  confident-caveat-aware-verdict thesis in action. Optional next: (a) do the T3 clusters map to the
  shared 12q13 locus? (b) NAB2-vs-STAT6 downstream DE overlap.

## Independent replication (2026-07-08) — 5-agent lab, UNANIMOUS PASS
3 Opus + 2 Codex agents, each re-deriving from raw CSVs (adversarial; 2 clean-room re-implementations).
Full report: `docs/replication_report_2026-07-08.md`. **The finding replicates** — every headline
number reproduced to the unit (NAB2 receipt; funnel 3,935→22,039→43→30/10/3/1; NUDT1 pure-disjoint);
code confirmed answer-free + full-chain-correct; STAT6 + EGR confounders could not be made to stick.
Errors caught & FIXED (why we trust it): (1) cluster-ID misalignment 74→**90/100** (script de-hardcoded,
re-run confirms genome-wide modules BACH2/BCL6/IRF4/CD28); (2) "8×" is effect-size, **~3× on z**;
(3) reframed distinctness onto co-membership+magnitude+guide-specificity (not the identical disease
profile) and anti-EGR onto D3 paralog-opposition (not the weak cross-cohort D2). Framing caveats now
documented: PROGRAM hop is a funnel tautology (refuted_program≡0 in A); "43" is a joint gate×referee
product (referee alone supports 395/47,220). Synthesis + finding writeup updated to match.

## Next move
Lock the NAB2 story with the honest framing above; write the demo-facing finding artifact
(`docs/lbd_finding_*.md`) + emit is done (`lbd_questions_Stim8hr.json`). Optional bonus: Rest/
Stim48hr sweeps. Then the demo video + README-as-paper (M5). (1) over the whole program-significant
A universe (4,373) compute the bridges + novelty score and RANK; (2) **cull the top candidates
through `referee_triple`** — a survivor is the money-shot only when the referee supports the
gene→program→*specific-disease* chain (F-001/F-012); (3) sanity-check the pipeline against
known-strong regulators (GATA3/EGR2 — for validation only, NOT to seed A, per F-011) to confirm
a *compelling* survivor emerges, not just an obscure one. Build order: `referee_triple` adapter
→ `propose.py` (rank + cull) → `emit.py` (`lbd_questions.json`). The full A–B/A–C-lit sweep is
~4.4k + survivor A–C-lit calls (rate-limited, cached) — run as a background job.
