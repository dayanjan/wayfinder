# NEXT_SESSION — async handoff (canonical; written/read by session-closer & session-start)

## 🚀 SUBMISSION FIRE-READY — still governs (unchanged)
The Wayfinder hackathon submission remains BUILT + staged. On operator **"scrub and flip" / "we're ready"**:
run `SUBMIT_CHECKLIST.md` (gitignored, repo root) steps 1–5 → scrub `wijesingheds` paths (LAST) · add video
link · leak grep · commit · `gh repo edit dayanjan/wayfinder --visibility public` → hand back the public URL.
Deadline: official EOD ET **Mon 2026-07-13**. See memory `submission-fire-ready`. Independent of the
manuscript thread below.

---

## Next session priorities — written 2026-07-11 20:35 (full-close)

**Current state**: Manuscript revision MVP **underway**. Four tested slices landed + pushed this session
(`cde28b2`→`676fead`): **reframe** (title → "Receipt-backed prioritization…"; top-line = prioritization +
abstention + falsification; "calibrated"=language-only; CS→replicable-in-principle), **12q13 foregrounding**
(§4.4b), **C10 gate grid** (`gate_grid.py`+§4.1c), **C2 hard negatives** (`hard_negatives.py`+§4.2b, rebuts
B1). Manuscript compiles **23pp, 0 errors**. All diagnostics run LOCALLY (repo code + `data/lbd_cache/`,
doctrine §19), cache-free/deterministic. Tree clean; all pushed. **LaTeX .tex is authoritative** — edit
`docs/manuscript/latex/sections/*.tex` directly; do NOT re-run `build_tex.py`.

**Next action** — **build the 4 essential figures** (roadmap step 4; zero exist — the reviewers' highest-
visibility gap). Recommended order + the data are ready:
1. **Fig 4 — sensitivity/permutation panel** [CLAUDE, local render]: render from the committed JSON
   (`docs/manuscript/analysis/{sensitivity_results,gate_grid_results,hard_negatives_results}.json`) via
   matplotlib or HTML/SVG — Control 1/2/3 + C10 grid + C2 decomposition. Pure §19 direct path, no CS needed.
2. **Fig 3 — NAB2 4-hop chain + 12q13 caveat** [CLAUDE, HTML/SVG or CS kernel]: the hop-by-hop receipt
   chain with the disease hop annotated "GWAS label; LD provenance open (§4.4b)".
3. **Fig 1 — architecture, construction-vs-referee visually separated** [CLAUDE, HTML/SVG schematic] (C1/C7).
4. **Fig 2 — ledger + honest funnel annotated with C2/C6 diagnostics** [CLAUDE, HTML/SVG or data].
   Then `\includegraphics` them into the .tex + captions; recompile.

**Prerequisites**: none blocking. Figure data all committed as JSON. If a data figure is built in the CS
kernel instead of locally, CS daemon is on **port 8000** (skill default 8765 is stale — pass the port).
Recommend LOCAL render (matplotlib/HTML-SVG) per §19 — deterministic, no CS dependency.

**Open questions**:
- Data figures local-render (matplotlib/HTML-SVG from committed JSON) vs CS kernel? Recommend LOCAL (§19).
- **C6**: Control 2 (§4.1b) is already a disease-label shuffle; R2 wants ONE principled null preserving
  cluster/gene-set + row marginals. Low marginal value (Control 2 largely covers it) — refine in place or
  skip for MVP?
- Do the offline strengtheners (C3c positive control blinded to novelty gate; C3a frozen-cohort temporal)
  before or after the figures? Harness pattern is now in place (`gate_grid.py`/`hard_negatives.py`).

**Do not touch**: the submission artifacts / demo video (fire-ready; "scrub and flip" governs). Do NOT
re-run `docs/manuscript/latex/build_tex.py` (overwrites hand-edited .tex). `references/*.pdf` gitignored;
`data/lbd_cache/` gitignored (39 new ac_lit entries from gate_grid live there — re-runs are deterministic
on this machine; a fresh clone would re-fetch). `.claude/scratch/` gitignored.

**Context to preload** (≤10): `docs/reviews/codex-debate_revision-plan_2026-07-11.md` (THE roadmap — figure
spec in "Figures — minimum viable set"); `docs/manuscript/reviews/REVIEW_DOSSIER_2026-07-11.md`;
`docs/manuscript/analysis/gate_grid_results.json`; `docs/manuscript/analysis/hard_negatives_results.json`;
`docs/manuscript/analysis/sensitivity_results.json`; `docs/manuscript/latex/sections/04_results.tex`;
`docs/manuscript/latex/main.tex`; `docs/manuscript/latex/README.md`; `docs/lbd_finding_nab2_2026-07-08.md`;
`memory/NEXT_SESSION.md`.

**Estimated budget**: figures = one focused session (Fig 4 + Fig 3 the priorities; Fig 1/2 schematics
cheaper). Each remaining offline diagnostic (C3c/C3a) ≈ ½ session. Start with **Fig 4** (data ready, local
render, highest depth-per-effort).

## Mirror of this handoff is appended to memory/sessions/2026-07-11.md by session-closer.
