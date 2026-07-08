# LBD Question-Proposer — thin build spec (v2, fresh, new-work-only)

**Purpose.** Fill the Researcher-track **cold-start gap**: rich dataset, no question. This component
uses literature-based discovery (Swanson **ABC**) to *generate* the highest-value **untested**
questions the CD4+ T-cell Perturb-seq dataset can resolve, then hands each to a thin
**`referee_triple` adapter** over the already-built **referee**
(`docs/perturbseq-qc_2026-07-07/pyzobot_referee.py`) which answers it against the data.
Motivation + strategy: `memory/decisions/lbd-question-engine-reframe.md`.

**Compute:** laptop CPU + web APIs only. No GPU, no Colab. **Compliance:** all fresh code; public
data/APIs; git history is the proof.

> **v2 (hardened via 3-round repo-read codex-debate, 2026-07-07** —
> `docs/reviews/codex-debate_lbd-proposer-spec_2026-07-07.md`). Changes from v1, each repo-verified:
> A no longer keys off absent `*_regulator_coefficients.csv` (F-002) and is **not** seeded from the
> answer-conditioned `pyzobot_referee_ranked_full.csv` (F-009/F-011); B is **Th1/Th2 only** because no
> aging/cytokine receipt table exists in the substrate (F-003); "referee unchanged" is replaced by a
> **mandatory `referee_triple` adapter** that checks the *exact* requested disease C (F-001/F-005/F-012);
> the disjoint gate is a **ranked novelty score**, not a hard `ac_lit≤0` filter (F-007); C is the **14
> specific diseases** read from the CSV with umbrella terms excluded (F-006); "condition-specific" is
> claimed **only for the KD/effect/disease hops**, never the program hop (F-004).

---

## 1. Entities (bounded by the dataset — this is what keeps it thin)
Dataset = Zhu/Dann/Pritchard/Marson genome-scale CD4+ T-cell Perturb-seq (bioRxiv 2025.12.23.696273).

- **A = KD-gated significant regulators.** Derived **deterministically from tables that exist in
  `data/`**, independent of any disease answer (this is what keeps the proposer *generative*, F-011):
  1. **KD gate** — from `guide_kd_efficiency.suppl_table.csv`: keep genes with ≥1 guide
     `signif_knockdown=True` (same gate the referee's HOP-0 uses).
  2. **Significant effect** — from `DE_stats.suppl_table.csv`: keep genes with a significant on-target
     KD and/or ≥1 significant downstream DE gene.
  3. Optionally intersect with **T2 program membership**
     (`Th2_Th1_polarization_signature_DE_results_full.suppl_table.csv`, `variable` column).
  Target set ≈ 200–450 genes. **Do NOT seed A from `pyzobot_referee_ranked_full.csv`** — all 602 of its
  rows are already `disease_status=supported`, so seeding from it (even reading only `gene`/`condition`)
  biases A toward pre-survived referee winners and collapses the proposer into a re-ranker (F-011).
- **B = Th1/Th2 polarization program only.** The substrate has exactly one program receptor table
  (`pyzobot_join_spec.json` → `T2_Th2_Th1`; contrasts `Th2_vs_Th1 (Ota 2021)` and
  `Th2_vs_Th1 (Hollbacker 2021)`). **Aging and cytokine-production programs are OUT of v1 scope** —
  there is no receipt table for them, so a referee could not answer those questions (F-003). Condition
  ∈ {Rest, Stim8hr, Stim48hr} remains first-class for the KD / effect / disease hops (see §3).
- **C = 12 eligible specific diseases (of 14 non-negative-control rows)**, read from
  `cluster_autoimmune_enrichment_results.suppl_table.csv` at build time (F-006). The 12 specific-disease
  values are: ankylosing spondylitis, asthma, atopic eczema, celiac disease, Crohn's disease,
  Hashimoto's thyroiditis, multiple sclerosis, psoriasis, rheumatoid arthritis, systemic lupus
  erythematosus, type 1 diabetes mellitus, ulcerative colitis, **plus** the umbrella rows
  "autoimmune disease" and "inflammatory bowel disease" — which are **context only, NOT eligible C
  claims** (a novel-link claim must land on a specific disease). Read the list from the CSV; do not
  hardcode.

Matrix ≈ (200–450 A) × (1 program × 3 conditions B) × (12 eligible C) — small, computable in pandas.

## 2. Pipeline (3 stages, all CPU/API)

### Stage 1 — gather link evidence (API; cache everything to `data/lbd_cache/`, gitignored)
For each entity pair, get literature/DB co-mention counts. Prefer pre-computed resources over any NLP.
**v1 uses ONE co-mention source (Europe PMC, no key needed) + Open Targets for the known A–C set**
(F-008 — keep the API surface small; cache to fixtures so the demo is offline-reproducible):

| Link | v1 source (query) | Optional later |
|---|---|---|
| **A–B** gene↔program | Europe PMC co-mention count for gene × Th1/Th2 program-terms (Th2:"Th2 cells","GATA3","type 2 immunity"; Th1:"Th1 cells","IFN-gamma"). | PubTator3 `/relations`; OpenAlex count |
| **B–C** program↔disease | Europe PMC co-mention count for program-terms × disease name (+ synonyms). | PubTator3; OpenAlex |
| **A–C** gene↔disease (the KNOWN set to exclude) | **Open Targets GraphQL** association score for (gene, disease-EFO) + Europe PMC gene×disease lit co-mention count. | GWAS Catalog REST; DisGeNET |

Normalization: gene symbol→Ensembl/aliases via **MyGene**; disease→**Open Targets/MONDO id** via the
hand-pinned map in `src/arbiter/lbd/entity_maps.py` (the one non-mechanical step — **now pinned**,
resolved authoritatively against the Open Targets search API + EBI OLS4 on 2026-07-08, all 14 names
exact-matched; every canonical id is a **MONDO** id, NOT EFO — pinning EFO would silently return
"no known association" and falsely inflate novelty). NCBI API key → PubMed 10 req/s; 1 req/s otherwise.
Build note: query Open Targets from the **disease side** (`disease(id).associatedTargets`); the
target-side `associatedDiseases(efoIds:[...])` filter returned empty for the known GATA3×asthma pair.

### Stage 2 — rank novel A–C candidates (pandas, milliseconds)
**Preflight (mandatory before committing the demo claim, F-007):** compute a histogram of `ac_lit` and
`ac_known` (Open Targets score) over the whole A universe, so we know empirically how many strict-disjoint
candidates exist before promising one.

For every (A, B, C) triple with C in the 12 eligible diseases:
- `ab = cooccur(A,B)`, `bc = cooccur(B,C)`, `ac_lit = cooccur(A,C)`, `ac_known = OpenTargets_score(A,C)`.
- **Novelty score (ranked, NOT a hard gate):**
  `score = zscore(ab) + zscore(bc) − w·ac_lit − w2·ac_known`, higher = more novel-yet-literature-bridged.
  Keep the top N (e.g. 25). A soft eligibility band (`ab≥min_ab AND bc≥min_bc`) ensures both bridges
  exist; **`ac_lit` and `ac_known` push the rank DOWN rather than hard-excluding**, so "most novel
  available" always returns candidates even if strict-zero is empty. Defaults `min_ab=min_bc=3`, tuned
  from the preflight histogram.

### Stage 3 — emit questions (JSON handed to the adapter)
Each surviving triple → one question object (schema below), phrased in plain English so it reads as a
real research question, not a tuple.

## 3. Output contract → the `referee_triple` adapter (v1-MANDATORY, thin)
`lbd_questions.json`: a ranked list of:
```json
{
  "hypothesis_id": "H001",
  "question": "In CD4+ T cells, does perturbing <A> shift the Th1/Th2 polarization program, and is <A> a receipt-backed novel link to <C> — specifically in the <condition> state?",
  "A_gene": "GATA3",
  "B_program": "Th1_Th2_polarization",
  "C_disease": "asthma",
  "condition": "Stim8hr",
  "novelty": {
    "ab_cooccur": 41, "bc_cooccur": 120, "ac_lit_cooccur": 0,
    "ac_known_opentargets": 0.03, "is_disjoint": true
  },
  "score": 3.87,
  "sources": ["europepmc:...","opentargets:ENSG..-EFO_.."]
}
```

### The adapter contract (F-001 / F-005 / F-012 — the referee CORE is unchanged; this is a thin wrapper)
`referee_triple(A_gene, B_program, C_disease, condition)` — the deterministic map from a full triple to a
verdict **on that exact triple**. It reuses the referee's HOP-0/1/2 unchanged and **overrides only HOP-3**:

- **HOP-0 (gate) / HOP-1 (effect)** — as in `pyzobot_referee.py`, filtered by `condition` (condition-specific).
- **HOP-2 (program)** — Th1/Th2 shift across the Ota/Hollbacker contrasts. **This hop is contrast-based,
  NOT condition-resolved** (T2 grain is gene×contrast; F-004). The verdict text must NOT call the program
  shift condition-specific.
- **HOP-3 (exact disease C)** — filter `t3_exploded` (which already carries `gene`, `disease`, `gene_set`
  per `pyzobot_referee.py:70-74`) to `gene==A_gene AND disease==C_disease AND gene_set==downstream_<condition>`.
  - row exists AND `p_adj_fdr < 0.05` → **HOP-3 supported for C**.
  - gene appears in other diseases but the C row is absent or `FDR ≥ 0.05` → **HOP-3 refuted for C**
    (this is the case the generic referee would wrongly pass).
  - gate/effect failed upstream → **untested** (halt, per the hero-feature QC rule).
- **Triple verdict is synthesized AFTER exact-C HOP-3**, so `overall` can never report supported while C
  is refuted. Every status carries its receipt value, as the referee already does.

Then classify the *answer to the LBD question*:
- **disjoint in lit + `referee_triple` = supported on the specific C** → **receipt-backed NOVEL hypothesis**
  (the money shot: a gene→*specific-disease* link the literature never made, that the data supports).
- **`referee_triple` = untested** → knockdown failed the gate; unanswerable here (honest).
- **`referee_triple` = refuted for C** → LBD proposed it, data killed it (the cull; the R01 answer in action).

**Why this stays a GENERATIVE engine, not a lookup (round-2 tension, F-011):** A is built from raw
KD/DE tables with no disease answer in them; the A–C novelty signal comes from *external* literature
(Europe PMC / Open Targets), not from the referee's own outputs; and the referee runs *after* generation
and can **refute**. The generated-vs-survived counts are the evidence of independence — report them.

## 4. Demo scope (thin, for the video)
1. Run the proposer over the bounded entity set → `lbd_questions.json` (ranked untested questions the
   *dataset itself* suggested — "here's what to ask when you didn't have a question"). Show the
   **generated-vs-survived** counts.
2. `referee_triple` adjudicates the top few, live.
3. Land on ONE **disjoint-in-literature + data-supported specific-disease** result → the receipt-backed
   novel finding. Show one **refuted-for-C** to prove the cull is real.

## 5. Build notes
- New files only: `src/arbiter/lbd/` (`sources.py` Europe PMC + Open Targets clients, `entities.py` build
  A/B/C from the CSVs, `cooccur.py` set/score logic, `propose.py` orchestrator, `emit.py`) **plus** the
  thin `referee_triple` adapter (add to the referee module or a new `adapter.py` next to it). Third-party
  libs OK (`requests`/`httpx`, `pandas`, `pydantic`). Cache raw API JSON under gitignored `data/lbd_cache/`.
- **Effort: ~1–1.5 days fresh** (revised up from 0.5–1: MyGene alias resolution, disease→EFO map,
  Europe PMC + Open Targets clients, caching, the adapter, and the preflight are more than trivial pandas;
  F-008). Delegatable to Codex once this spec + the disease→EFO and program→keyword maps are pinned.
  Tag: `[HYBRID]` (Claude pins the entity/keyword maps + scoring + adapter semantics; Codex builds the
  clients/logic; Claude reviews). **The referee finding is already a complete submission — keep the LBD
  layer thin and protect demo-video time** (judges weight the demo heavily).

## 6. Risks
- **Generative-vs-lookup collapse (F-011)** — mitigated: A from raw KD/DE tables only; `ranked_full`
  banned from seeding; novelty from external literature; report generated-vs-survived counts as the proof.
- **Disease-specificity correctness (F-001/F-012)** — mitigated: `referee_triple` checks the exact C
  before synthesizing `overall`; umbrella diseases excluded as claims.
- **Overproduction** — mitigated: the referee is the mandatory cull; report generated-vs-survived.
- **Disease/program → keyword/EFO mapping quality** drives everything — pin these maps by hand (12
  diseases + 1 program) and eyeball them; the one non-mechanical step.
- **No disjoint survivor exists** (preflight shows zero) — fallback: widen the novelty band and rank, or
  demo `referee_triple` on 2–3 hand-built disjoint triples; the pipeline remains the method either way.
- **API rate limits** (not compute) — cache aggressively; NCBI key; one source in v1 keeps call volume low.
