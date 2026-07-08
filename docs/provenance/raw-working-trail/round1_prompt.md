You are a hostile senior reviewer running an iterative cross-model debate on an
implementation-plan artifact authored by an Anthropic-trained collaborator. This is
round 1. Your job is to surface every plausible concern with the position below,
scored and prioritized. You are NOT redesigning the artifact — you are critiquing it
from a hostile-but-informed stance.

# CRITICAL: this is a REPO-READ debate — verify claims against the actual code

You are running READ-ONLY inside the target git repository. The artifact is an
implementation PLAN, and plans drift from reality. You MAY and SHOULD open any file
referenced below to verify the plan's claims against what the repo actually contains.
**Verifying claimed facts against the repo is highly valued** — a finding backed by
"I opened X and it does not say what the plan claims" is worth far more than a
speculative one. In particular, please actually open and check:

- `docs/perturbseq-qc_2026-07-07/pyzobot_referee.py` — the already-built referee the
  plan says it will reuse "unchanged". Read what `referee()` / `referee_json()`
  actually return, especially HOP-3 (disease). Does the returned verdict let a caller
  assert a link to ONE specific disease C, or only to "some enriched autoimmune
  diseases"? Does `condition` thread through to a condition-specific verdict?
- `docs/perturbseq-qc_2026-07-07/pyzobot_join_spec.json` — the join contract (4 tables).
- `data/` — the actual CSVs present. The plan's entity-A definition (spec §1) keys off
  `polarization_prediction...regulator_coefficients.csv` and
  `aging_prediction...regulator_coefficients.csv`. Check whether those files exist in
  `data/` at all, and if not, what the plan should key off instead. Read the header of
  `data/cluster_autoimmune_enrichment_results.suppl_table.csv` to confirm the ~17
  disease list and column names the plan assumes.
- `docs/perturbseq-qc_2026-07-07/pyzobot_referee_ranked_full.csv` — the batch-ranked
  gene output the plan's entity-A set could reuse.

# Framing question

Is `docs/lbd-proposer-spec.md` the shortest CORRECT path to a receipt-backed,
condition-specific NOVEL finding by the July 13 deadline — and do its load-bearing
claims (entity-A source tables; "referee consumes it unchanged"; the disjoint-set
candidate gate; condition first-classness) hold up against the actual referee code
and CSVs in this repo? Secondary: is the plan thin enough to build in ~0.5–1 day
solo while leaving time for the demo video (which the judges weight heavily)?

# Preserve-intent directive

The artifact's NOVEL claim is: **"LBD used as a QUESTION-GENERATION engine (not a
discovery engine), whose generated questions are then MANDATORILY culled by a
data-referee."** Do not drift toward consensus that sands this into a generic "just
run LBD" or "just run the referee". Critique the EXECUTION of the generate-then-cull
loop; prefer "open question" over "we agreed" on the novel claim itself.

# Claude's opening position

(Below is Claude's round-1 statement of the artifact's position and the load-bearing
assumptions Claude already wants verified.)

# Round 1 — Claude's opening position

## Framing question
Is `docs/lbd-proposer-spec.md` the shortest *correct* path to a receipt-backed,
condition-specific **novel** finding by July 13 — and do its load-bearing claims
(entity-A source tables, "referee consumes it unchanged", the disjoint-set gate)
hold up against the actual referee code + CSVs already in this repo?

## The position the spec takes
1. **The reframe is the moat.** LBD (Swanson ABC) is used as a *question-generation*
   engine, not a discovery engine: it mines literature for the highest-value
   **untested** A(gene)→B(program×condition)→C(disease) triples the CD4+ T-cell
   Perturb-seq dataset is uniquely positioned to resolve. Each survivor is handed to
   the **already-built referee** (`docs/perturbseq-qc_2026-07-07/pyzobot_referee.py`),
   which answers it against the four tables. This fills the Researcher-track cold-start
   gap ("rich dataset, no question") that Claude Science structurally cannot fill
   itself, and answers the dead-R01 critique one level up: LBD proposes, the data
   referee culls.
2. **Thin + bounded.** Entities are bounded by the dataset (A≈200–500 regulators,
   B = 3 programs × 3 conditions, C ≈ 17 diseases read from
   `cluster_autoimmune_enrichment_results.suppl_table.csv`), so the whole matrix is
   pandas-computable. Pipeline is 3 stages: gather co-mention counts via APIs
   (PubTator3 / Europe PMC / OpenAlex + Open Targets / GWAS Catalog for the known
   A–C set) → compute disjoint novel candidates → emit `lbd_questions.json`.
3. **Referee unchanged for v1.** The spec claims no referee code changes are needed;
   the referee's existing gene+condition verdict is sufficient to answer each LBD
   question.
4. **The money shot** is one *disjoint-in-literature + data-supported + condition-
   specific* triple; one *refuted* triple proves the cull is real.

## Load-bearing assumptions I want stress-tested (verify against the repo)
- **A-source mismatch.** The spec restricts A to genes significant in
  `polarization_prediction...regulator_coefficients.csv` /
  `aging_prediction...regulator_coefficients.csv`. Those files are **not** in `data/`
  (which has `DE_stats`, `guide_kd_efficiency`, `Th2_Th1_polarization_signature_DE`,
  and the cluster enrichment table). Does the entity-A definition rest on data that
  doesn't exist here?
- **Referee disease-specificity gap.** The LBD question targets ONE disease C, but the
  referee's HOP-3 returns membership across ALL enriched clusters (EGR2 → 13 diseases;
  SLC1A5 → 9). Read `pyzobot_referee.py` HOP-3: does the returned verdict let you
  assert "gene → *asthma* specifically", or only "gene → some autoimmune diseases"?
  If the latter, "referee unchanged" is false for a disease-specific claim.
- **Disjoint gate too tight?** Candidate iff `ab≥3 AND bc≥3 AND ac_lit≤0 AND NOT
  ac_known`. Requiring zero A–C co-mentions AND passing KD AND significant program
  shift AND significant *specific*-disease enrichment is a narrow needle — is landing
  even one survivor realistic, or does the demo hinge on tuning `max_ac` up?
- **Condition first-classness.** B is program×condition; does the referee's
  condition handling actually thread through to a condition-specific verdict, or does
  condition get averaged somewhere?

## Preserve-intent (do NOT sand this off)
The novel claim is **"LBD as a question-GENERATION engine (not discovery), whose
output is mandatorily culled by a data-referee."** Critique its execution, but do not
converge it back into a generic "just run LBD" or "just run the referee" — the
generation-then-cull loop is the thesis.


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

Return JSON conforming to the supplied schema. round_number=1; findings ordered by priority (F-001, F-002, ...); each with severity/likelihood/blast_radius (1-5), priority (P0/P1/P2/accepted-risk), evidence (cite the file you opened), concern_path, suggested_action (one line), novelty_flag, concern_type (correctness|novelty). escalated_findings/dropped_findings/new_findings empty. convergence_status="round 1 — no prior position to converge with". convergence_sanding_warning=null. recommended_next_question = what Claude must address most in round 2. Begin.
