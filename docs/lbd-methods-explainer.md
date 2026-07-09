# How the LBD worked — plain-language explainer + manuscript Methods seed

**2026-07-09.** Two layers: **Part 1** is the intuitive explanation (the version that landed in
conversation); **Part 2** is the precise mechanism as actually implemented (`src/arbiter/lbd/`);
**Part 3** is a draft Methods paragraph. Source of truth for the code: `docs/lbd-proposer-spec.md`
(v2) + `docs/pipeline-inventory-and-cs-mapping_2026-07-09.md` (steps A–B).

---

## Part 1 — The intuition (plain language)

### The one idea: Swanson's triangle
Literature-Based Discovery (LBD) looks for **two facts that are each written down somewhere, but that
nobody has connected.** Every hypothesis is a triangle with three corners:

> **A (a gene) → B (a biological program) → C (a disease)**

We want pairs where **A links to B**, and **B links to C**, but **A and C have never been directly
linked.** If A→B and B→C are both true, then A→C is *implied* — and if no one has written it down, that
implied link is a **candidate discovery.** This is Don Swanson's 1986 move: his classic case was fish
oil (A) → blood viscosity (B) → Raynaud's disease (C), where no paper connected fish oil to Raynaud's;
he found it by joining the two halves, and it later checked out.

### What we actually "searched for" — a fixed grid, not clever terms
The subtle part: **we did not brainstorm search terms.** The three corners were nailed down in advance,
so the search was mechanical and reproducible (no cherry-picking):

- **B was fixed to one program:** Th1/Th2 T-cell polarization — the only program our dataset can speak to.
- **C was a fixed menu of 12 diseases** (asthma, atopic eczema, lupus, …), each pinned to its canonical
  ontology ID.
- **A — the genes — came from the DATA, not from reading papers.** We took every gene that, in the real
  CRISPRi Perturb-seq experiment, (1) was successfully knocked down, (2) had a real downstream effect, and
  (3) measurably shifted the Th1/Th2 program → **~3,935 candidate genes**, built **without ever looking at
  disease information** (so we never peek at the answer).

So "what to search for" = **every (gene, disease) pair** — and for each, the same three fixed questions.

### The three literature questions (just counting papers)
For a gene A and disease C we ran three **co-mention counts** ("how many papers mention both?"):

1. **A–B:** papers mentioning *gene A* + *Th1/Th2*? → want **> 0** (gene should plausibly touch the program).
2. **B–C:** papers mentioning *Th1/Th2* + *disease C*? → want **> 0** (program should matter to the disease).
3. **A–C:** papers mentioning *gene A* + *disease C* directly? → want **LOW / ZERO** (if already connected,
   it's not a discovery).

Plus a curated-database check: is A already a **known** target for C in **Open Targets** (genetics
evidence)? → want near-zero. **The winning pattern:** A↔B present, B↔C present, but A↔C is a **hole** in
both the literature and the databases — the missing edge.

### The twist that beats plain Swanson: anchor in real data
Pure literature-LBD floods you with "novel" links that are really just **obscure** (a gene looks novel
only because nobody studied it). We fixed that by requiring an **experimental anchor**:

- the gene doesn't just get *mentioned* near Th1/Th2 — it **actually shifts Th1/Th2 when knocked out in the
  lab**;
- the disease link isn't just "Th1/Th2 matters for eczema" — the gene's **downstream fingerprint is
  statistically enriched in eczema-associated gene clusters in the data.**

**Literature tells us what's NOT connected yet (the gap); the data tells us it's actually real (the
receipt).** We then rank candidates to reward exactly that combination — *quiet in the literature, loud in
the data* — and a separate deterministic referee checks each survivor's receipt at every hop.

### NAB2, concretely
- **Literature:** essentially nothing connects NAB2 to eczema (6 stray co-mentions, no curated genetic
  association) → **the gap**.
- **Data:** knock out NAB2 → big effect (301 downstream genes), clear Th1/Th2 shift, downstream signature
  enriched in eczema clusters (OR ≈ 3.5–3.9) → **the receipt**.
- Two facts in plain sight — "NAB2 controls Th1/Th2" (our data) and "Th1/Th2 drives eczema" (literature) —
  that **nobody had joined into "NAB2 → eczema."** That join is the finding.

---

## Part 2 — The precise mechanism (as implemented)

### Entities (the three corners, pinned)
- **A universe (`entities.build_a_universe`, answer-free):** genes passing **T4 KD-gate** (≥1 guide
  `signif_knockdown`) ∩ **T1 significant effect** (`ontarget_significant` or `n_downstream>0`) ∩ **T2
  program-significant** (Th1/Th2 signature `adj_p_value<0.05`). Never touches the disease table T3. Carries
  `n_downstream` as the **effect-strength prior**. Stim8hr: **3,935 genes**.
- **B (`entity_maps.PROGRAM`):** Th1/Th2 polarization; keyword arms for process ("Th2 cells", "T helper 2",
  …) and markers (GATA3, IL-4, T-bet, IFN-γ). Asymmetric use: **A–B uses process terms only** (don't inflate
  on marker proximity); **B–C keeps markers** (disease literature legitimately cites them).
- **C (`entity_maps.DISEASES` + `verify_disease_ids`):** 12 eligible diseases → **MONDO** IDs (e.g. atopic
  eczema `MONDO_0004980`), each re-verified live against **Open Targets search + EBI OLS4**. Load-bearing:
  MONDO ≠ EFO — a wrong ID makes Open Targets return "no known association" for every gene and falsely
  inflates novelty everywhere.

### The five signals per (A, B, C) — all deterministic lookups
1. `ab` = Europe PMC `hitCount("A" AND Th1/Th2 process terms)` (`sources.cooccur_count`; all terms quoted).
2. `bc` = Europe PMC `hitCount(Th1/Th2 terms+markers AND "C")` (constant per disease).
3. `ac_known` = **Open Targets GraphQL** disease→targets association score for A (0 if absent = novelty).
4. `ac_lit` = Europe PMC `hitCount("A" AND "C")` (computed only for referee survivors, for API cost).
5. `effect` = `n_downstream` from T1 (the in-data strength prior).

### The objective (gated + balanced, not a naive sum) — `cooccur.py`
- **GATE (eligibility, all must hold):** `ab ≥ ab_gate` (a universe percentile, default the median — kills
  "novel-only-because-understudied") **AND** `bc ≥ 3` **AND** `ac_known ≤ 0.1`. Note `ac_lit` is **not** in
  the gate (raw co-mention is noisy; hard-gating it would exclude every well-studied strong regulator).
- **RANK score:**
  `score = min( z(log1p ab), z(log1p bc) ) + β·z(log1p effect) − w·log1p(ac_lit) − w2·ac_known`
  (β=1, w=1, w2=3; z over the universe). `min(z_ab,z_bc)` = a **balanced** bridge (one strong axis can't
  rescue a weak other); `β·z(effect)` = the **"loud in the data"** reward; the last two terms push
  novel-yet-bridged candidates up without hard-excluding. (Objective *designed* via Codex consult +
  3-round codex-debate.)

### The funnel — `propose.sweep` (order minimises API cost)
Build A + prefetch `bc`/`ac_known` (12 calls each) + `ab` (one/gene) → **GATE** → **referee-cull-first**
(the deterministic 4-hop referee runs locally, free, keeping only `supported*`) → compute `ac_lit` + final
score for survivors → rank → emit. **Stim8hr: 3,935 genes → 22,039 eligible pairs → 43 disease-supported →
30 clean full-chain.** Literature/DB gate ∩ referee is a **joint** cull (the referee alone supports
395/47,220; the novelty gate takes 395→43).

### Why this is honest
- **Answer-free A** (never reads T3 or the referee's own ranked output) ⇒ the gene list can't be
  contaminated by the disease answer.
- **Deterministic throughout** ⇒ no LLM asserts biology; Claude only interprets receipts. The only judgment
  is *offline, at build time*: pinning the disease/program menus and *designing* the scoring objective.
- Ranking by **effect** (not hard-gating on `ac_lit=0`) tracks *importance*, not *obscurity* (the
  pure-disjoint hit NUDT1×T1D was demoted for a trivial 4-gene effect — proof the ranking works).

---

## Part 3 — Draft Methods paragraph (manuscript seed)

> **Literature-based candidate generation.** We framed hypotheses as directed triples *gene → Th1/Th2
> polarization program → autoimmune/allergic disease* (Swanson ABC discovery). The gene set (A) was defined
> *a priori* from the perturbation data alone — genes with ≥1 significantly knocked-down guide (guide-KD
> table), a significant on-target or downstream transcriptional effect (DE table), and a significant Th1/Th2
> polarization shift (polarization-signature table) — without reference to any disease annotation (n = 3,935
> at the 8-h stimulation condition). The program (B) was fixed; the disease set (C) comprised 12 immune
> diseases mapped to MONDO identifiers and verified against Open Targets and the EBI Ontology Lookup Service.
> For each (gene, disease) pair we quantified three literature co-mention counts via Europe PMC — gene↔program
> (A–B), program↔disease (B–C), and gene↔disease (A–C) — and the curated gene→disease genetic-association
> score from Open Targets. Candidates were required to satisfy A–B ≥ the cohort-median count, B–C ≥ 3, and a
> curated association ≤ 0.1 (i.e. no established gene–disease link), and were ranked by a balanced objective
> rewarding the weaker of the two bridge axes and the in-data effect size while penalising any existing
> gene–disease co-mention, so that candidates were understudied in the literature yet strong in the data.
> Surviving triples were adjudicated by a deterministic four-hop referee (below), yielding 30 clean
> full-chain nominations at the 8-h condition, of which NAB2 → Th1/Th2 → atopic eczema was the highest-ranked
> near-novel candidate.

*(Companion referee Methods live in the referee reconstruction; confounder/validation Methods in
`docs/replication/README.md` + `docs/source_paper_read_eczema_2026-07-08.md`.)*
