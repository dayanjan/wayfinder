# Revision roadmap — Wayfinder Major-Revision response (repo-grounded) — 2026-07-11

Synthesis of a codex-debate on how to address two independent Major-Revision reviews (dossier:
`docs/manuscript/reviews/REVIEW_DOSSIER_2026-07-11.md`). **Round 1 was excellent and repo-feasibility-checked
(8 findings, all accepted); round 2 confabulated** (returned hallucinated manuscript-prose findings from an
unrelated earlier debate — archived `round_02_codex.CONFABULATED.*`). Codex has confabulated repeatedly on
this repo when handed large multi-part artifacts; the reliable output is the round-1-hardened plan below.
Every [CS]/[LIT] item was checked against actual repo data.

> **UPDATE — debate CONVERGED (3 rounds).** After the Codex model was upgraded (0.141.0→0.144.1,
> `gpt-5.5`→`gpt-5.6-sol`), rounds 2–3 ran cleanly (no confabulation). Trajectory: R1 (8 findings) → R2 (6,
> corrected the *design* of nearly every analysis) → **R3 (0 new, converged, no sanding — "debate
> concluded")**. Codex's closing position: the plan is credible for Major Revision *because* it narrows the
> contribution to receipt-backed prioritization + abstention + falsification diagnostics, not demonstrated
> correctness. The "Round-2 refinements" at the end are authoritative on analysis design.

## THE decision (settles the reviewers' core tension)
The paper's top-line claim is **"receipt-backed *prioritization* with explicit *abstention* and falsification
diagnostics"** — NOT empirical correctness, and NOT "calibrated" as a *performance* claim (R2 F-009: no
artifact estimates predictive calibration/precision; reserve "calibrated" strictly for *vocabulary*
discipline). Every new analysis is a **diagnostic of the machinery's behavior**, never validation. Retitle →
*"Receipt-backed prioritization for literature-based discovery using Perturb-seq evidence."* Soften
"adjudication" → "prioritization/evidence integration" wherever the disease hop is involved; keep
"adjudication" only for the hops the referee genuinely owns (QC + effect).

## Analyses to run (all feasible offline from repo data unless noted; all reported as DIAGNOSTICS)
| ID | Analysis | Feasibility (repo evidence) | Framing guardrail |
|---|---|---|---|
| **C6** | **Pipeline-level permutation diagnostic** — expected clean survivors under *constrained* nulls (disease-label perm within T3; gene-label perm within condition; eligible-pair perm) vs observed 30 | FEASIBLE offline: `data/*.suppl_table.csv` + `data/lbd_out/sweep_Stim8hr.json` + `data/lbd_cache/` + `src/arbiter/lbd/propose.py` | NOT a "joint FDR"; a selectivity diagnostic |
| **C3a** | **Temporal robustness** across Rest/Stim8hr/Stim48hr | FEASIBLE: `docs/cs-full-pipeline_2026-07-09/live-fullsweep-loose/sweep_{Rest,Stim8hr,Stim48hr}.json` | robustness on the *same* substrate, not external |
| **C3b** | **Prioritization-behavior comparators** — random / literature-rarity / Open Targets ranking vs referee-supported set | FEASIBLE offline + `tools/` APIs | behavior, not accuracy |
| **C3c** | **Literature-curated positive-control panel** — canonical Th1/Th2 regulators, do they recover? | NEEDS-FRESH-LIT via `tools/{semantic_scholar,pubmed_fetch}.py` | crude recovery *proxy*, labelled |
| **C2** | **Out-of-funnel discrimination, two panels** — (1) arbitrary genes (descriptive), (2) **hard negatives** (literature-plausible / eligible pairs that fail exact-C or effect) vs naive literature-only nomination | FEASIBLE offline: referee over `data/*.csv`; existing anecdotes `docs/perturbseq-qc_2026-07-07/pyzobot_referee_results.md` | the referee's *own* edge (QC/effect), not "confident-no accuracy" |
| **C10** | **Threshold sensitivity grid** — ab_gate_pct × min_bc × tau (Stim8hr); clean-survivor count, NAB2 rank, Jaccard overlap | FEASIBLE: extend `sensitivity_panel.py` (only does Control 1/2/3); `propose.sweep()` exposes the params; cache exists | complements the existing weight sweep |
| **C9** | **LIT audit of the six NAB2×Th1/Th2 Europe PMC co-mentions** — title/year/context; does each assert the mechanism? | NEEDS-FRESH-LIT (`sources.py` cached counts only, pageSize=1) via `tools/` | reconcile ac_lit=6 vs "zero mechanistic papers" |
| **C4-sanity** | **12q13 locus-wide neighbor check** — do other 12q13 genes share NAB2's eczema clusters? | FEASIBLE offline (T3) | a sanity check, **NOT** an LD resolution |

## Reframes / restructure (no new analysis)
- **C1 circularity** — separate **construction filters** (KD/effect/program pre-gate) from **referee decisions** (disease-C specificity + demotions) *textually and in Fig 1*; lean on the out-of-funnel ledger (C2) as the independence evidence.
- **C4 12q13/LD** — **foreground limitation subsection** (balance the STAT6 subsection) + a **12q13 GWAS literature subsection**; state colocalization unavailable; never claim discharged.
- **C7 hop-2 tautology** — mark hop-2 as construction-inherited (not an independent funnel filter) in Fig 1/§3.3.
- **C12/C14 NAB2/scope** — Results lead with ledger + discrimination diagnostics; **NAB2 becomes one (deep) case study**; move NAB2-direction/DepMap fully to Discussion/supplementary.
- **C13/C16/C17 CS de-weight** — compress §3.4/§4.5 to a Methods subsection + appendix; separate **language-hygiene self-audit** from epistemic verification; downgrade "reproducible" → **"replicable-in-principle (UI-dependent)"**.
- **C11** — state the corrected confounder script was re-derived by the 5-agent replication (`docs/replication_report_2026-07-08.md`).
- **C15 vision** — short framing paragraph (Intro + Discussion): general architecture for evidence-grounded hypothesis adjudication.
- **C19 title** — retitle (above). **C8** — "adjudication" → "prioritization" at the disease hop.

## Figures — minimum viable set (currently ZERO exist)
1. **Fig 1** — architecture, with **construction-vs-referee visually separated** (addresses C1/C7). [schematic]
2. **Fig 2** — ledger + honest funnel, annotated with the **C2/C6 diagnostics**. [schematic/data]
3. **Fig 3** — NAB2 4-hop chain **with the 12q13 caveat on the disease hop**. [CS kernel]
4. **Fig 4** — the sensitivity / permutation-null panel (Control 1/2/3 + C6/C10). [CS kernel]
5. Fig 5 (self-audit) — only if space; it is the most dispensable given C13/C16.

## Quick fixes
Split the abstract (2–3 paragraphs); reconcile −16.9 vs −16.88; note the substrate is a **2025 preprint**;
[DONE] equation display-math + black headings.

## Deferred (state as future work)
Wet-lab validation of a supported call; LD/colocalization *resolution* for NAB2 (only foregrounded, not resolved).

## Execution order (MVP → ideal)
1. **Reframe first** (top-line claim, title, adjudication→prioritization, construction-vs-referee, CS de-weight) — cheap, unblocks everything.
2. **Run the diagnostics** C6 → C3(a/b/c) → C10 → C2 hard-negatives → C9 LIT audit — all labelled diagnostics.
3. **Restructure** Results (NAB2 → case study; CS → Methods/appendix); write the 12q13 limitation + literature subsections.
4. **Build the 4-figure minimum set.**
5. Quick fixes; final full-draft pass (per-section, grounded — NOT one big inline codex-debate, which degrades).

**MVP for resubmission credibility:** the reframe + C6 + C2-hard-negatives + the 12q13 foregrounding + Figs 1–4.
Everything else strengthens but is not strictly gating.

---

## Round-2 refinements (gpt-5.6-sol, grounded — AUTHORITATIVE on analysis design)
Round 2 dropped 5 round-1 findings as addressed and raised 6 new, file-cited ones. These correct the
*design* of the analyses (the round-1 table above named the right analyses; R2 fixes how to run them so they
are not circular). Model note: this ran cleanly on the upgraded `gpt-5.6-sol`; the earlier gpt-5.5 round-2
attempt confabulated (archived `round_02_codex.CONFABULATED.*`).

- **Top-line (F-009):** drop "calibrated" as a performance word → **"receipt-backed prioritization with
  explicit abstention and falsification diagnostics."** "Calibrated" only ever refers to vocabulary discipline.
- **C6 permutation diagnostic (F-010):** my three nulls were partly mis-specified — permuting *already-eligible*
  pairs is circular (eligibility is deterministic from AB/BC/Open Targets, `propose.py:68-71`). Use **ONE
  primary randomization test**: permute the disease labels among the T3 enrichment rows *preserving condition,
  cluster/gene-set structure, and row marginals*, and ask whether exact-disease matching is informative beyond
  cluster membership. Report expected clean survivors under that single principled null vs observed 30.
- **C3c positive control (F-011):** canonical Th1/Th2 regulators (STAT6/GATA3/TBX21/IL4) are **excluded by the
  novelty gate** (`ac_known ≤ τ`, `propose.py:69-71`) — so "do they recover?" is confounded with the funnel.
  Instead test them **against the referee substrate ONLY, blinded to the literature/novelty gate**: do the
  expected QC/effect/program receipts recover? Keep the referee-recovery test separate from the novelty gate.
- **C2 hard negatives (F-012):** must not be selected by the verdict being evaluated (exact-C/effect failure
  *is* the outcome). Sample from a **frozen literature-only nomination rule**, stratified by condition / AB
  strength / disease / assay coverage; *then* apply the referee and report the pre-specified decomposition.
- **C3a temporal (F-013):** not a held-out test as written (each condition rebuilds its own A-universe). Use a
  **frozen common cohort**: pre-register Stim8hr as discovery, freeze its eligible pairs + scoring inputs, and
  evaluate only *those* pairs' QC/effect/program/exact-C receipts at Rest/Stim48hr. Report coverage first,
  then a transition matrix.
- **MVP re-ordered (F-014):** reframe/C1 architecture · **C2 frozen-literature-nomination decomposition** ·
  **C10 small gate grid** (cheap; code exposes ab_gate_pct/min_bc/tau) · **frozen-cohort C3a** · C4 foreground
  limitation · C9 enumeration (if literature access works) · four essential figures. (C6 stays, but as ONE
  well-specified null, not the headline.)

**Net:** the reframe is necessary but not sufficient; the analyses are feasible offline but must be
**outcome-independent and pre-specified** to count. Do not claim wet-lab, LD, or statistical-calibration
validation. Debate is substantively converged after 2 grounded rounds (R1 gpt-5.5 + R2 gpt-5.6-sol).
