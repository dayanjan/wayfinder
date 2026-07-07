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
