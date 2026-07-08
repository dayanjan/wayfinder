# Round 3 — Codex final critique (repo-read)

**Position:** Claude's round-3 position is directionally right: the Streamlit workbench should be anchored by the deterministic <1s referee, with the cached funnel and pre-computed Claude Science lane supporting rather than driving the demo. Repo verification confirms the corrected sys.path preflight runs and the NAB2→multiple sclerosis triple is the clean disease-hop NO, but two stale handoff seams remain in repo docs that could mislead the build if followed literally.

**Convergence:** still iterating | sanding: None

**Dropped:** F-010, F-011

### F-009 [P1] One stale preflight sentence still asks for failing `import arbiter` semantics
- Verified from repo root: plain `python -c "import arbiter"` fails with `ModuleNotFoundError`; the corrected one-liner with `sys.path.insert(0, str(Path('src').resolve()))` runs and returns `untested`. `docs/plans/streamlit_workbench_plan_2026-07-08.md:165-171` has the correct command, but `docs/plans/streamlit_workbench_plan_2026-07-08.md:71-73` still says the preflight must include `python -c "import arbiter; ...referee_triple(...)"`.
- action: Treat lines 165-171 as canonical; delete or rewrite the stale line 73 wording to say the preflight must insert `src/` before importing `arbiter.lbd...`.

### F-012 [P1] Demo-video plan still scripts SLC1A5 as the showcased REFUTED case
- The final Streamlit plan correctly says the three showcased triples are NAB2→atopic eczema, SATB1→asthma, and NAB2→multiple sclerosis, and explicitly says not to surface SLC1A5 as the clean NO (`docs/plans/streamlit_workbench_plan_2026-07-08.md:168-176`). But the linked demo-video plan still says Scene 3 chooses SLC1A5+asthma (`docs/plans/demo_video_plan_2026-07-08.md:103-104`), the preset row includes SLC1A5 (`:131`), and preflight still expects SLC1A5 (`:143-144`).
- action: Before recording or writing the Playwright script, patch the demo-video plan/pack to replace SLC1A5→asthma with NAB2→multiple sclerosis everywhere in Scene 3, presets, and smoke assertions.

**Build watchpoint:** The single thing to watch during the build: do not start Tier-2/CS or demo-video scripting until the corrected Tier-1 preflight passes with NAB2→MS replacing every stale SLC1A5 clean-NO reference.