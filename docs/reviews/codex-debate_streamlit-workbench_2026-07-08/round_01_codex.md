# Round 1 — Codex critique (repo-read)

**Position:** Claude's latency-tier split is directionally right and the async/precomputed Claude Science lane should be preserved. The hostile read is that the plan underestimates integration risk, overbuilds beyond the 3-minute demo arc, and has a few contract mismatches that could turn the flagship screen into a Potemkin-looking UI if not fixed before implementation.

### F-001 [P0] Streamlit cannot import `arbiter` from repo root as planned
- sev5/lik4/blast4 · correctness · NOVELTY
- evidence: `docs/plans/streamlit_workbench_plan_2026-07-08.md:56` says `from arbiter.lbd.referee_triple import ...`; `requirements.txt` has only pandas/requests/h5py/s3fs and no installable package metadata. A clean `python -c "import arbiter"` from repo root fails with `ModuleNotFoundError`. The source package lives under `src/`, so Streamlit launched from repo root does not automatically see it.
- action: Make import setup explicit before UI work: add a minimal packaging file or insert the repo `src` path at app startup, then include this in the preflight gate. Do not rely on 'run from repo root' alone.

### F-002 [P0] The SLC1A5 demo claim is not a clean disease-hop refutation
- sev5/lik4/blast4 · correctness · NOVELTY
- evidence: Running the real contract gives `SLC1A5 asthma Stim8hr -> answer=refuted_for_c` but hops are GATE supported, EFFECT refuted, PROGRAM supported, DISEASE refuted. `referee_triple.py:121-124` prioritizes `classification != supported` before effect/program checks, so `answer` becomes `refuted_for_c` even when EFFECT is already refuted. The demo plan says Scene 3 is a confident NO at disease hop; `docs/plans/demo_video_plan_2026-07-08.md:103-104`.
- action: Either choose a refuted example whose upstream hops are genuinely green, or narrate SLC1A5 as a chain refutation with both effect and disease receipts. Round 2 must resolve whether the flagship NO is disease-specific or whole-chain.

### F-003 [P1] Live Claude Science trigger is substantially less Streamlit-ready than the plan implies
- sev4/lik5/blast4 · novelty · NOVELTY
- evidence: The skill requires WSL daemon lifecycle and nonce minting (`SKILL.md:13-21`, `30-40`), manual artifact discovery/copy via WSL paths (`41-48`), full-auto approval of network/data grants (`58-64`), and warns scraped text is unreliable (`66-70`). The driver hardcodes Playwright from `C:/Users/wijesingheds/.claude-c/skills/demo-video/node_modules/playwright` (`cs-drive.js:4`) and requires `--nonce` on expired auth (`cs-drive.js:29-34`).
- action: Preserve the async/precomputed split, but make live CS a disabled or operator-only stretch until there is a wrapper that handles daemon status, nonce minting, prompt file creation, artifact copy, timeout, and error display. Do not implement the raw driver call in the demo-critical app path.

### F-004 [P1] Three-tier workbench scope exceeds what the actual demo plan needs
- sev4/lik4/blast4 · novelty · NOVELTY
- evidence: The demo plan’s settled arc is Streamlit referee hero, one funnel beat, and the pre-rendered CS figure, explicitly 'never a live S3 run' for Scene 5 (`demo_video_plan_2026-07-08.md:109-113`). The app plan makes Tier 2 and Tier 3-precomputed demo-critical and specifies a full three-screen workbench with nav, table, figure, narrative panel, themes, and optional live trigger (`streamlit_workbench_plan_2026-07-08.md:38-49`, `101-120`).
- action: Keep Tier 1 as the implementation spine. Build the funnel and CS artifact as compact supporting sections only after the three flagship triples pass screen-only smoke. Treat sortable explorer, themes, and live trigger as post-preflight work.

### F-005 [P1] The UI contract invents downstream cards for HOP-0 failures while also claiming every value comes from `referee_triple`
- sev3/lik5/blast3 · correctness · NOVELTY
- evidence: `referee_triple.py:103-106` returns only HOP-0 when the gate fails. The plan correctly states gate-fail is only HOP-0 (`streamlit_workbench_plan_2026-07-08.md:58-60`) but the design asks EFFECT/PROGRAM/DISEASE to render greyed and struck through (`91-94`) while the risk section says every verdict/receipt comes from `referee_triple` with no hardcoding (`154-155`).
- action: Define synthetic downstream placeholders as presentation-only with no receipts, derived solely from `answer == 'untested'` and the HOP-0 receipt. Label them 'not evaluated' rather than treating them as returned hops.

### F-006 [P2] LBD cached data dependency is gitignored, so the recommended check-in needs a concrete hygiene mechanism
- sev3/lik4/blast3 · correctness
- evidence: .gitignore:38-39 ignores all `data/lbd_out/`. The two needed files exist locally and are small: `sweep_Stim8hr.json` is 35,112 bytes and `lbd_questions_Stim8hr.json` is 13,241 bytes. The plan says check in a small copy is recommended (`streamlit_workbench_plan_2026-07-08.md:145-146`) but does not decide whether to force-add ignored generated outputs or move curated fixtures elsewhere.
- action: Create a deliberate checked-in fixture path such as `docs/demo_fixtures/` or `app/fixtures/` containing only the two curated JSONs plus provenance. Keep `data/lbd_out/` ignored as regenerable scratch.

### F-007 [P2] The Claude Science artifact vocabulary does not match the app verdict taxonomy cleanly
- sev3/lik4/blast2 · correctness
- evidence: `claude_science_verdict.json` uses statuses like `passed`, `supported (1 of 2 contrasts)`, `UNTESTED`, `REFUTED (at disease hop)`, and `cis-artifact WEAKENED` (`claude_science_verdict.json:8`, `20`, `47`, `52`). The app taxonomy is `supported`, `supported_weak`, `supported_flagged`, `untested`, `untested_for_c`, `refuted_for_c`, `refuted_effect`, `refuted_program` (`streamlit_workbench_plan_2026-07-08.md:97-99`).
- action: Render the CS lane as provenance/narrative evidence, not as the same deterministic verdict object, unless a small adapter maps statuses explicitly and preserves the original wording.

### F-008 [P2] The 'refused ~22,000' funnel wording is directionally good but numerically sloppy
- sev2/lik4/blast2 · correctness
- evidence: `sweep_Stim8hr.json` funnel has `eligible_pairs: 22039`, `refuted_for_c: 21995`, `supported: 30`, `supported_weak: 10`, `supported_flagged: 3`, and `refuted_effect: 1`. The plan says 22,039 -> 30 and 'refused ~22,000' (`streamlit_workbench_plan_2026-07-08.md:107-110`).
- action: Show the full chain class breakdown: 21,995 refuted-for-C, 1 refuted-effect, 10 weak, 3 flagged, 30 clean supported. Narrate 'about twenty-two thousand did not become clean full-chain findings' rather than 'the referee refuted the rest.'

**Next question:** Round 2 must first resolve the flagship demo spine: what exact three live triples will be shown, especially the 'confident NO', and what is the minimum app surface that passes screen-only preflight before any Tier-2/Tier-3 expansion or live-CS stretch work?