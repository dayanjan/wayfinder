# WORK_PROGRESS.md — PyZoBot Arbiter

Live snapshot dashboard. Updated by `session-closer` at each session close and by
`freshen` on demand. The plan of record is `docs/plan.md` (v7 — Researcher-track reframe, §0).

## Snapshot
- **Phase:** Researcher-track finding — referee (Validator) BUILT; LBD question-engine reframe specced
- **Active workstream:** next = LBD question-proposer (spec: `docs/lbd-proposer-spec.md`) — not started
- **Last updated:** 2026-07-07 19:30
- **Deadline:** 2026-07-13 (official EOD ET; operator personal stop 9:00 PM ET)
- **Repo:** `dayanjan/pyzobot-arbiter` (private; flip public before deadline — light identifier scrub first)
- **Claude Science:** installed on WSL, driven headless via the `drive-claude-science` skill (validated E2E, zero-click)

## Milestones (judging aims: Demo 30% · Claude Use 25% · Impact 25% · Depth 20% — WEIGHTS UNVERIFIED, confirm on CV form)
| # | Milestone | Status |
|---|-----------|--------|
| M0 | Repo scaffold + PM tooling | 🟢 done |
| M1 | Deterministic Validator (3-hop + KD-QC) proven on real genes | 🟢 done (built via Claude Science; `docs/perturbseq-qc_2026-07-07/`) |
| M2 | Receipt-backed YES / UNTESTED / REFUTED demonstrated (the moat) | 🟢 done (EGR2/GATA3 YES · IL2 UNTESTED · SLC1A5/CTLA4 REFUTED) |
| M3 | **LBD question-proposer** (generate untested questions → referee answers) | ⚪ not started — spec ready |
| M4 | Anchor lock (operator-vetted known-true + non-obvious) | ⚪ not started (candidates ranked; need biology vetting) |
| M5 | Deploy / demo capture + 3-min video + README-as-paper | ⚪ not started |

Legend: 🟢 done · 🟡 in progress · 🔴 blocked · ⛔ off-track · ⚪ not started

## Active blockers
None. (Claude Science entitlement + sandbox verified; endpoint does not block it.)

## Progress log
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
