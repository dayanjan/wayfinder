# Round 2 — Codex findings (prose debate, verified against v2 file)

**Position summary:** v2 materially fixed the main round-1 correctness blockers (triage scoped, `ac_known`
= overall OT score, disease hop kept as association, self-audit/no-API bounded). Not fully converged: a few
residual shorthand phrases + newly-introduced control/guardrail claims still create small attack surface.

**Dropped (verified resolved):** F-001, F-002, F-004, F-005, F-006, F-007, F-008, F-009, F-010, F-011,
F-012, F-013 (12 of 14).

**Open → all ACCEPTED and fixed in v2.1:**

| ID | Pri | Gap | v2.1 fix |
|----|-----|-----|----------|
| F-003 (residual) | P2 | §3.2 funnel still said "chain-supported survivors" / "43 disease-supported" | → "chain-held (receipt-complete)" / "43 with a positive disease-hop enrichment" |
| F-014 (partial) | P1 | label-shuffle "refutation rate should approach chance" statistically vague | → "which estimate the null disease-hop pass rate" (exact null deferred to §4) |
| F-015 (new) | P2 | headers still "DRAFT v1" after v2 | → "DRAFT v2 — post CS-review + codex-debate" ×3 |
| F-016 (new) | P2 | "network access is confined…" implies an enforced allowlist | → "approvals granted only for the named endpoints the task used — an auditable trail, not a claim of an enforced allowlist" |

**Preserve-intent:** `sanding_warning: null` — no over-correction; novel claims stayed sharp.
**Convergence:** still iterating; round-3 ask = verify the 4 small cleanups landed.
