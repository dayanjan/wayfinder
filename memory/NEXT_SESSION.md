# NEXT_SESSION — async handoff (canonical; written/read by session-closer & session-start)

## 🧭 READ-FIRST (anti-amnesia — do not skip)
Before ANY claim audit, review, referee-response, revision, or new experiment, read
**`docs/CLAIMS_EVIDENCE_LEDGER.md`** — the single living index of claim → status → evidence artifact →
source → critique. **Rule:** reconcile every claim against BOTH the literature AND the experiment corpus it
indexes; literature tells you if a claim is *novel*, the experiments tell you if it's *supported*. (This
protocol exists because a 2026-07-12 literature-only audit forgot the CS confounder experiments and
over-generalized the STAT6 critique. Don't repeat it.)

## 🚀 SUBMISSION FIRE-READY — still governs (unchanged)
The Wayfinder hackathon submission remains BUILT + staged. On operator **"scrub and flip" / "we're ready"**:
run `SUBMIT_CHECKLIST.md` (gitignored, repo root) steps 1–5 → scrub `wijesingheds` paths (LAST) · add video
link · leak grep · commit · `gh repo edit dayanjan/wayfinder --visibility public` → hand back the public URL.
Deadline: official EOD ET **Mon 2026-07-13**. Independent of the manuscript thread below.

---

## Next session priorities — written 2026-07-12 (contribution audit + claims↔experiments reconciliation done)

**Current state**: A **13-agent mixed-model literature novelty audit** (`docs/reviews/contribution-novelty-audit_2026-07-12/`,
capped by `VERDICT.md`) + a **claims↔already-run-CS-experiments reconciliation**
(`docs/claims-vs-experiments_2026-07-12/`, capped by `RECONCILIATION.md`) are COMPLETE, committed, pushed
(`e626b4c`→`bba1e18`+ledger). The findings are folded into the canonical **`docs/CLAIMS_EVIDENCE_LEDGER.md`**.

**Verdict (re-balanced by the reconciliation):**
- **Method** = novel-but-NARROW **and UNEVALUATED** (no precision/recall/baseline exists — confirmed by the
  experiments themselves). This is the one thing blocking an evaluated-methods publication → gap **G1**.
- **Biology** = stronger/better-defended than the literature audit alone implied. The STAT6 "mistaken identity"
  attack was RETRACTED: of 3 confounder channels the experiments CLOSE two (expression cis-artifact B3 ·
  cluster-membership B4); only the 12q13 GWAS-disease-label (B5) is open, and the paper foregrounds it → gap **G2**.
- **Honesty** = largely accurate, with **9 specific fixes** to apply (in `NEW_EXPERIMENTS.md`; e.g. "byte-for-byte"
  is literally false, 395-vs-406 funnel discrepancy, "flagged & removed" half-true, a self-caught wrong-cluster bug).

**Next action** — `docs/claims-vs-experiments_2026-07-12/NEW_EXPERIMENTS.md` is the plan. In order:
1. **G1 de-risk spike** [CLAUDE — needs live network]: confirm Europe PMC as-of-T date-windowing behaves + size
   the post-T positive class at T∈{2016,2018,2020}. Decides held-out-eval (Option A) vs promote-hard_negatives
   (Option B). Scope: `docs/plans/heldout-eval-scope_2026-07-12.md`. Output → `docs/spikes/heldout-eval-feasibility_<date>.md`.
2. **Apply the 9 manuscript honesty fixes** [CLAUDE] — cheap, independent, record-hygiene.
3. **G3 frozen EGR-distinctness receipt** [CLAUDE — small]: re-run `nab2_egr_mechanism_check.py`, commit its output JSON.
4. **G2 eQTL-existence spike** [CODEX-SPIKE→CLAUDE]: does a NAB2 CD4⁺ cis-eQTL exist? (if not, B5 stays honestly-open).
5. Build the chosen **G1 eval** [CODEX-RESCUE→CLAUDE] → the method becomes *measured* → re-assess publishability.

**Prerequisites**: none blocking. Live literature tool works (`src.arbiter.lit.search.search_all`, .env keys).
`main.pdf` still compiles (32pp) via the 4-pass `pdflatex; bibtex main; pdflatex; pdflatex` (latexmk broken).

**Do not touch**: submission artifacts / demo video (fire-ready; "scrub and flip" governs). Do NOT re-run
`build_tex.py` (overwrites hand-edited .tex). The dated audit/reconciliation records are IMMUTABLE — cite,
don't edit; update `docs/CLAIMS_EVIDENCE_LEDGER.md` for status changes.

**Context to preload** (≤10): `docs/CLAIMS_EVIDENCE_LEDGER.md` (READ FIRST — the living index);
`docs/claims-vs-experiments_2026-07-12/RECONCILIATION.md`; `docs/claims-vs-experiments_2026-07-12/NEW_EXPERIMENTS.md`;
`docs/reviews/contribution-novelty-audit_2026-07-12/VERDICT.md`; `docs/plans/heldout-eval-scope_2026-07-12.md`;
`docs/manuscript/latex/main.pdf`; `memory/NEXT_SESSION.md`.

**Estimated budget**: G1 spike ≈ ½ session; fixes ≈ ½ session; G1 build ≈ 1 session; G2 ≈ 1 session.

## Mirror of this handoff is appended to memory/sessions/2026-07-12.md by session-closer.
