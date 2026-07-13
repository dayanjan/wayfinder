# NEXT_SESSION — async handoff (canonical; written/read by session-closer & session-start)

## 🧭 READ-FIRST (anti-amnesia — do not skip)
Before ANY claim audit, review, referee-response, revision, or new experiment, read
**`docs/CLAIMS_EVIDENCE_LEDGER.md`** — the single living index of claim → status → evidence → source → critique.
**Rule:** reconcile every claim against BOTH the literature AND the experiment corpus it indexes.

## 🚀 SUBMISSION FIRE-READY — still governs (unchanged)
The Wayfinder hackathon submission remains BUILT + staged. On operator **"scrub and flip"**: run
`SUBMIT_CHECKLIST.md` steps 1–5 → flip `dayanjan/wayfinder` public → hand back the URL. Facts: `docs/HACKATHON.md`.

---

## Next session priorities — written 2026-07-13 (full-close)

**Current state**: Manuscript **finalized for this pass** — 36 pp, 6 figures, 0 errors, 4-pass clean, all
pushed (through `c802fd1`); tree clean. This session: G1 measured-null + **CS corroboration** (blind, §4.7 +
Fig 6), 9 honesty fixes, contribution reframe (finding-first Contributions block, §1), self-praise sweep, **G3**
EGR-distinctness receipt (R5 closed), and a **retitle** to foreground Claude Science for the hackathon. Deliverable:
`docs/manuscript/latex/main.pdf` (regenerate via 4-pass `pdflatex; bibtex main; pdflatex; pdflatex`).

**Next action — REFERENCE VERIFICATION (no hallucinations + relevance).** Two checks over the manuscript's
citations (**39 `\cite` commands** across `docs/manuscript/latex/sections/` + `main.tex`; entries in
`docs/manuscript/latex/references.bib`):
1. **No hallucinated references** — every `references.bib` entry is a real paper with a resolving DOI. Prior
   sessions DOI-resolved them, but re-verify. **In-repo tools already present:**
   `tools/{crossref_lookup,semantic_scholar,zotero_sync}.py` (the ported LightsOut citation stack) — use these
   to resolve/confirm each DOI/title programmatically (deterministic, §19 direct-tool-over-MCP).
2. **Relevance** — for each `\cite`, confirm the cited paper actually supports the specific statement it backs
   (the common failure: a real paper cited for the wrong claim). This needs reading each cited title/abstract
   and matching to the sentence. **Reuse skills from the LightsOut R01 / R01-template sibling projects** —
   the operator says those have citation-audit / reference-relevance skills; find + reuse them rather than
   rebuild. (Locate via the sibling repos; check their `.claude/skills/`.)
   **[CLAUDE + in-repo tools; reuse LightsOut R01 skills]**

**Then (lower priority)**:
- **Re-assess publishability** (the audit's "do not publish until measured" bar is met; R5 has a receipt now).
- **Frontiers/FRMA submission formatting** (current build = LightsOut LaTeX template).
- **G2 eQTL-existence spike** — does a NAB2 CD4⁺ cis-eQTL exist (gates whether B5/12q13 is resolvable)? **[CODEX-SPIKE then CLAUDE]**

**Prerequisites**: none blocking. `tools/*.py` need the project `.env` keys (already present per prior sessions).

**Open questions**: any citation cited for a claim it does not actually support? Any bib entry that fails to resolve?

**Do not touch**: submission artifacts / demo video (fire-ready). Committed G1/G3 receipts
(`data/eval_out/{count_manifest_full_T2016_k5,eval_results_T2016_k5,sensitivity,cs_verify_result}.json`,
`docs/manuscript/analysis/egr_distinctness_results.json`) + dated audit records are IMMUTABLE — cite, don't edit;
update `CLAIMS_EVIDENCE_LEDGER.md` for status.

**Context to preload** (≤10): `docs/CLAIMS_EVIDENCE_LEDGER.md`; `docs/manuscript/latex/references.bib`;
`docs/manuscript/latex/sections/` (for the `\cite` sites); `tools/crossref_lookup.py`;
`tools/semantic_scholar.py`; `docs/g1-build-log_2026-07-12.md`; `docs/HACKATHON.md`; `memory/NEXT_SESSION.md`.

**Estimated budget**: reference verification ≈ 1 session (39 cites; tool-assisted).

## Mirror of this handoff is appended to memory/sessions/2026-07-13.md by session-closer.
