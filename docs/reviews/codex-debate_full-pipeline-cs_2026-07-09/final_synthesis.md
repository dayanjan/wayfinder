# Codex-debate synthesis — full-pipeline-in-CS plan (3 rounds, 2026-07-09)

**Framing question:** is the plan to reproduce the LBD→NAB2 pipeline natively in Claude Science correct,
minimal, and executable next session — and what stays external?

**Verdict: SHIP.** Repo-read debate (`-s read-only`, from the repo; Codex told each round it may open
referenced files to verify — doctrine §22). Findings arrived repo-verified (cited file:line), so
acceptance was cheap and convergence fast.

## Trajectory
- **Round 1 — 11 findings, all accepted.** The big ones: kernel-HTTP (not connectors) is the path
  (Europe PMC `hitCount` GET + Open Targets GraphQL POST, verified in `sources.py`); re-scope to an MVP
  (Stage 0/1/3/5; drop Stage 4 — delegation is gated headlessly); provenance must be kernel-saved
  (`executed_code.py`+JSON+receipt), DB = corroboration; corrected call-volume math; tightened accept
  numbers; removed the non-existent `host.capabilities()`; fixed "clean-room" → "native port."
- **Round 2 — 0 re-escalations, 8 spec-completions accepted.** Re-verified every accept number against
  the committed JSON; added the exact 7-query Stage-5 provenance SQL, the cache `--new` import/export
  caveat, a runnable per-stage checklist, the Stage-0 package-vs-network distinction, and conditional
  S3-fallback wording.
- **Round 3 — no material findings. SHIP.** All round-2 gaps confirmed closed; executable-without-
  re-derivation confirmed; repo facts re-checked.

## The two load-bearing outcomes
1. **Kernel HTTP, not connectors.** Our validated `sources.py`/`_http.py` port directly into the CS
   kernel (with a CS-local SHA1 cache) behind a network-domain approval — zero connector-shape risk.
2. **Honest architecture (persistent disagreement resolved to a framing rule):** "full pipeline in CS"
   is NOT intrinsically better than "the right stages in CS." **CS = the instrument (generation →
   referee → provenance); Codex = the external cross-model auditor.** Cross-model independence is
   structurally outside CS, and no CS stage changes that — so the acceptance claim is stated
   conditionally and never overstates.

## Committed scope (MVP)
Stage 0 (probe: EPMC/OT/S3 via kernel HTTP) → Stage 1 (LBD proposer over the full 3,935-gene sweep;
accept 3935/22039/43/30 + NAB2 rank 4/ab 66/bc 2184/ac_lit 6/ac_known 0.0376/effect 301) → Stage 3
(definitive STAT6 cis-check; +0.09/0.79 — in-CS if S3 works, else labelled external fallback) → Stage 5
(receipt chain + provenance from `operon-cli.db`). Stage 2 (confounders) = stretch. Stage 4 = excluded.

**Next session:** implement per §9 runnable checklist in the plan.
