# NEXT_SESSION — async handoff (canonical; written/read by session-closer & session-start)

## 🧭 READ-FIRST (anti-amnesia — do not skip)
Before ANY claim audit, review, referee-response, revision, or new experiment, read
**`docs/CLAIMS_EVIDENCE_LEDGER.md`** — the single living index of claim → status → evidence → source → critique.
**Rule:** reconcile every claim against BOTH the literature AND the experiment corpus it indexes. (Born
2026-07-12 when a literature-only audit forgot the CS confounder experiments and over-generalized the STAT6 critique.)

## 🚀 SUBMISSION FIRE-READY — still governs (unchanged)
The Wayfinder hackathon submission remains BUILT + staged. On operator **"scrub and flip"**: run
`SUBMIT_CHECKLIST.md` (gitignored) steps 1–5 → flip `dayanjan/wayfinder` public → hand back the URL. Full
hackathon facts: `docs/HACKATHON.md`. Official deadline EOD ET Mon 2026-07-13.

---

## Next session priorities — written 2026-07-12 (full-close)

**Current state**: MANUSCRIPT-strengthening thread. The **contribution audit + claims↔experiments reconciliation
+ traceability spine** are DONE. **G1 (the held-out eval = the publish gate) is FULLY DE-RISKED and SPEC-FROZEN
and READY TO BUILD:** sizing GO Option A (~1,469 positives), plan **v3** codex-debate-hardened (converged,
repo-verified, no sanding), and **CS-driver health-check PASSED** (CS drivable on port 8000). Commits
`e626b4c`→`4952c9a`, all pushed; tree clean.

**Next action**: **BUILD the G1 held-out eval to plan v3** (`docs/plans/heldout-eval-implementation-plan_2026-07-12.md`).
Recommended shape: write the codex-rescue brief FROM v3 and launch it **[CODEX-RESCUE]** (a debate-hardened spec
should land near one-shot), then **[CLAUDE]** run it in CS + integrate. Concrete build order (from v3):
1. Add `cooccur_count_asof(a,b,T)` to `src/arbiter/lbd/sources.py` (append `FIRST_PDATE:[... TO {T}]`; VERIFIED).
2. Enumerate the novel-at-T frame exactly (`ac_lit_asof(2016)≤1`) + a committed **count manifest** (freeze/hash
   query,result,date) + the **blinded feasibility gate** (label counts only; re-confirm positives ≥100 after the
   as-of-T ab-gate — the plan's build-time checkpoint).
3. Implement 6 rankers — Wayfinder (exhaustive 8-class verdict order incl. `refuted_program`, then §3.2 score
   as-of-T, `ac_known`=0), **B-disease-hop-only** (min-FDR collapse mirroring `_hop3_for_disease`), B-lit-rarity,
   B-effect, B-enrichment-continuous, B-random.
4. Two **co-primary** contrasts (C-broad vs lit-rarity; C-mech vs disease-hop-only) + gene&disease two-way-clustered
   paired-difference bootstrap CIs; **report a null straight** per the frozen joint-outcome table.
5. **Run in Claude Science** (native; CS drivable on **port 8000**, driver defaults 8765 — override
   `--url http://localhost:8000/`, mint nonce on :8000) → §4 paragraph + one figure. Fallback: local + say-so.

Then (lower priority): G3 (frozen EGR receipt), the 9 manuscript honesty fixes, G2 eQTL-existence spike.

**Prerequisites**: none blocking. `search_all` + as-of-T windowing verified. CS up (pid on :8000). latexmk broken
(4-pass `pdflatex; bibtex main; pdflatex; pdflatex`).

**Open questions**: does the as-of-T ab-gate keep positives ≥100 (build checkpoint)? does a NAB2 CD4⁺ cis-eQTL
exist (gates G2)?

**Do not touch**: submission artifacts / demo video (fire-ready; "scrub and flip"). Do NOT re-run `build_tex.py`.
Dated audit/reconciliation/debate records are IMMUTABLE — cite; update `docs/CLAIMS_EVIDENCE_LEDGER.md` for status.

**Context to preload** (≤10): `docs/CLAIMS_EVIDENCE_LEDGER.md` (READ FIRST); `docs/plans/heldout-eval-implementation-plan_2026-07-12.md`
(the v3 build spec); `docs/reviews/codex-debate_heldout-eval-plan_2026-07-12.md` (debate synthesis);
`docs/claims-vs-experiments_2026-07-12/RECONCILIATION.md`; `docs/claims-vs-experiments_2026-07-12/NEW_EXPERIMENTS.md`;
`docs/reviews/contribution-novelty-audit_2026-07-12/VERDICT.md`; `src/arbiter/lbd/{sources,propose,referee_triple}.py`;
`memory/NEXT_SESSION.md`.

**Estimated budget**: codex-rescue build ≈ 1 session; CS run + integration ≈ ½–1 session.

## Mirror of this handoff is appended to memory/sessions/2026-07-12.md by session-closer.
