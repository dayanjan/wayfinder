# WORK_PROGRESS.md — PyZoBot Arbiter

Live snapshot dashboard. Updated by `session-closer` at each session close and by
`freshen` on demand. The plan of record is `docs/plan.md` (v7 — Researcher-track reframe, §0).

## Snapshot
- **Phase:** Researcher-track finding — LBD proposer BUILT + swept; **finding NAB2→Th1/Th2→atopic eczema INDEPENDENTLY REPLICATED (5-agent lab, unanimous PASS) + vetted against the source paper → reframed as a novel, reproducible NOMINATION with the disease link FLAGGED (STAT6 shadow argued-against, not fully excluded)**
- **Active workstream:** next = M5 (demo video + README-as-paper); optional = deposited-DE cis-check (NAB2-KD→STAT6 mRNA), Rest/Stim48hr sweeps
- **Last updated:** 2026-07-08
- **Deadline:** 2026-07-13 (official EOD ET; operator personal stop 9:00 PM ET)
- **Repo:** `dayanjan/pyzobot-arbiter` (private; flip public before deadline — light identifier scrub first)
- **Claude Science:** installed on WSL, driven headless via the `drive-claude-science` skill (validated E2E, zero-click)

## Milestones (judging aims: Demo 30% · Claude Use 25% · Impact 25% · Depth 20% — WEIGHTS UNVERIFIED, confirm on CV form)
| # | Milestone | Status |
|---|-----------|--------|
| M0 | Repo scaffold + PM tooling | 🟢 done |
| M1 | Deterministic Validator (3-hop + KD-QC) proven on real genes | 🟢 done (built via Claude Science; `docs/perturbseq-qc_2026-07-07/`) |
| M2 | Receipt-backed YES / UNTESTED / REFUTED demonstrated (the moat) | 🟢 done (EGR2/GATA3 YES · IL2 UNTESTED · SLC1A5/CTLA4 REFUTED) |
| M3 | **LBD question-proposer** (generate untested questions → referee answers) | 🟢 done — v2 spec (debate-hardened) + fresh tool layer + full Stim8hr sweep; funnel 22,039→30 clean supported |
| M4 | Anchor lock + finding validation | 🟢 done — **NAB2→Th1/Th2→atopic eczema** replicated (5-agent lab, unanimous PASS: `docs/replication/`), STAT6+EGR+cis confounders stress-tested, source-paper-vetted → reframed as novel reproducible NOMINATION (disease link flagged) |
| M5 | Deploy / demo capture + 3-min video + README-as-paper | ⚪ not started — finding + validation fully documented; needs operator direction on narrative/format |

Legend: 🟢 done · 🟡 in progress · 🔴 blocked · ⛔ off-track · ⚪ not started

## Active blockers
None. (Claude Science entitlement + sandbox verified; endpoint does not block it.)

## Progress log
### 2026-07-08 (cont.) — Independent validation + source-paper vetting → nomination reframe
After the finding landed, hardened it against every challenge. **Independent literature audit**
(4-agent team via new `src/arbiter/lit/`): NAB2→Th1/Th2 and NAB2→atopic eczema BOTH novel (0 papers);
surfaced the **STAT6-adjacency** confounder. **In-data confounder checks** (`docs/nab2_stat6_confounder_
check.py`, `docs/nab2_egr_mechanism_check.py`): STAT6-locus and EGR-mediation both argued-against.
**5-agent independent replication** (3 Opus + 2 Codex, 2 clean-room re-impls; `docs/replication/` +
`docs/replication_report_2026-07-08.md`): **UNANIMOUS PASS** — every number reproduced; caught+fixed a
cluster-ID bug (74→90/100), a stat overstatement (8×→3× on z), and reframed the arguments.
**Source-paper read** (`docs/source_paper_read_eczema_2026-07-08.md`): paper never mentions NAB2
(novelty confirmed); disease labels are Open Targets GWAS-genetic (LD-susceptible, no coloc control);
sharpest concern = CRISPRi **cis-artifact** — tested (`docs/nab2_cis_artifact_check.py`): NAB2 & STAT6
don't co-cluster + NAB2 reproducible (cross-guide/donor R 0.74) → argues against cis (definitive
NAB2-KD→STAT6-mRNA check needs deposited DE matrix). **Reframed** to a novel, reproducible NOMINATION
with the disease link FLAGGED. Source paper in `references/` (gitignored); analysis repo
`github.com/emdann/GWT_perturbseq_analysis_2025` recorded. ~14 commits.

### 2026-07-08 — Autonomous overnight session: LBD proposer built + finding landed
Hardened the LBD spec v1→v2 via a **3-round repo-read codex-debate** (9→3→0 findings, build-ready)
and an independent Fable-5 read. Authored the **fresh tool layer** (`src/arbiter/lbd/`:
entity_maps, _http, sources, entities, referee_triple, cooccur, propose, verify_disease_ids) —
new-work-only, all verified live. Disease→id map resolved authoritatively (Open Targets/OLS4 →
**MONDO not EFO**; caught before it silently broke novelty). `referee_triple` = thin exact-disease
adapter (F-001/F-012), verified discriminating. A **Codex code consult** found the scoring rewarded
obscurity + a full-chain bug; both fixed. **Full Stim8hr sweep:** 22,039 candidate questions →
**30 clean full-chain referee-supported**. Headline finding **NAB2 → Th1/Th2 → atopic eczema**
(near-novel ac_lit=6, receipt-backed, Codex-vetted keep-with-caveat). 5 commits; finding writeup at
`docs/lbd_finding_nab2_2026-07-08.md`; process log `docs/lbd-build-log.md`.

### 2026-07-07 — Session close (checkpoint): PM tooling bootstrap
Pulled session-lifecycle skills (`session-start`, `session-closer`, `freshen`,
`atomic-planner`) from the sibling generator/Halcyon repos; instantiated the
`memory/` scaffold, `MEMORY.md`, this dashboard, and migrated the handoff to
`memory/NEXT_SESSION.md`. Product work not yet started.

### 2026-07-07 13:10 — Session close (full-close): PM tooling + repo live
Verified the `.env` Anthropic key is active (models 200 + minimal messages 200).
Created private GitHub repo `dayanjan/pyzobot-arbiter`, gitignored the local
`01-hackaton details/` folder, and pushed both commits. Secrets/data confirmed
absent from remote history. M0 complete; next up is M1 (deterministic Validator).

### 2026-07-07 19:30 — Session close (full-close): Claude Science + Validator + LBD reframe
Huge session. Committed to the **Researcher track** (plan v7). Installed **Claude Science** on WSL
(paste-only, no-password; sandbox verified on the managed laptop; entitlement confirmed) and built
a reusable **`drive-claude-science` skill** to drive it fully headless via Playwright — validated
end-to-end zero-click on a fresh project (auto-approves cards). Through it, built the **referee /
Validator** (3-hop + KD-QC gate) and demonstrated **YES / UNTESTED / REFUTED** with real receipts;
batch-ranked 602 genes for anchor candidates. Researched Claude Science exhaustively (4 agents + live
UI) → curated capability reference (`docs/claude-science-capabilities.md` + HTML + Artifact + a
Wednesday reminder). Reframed the project's strategic heart: **LBD generates the questions, Claude
Science + data answers them** — specced at `docs/lbd-proposer-spec.md`. All committed + pushed.
