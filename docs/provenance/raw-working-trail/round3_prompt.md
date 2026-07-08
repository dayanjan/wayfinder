You are continuing an iterative cross-model debate on an implementation-plan artifact.
This is round 3 (the FINAL round) and it is the ACCEPTANCE GATE. Between round 2 and now,
Claude REWROTE the artifact `docs/lbd-proposer-spec.md` to v2 to land the accepted findings
(this directly addresses your round-2 P0 F-010). Your job: verify the REVISED artifact
against the repo. ESCALATE anything still wrong, DROP what is now fixed, SURFACE any NEW
gap the rewrite introduced, and decide convergence.

# CRITICAL: repo-read acceptance gate — verify the REVISED artifact against the code

You are READ-ONLY inside the target repo. The artifact below is the NEW v2 text (re-read it
fresh; do not rely on your memory of v1). Open referenced files to confirm the rewrite is
faithful. Specifically:
- `data/guide_kd_efficiency.suppl_table.csv` and `data/DE_stats.suppl_table.csv` headers —
  does A ("KD-gated significant regulators") actually derive from these? Do they carry a
  `signif_knockdown`-style gate column and a significance/effect column?
- `docs/perturbseq-qc_2026-07-07/pyzobot_referee.py` lines ~70-74 (`t3_exploded`) and the
  HOP-3 logic — is the v2 `referee_triple` HOP-3 override (filter on
  `disease==C_disease AND gene_set==downstream_<condition>`, supported iff FDR<0.05,
  else refuted-for-C) faithfully specified against the real code?
- `data/cluster_autoimmune_enrichment_results.suppl_table.csv` — are the 14 diseases and the
  two excluded umbrella terms correct?
- Grep the v2 artifact for any RESIDUAL v1 claim that should have been removed (absent
  `*_regulator_coefficients.csv`; aging/cytokine programs as in-scope; "referee consumes it
  unchanged"; hard `max_ac=0` gate; ~17 diseases; 0.5-1 day).

# Framing question

Is the REVISED v2 `docs/lbd-proposer-spec.md` now build-ready — the shortest CORRECT path to
a receipt-backed, condition-specific NOVEL finding by July 13, faithful to the repo? And is
the constrained pipeline still a genuinely GENERATIVE LBD engine (Claude argues yes; take a
final position)?

# Preserve-intent directive

Novel claim: "LBD as a QUESTION-GENERATION engine whose output is MANDATORILY culled by a
data-referee." v2 closes the answer-leak path (bans `ranked_full` seeding). Confirm the claim
is intact and not sanded; if you think the constrained substrate is too thin to be generative,
say so as an open question rather than agreeing by default.

# Round history

## Round 1 — Codex findings (ids): F-001..F-009 (see prior). All accepted by Claude conceptually.
## Round 2 — Codex: DROPPED F-004, F-006; ESCALATED F-001/2/3/5/7/8/9 because the artifact was
unedited; NEW F-010 (P0 fixes-didn't-land), F-011 (ranked_full answer-conditioned at row level —
all 602 rows disease_status=supported), F-012 (adapter needs exact-C verdict semantics).

## Round 2 — Codex findings (verbatim JSON)
[
 {
  "id": "F-010",
  "title": "Accepted fixes did not land in the implementation-plan artifact",
  "severity": 5,
  "likelihood": 5,
  "blast_radius": 5,
  "priority": "P0",
  "evidence": "`docs/lbd-proposer-spec.md:17-27` still names absent `*_regulator_coefficients.csv`, aging/cytokine programs, ~17 diseases, and a 3 programs x 3 conditions matrix; `docs/lbd-proposer-spec.md:46-47` still uses a hard `max_ac=0` candidate gate; `docs/lbd-proposer-spec.md:74-76` still says no referee changes are needed and to call `referee(A_gene, condition_hint...)`; `docs/lbd-proposer-spec.md:94` still claims ~0.5-1 day fresh effort.",
  "concern_path": "A builder following the artifact, rather than Claude\u2019s prose disposition, will implement the already-rejected plan: wrong source tables, unsupported B programs, generic gene-condition referee calls, hard disjoint filtering, and the old time estimate. This reintroduces the round-1 correctness failures despite Claude accepting them conceptually.",
  "suggested_action": "Revise `docs/lbd-proposer-spec.md` itself before implementation: A from KD/DE/T2 only, B = Th1/Th2 only, exact CSV-derived disease list with umbrella exclusion, ranked novelty not hard zero, and mandatory `referee_triple(A,B,C,condition)`.",
  "novelty_flag": false,
  "concern_type": "correctness"
 },
 {
  "id": "F-011",
  "title": "`ranked_full` is answer-conditioned even if only gene/condition columns are read",
  "severity": 4,
  "likelihood": 5,
  "blast_radius": 4,
  "priority": "P1",
  "evidence": "`docs/perturbseq-qc_2026-07-07/pyzobot_referee_ranked_full.csv:1` contains answer fields including `top_disease`, `overall_status`, `disease_OR`, `disease_FDR`, `chain_score`, and statuses. CSV inspection showed 602 rows, 457 genes, all rows `disease_status=supported`, with 350 rows already labelled as validated chains plus 15 caveated validated chains.",
  "concern_path": "Even selecting only `gene,ensg,condition` from this file biases the proposer toward genes already passing HOP-3 disease support. The LBD layer then becomes a literature novelty sorter over pre-survived referee outputs, which weakens the generate-then-cull claim and makes generated-vs-culled counts misleading.",
  "suggested_action": "Do not seed A from `ranked_full`. Build A directly from `guide_kd_efficiency.suppl_table.csv`, `DE_stats.suppl_table.csv`, and optionally T2 membership, then let the referee determine disease support after question generation.",
  "novelty_flag": true,
  "concern_type": "novelty"
 },
 {
  "id": "F-012",
  "title": "The adapter is thin for C, but the artifact still lacks the exact verdict semantics",
  "severity": 4,
  "likelihood": 4,
  "blast_radius": 4,
  "priority": "P1",
  "evidence": "`docs/perturbseq-qc_2026-07-07/pyzobot_referee.py:70-74` builds `t3_exploded` with `gene`, `cluster`, `disease`, and `gene_set`, so exact C filtering is small. But `_hop3` logic at `pyzobot_referee.py:251-266` supports any significant disease after filtering only `gene` and `gene_set`, and `docs/lbd-proposer-spec.md:74-76` still claims the existing `referee(A_gene, condition)` already checks disease C.",
  "concern_path": "If the adapter is not specified precisely, implementers may only post-filter the receipt after `overall` has already been synthesized. That can leave inconsistent verdicts where `overall` says supported while exact C is refuted or untested.",
  "suggested_action": "Specify `referee_triple` as a first-class contract that computes exact-C HOP-3 status before synthesizing the triple verdict, including what happens when the gene appears in other diseases but not requested C.",
  "novelty_flag": true,
  "concern_type": "correctness"
 }
]

## Round 3 — Claude's revision: REWROTE the artifact to v2. F-010 resolved (spec rewritten);
F-011 accepted+hardened (ranked_full fully banned from seeding; A from raw KD/DE/T2 only);
F-012 accepted (referee_triple exact-C contract specified). Position on the generative-vs-lookup
tension: stays generative (A from answer-free tables; novelty from external lit; referee culls
after generation), with a documented fallback if no disjoint survivor exists.

# Claude's round 3 position (full text follows)

# Round 3 — Claude's final position (the artifact is now rewritten)

The round-2 P0 was correct and decisive: my accept/reject was prose; the **artifact**
still encoded the rejected v1 design. I have now **rewritten `docs/lbd-proposer-spec.md`
to v2**, landing every accepted finding into the spec a builder actually follows. This
round is the acceptance gate: verify the *revised* artifact against the repo.

## Disposition on round-2 findings
- **F-010 (P0, fixes didn't land in the artifact) — RESOLVED.** The spec is rewritten.
  A now derives from `guide_kd_efficiency` + `DE_stats` (+ optional T2), not the absent
  `*_regulator_coefficients.csv`; B = Th1/Th2 only; C = 14 CSV-read diseases with the two
  umbrella terms excluded; the disjoint hard-gate is now a ranked novelty score with a
  mandatory preflight histogram; "referee unchanged" is replaced by the mandatory
  `referee_triple` adapter; effort revised to ~1–1.5 days. See the v2 banner + §1–§6.
- **F-011 (P1, ranked_full is answer-conditioned at the row level) — ACCEPT, HARDENED.**
  You're right that all 602 rows are `disease_status=supported`, so even reading only
  `gene`/`condition` biases A. v2 **bans `ranked_full` from seeding entirely** (§1, bold)
  and builds A only from raw KD/DE/T2 tables that contain no disease answer. The
  "generative not lookup" rationale is now written into §3.
- **F-012 (P1, adapter needs exact verdict semantics) — ACCEPT.** §3 now specifies
  `referee_triple` as a first-class contract: HOP-3 filters `t3_exploded` on
  `disease==C_disease AND gene_set==downstream_<condition>`; supported iff that exact row
  FDR<0.05; "gene in other diseases but not C" → **refuted-for-C**; the triple `overall`
  is synthesized **after** exact-C HOP-3, so it can never say supported while C is refuted.
- **F-004 / F-006 (dropped in round 2) — stay resolved** in the rewrite (condition
  wording names only KD/effect/disease hops; 14 diseases read from CSV, umbrellas excluded).

## Position on the round-2 generative-vs-lookup tension
The constrained pipeline **remains a generative LBD engine**, and v2 §3 states why:
(1) A is built from raw KD/DE tables with no disease answer in them; (2) the A–C novelty
signal comes from *external* literature (Europe PMC / Open Targets), independent of the
referee; (3) the referee runs *after* generation and can refute. The generated-vs-survived
counts are the falsifiable proof of independence. The single-program substrate is a real
limit, so v2 documents the honest fallback (§6): if the preflight histogram shows no
disjoint survivor, widen the band or demo `referee_triple` on 2–3 hand-built triples — the
pipeline stays the method. I do NOT think the honest move is to drop the proposer: the
generate-then-cull loop with reported counts is the thesis, and it survives the constraints.

## Preserve-intent check (final)
The novel claim — **LBD generates questions, a data-referee mandatorily culls them** — is
intact and now *more* defensible, because the answer-leak path (ranked_full seeding) that
would have quietly turned it into a re-ranker is explicitly closed.

## What round 3 should verify
Read the **rewritten** `docs/lbd-proposer-spec.md` against the repo and confirm: (a) A is
now derivable from the named existing tables (check `guide_kd_efficiency` /`DE_stats`
headers carry the needed gate/significance columns); (b) the `referee_triple` HOP-3
override is faithfully specified against `pyzobot_referee.py:70-74` / `:251-266`; (c) no
residual v1 claim survived the rewrite. Flag anything still inconsistent, or confirm the
spec is build-ready.


# Artifact (REVISED v2 — read fresh)

## FILE: docs/lbd-proposer-spec.md

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
- **C = 14 specific autoimmune diseases**, read from
  `cluster_autoimmune_enrichment_results.suppl_table.csv` at build time (F-006). The non-negative-control
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

Normalization: gene symbol→Ensembl/aliases via **MyGene**; disease→EFO via a small **static hand-pinned
map** built once from the 14 CSV disease names (this is the one non-mechanical step — pin + eyeball it).
NCBI API key → PubMed 10 req/s; 1 req/s politeness otherwise.

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


# Output requirements

Return JSON conforming to the supplied schema. round_number=3. findings = current-round set. escalated_findings = prior F-ids still wrong (rationale). dropped_findings = prior F-ids now fixed by the rewrite (rationale). new_findings = F-ids first surfaced this round. convergence_status = "converged" if new_findings empty AND >=80%% of prior findings addressed, else "still iterating". convergence_sanding_warning: set only if converged AND novel claim sanded, else null. recommended_next_question = the single most important thing to do before building (or "debate concluded"). Cite file:line for any repo-verified finding. Begin.
