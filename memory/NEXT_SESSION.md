# NEXT_SESSION — async handoff (canonical; written/read by session-closer & session-start)

## Next session priorities — written 2026-07-08 (autonomous overnight session)

**Current state**: Tree clean-ish (5 commits landed; a few PM-doc edits may be uncommitted — see
below). **M3 done, finding landed.** The LBD question-proposer is BUILT end-to-end and a
**receipt-backed near-novel finding** is locked: **NAB2 → Th1/Th2 polarization → atopic eczema**
(@ Stim8hr). Full arc this session: spec hardened v1→v2 via 3-round repo-read codex-debate; fresh
tool layer authored + verified; disease ids resolved to MONDO (not EFO); `referee_triple` exact-disease
adapter built + verified; a Codex code consult found + we fixed a scoring-rewards-obscurity issue and
a full-chain verdict bug; full Stim8hr sweep = **22,039 candidate questions → 30 clean full-chain
referee-supported**. Finding writeup: `docs/lbd_finding_nab2_2026-07-08.md`. Everything is documented
in `docs/lbd-build-log.md` (read it first — it has the Codex verdicts + framing caveats).

**Next action**: **Operator eyeball the NAB2 finding + honest framing**, then start **M5 (demo video
+ README-as-paper)** — the finding writeup is the paper seed. The demo story is the funnel
(22,039→30) + NAB2's per-hop receipt + the cull examples (NUDT1 weak / DNAJB9 off-target / 21,995
refuted). [CLAUDE for README-as-paper synthesis; demo-video skill for the 3-min capture.] Optional
bonus before the demo: run Rest + Stim48hr sweeps (`python -m arbiter.lbd.propose --condition Rest`)
for appendix candidates — Codex said Stim8hr alone is sufficient, do NOT let this delay the demo.

**Prerequisites**: `pip install -r requirements.txt` (pandas+requests). API cache in `data/lbd_cache/`
(gitignored) makes the sweep re-run fast/offline. No GPU/Colab.

**Open questions / honest-framing guardrails (Codex-vetted — respect these in the demo)**:
(1) NAB2 is **near-novel, NOT novel** — ac_lit=6 is a low noisy count, never say "known/established";
(2) only **1 of 2 program contrasts** significant (Ota yes, Hollbacker no) — state it;
(3) the **EGR2–NAB2 corepressor** link is a *hypothesis-strengthener, NOT referee evidence* — subordinate to the receipt;
(4) judging **weights still unverified** on the CV form (only "demo video super important" confirmed).

**Do not touch**: never commit `.env`, `data/*.csv`, `data/lbd_cache/`, `data/lbd_out/`,
`.claude/scratch/`, `01-hackaton details/`. The referee lives in `docs/perturbseq-qc_2026-07-07/`.

**Context to preload**: `docs/lbd_finding_nab2_2026-07-08.md`, `docs/lbd-build-log.md`,
`docs/lbd-proposer-spec.md` (v2), `docs/reviews/codex-debate_lbd-proposer-spec_2026-07-07.md`,
`src/arbiter/lbd/propose.py`, `src/arbiter/lbd/referee_triple.py`, `WORK_PROGRESS.md`, `MEMORY.md`.

**If PM docs are uncommitted**: `WORK_PROGRESS.md` + `MEMORY.md` + this file may be staged/dirty from
the overnight session — commit them as housekeeping (`git add WORK_PROGRESS.md MEMORY.md memory/NEXT_SESSION.md && git commit`).

**Estimated budget**: M5 demo + README-as-paper ~0.5–1 day. Deadline 2026-07-13 9:00 PM ET.
