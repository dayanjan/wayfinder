# Codex-debate synthesis — Streamlit Researcher's Workbench (2026-07-08)

**Framing question.** Is the 3-tier Researcher's Workbench (instant deterministic **referee** hero +
cached **LBD explorer** + async **Claude Science** lane with a pre-computed default + optional live
trigger) the right Streamlit app to anchor the demo — the CS bidirectional decision, the scope vs the
2026-07-13 deadline, and the Streamlit/`referee_triple` integration snags. Solo builder; Researcher track
("a researcher who also builds"); judged Demo 30% / Claude Use 25% / Impact 25% / Depth 20%.

**Mode.** 3 rounds, `--preserve-intent`, **repo-read** (Codex verified every claim against the actual
files — `referee_triple.py`, `entities.py`, `sweep_Stim8hr.json`, the CS artifacts, the `drive-claude-
science` driver, both plans). Per-round artifacts in `docs/reviews/codex-debate_streamlit-workbench_2026-07-08/`.

## Trajectory
- **R1 — 8 findings.** Two P0 must-fixes: (F-001) Streamlit **cannot `import arbiter`** (no package
  metadata — confirmed live), needs a `sys.path.insert(.../src)` at startup; (F-002) **SLC1A5→asthma is
  not a clean disease-hop NO** (its EFFECT hop refutes upstream). Plus: live-CS far less ready than
  implied (F-003), 3-tier scope exceeds the demo's needs (F-004), the UNTESTED greyed cards contradict
  "everything real" (F-005), gitignored data needs a fixture path (F-006), CS vocabulary ≠ app taxonomy
  (F-007), funnel wording sloppy (F-008).
- **R2 — dropped 7/8**, escalated 1, +3 new: preflight command must mirror the sys.path fix (F-009), the
  app's CS panel must not surface the stale SLC1A5 case (F-010), the design brief still invited
  post-preflight scope into the first build (F-011).
- **R3 — converged.** 2 residual stale-text seams only: a leftover preflight phrase (F-009) and a
  cross-document catch — the **demo-video plan still scripted SLC1A5** as the Scene-3 NO (F-012). Both patched.

## Decisions of record (what the app will be)
1. **Tiered by latency.** Tier-1 **referee** (<1s, deterministic) is the interactive/demo **spine** and
   the ONLY thing that must pass screen-only preflight first. Compact funnel strip + static CS figure are
   demo-supporting. Full explorer / theming / motion / live-CS are post-preflight.
2. **Claude Science = async deep-dive lane, pre-computed default.** The pre-computed evidence chain
   carries the "genuine CS use" credit instantly; the **live trigger is a disabled operator-only stretch**
   behind a proper wrapper, never on the demo path (the driver's daemon/nonce-3min/full-auto/artifact-copy
   realities make a casual live integration a deadline + on-camera risk). **The novel claim survived
   intact and was reinforced** — CS is never the synchronous core.
3. **The three showcased triples (sharpened):** NAB2→atopic eczema (**YES**) · SATB1→asthma (**UNTESTED**,
   halts at the gate) · **NAB2→multiple sclerosis** (**clean NO** — GATE/EFFECT/PROGRAM green, DISEASE
   red). YES and NO share the gene, isolating the disease hop — a stronger disease-specificity story than
   the discarded SLC1A5. (Both the workbench plan AND the demo-video plan now use NAB2→MS.)
4. **Integration:** app inserts `src/` on `sys.path` at startup; `load_referee_data()` under
   `@st.cache_resource`; UNTESTED downstream cards are **presentation-only placeholders** ("not
   evaluated"), not fabricated hops; LBD data from a checked-in **`app/fixtures/`** (`data/lbd_out/` stays
   gitignored); the CS lane is provenance/narrative, not coerced into the referee badge taxonomy.
5. **Build order:** Tier-1 referee → **preflight gate** (sys.path import check + 3 triples + Playwright
   smoke asserting visible text, twice from a fresh context) → compact funnel + static CS → post-preflight
   polish → (stretch) live-CS.

## Persistent disagreement — none unresolved
The one live question (build the live-CS trigger at all?) resolved to: build it only as a disabled
operator-only stretch after everything else is demo-ready; the pre-computed view is the reliable credit.
No convergence-sanding fired in any round.

## Preserve-intent check — PASSED
The novel claim (**CS async/pre-computed, not the synchronous core; the <1s referee is the demo spine**)
survived and was sharpened, not sanded.

## The build watchpoint (Codex's final north star)
> Do NOT start Tier-2 / CS / demo-video scripting until the corrected **Tier-1 preflight passes** with
> **NAB2→MS replacing every stale SLC1A5 clean-NO reference**.

## Recommended next move
The plan (`docs/plans/streamlit_workbench_plan_2026-07-08.md`) is a production-ready Tier-1-first build
handoff. Two parallel tracks: (a) hand the §3 design brief (Tier-1 MVP demarcated) to Claude co-design;
(b) build `app/streamlit_app.py` (Tier-1) → preflight gate → then the compact funnel + static CS.
