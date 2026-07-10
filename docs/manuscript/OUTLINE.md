# Wayfinder manuscript — working outline (v1.2, post-debate — build-ready)

**Status:** draft skeleton for a 3-round repo-read codex-debate (`--preserve-intent`). This is a
*plan/spec*, not prose. The debate should (a) verify every claim in §7 against the repo, and (b)
attack the structure/positioning as a hostile FRMA reviewer.

**Changelog — v1.1 (2026-07-10):** round-1 debate fixes folded in (Codex verified C1–C21 hold).
Resolved: DOI = `10.64898/2025.12.23.696273` (Crossref-registered; `10.1101/…` is unregistered).
Applied: CTLA4 dropped from the ledger (mis-sourced); "oracle" → substrate-for-perturbation-hops +
association-receipt-for-disease; CS-liveness split into replay vs. live-microsweep vs. external;
program-hop tautology surfaced into Methods/Results; self-audit independence operationalized; ledger
reframed as demonstration; manuscript-facing calibrated-language rule added; §7 sources repointed to
primary JSON/receipt artifacts.

**Changelog — v1.2 (2026-07-10):** round-2 self-consistency fixes. Codex dropped 5 findings as resolved
(DOI, program-tautology, liveness, independence, R01) and caught stale top-of-file sentences: the §0
headline now names both receipt classes + says the ledger *demonstrates* (not "proves"); CTLA4 removed
from the §0 demo-scope line too; C1–C10 rows repointed to primary JSON; new F-011 handled (cite Stage-1
JSON for numbers, post-critic Stage-5 receipt for prose — the pre/post-critic diff IS the self-audit).

---

## 0. Bibliographic frame (decided)

- **Type:** ORIGINAL RESEARCH (methods + demonstration fused into a discovery narrative — the Henry
  house style, see `references/frma-06-644728.pdf`).
- **Framing stance (decided 2026-07-10):** Wayfinder is an **APPROACH / method**, NOT a software product.
  The contribution is *receipt-backed adjudication of machine-generated hypotheses* + what it found;
  the code / CS pipeline / notebook are the **vehicle** that shows the approach is real and reproducible,
  not a released, supported tool. Rhetorical rule for all drafting: name Wayfinder as "an approach / a
  method"; "the referee" is a *component* of it; reserve "workbench / platform / product" for **Claude
  Science** (someone else's product the approach runs on). This deliberately lowers the reviewer burden
  (no packaging / user-study / generality-across-datasets expectations) and matches Henry's "the novelty
  is how known components are applied." Consistent with `CLAUDE.md` ("the tooling is the method/vehicle;
  the deliverable is a reproducible finding + how Claude Science reached it").
- **Venue:** *Frontiers in Research Metrics and Analytics*, "Text-mining and Literature-based
  Discovery" section — the same venue as the Henry lineage paper. Audience = LBD/informatics
  readers + bench scientists (dual-teach).
- **Author:** Dayanjan Shanaka Wijesinghe (solo).
- **Title (locked 2026-07-10):** *Closing the loop on literature-based discovery: receipt-backed
  adjudication of machine-generated hypotheses against Perturb-seq data.* (Method-forward, approach-framed,
  Henry-echo. Chosen from 4 variants.)
- **Headline contribution (decided):** the **agentic loop** — Claude generates hypotheses,
  deterministic tools adjudicate each hypothesis with a receipt at every hop — *perturbation-substrate*
  receipts for the KD / effect / program hops and an *association / enrichment* receipt for the disease
  hop (F-008) — and an independent critic model (role/model/checkpoint, F-009) enforces calibrated
  language on the platform's own output. NAB2 is the worked example; the verdict **ledger**
  *demonstrates* the referee discriminates on worked examples (supported / untested / refuted) — a
  demonstration, not a validated accuracy benchmark (F-003).
- **Demonstration scope (decided):** verdict **ledger + NAB2 hero**. NAB2 deep worked case (all hops
  + STAT6 cis-refutation) PLUS the discriminating ledger (EGR2 supported / IL2 untested / **SLC1A5
  refuted** / NUDT1 supported-weak). *(CTLA4 excluded — F-002.)*
- **NAB2 drug-direction thread (decided):** DepMap + GEO direction-mining ("NAB2 = Th2 brake,
  knockdown likely backwards → restore/UP-modulate") goes to **Discussion as the next experiment**,
  NOT Results (association-backed, needs perturbation proof — widening it into Results widens the
  honesty surface for no evidentiary gain).

---

## 1. The template we inherit (Henry et al. 2021)

Henry, **Wijesinghe**, Myers, McInnes (2021), *Using Literature Based Discovery to Gain Insights Into
the Metabolomic Processes of Cardiac Arrest*, Front. Res. Metrics Anal. 6:644728,
doi:10.3389/frma.2021.644728. The operator is second author — this is his own LBD lineage.

**Inherited wholesale:** the genre ("we developed the approach, here is the finding it produced — the
novelty is in how known components are applied", Henry's own words);
the Intro→Background(dual-teach)→Methods→Results→Discussion skeleton; the figure grammar (a
method-as-loop Fig 1; a generic-then-specific pipeline pair; a mechanism figure; **tables that show
the tool's actual output on the page** — Henry's Table 2 is the ancestor of our receipt ledger);
calibrated language; the human-in-the-loop philosophy ("the tool sparks; the human/referee decides");
"re-derive the known to earn trust for the novel"; a candid, generous Limitations section.

**Where Wayfinder must build new scaffolding (no Henry analog):**
1. The **falsification thesis** — the confident, receipt-backed NO + the knockdown-QC gate
   (failed KD → *untested*, not *negative*). Henry is confirmation-shaped.
2. **Retrospective adjudication** against a pre-existing Perturb-seq substrate (receipt = OR/p/effect
   lookup), vs. Henry's prospective in-vivo rat validation.
3. The **agentic Claude layer** — deterministic tools vs. Claude judgment; actor–critic; native
   Claude Science reproduction + self-audit. Henry = deterministic co-occurrence + manual review.

**The narrative frame we own:** three NIH reviewers killed the R01 (**1R01LM015392-01**) with
*"the same major problem that has plagued all LBD work: it generates an enormous number of
hypotheses, almost none of which ever get followed up."* Henry is the lineage that provoked that
critique; **Wayfinder is the paper that answers it.**

---

## 2. Section skeleton

**1. Introduction** (~2.5 pp) — the two floods (>1M papers/yr + omics runs returning millions of
measurements/sample); LBD as the bridge; **the follow-up problem** (quote the R01 critique verbatim);
thesis = the agentic loop that generates *and* adjudicates *and* self-audits; roadmap sentence (Henry move).

**2. Background** (dual-teach, ~3 pp)
- **2.1 The LBD follow-up problem.** Swanson ABC recap (brief — this audience knows it); the
  overproduction/no-validation gap; Henry as the lineage that hits the wall.
- **2.2 The Perturb-seq substrate: what counts as a receipt at each hop.** What genome-scale CRISPRi
  Perturb-seq is; why 4 aggregated supplementary tables (guide-KD, DE, Th1/Th2 signature, cluster
  disease-enrichment) function as a receipt store; CPU-feasible (no raw 22M-cell matrices).
  **Two receipt classes, stated up front (F-008):** the KD / effect / program hops are backed by a
  *held experimental substrate* (real perturbation measurements); the disease hop is an *association /
  enrichment receipt* (Open Targets GWAS-genetic, no colocalization/LD control) — a nomination, NOT an
  experimental oracle for disease causality. The paper never calls the disease hop experimental proof.
- **2.3 Agentic LLMs for science** (teach — new to the FRMA reader). Tool-use; the actor–critic
  pattern; the discipline "Claude *interprets* receipts, it never asserts biology"; deterministic
  lookups are tools, visible agency is reserved for judgment; Claude Science as the workbench.

**3. Materials and Methods** (~2.5 pp)
- **3.1 Materials.** The 4 Perturb-seq tables (source + `fetch_data.sh`); the 12 disease→MONDO menu
  (verified vs. Open Targets + EBI OLS4; MONDO≠EFO caveat); Europe PMC + Open Targets GraphQL; the
  model cast (Opus 4.8 author / Sonnet 5 critic / Haiku 4.5 inline).
- **3.2 Generation.** Answer-free A-universe (KD-gate ∩ effect ∩ program-significant, never touches
  disease); the 5 deterministic signals (ab, bc, ac_known, ac_lit, effect); the gate + balanced
  objective `min(z_ab,z_bc)+β·z(effect)−w·log1p(ac_lit)−w2·ac_known`.
- **3.3 The referee.** The 4-hop chain (QC gate → effect → program → disease) + supported / refuted /
  **untested** logic; determinism; the confident-NO mechanism (refuted_effect / supported_weak /
  QC-untested demotions). **State plainly here (F-004):** the A-universe is *preselected* on
  program-significance (`entities.build_a_universe`, `program_significant=True`), so inside the funnel
  the program hop is a tautology (`refuted_program ≡ 0` by construction). The program hop discriminates
  in the *individual receipt* (NAB2's Ota z=7.71), not as an independent funnel filter — say so in
  Methods, not only in Limitations.
- **3.4 The agentic loop in Claude Science.** How CS authored + ran the generator + referee; provenance
  from its own audit DB (`operon-cli.db`); the critic model's calibrated-language enforcement. (Carries
  the headline contribution.) **How we OPERATE the instrument (distinctive, under-appreciated — give it
  weight):** Claude Science exposes **no task-submission API/CLI**; the only way to make it *scriptable
  and reproducible* is to drive its web UI. We built a headless driver (Playwright + a saved
  authenticated session/`STORAGE_STATE`) that submits a task prompt, **auto-approves CS's in-loop
  sandbox cards — folder / code-execution / network — for true zero-click operation**, polls the run to
  completion, and pulls the resulting artifacts + provenance from CS's own audit DB. The driver is
  orchestrated from **Claude Code** (an agent driving an agentic workbench). This is what turns a
  click-once web session into a *reproducible* pipeline run; it is also an honest **limitation** (UI
  automation depends on the CS front-end; there is no stable public contract) → note in §5.3. Connects to
  the "prefer a direct API" principle by its exception: *no direct API exists, so automation is the
  necessity, stated as such.* **Three liveness claims kept distinct (F-005), never blurred:**
  (a) *full-scale reproduction* — the real `propose.sweep()` ran unchanged over the full 3,935-gene
  universe **inside CS**, but as a **cached-receipt replay under a pure-replay guard** (cache delta 0;
  no live web calls during the sweep); (b) *live authorship* — a separate **12-gene from-scratch
  microsweep** where CS wrote its own generator and made live Europe PMC / Open Targets calls (NAB2's
  effect was too low to rank top-12, so it did **not** appear — no cherry-picking), plus a Stage-0 probe
  proving live external access; (c) *cross-model independence* — kept **external by design** (Codex + the
  5-agent replication), NOT claimed as CS-native. **Independence, operationalized (F-009):** the CS
  self-audit is *role/model/checkpoint* independence (Opus 4.8 author vs. an independent Sonnet 5 critic
  at 3 checkpoints), NOT cross-vendor independence — that role is Codex's, externally.

**4. Results** (~3.5 pp)
- **4.1 The funnel + the verdict ledger** (Table 2 — the money table). Framed as **demonstration
  evidence that the referee discriminates** on worked examples, NOT as a validated precision/recall
  benchmark (F-003) — the honest claim is "here is the referee saying supported / untested / refuted
  with a receipt each," not "we measured its accuracy." Restate the funnel-honesty
  caveats here, not only in Limitations: the program hop is a funnel tautology (F-004); "43 supported"
  is a joint gate×referee product (referee alone supports 395/47,220).
- **4.1b The discrimination sensitivity panel** (DECIDED — §8.2). Two negative controls that turn "the
  referee discriminates" from assertion into a small measured result: (a) failed-KD genes → all return
  *untested* (QC gate works); (b) permuted/label-shuffled disease → refutation rate ≈ chance (disease
  hop isn't rubber-stamping). Built as a bounded CS-kernel analysis; reported as a compact panel/table.
- **4.2 The confident NO / the QC catch** (own subsection — the moat): IL2 *untested* (QC failed,
  0/2 guides) as an artifact caught not a false negative; **SLC1A5 *refuted*** as the correctly-sourced
  refuted exemplar (`docs/perturbseq-qc_2026-07-07/`). *(CTLA4 dropped from the headline ledger per
  F-002 — it is **supported** in the perturbseq-qc source; a CTLA4-at-Rest refutation exists in the
  separate `perturbseq-e2e-autorun_2026-07-07` artifact and may be cited with explicit condition/disease
  scope if a second refuted example is wanted, but is not needed.)*
- **4.3 NAB2 → Th1/Th2 → atopic eczema — the worked hero** (Fig 4, the 4-hop receipt chain).
- **4.4 Falsifying the hardest confounder** — STAT6 cis-refutation against the authors' own
  genome-wide DE (STAT6 unmoved under NAB2-KD).
- **4.5 Native reproduction + self-audit in Claude Science** (Fig 5 — the Sonnet critic flagging
  "validated"/"definitive" and forcing the edit). The platform checked its own work — stated as
  *role/model/checkpoint* self-audit (F-009), with the full-scale sweep explicitly a cached-receipt
  replay and live authorship shown by the microsweep (F-005). **Meta-discipline (F-007):** because the
  paper's own thesis is calibrated language, the manuscript must practice it — every manuscript-facing
  verdict/figure label reads "refuted" / "consistent with NAB2 perturbation" / "nomination," never
  "definitive" / "genuine" / "proven," even though some internal source scripts still carry the stronger
  wording as edit history.
- **4.6 Independent cross-model replication** — the 5-agent lab (3 Opus + 2 Codex), unanimous PASS,
  errors caught + fixed (this is *why* it replicates).

**5. Discussion** (~2.5 pp)
- **5.1 What the agentic loop changes** — answers the R01 critique explicitly, but **scoped precisely
  (F-010):** Wayfinder's answer is *automated follow-up triage / adjudication against a held substrate*
  (generate + test + audit on one bench), NOT a replacement for prospective experimental follow-up. It
  makes "which of the 22,039 do you even look at" answerable with a receipt; the wet-lab confirmation of
  a survivor remains future work. This is the honest reading of "almost none get followed up."
  **Reproducibility angle:** because we drive the (API-less) workbench programmatically and pull its own
  provenance, an analysis that would otherwise be a one-off web session becomes a re-runnable, audited
  pipeline — a small but real step toward reproducible *agentic* science, not just reproducible code.
- **5.2 The next experiment (NAB2 direction).** DepMap-negative + GEO direction-mining → NAB2 reads as
  a Th2 *brake* lost in chronic disease → the therapeutic move is likely *restore/UP-modulate*, not
  knockdown. Association-backed; the falsifiable next step is a perturbation.
- **5.3 Limitations** (Henry-candid): nomination not causation; the disease *label* is Open Targets
  GWAS-genetic (no colocalization); retrospective substrate (no new wet-lab); single program/dataset;
  the program hop is a tautology *inside the funnel*; "43 supported" is a joint gate×referee product;
  the determinism boundary (where does Claude judgment enter?); LLM-judgment scope; **UI-automation
  dependence** (CS exposes no public API, so the driver depends on the front-end — a reproducibility
  bridge, not a stable contract); single model-family for the CS self-audit (cross-family is external).
- **5.4 Conclusion.**

**Data & Code Availability** — GitHub (MIT, new-work; git history is the compliance proof);
`data/fetch_data.sh`; the evidence-chain notebook; `docs/cs-full-pipeline_2026-07-09/` provenance.

---

## 3. Figure plan

| # | Figure | Class | Produced where |
|---|--------|-------|----------------|
| 1 | The Wayfinder **loop** (Henry Fig 1 analog): LBD generates → referee adjudicates against receipts → supported/refuted/untested → confident-NO feeds back; actor–critic wrapped around it | schematic | HTML/SVG asset pipeline |
| 2 | Generic Swanson ABC triangle (brief, textbook) | schematic | HTML/SVG (reuse video Swanson asset) |
| 3 | The specific Wayfinder **system**: answer-free A-universe → 5 signals → gate → 4-hop referee → ledger; agent-cast overlay (tools vs. Claude judgment; Opus author + Sonnet critic). **Inset: how we operate it** — Claude Code → Playwright (saved auth, zero-click card approval) → CS web UI → artifacts + `operon-cli.db` (the no-API driver) | schematic | HTML/SVG asset pipeline |
| 4 | NAB2 **4-hop receipt chain** (the mechanism/hero figure) + STAT6 cis-refutation callout | data | **CS kernel** (matplotlib/plotly) |
| 5 | The **self-audit made visible** — the Sonnet reviewer flagging "validated"/"definitive" and forcing the edit | schematic/data | HTML/SVG + CS provenance excerpt |

## 4. Table plan

| # | Table | Source |
|---|-------|--------|
| 1 | Inputs: the 4 Perturb-seq tables + the 12 disease→MONDO menu | `data/`, `entity_maps` |
| 2 | **The verdict ledger** (money table): NAB2 supported / EGR2 supported / IL2 untested / SLC1A5 refuted / NUDT1 supported-weak, each with per-hop receipts (CTLA4 dropped — F-002) | `docs/perturbseq-qc_2026-07-07/pyzobot_referee_results.md`, `stage1/sweep_Stim8hr.json`, `docs/lbd_finding_nab2_*` |
| 3 | The honest funnel (3,935 → 22,039 → 43 → 30) | `cs-full-pipeline` README, replication report |
| 4 | NAB2 receipts + confounder/replication summary | finding doc + replication report |

## 5. Production pipeline (division of labor)

| Task | Where | Why |
|---|---|---|
| Data figures (Fig 4) + legends | **CS kernel** | live numbers, reviewer-verified, provenance in `operon-cli.db` |
| Schematic figures (Figs 1/2/3/5) | **HTML/SVG asset pipeline** (reuse video toolchain) | design diagrams, not data plots |
| Section drafting | **Main thread** (architect) → **CS actor–critic review** per section | prose is authored; Sonnet reviewer number-checks + enforces calibrated language (the dogfood gate) |
| Citations | **Repo-native resolver** (Crossref/OpenAlex REST → `.bib` + CSL-JSON, stable keys), runnable in CS kernel | reproducible per doctrine §19; preserves the CS-native story |
| Provenance / self-audit | **CS** (`operon-cli.db`) | it is the paper's thesis |

## 6. Build tasks + delegation tags (per doctrine §10)
- Section drafting — `[CLAUDE]` (synthesis from the finding docs + Henry template; CS-reviewed). **Next: §1 Introduction.**
- Negative-control / discrimination panel (§4.1b, DECIDED) — `[CLAUDE via CS]` (bounded CS-kernel analysis: failed-KD→untested; permuted-disease→refutation rate).
- Data figures (Fig 4 + the 4.1b panel) — `[CLAUDE via CS]` (kernel plotting; not a Codex task).
- Schematic figures (Figs 1/2/3/5) — `[CLAUDE]` (HTML/SVG asset pipeline).
- Citation resolver — `[CODEX-RESCUE]` (mechanical, clear spec, cheaply verifiable; ~1,200-tok brief).
- Full-draft codex-debate before submission — `[CODEX-DEBATE]` (prose overclaim, figure-label calibration F-007, citation completeness).

---

## 7. Claim inventory — every quantitative claim the paper will assert, with its source file
**Round-1 status (2026-07-10):** Codex opened the repo and verified C1–C21 HOLD against primary
artifacts. **Source-of-truth rule (F-006):** cite the line-bearing JSON/receipt artifact, with prose
docs only as narrative corroboration. Primary artifacts: `stage1/sweep_Stim8hr.json` (C1–C8),
`stage1/lbd_questions_Stim8hr.json` (C9–C10), `stage3/stage3_cis.json` + `stage3/receipt.md` (C15–C16),
`cs-full-pipeline README` §Stage-5 (C18–C20), `replication_report` (C11–C14, C21),
`perturbseq-qc_2026-07-07/pyzobot_referee_results.md` (C17). Paths under
`docs/cs-full-pipeline_2026-07-09/`.

**Pre-critic vs post-critic receipts (F-011).** The Stage-1 generation JSON
(`stage1/lbd_questions_Stim8hr.json`) still carries a pre-critic `referee_overall: "…consistent with a
**validated** … chain…"` string — the exact word the Sonnet critic later forced out. **Rule:** cite
Stage-1 JSON **only for numeric values** (the receipts' numbers); for any manuscript-facing *prose*
verdict, cite the **post-critic Stage-5 receipt** (`stage5/receipt_chain.md` / `chain.json`), where the
calibrated language is authoritative. This is not a defect to hide — the pre-critic→post-critic
diff **is** the self-audit, and Fig 5 should show exactly that word being changed. Do NOT hand-edit the
Stage-1 artifact (it is provenance; hand-editing would corrupt the "this is what CS produced" claim).

| # | Claim | Value | Source of truth |
|---|-------|-------|-----------------|
| C1 | A-universe (KD-gated, program-significant) @ Stim8hr | 3,935 genes | **primary:** `stage1/sweep_Stim8hr.json` (`a_genes`); corrob: finding doc |
| C2 | Eligible (gene×disease) pairs after gate | 22,039 | **primary:** `stage1/sweep_Stim8hr.json` (`eligible_pairs`) |
| C3 | Referee disease-C-supported | 43 | **primary:** `stage1/sweep_Stim8hr.json` |
| C4 | Clean full-chain supported | 30 | **primary:** `stage1/sweep_Stim8hr.json` |
| C5 | Refuted for the specific disease | 21,995 | **primary:** `stage1/sweep_Stim8hr.json` (class split) |
| C6 | Class split | supported 30 / weak 10 / flagged 3 / refuted_effect 1 | **primary:** `stage1/sweep_Stim8hr.json:17-25` |
| C7 | Pure-disjoint clean | 1 (NUDT1) | **primary:** `stage1/sweep_Stim8hr.json`; corrob: replication |
| C8 | ab_gate value | 26 | **primary:** `stage1/sweep_Stim8hr.json` (`ab_gate_value`) |
| C9 | NAB2 rank | 4 of 30 | **primary:** `stage1/lbd_questions_Stim8hr.json:48-58` |
| C10 | NAB2 signals | ab 66 · bc 2184 · ac_lit 6 · ac_known 0.0376 · effect 301 · score −1.137 | **primary:** `stage1/lbd_questions_Stim8hr.json:48-58` |
| C11 | NAB2 KD-QC | 2/2 guides signif, best adj-p 1e-16 (guide expr 0.056 vs NTC 0.567) | finding doc hop-0 |
| C12 | NAB2 effect magnitude | −16.9 (−16.88), 301 downstream DE, no off-target flag | finding doc; replication |
| C13 | NAB2 program (Ota) | z 7.71, adj-p 1.96e-13, log_fc +0.63; Höllbacher n.s. | finding doc hop-2 |
| C14 | NAB2 disease clusters | OR 3.90 FDR 0.0028; OR 3.43 FDR 0.0224; clusters 90 & 100 | finding doc hop-3; replication (74→90/100 fix) |
| C15 | STAT6 cis-check | STAT6 log2FC +0.0870, adj_p 0.7884, UNMOVED; NAB2 self −3.0783, adj_p 7.2e-60 | **primary:** `stage3/stage3_cis.json:6-17,47-50` + `stage3/receipt.md:12-20`; corrob: `docs/nab2_stat6_definitive_check.py` |
| C16 | STAT6 rank / genes moved | STAT6 |log2FC| rank 5444/10282; 302 of 10,282 genes moved by NAB2-KD | **primary:** `stage3/stage3_cis.json` |
| C17 | Ledger verdicts | EGR2/GATA3 YES · IL2 UNTESTED (0/2 guides) · **SLC1A5 REFUTED** *(CTLA4 REMOVED — F-002: CTLA4 is **supported** in this source; CTLA4-at-Rest refutation lives in `docs/perturbseq-e2e-autorun_2026-07-07/referee_writeup.md` with different scope)* | `docs/perturbseq-qc_2026-07-07/pyzobot_referee_results.md:25-40` |
| C18 | CS run cost | Stage 0/1/3/5 ~$6.41 total | cs-pipeline README |
| C19 | CS model cast | OPERON = Opus 4.8; REVIEWER = Sonnet 5; inline = Haiku 4.5 | cs-pipeline README; capability tests |
| C20 | Self-audit catch | reviewer flagged "validated" (title) + "definitive" (Stage-3 heading); both edited out | cs-pipeline README Stage 5 |
| C21 | Replication | 5 agents (3 Opus + 2 Codex), unanimous PASS; caught cluster-ID 74→90/100 and 8×→3× z | `docs/replication_report_2026-07-08.md` |
| C22 | Dataset attribution + title | **Zhu, Dann, Yan, … Marson** (Gladstone/UCSF), bioRxiv/openRxiv 2025 · title *"Genome-scale perturb-seq in primary human CD4+ T cells maps context-specific regulators of T cell programs and human immune traits"* | Crossref (verified 2026-07-10); `references/README.md` |
| C23 | Dataset DOI — ✅ **RESOLVED** | **`10.64898/2025.12.23.696273`** (Crossref-registered, bioRxiv/openRxiv prefix). The `10.1101/…` form is NOT registered (404). `references/README.md` corrected 2026-07-10. | Crossref API |
| C24 | Henry citation | Henry, Wijesinghe, Myers, McInnes 2021, FRMA 6:644728, doi:10.3389/frma.2021.644728 | `references/frma-06-644728.pdf` |
| C25 | R01 grant number | 1R01LM015392-01 | main `README.md` |

---

## 8. Open questions (round-1 resolutions marked ✅; live items for rounds 2–3)
1. ✅ *Numbers* — Codex verified C1–C21 hold; DOI resolved (C23); CTLA4 mis-source fixed (C17). No
   remaining known number that the repo does not support.
2. ✅ **DECIDED (2026-07-10): YES — build the small negative-control / discrimination panel.** Two
   controls: (a) *failed-KD genes → must return UNTESTED* (the QC gate does its job); (b) *label-shuffled
   / permuted disease assignment → refutation rate rises to ~chance* (the disease hop isn't rubber-stamping).
   Upgrades §4.1 from *demonstration* to a modest *sensitivity result* and answers F-003 directly. Build
   as a bounded CS-kernel analysis → its own small panel in Fig 4 (or a companion Table). Becomes a
   **build task** (below).
3. Does the **agentic headline** survive a hostile FRMA/LBD reviewer, or over-reach for a text-mining
   venue? Is the R01-critique frame (now scoped to *triage/adjudication*, F-010) a strength or does it
   invite "then why trust *this* LBD tool"?
4. Is the disease-hop scoping (F-008: substrate vs. association receipt) now tight enough, or does a
   wet-lab reviewer still read any disease claim as overreach?
5. Section-order: does §2.3 (agentic LLMs) belong in Background, or should the agent architecture live
   entirely in Methods? Does Background at ~3 pp overweight the front-matter for this venue?
6. Is dropping CTLA4 (vs. re-citing CTLA4-at-Rest with scope) the right call, or does the ledger want a
   *second* correctly-sourced refuted example for strength?
7. What must the *second* (full-draft) debate check that this outline debate cannot — e.g. actual prose
   overclaim, figure-label calibration (F-007), citation completeness?
