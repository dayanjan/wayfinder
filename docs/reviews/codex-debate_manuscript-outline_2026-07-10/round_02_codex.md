# Round 2 — Codex findings (repo-read, verified against the updated file)

**Position summary:** v1.1 fixed the high-risk issues in substance (DOI repo-consistent, liveness split
explicit, program-hop tautology surfaced, independence scoped). But the file was not yet internally
self-consistent: stale headline/demo-scope sentences still overclaimed the ledger, retained CTLA4, and
blurred the disease hop back into the experimental-substrate framing.

**Dropped (verified resolved):** F-001 (no `10.1101/…` anywhere; repo DOI-consistent), F-004 (program
tautology stated in §3.3/§4.1), F-005 (liveness split in §3.4/§4.5), F-009 (independence operational),
F-010 (R01 scoped to triage/adjudication).

**Escalated / still open → all ACCEPTED and fixed in v1.2:**

| ID | Pri | Gap (stale top-level sentence) | v1.2 fix |
|----|-----|-------------------------------|----------|
| F-002 | P1 | §0 demo-scope line still said "SLC1A5+CTLA4 refuted" | CTLA4 removed from §0 line |
| F-003 | P2 | §0 headline still said ledger "proves" discrimination | → "*demonstrates* … on worked examples … not a validated accuracy benchmark" |
| F-006 | P2 | §7 header named primaries but C1–C10 *rows* still cited prose/`same` | rows repointed to `stage1/sweep_Stim8hr.json` + `stage1/lbd_questions_Stim8hr.json` |
| F-008 | P1 | §0 headline still said "a receipt at every hop / against a held experimental substrate" | headline now names both receipt classes (substrate vs. association) |
| **F-011** | P2 | **NEW** — cited Stage-1 JSON still contains pre-critic "validated" prose | rule: Stage-1 JSON for *numbers only*; post-critic Stage-5 receipt for prose; the pre/post diff IS the self-audit (Fig 5) |

**Preserve-intent check:** no sanding; `convergence_sanding_warning: null`. Novel claims intact.

**Convergence:** still iterating. Codex's round-3 ask: verify the cleanup pass (stale CTLA4/"proves"
gone, headline receipt-classes correct, JSON "validated" quarantined/handled).
