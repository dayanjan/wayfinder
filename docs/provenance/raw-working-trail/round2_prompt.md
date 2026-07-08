You are continuing an iterative cross-model debate on an implementation-plan artifact.
This is round 2. You have seen your round-1 critique and Claude's revision. Your job now:
1. ESCALATE findings Claude did not adequately address.
2. DROP findings Claude addressed.
3. SURFACE NEW findings exposed by Claude's revision.
4. Decide if the debate has converged (no new findings, >=80% prior findings addressed).
Do NOT repeat findings unchanged. Either escalate, drop, or replace.

# CRITICAL: still a REPO-READ debate — keep verifying against the actual code

You are READ-ONLY inside the target repo. Continue to open referenced files to verify
claims; a repo-verified finding is worth far more than a speculative one. Claude's
revision proposes concrete moves (a thin `referee_triple` adapter; redefining A off
`guide_kd_efficiency`/`DE_stats`; constraining B to Th1/Th2; reading C from the CSV;
converting the disjoint hard-gate to a ranked novelty score). Where those moves make
claims about the repo, CHECK them. Specifically worth re-opening:
- `docs/perturbseq-qc_2026-07-07/pyzobot_referee.py` — is a HOP-3 disease-C filter really
  thin (does the exploded T3 table carry a usable `disease` column per gene)? Read the
  `t3_exploded` construction and the `_hop3` logic to confirm the adapter is small.
- `data/DE_stats.suppl_table.csv` and `data/guide_kd_efficiency.suppl_table.csv` headers —
  can A ("KD-gated significant regulators") actually be derived deterministically from
  these, or is a coefficient/significance column missing?
- `docs/perturbseq-qc_2026-07-07/pyzobot_referee_ranked_full.csv` — does it carry the
  columns needed to seed the A universe WITHOUT leaking answers (per F-009)?

# Framing question

Same as round 1: is the (now-revised) LBD proposer the shortest CORRECT path to a
receipt-backed, condition-specific NOVEL finding by July 13, holding up against the
actual repo? PLUS the round-2 tension Claude raises: after constraining A/B/C, is this
still a genuinely GENERATIVE LBD engine, or has it collapsed into a lookup/reranker of
the 457 already-scored genes? If the latter, is demoing the referee on 2-3 hand-built
disjoint triples (and dropping the proposer) the stronger submission? Take a position.

# Preserve-intent directive

The novel claim is "LBD as a QUESTION-GENERATION engine whose output is MANDATORILY
culled by a data-referee." Do not sand it into "just run LBD" or "just run the referee."
But you MAY legitimately argue the constrained substrate is too thin to be generative —
that is critiquing execution, not sanding the claim. Prefer "open question" over false
agreement.

# Round history

## Round 1 — Claude's position (summary)
The spec's reframe (LBD generates questions -> referee culls) is the moat; entities are
bounded by the dataset so the matrix is pandas-computable; referee reused unchanged for
v1; money shot = one disjoint-in-lit + data-supported + condition-specific triple. Claude
flagged four assumptions for verification: A-source CSVs, referee disease-specificity,
disjoint-gate feasibility, condition first-classness.

## Round 1 — Codex's findings (verbatim JSON)
[
 {
  "id": "F-001",
  "title": "Existing referee cannot adjudicate the requested disease C unchanged",
  "severity": 5,
  "likelihood": 5,
  "blast_radius": 5,
  "priority": "P0",
  "evidence": "In docs/perturbseq-qc_2026-07-07/pyzobot_referee.py, referee(gene, condition, data) accepts only gene and condition. HOP-3 filters only by gene and gene_set == downstream_<condition>, then marks DISEASE supported if the gene is in >=1 significant disease cluster and returns receipt.diseases/top_hits. It never takes C_disease and never checks that the requested disease is present. The claim text is 'gene is a member of >=1 autoimmune-disease-enriched cluster'.",
  "concern_path": "An LBD question can ask GATA3 -> asthma, but referee(A_gene, Stim8hr) may return supported because GATA3 appears in some other significant disease cluster. The caller would then overclaim a condition-specific, disease-specific novel finding that the referee did not actually test.",
  "suggested_action": "Make the plan require a thin wrapper or referee extension that filters HOP-3 receipts by C_disease and returns supported/refuted for that exact disease.",
  "novelty_flag": true,
  "concern_type": "correctness"
 },
 {
  "id": "F-002",
  "title": "Planned regulator coefficient source tables are absent from data/",
  "severity": 5,
  "likelihood": 5,
  "blast_radius": 4,
  "priority": "P0",
  "evidence": "data/ contains only cluster_autoimmune_enrichment_results.suppl_table.csv, DE_stats.suppl_table.csv, guide_kd_efficiency.suppl_table.csv, fetch_data.sh, README.md, and Th2_Th1_polarization_signature_DE_results_full.suppl_table.csv. A recursive search for polarization_prediction, aging_prediction, cytokine, and regulator_coefficients returned no files. docs/perturbseq-qc_2026-07-07/pyzobot_referee_ranked_full.csv exists with 602 rows, 457 genes, and all three conditions.",
  "concern_path": "Stage 1 cannot build A as specified. A solo 0.5-1 day build will immediately stall or silently redefine A, making the spec's bounded matrix and novelty claims non-reproducible.",
  "suggested_action": "Revise A to use existing deterministic tables: KD gate + DE_stats/T2 membership, or explicitly reuse pyzobot_referee_ranked_full.csv only as an A universe, not as answer labels.",
  "novelty_flag": false,
  "concern_type": "correctness"
 },
 {
  "id": "F-003",
  "title": "The repo does not support B = 3 programs x 3 conditions as specified",
  "severity": 5,
  "likelihood": 5,
  "blast_radius": 5,
  "priority": "P0",
  "evidence": "pyzobot_join_spec.json has T2_Th2_Th1 only, with semantic 'gene -> PROGRAM shift (Th1<->Th2 log_fc/zscore)'. The T2 CSV header is variable,baseMean,log_fc,...,contrast,zscore, and its only contrast values are 'Th2_vs_Th1 (Hollbacker 2021)' and 'Th2_vs_Th1 (Ota 2021)'. No aging or cytokine production table is present in data/.",
  "concern_path": "The proposer may emit aging or cytokine_production questions, but the existing referee has no corresponding HOP-2 evidence table. Those questions cannot be receipt-backed by the current four-table substrate.",
  "suggested_action": "Constrain v1 B_program to Th1_Th2_polarization, or add explicit new receipt tables and referee logic before claiming 3 programs.",
  "novelty_flag": false,
  "concern_type": "correctness"
 },
 {
  "id": "F-004",
  "title": "Condition is only partially first-class; HOP-2 program verdict is not condition-specific",
  "severity": 4,
  "likelihood": 5,
  "blast_radius": 4,
  "priority": "P1",
  "evidence": "In pyzobot_referee.py, HOP-0 and HOP-1 filter by culture_condition, and HOP-3 checks gene_set = downstream_<condition>. But HOP-2 uses t2r = data.t2[data.t2.variable == sym] with no condition field, then reports significance across the two literature reference contrasts. The join spec also says T2 grain is gene(SYMBOL) x contrast, not gene x condition.",
  "concern_path": "A final claim can say 'specific to Stim8hr', but the program-shift hop is shared across conditions. The condition-specificity is coming from KD/effect and disease gene_set, not from the program B evidence itself.",
  "suggested_action": "Downgrade the plan's condition-specific wording or define condition-specificity as HOP-0/HOP-1/HOP-3 only; do not claim HOP-2 is condition-specific without new data.",
  "novelty_flag": true,
  "concern_type": "correctness"
 },
 {
  "id": "F-005",
  "title": "Referee output contract is incompatible with lbd_questions.json as written",
  "severity": 4,
  "likelihood": 5,
  "blast_radius": 4,
  "priority": "P1",
  "evidence": "The planned JSON includes A_gene, B_program, C_disease, and condition_hint. pyzobot_referee.referee_json(gene, condition, data) serializes only referee(gene, condition, data). There is no parameter or branch for B_program or C_disease; HOP-2 is hardwired to Th1/Th2 and HOP-3 is hardwired to any significant autoimmune disease cluster.",
  "concern_path": "The orchestrator has no deterministic way to map a generated triple to a verdict on that triple. It can only map to a generic gene-condition chain, so supported/refuted labels would be post-hoc interpretation rather than a direct receipt-backed answer.",
  "suggested_action": "Add an adapter contract that consumes the full LBD question and evaluates exact B_program and C_disease, even if v1 only supports one B_program.",
  "novelty_flag": true,
  "concern_type": "correctness"
 },
 {
  "id": "F-006",
  "title": "Disease universe is not ~17 specific autoimmune diseases",
  "severity": 3,
  "likelihood": 5,
  "blast_radius": 3,
  "priority": "P1",
  "evidence": "The real non-negative-control disease values in data/cluster_autoimmune_enrichment_results.suppl_table.csv are 14: ankylosing spondylitis, asthma, atopic eczema, autoimmune disease, celiac disease, Crohn's disease, Hashimoto's thyroiditis, inflammatory bowel disease, multiple sclerosis, psoriasis, rheumatoid arthritis, systemic lupus erythematosus, type 1 diabetes mellitus, ulcerative colitis. The header is cluster,disease,gene_set,odds_ratio,ci_low,ci_high,p_value,p_adj_fdr,cluster_size,...,intersecting_genes,negative_control_disease.",
  "concern_path": "The plan's matrix size, synonym/EFO-map work, and demo disease examples are slightly inflated and include generic umbrella terms like 'autoimmune disease' and 'inflammatory bowel disease' that are not equivalent to specific disease claims.",
  "suggested_action": "Read C from the CSV at build time, report the exact 14 values, and decide whether umbrella rows are eligible C claims or only supporting context.",
  "novelty_flag": false,
  "concern_type": "correctness"
 },
 {
  "id": "F-007",
  "title": "Disjoint gate plus current supported genes is likely too narrow for the demo promise",
  "severity": 4,
  "likelihood": 4,
  "blast_radius": 4,
  "priority": "P1",
  "evidence": "docs/lbd-proposer-spec.md defaults to ab>=3, bc>=3, ac_lit<=0, and NOT ac_known. The existing top supported examples in pyzobot_referee_ranked_full.csv include canonical immune/asthma genes like ITK, ZBTB25, CHD7, EGR2-context hits, which are unlikely to have zero gene-disease literature/known associations once Open Targets/GWAS/PubTator are queried.",
  "concern_path": "The demo requires one disjoint-in-literature + data-supported + condition-specific survivor. With max_ac=0 and known-association exclusion, the highest-confidence data-supported hits may be filtered out, leaving no money-shot candidate under deadline.",
  "suggested_action": "Require a preflight histogram over ac_lit/ac_known for the 457-gene ranked universe and define fallback thresholds before committing the demo claim.",
  "novelty_flag": true,
  "concern_type": "novelty"
 },
 {
  "id": "F-008",
  "title": "0.5-1 day estimate ignores API/entity-normalization complexity",
  "severity": 3,
  "likelihood": 4,
  "blast_radius": 3,
  "priority": "P2",
  "evidence": "The spec requires MyGene alias resolution, disease-to-EFO/MeSH mapping, PubTator3/Europe PMC/OpenAlex co-mentions, Open Targets GraphQL, GWAS Catalog REST, caching, thresholds, and provenance sources. The repo currently has no src/arbiter/lbd implementation, and the data source mismatch means the entity map must be redesigned first.",
  "concern_path": "Even if the pandas scoring is trivial, API semantics, rate limits, identifier misses, and hand-built synonym maps can consume the entire build window and crowd out the demo video, which the framing says is heavily weighted.",
  "suggested_action": "Scope v1 to one or two sources and a fixed candidate universe, with cached fixtures and generated-vs-culled counts as the deliverable.",
  "novelty_flag": false,
  "concern_type": "correctness"
 },
 {
  "id": "F-009",
  "title": "Using pyzobot_referee_ranked_full.csv naively would leak referee answers into the proposer",
  "severity": 3,
  "likelihood": 3,
  "blast_radius": 3,
  "priority": "P2",
  "evidence": "pyzobot_referee_ranked_full.csv contains not just genes and conditions but top_disease, overall_status, program_adj_p, disease_OR, disease_FDR, statuses, and chain_score. It is attractive as a replacement A source because it has 457 genes, but it already encodes the referee's disease-supported outputs.",
  "concern_path": "If Stage 1 uses this file beyond defining the A universe, the LBD component stops being an independent question generator and becomes a reranker of known referee winners. That weakens the novel generate-then-cull thesis.",
  "suggested_action": "If reusing ranked_full, restrict it to A_gene eligibility only and hide disease/status/score columns from the proposer stage.",
  "novelty_flag": true,
  "concern_type": "novelty"
 }
]

## Round 2 — Claude's revision (summary)
Claude ACCEPTS all nine findings (none rejected/deferred). Key moves: (F-001/F-005) add a
thin `referee_triple(A,B,C,condition)` adapter that filters HOP-3 to the exact C; drop
"referee unchanged" wording. (F-002) redefine A off `guide_kd_efficiency`+`DE_stats`;
ranked_full seeds A-universe only. (F-003) v1 B = Th1/Th2 only; aging/cytokine out of
scope. (F-004) reword "condition-specific" to name only the KD/effect/disease hops, not
HOP-2. (F-006) read the 14 diseases from the CSV; umbrella terms = context only, not
eligible C claims. (F-007) convert `ac_lit<=0` hard gate to a ranked novelty score + a
preflight ac_lit/ac_known histogram. (F-008) v1 = one co-mention source (Europe PMC) +
Open Targets, cached fixtures, generated-vs-culled counts as deliverable, protect demo
time. (F-009) ranked_full used for A-eligibility only, answer columns hidden.

# Claude's round 2 position (full text follows)

# Round 2 — Claude's revision (explicit accept / reject / defer per finding)

Codex's round-1 findings are almost entirely **repo-verified facts**, not opinions.
I accept the substance of all nine. Below: my disposition on each, then the revised
spec position, then one tension I push back to Codex.

## Disposition per finding

- **F-001 (P0, referee can't adjudicate specific disease C) — ACCEPT.** Confirmed: HOP-3
  marks DISEASE `supported` on membership in ≥1 significant cluster, never checks the
  requested C. Fix: a **thin adapter** (`referee_triple(A_gene, B_program, C_disease,
  condition)`) that filters HOP-3 receipts to the requested C and returns
  supported/refuted **for that exact disease**. The referee CORE logic is unchanged; I
  am dropping the spec's "referee consumes it unchanged" wording — it's a thin wrapper,
  not zero code.
- **F-002 (P0, A-source CSVs absent) — ACCEPT.** The `*_regulator_coefficients.csv`
  files don't exist. Redefine A deterministically from tables that DO exist: the KD gate
  (`guide_kd_efficiency`) + significant on-target/downstream effect (`DE_stats`/T2
  membership). `pyzobot_referee_ranked_full.csv` (457 genes, 3 conditions) may seed the A
  **universe only** — see F-009 guardrail.
- **F-003 (P0, B ≠ 3 programs × 3 conditions) — ACCEPT.** There is no aging or cytokine
  receipt table in the substrate. **v1 B = `Th1_Th2_polarization` only.** Aging/cytokine
  are explicitly out of scope until their tables + HOP-2 logic exist. This is the honest
  substrate.
- **F-004 (P1, HOP-2 not condition-specific) — ACCEPT + REWORD.** The program-shift hop
  keys on literature contrasts (Ota/Hollbacker), grain = gene×contrast, no condition
  field. So "condition-specific" is legitimate ONLY for HOP-0 (KD gate), HOP-1 (effect),
  HOP-3 (condition-suffixed `gene_set`). I will reword every "condition-specific" claim
  to name which hops carry it, and NOT claim the program-direction call is
  condition-resolved.
- **F-005 (P1, output contract incompatible) — ACCEPT.** Merges with F-001: the adapter
  is the deterministic map from a full (A,B,C,condition) triple to a verdict on that
  triple. Without it, labels are post-hoc interpretation. The adapter is v1-mandatory.
- **F-006 (P1, disease universe is 14, includes umbrellas) — ACCEPT.** Read C from the
  CSV at build time (14 values, not ~17). Umbrella rows ("autoimmune disease", "IBD")
  are **supporting context only, not eligible C claims** — a novel-link claim must land
  on a specific disease.
- **F-007 (P1, disjoint gate too narrow) — ACCEPT.** Before committing the demo promise,
  run a **preflight histogram** of `ac_lit`/`ac_known` over the A universe. Convert the
  hard `ac_lit ≤ 0` gate to a **ranked novelty score** with a tunable band, so "most
  novel available" is guaranteed to return something even if strict-zero is empty.
- **F-008 (P2, 0.5–1 day underestimates API/normalization) — ACCEPT.** v1 = **one
  co-mention source** (Europe PMC, no key needed) + Open Targets for the A–C known set;
  cache to fixtures; **generated-vs-culled counts are the deliverable**. Protect demo-video
  time — the referee finding is already complete, so the LBD layer must not eat the video.
- **F-009 (P2, ranked_full leaks referee answers) — ACCEPT.** If ranked_full seeds A, use
  **A_gene eligibility only**; the proposer never sees `top_disease/overall_status/
  disease_FDR/chain_score`. The proposer mines external literature independently; the
  referee is the only thing that touches the answer.

**Rejected/deferred:** none rejected. Nothing deferred — all nine fold into v1 scope.

## Revised spec position (what v1 actually is)
LBD proposer over **A = KD-gated significant regulators** × **B = Th1/Th2 polarization
(one program)** × **C = the 14 specific diseases from the enrichment CSV**. Mine Europe
PMC co-mention counts (A–B, B–C) + Open Targets/GWAS for the A–C *known* set; rank by a
novelty score (not a hard zero-gate); emit `lbd_questions.json`; a **thin
`referee_triple` adapter** answers each on the exact (A,B,C,condition), with
condition-specificity claimed only for the KD/effect/disease hops. Deliverable includes
generated-vs-survived counts. Money shot = one disjoint-in-lit + data-supported triple on
a specific disease; one refuted triple shows the cull.

## Preserve-intent check
The novel claim — **LBD generates questions, a data-referee mandatorily culls them** —
is fully intact. Constraining to one program, 14 diseases, and a thin disease-C filter
does not sand it; it runs the same generate-then-cull loop on an honest substrate.

## Tension I push back to Codex (round 2 focus)
After A is constrained to KD-gated regulators, B to one program, and C to 14 diseases,
the candidate space is roughly 300–450 genes × 1 program × 14 diseases. **Is that still a
genuinely *generative* LBD engine, or has it collapsed into "rank the 457 already-scored
genes against 14 diseases by literature co-occurrence" — i.e., a lookup with novelty
sorting?** What is the minimum that keeps it *generative* (proposing a question a human
with the dataset would not have asked) rather than a reranker — and is the single-program
substrate rich enough for even ONE defensible novel A→C bridge to exist? If not, the
honest move might be to demo the referee on 2–3 hand-built disjoint triples and drop the
proposer entirely. Argue which is the stronger July-13 submission.


# Artifact

## FILE: docs/lbd-proposer-spec.md

# LBD Question-Proposer — thin build spec (fresh, new-work-only)

**Purpose.** Fill the Researcher-track **cold-start gap**: rich dataset, no question. This component
uses literature-based discovery (Swanson **ABC**) to *generate* the highest-value **untested**
questions the CD4+ T-cell Perturb-seq dataset can resolve, then hands each to the already-built
**referee** (`docs/perturbseq-qc_2026-07-07/pyzobot_referee.py`) which answers it against the data.
Motivation + strategy: `memory/decisions/lbd-question-engine-reframe.md`.

**Compute:** laptop CPU + web APIs only. No GPU, no Colab. **Compliance:** all fresh code; public
data/APIs; git history is the proof.

---

## 1. Entities (bounded by the dataset — this is what keeps it thin)
Dataset = Zhu/Dann/Pritchard/Marson genome-scale CD4+ T-cell Perturb-seq (bioRxiv 2025.12.23.696273).

- **A = regulators (genes).** NOT all ~11.5k perturbed genes — restrict to **significant regulators
  of the measured programs**: genes with (a) a passing knockdown gate and (b) a significant coefficient
  in `polarization_prediction...regulator_coefficients.csv` / `aging_prediction...regulator_coefficients.csv`,
  OR a significant on-target DE effect. Target set ≈ 200–500 genes.
- **B = programs × condition.** The named axes: `Th1_Th2_polarization`, `aging`, `cytokine_production`,
  each crossed with `condition ∈ {Rest, Stim8hr, Stim48hr}`. (Condition is first-class — the paper's
  headline is context-specificity.)
- **C = autoimmune diseases.** The ~17 diseases in `cluster_autoimmune_enrichment_results.suppl_table.csv`
  (asthma, T1D, Crohn's, RA, MS, SLE, atopic eczema, …). Read the exact list from that CSV at build time.

Matrix ≈ (200–500 A) × (3 programs × 3 conditions B) × (~17 C) — small, computable in pandas.

## 2. Pipeline (3 stages, all CPU/API)

### Stage 1 — gather link evidence (API; cache everything to `data/lbd_cache/`, gitignored)
For each entity pair, get literature/DB co-mention counts. Prefer pre-computed resources over any NLP:

| Link | Primary source (query) | Fallback |
|---|---|---|
| **A–B** gene↔program | Map program→MeSH/keyword set (Th2:"Th2 cells","GATA3","type 2 immunity"; aging:"immunosenescence","T cell aging"; cytokine:"cytokine production"). PubTator3 `/relations` or Europe PMC co-mention count for gene × program-terms. | OpenAlex `works?filter=title_and_abstract.search:"<gene>" "<program-term>"` count |
| **B–C** program↔disease | Europe PMC / PubTator3 co-mention count for program-terms × disease name (+ synonyms via MeSH/EFO). | OpenAlex search count |
| **A–C** gene↔disease (the KNOWN set to exclude) | **Open Targets GraphQL** `associationDatatypes` for (gene, disease EFO) → association score + literature evidence count; **GWAS Catalog** REST for gene-near loci of the disease; PubTator3 gene×disease co-mention count. | DisGeNET if reachable |

Normalization: gene symbol→Ensembl/aliases via **MyGene**; disease→EFO/MeSH via a small static map built
once from the enrichment table's disease names. NCBI API key → PubMed 10 req/s; 1 req/s politeness otherwise.

### Stage 2 — compute the disjoint (novel) A–C candidates (pandas, milliseconds)
For every (A, B, C) triple:
- `ab = cooccur(A,B)`, `bc = cooccur(B,C)`, `ac_lit = cooccur(A,C)`, `ac_known = OpenTargets_score(A,C) > τ OR gwas_hit(A,C)`.
- **Candidate hypothesis** iff `ab ≥ min_ab AND bc ≥ min_bc AND ac_lit ≤ max_ac AND NOT ac_known`.
  (Defaults: `min_ab=min_bc=3` co-mentions, `max_ac=0`, `τ=0.1`. Tune from the data.)
- **Novelty/interest score:** `score = zscore(ab) + zscore(bc) − w·ac_lit − w2·OpenTargets_score`, higher = more
  novel-yet-literature-bridged. Rank descending. Keep top N (e.g. 25).

### Stage 3 — emit questions (JSON handed to the referee)
Each surviving triple → one question object (schema below), phrased in plain English so it reads as a real
research question, not a tuple.

## 3. Output contract → the referee
`lbd_questions.json`: a ranked list of:
```json
{
  "hypothesis_id": "H001",
  "question": "In CD4+ T cells, does perturbing GATA3 shift the Th2 polarization program and thereby link to asthma risk — and is that link specific to the Stim8hr state?",
  "A_gene": "GATA3",
  "B_program": "Th1_Th2_polarization",
  "C_disease": "asthma",
  "condition_hint": "Stim8hr",
  "novelty": {
    "ab_cooccur": 41, "bc_cooccur": 120, "ac_lit_cooccur": 0,
    "ac_known_opentargets": 0.03, "ac_gwas_hit": false, "is_disjoint": true
  },
  "score": 3.87,
  "sources": ["europepmc:...","opentargets:ENSG..-EFO_..","gwascatalog:..."]
}
```

### How the referee consumes it (already built — no referee changes needed for v1)
For each question: call `referee(A_gene, condition_hint or each condition)`. The verdict already traces:
HOP-0 KD gate → HOP-1 effect → **HOP-2 does it shift program B** → **HOP-3 does its cluster enrich for disease C**.
Then classify the *answer to the LBD question*:
- **disjoint in lit + referee = supported** → **receipt-backed NOVEL hypothesis** (the money shot: a gene→disease
  link the literature never made, that the data supports — bonus if condition-specific).
- **referee = untested** → knockdown failed; question unanswerable here (honest).
- **referee = refuted** → LBD proposed it, data killed it (the cull; the R01 answer in action).

## 4. Demo scope (thin, for the video)
1. Run the proposer over the bounded entity set → `lbd_questions.json` (25 ranked untested questions the
   *dataset itself* suggested — "here's what to ask when you didn't have a question").
2. Referee adjudicates the top few, live.
3. Land on ONE **disjoint-in-literature + data-supported + condition-specific** result → the receipt-backed
   novel finding. Show one **refuted** to prove the cull is real.

## 5. Build notes
- New files only: `src/arbiter/lbd/` (`sources.py` API clients, `cooccur.py` set logic, `propose.py` orchestrator,
  `emit.py`). Third-party libs OK (`requests`/`httpx`, `pandas`, `pydantic`). Cache raw API JSON under gitignored
  `data/lbd_cache/`.
- Effort: ~0.5–1 day fresh. Delegatable to Codex once this spec + the disease/program keyword maps are pinned
  (mechanical API-client + pandas work). Tag: `[HYBRID]` (Claude pins the entity/keyword maps + scoring; Codex
  builds the clients/logic; Claude reviews).
- Optional richer variant (still no GPU): Voyage-embed abstracts for *semantic* co-occurrence — API, off critical path.

## 6. Risks
- **Overproduction returns** — mitigated: the referee is the mandatory cull; report generated-vs-survived counts.
- **Disease/program → keyword mapping quality** drives everything — pin these maps by hand (small, ~17 diseases +
  3 programs) and eyeball them; this is the one non-mechanical step.
- **API rate limits** (not compute) — cache aggressively; NCBI key; bounded entity set keeps call volume low.


# Output requirements

Return JSON conforming to the supplied schema. round_number=2. findings = the current-round finding set (may restate replaced findings with new ids). escalated_findings = prior F-ids you are escalating (with rationale). dropped_findings = prior F-ids Claude addressed (with rationale). new_findings = F-ids first surfaced this round. convergence_status = "converged" if new_findings empty AND >=80%% of prior findings addressed, else "still iterating". convergence_sanding_warning: set only if converged AND the novel claim was sanded off, else null. recommended_next_question = what Claude must address most in round 3. Cite the specific file/line you opened for any repo-verified finding. Begin.
