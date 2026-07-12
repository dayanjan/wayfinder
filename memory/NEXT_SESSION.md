# NEXT_SESSION — async handoff (canonical; written/read by session-closer & session-start)

## 🧭 READ-FIRST (anti-amnesia — do not skip)
Before ANY claim audit, review, referee-response, revision, or new experiment, read
**`docs/CLAIMS_EVIDENCE_LEDGER.md`** — the single living index of claim → status → evidence → source → critique.
**Rule:** reconcile every claim against BOTH the literature AND the experiment corpus it indexes.

## 🚀 SUBMISSION FIRE-READY — still governs (unchanged)
The Wayfinder hackathon submission remains BUILT + staged. On operator **"scrub and flip"**: run
`SUBMIT_CHECKLIST.md` steps 1–5 → flip `dayanjan/wayfinder` public → hand back the URL. Facts: `docs/HACKATHON.md`.

---

## Next session priorities — written 2026-07-12 (full-close, autonomous G1 build)

**Current state**: **G1 (the held-out evaluation = the manuscript's publish gate) is BUILT, RUN, and
INTEGRATED.** The audit's central FATAL — "method demonstrated, never measured" — is **CLOSED**: the method is
now *measured*, and the honest result is a **NULL at the pre-registered primary metric**, reported straight in
new **§4.7 + Fig 5**. Manuscript compiles clean (**34 pp, 0 errors**). Full audit trail:
`docs/g1-build-log_2026-07-12.md`. Commits `8858d67`→`a3f3141`, all pushed; tree clean.

**G1 result (for context)**: frame 22,437 novel-at-2016 pairs, 5,570 positives (24.8%). C_broad (Wayfinder−lit-
rarity) +0.20 [−0.20,+0.65]; C_mech (Wayfinder−disease-hop-only) −0.15 [−0.35,+0.30]; joint `broad_null`, robust
across k=3/k=5/pure-disjoint. Wayfinder leads on secondary p@5 (0.80) + MAP (0.287) but not the primary; disease-
hop-only matches/beats it at p@20 — the measured face of §4.1b's substrate-inherited stringency.

**Next action** (pick one; ordered by value):
1. **Apply the 9 manuscript honesty fixes** from `docs/claims-vs-experiments_2026-07-12/NEW_EXPERIMENTS.md`
   (M6 "byte-for-byte"→"value-identical"; M5 "flagged & removed" wording; R2 funnel 395↔406; M8/R4 rank-
   stability conditions; B6 T/NK n.s.; retire the buggy [74,90] script cite; stale "1.9 kb"; M7 wording; B7
   EGR2 caveat). Cheap, independent, honest-record hygiene. **[CLAUDE]**
2. **Re-assess the manuscript contribution framing** now that G1 is measured (null): the paper is honestly
   "receipt-backed prioritization + abstention + falsification with an evaluated null"; confirm the abstract +
   §1 + §5 lead with that and don't overclaim ranking superiority. **[CLAUDE]**
3. **(Optional) CS independent-verification of G1 metrics**: drive CS (:8000) to recompute the two co-primary
   contrasts from the committed manifest + reviewer-verify +0.20/−0.15/broad_null (a §4.5-consistent check).
   Lower priority — the null is already backed by the committed manifest + codex code-review + unit tests. **[CLAUDE]**
4. **G3 (frozen EGR receipt)** — re-run `nab2_egr_mechanism_check.py`, commit the output JSON (R5). **[CLAUDE — small]**

**Prerequisites**: none blocking. Manuscript compiles via 4-pass `pdflatex; bibtex main; pdflatex; pdflatex`
(latexmk broken). CS up on :8000 if pursuing #3.

**Open questions**: does the null survive an external ground-truth panel + a larger (>12) disease panel (raises
power)? Given G1 is now measured, is the paper publishable as-is (audit's "do not publish until measured" is met)?

**Do not touch**: submission artifacts / demo video (fire-ready; "scrub and flip"). The committed G1 receipts
(`data/eval_out/count_manifest_full_T2016_k5.json`, `eval_results_T2016_k5.json`, `sensitivity.json`) and the
dated audit/reconciliation/debate records are IMMUTABLE — cite, don't edit; update `CLAIMS_EVIDENCE_LEDGER.md`.

**Context to preload** (≤10): `docs/g1-build-log_2026-07-12.md`; `docs/CLAIMS_EVIDENCE_LEDGER.md`;
`docs/manuscript/latex/sections/04_results.tex` (§4.7); `data/eval_out/SUMMARY.md`;
`docs/claims-vs-experiments_2026-07-12/NEW_EXPERIMENTS.md`; `docs/reviews/diff_g1-harness_2026-07-12.md`;
`src/arbiter/eval/`; `memory/NEXT_SESSION.md`.

**Estimated budget**: honesty fixes ≈ ½ session; contribution reframe ≈ ½ session; CS verify ≈ ½–1 session.

## Mirror of this handoff is appended to memory/sessions/2026-07-12.md by session-closer.
