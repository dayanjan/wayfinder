# Round 2 — Codex re-critique (repo-read)

**Position:** Claude's revision fixes the main strategic error: the demo spine is now a deterministic, sub-second referee, with Claude Science preserved as an async/provenance lane rather than the synchronous core. The revised NAB2→MS NO is repo-real and much stronger than SLC1A5, but the plan still has a few implementation traps where stale wording or handoff instructions can reintroduce old risks.

**Convergence:** still iterating

**Dropped:** F-002, F-003, F-004, F-005, F-006, F-007, F-008
**Escalated:** F-001

### F-009 [P1] Preflight command still contradicts the required src-path import fix
- Verified from repo root: `python -c "import arbiter"` fails with `ModuleNotFoundError`. Verified the app-style fix works: inserting `Path.cwd() / 'src'` allows `from arbiter.lbd.referee_triple import ...` and the three live triples run correctly. The revised plan still says the preflight must include `python -c "import arbiter; ...referee_triple(...)"`, which will fail unless the command itself inserts `src` or the package is installed.
- action: Make the preflight command mirror the app exactly: `python -c "import sys; from pathlib import Path; sys.path.insert(0, str(Path.cwd()/'src')); from arbiter.lbd.referee_triple import ..."`, or add minimal packaging and test that instead.

### F-010 [P1] The static Claude Science artifact still contains the stale SLC1A5 disease-hop wording
- `docs/claude-science-evidence-chain_2026-07-08/claude_science_verdict.json` has `contrast_cases.SLC1A5.status = "REFUTED (at disease hop)"`. Round 1 established SLC1A5 is not the clean NO demo example, and the live referee output now confirms the clean NO is NAB2→multiple sclerosis: GATE/EFFECT/PROGRAM supported, DISEASE refuted, `answer=refuted_for_c`.
- action: For the CS lane, either omit the SLC1A5 contrast case from the compact app view or label it as a legacy/chain-level contrast, while making NAB2→MS the only showcased clean disease-hop NO.

### F-011 [P2] The co-design brief still invites post-preflight scope back into the first build
- The sequencing section correctly says Tier 1 passes smoke before Tier 2/3, with sortable explorer, theme polish, motion, and live CS post-preflight. But the self-contained design brief still asks for three screens, light and dark themes, full sortable table, motion, and a visible fresh-CS button as if all are part of the design deliverable.
- action: Split the brief into `Tier-1 mandatory design` and `post-preflight design notes`; remove light/dark themes, full explorer, and live-CS button from the first implementation handoff.

**Next:** Round 3 should settle the exact Tier-1-first implementation handoff: the corrected preflight command, whether the compact demo includes any funnel seconds, and how the CS panel avoids surfacing the stale SLC1A5 contrast while preserving the async deep-dive lane.