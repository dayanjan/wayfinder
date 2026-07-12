# NEXT_SESSION — async handoff (canonical; written/read by session-closer & session-start)

## 🚀 SUBMISSION FIRE-READY — still governs (unchanged)
The Wayfinder hackathon submission remains BUILT + staged. On operator **"scrub and flip" / "we're ready"**:
run `SUBMIT_CHECKLIST.md` (gitignored, repo root) steps 1–5 → scrub `wijesingheds` paths (LAST) · add video
link · leak grep · commit · `gh repo edit dayanjan/wayfinder --visibility public` → hand back the public URL.
Deadline: official EOD ET **Mon 2026-07-13**. See memory `submission-fire-ready`. Independent of the
manuscript thread below.

---

## Next session priorities — written 2026-07-11 (overnight autonomous session)

**Current state**: MANUSCRIPT thread — **submission-ready draft COMPLETE, review-hardened, and polished**
(full-close; commits `62bb929` → `4f4337f` → `ab87fb2`, all pushed). The manuscript has **4 figures** (padded
boxes), a **related-work §2.4**, an **evidence-strengthening §5.3b**, a **corrected NAB2/STAT6 genomics**,
**first-line paragraph indents** (run-in bold headings kept flush), and an **Acknowledgements + Data/code
availability** section (Cerebral Valley hackathon; Marson lab dataset; Claude Science; Anthropic Claude Max +
API credits). Every P0/P1 from a **5-reviewer pass (4 Claude + Codex) + a final Codex debate** is applied.
Compiles at **32 pp, 0 errors, 0 undefined citations, 0 bibtex warnings**. Codex verdict: *"submission-defensible
on its own terms."* The plausibility2026 byline is now filled (Yuan et al.) and the frozen markdown's stale
genomics is synced.

**THE DELIVERABLE TO READ**: `docs/manuscript/latex/main.pdf` (32 pp, freshly compiled). Open it directly.

**Next action** — operator reads `main.pdf`; then choose one of:
1. **Frontiers formatting for submission** [CLAUDE/HYBRID]: swap `natbib` numbered-super → Frontiers
   author-year style + a Frontiers CSL for the DOCX path; apply the Frontiers article template; fill the one
   pending byline (`plausibility2026` = arXiv:2606.01042 — bib placeholder "Byline pending"). (README "Still
   to do".)
2. **Execute an offline evidence-strengthener** the paper now promises in §5.3b [CLAUDE/CODEX]: the
   highest-value is a **time-sliced held-out eval** (freeze literature at a cutoff, measure recovery); also a
   **12q13 colocalization** attempt for NAB2 vs STAT6 (coloc/SMR) — both are real analyses, likely
   post-hackathon.
3. **Return to the hackathon submission** — say **"scrub and flip"** (governed above).

**Prerequisites**: none blocking. `main.pdf` is current. If recompiling: `latexmk` is BROKEN on this machine
(MiKTeX lost its `perl` engine) — compile with the 4-pass `pdflatex; bibtex main; pdflatex; pdflatex`
sequence instead (documented in `docs/manuscript/latex/README.md`).

**Open questions** (all TODOs from the prior close are now done):
- **Frontiers submission formatting** remains (the real pre-submission step, not "small"): swap `natbib`
  numbered-super → Frontiers author-year + a Frontiers CSL for the DOCX path; apply the Frontiers article/Word
  template. Deferred to actual submission.
- Optional polish NOT applied (low-value, reviewer-noted; safe to skip): trim the CS `$6.41`/scriptability
  detail to supplementary (§4.5); a fully-worked second survivor (EGR2) — handled by the n=1 limitation;
  one-line PerTurboAgent cite; `12q13`→`12q13.3` once.

**Do not touch**: the submission artifacts / demo video (fire-ready; "scrub and flip" governs). Do NOT re-run
`docs/manuscript/latex/build_tex.py` (overwrites hand-edited `.tex`). Figures regenerate deterministically via
`docs/manuscript/latex/figures/make_figures.py` from the committed analysis JSON.

**Context to preload** (≤10): `docs/manuscript/latex/main.pdf` (the deliverable);
`docs/reviews/agent-review-and-resolution_manuscript_2026-07-11.md` (what the 5 reviewers found + how each was
fixed); `docs/reviews/codex-debate_manuscript-final_2026-07-11.md` (final verdict);
`docs/manuscript/latex/sections/04_results.tex`; `docs/manuscript/latex/sections/02_background.tex` (§2.4);
`docs/manuscript/latex/sections/05_discussion.tex` (§5.3b); `docs/manuscript/latex/README.md`;
`references/references.bib`; `docs/manuscript/latex/figures/make_figures.py`; `memory/NEXT_SESSION.md`.

**Estimated budget**: Frontiers formatting = ½–1 session. A held-out eval or colocalization = 1 session each.

## Mirror of this handoff is appended to memory/sessions/2026-07-11.md by session-closer.
