# Round 1 — Claude's opening position

**Framing question.** Is the **3-tier Researcher's Workbench** the right design for the Streamlit app
that anchors the demo — (1) an instant deterministic **referee** hero, (2) a cached **LBD explorer**,
(3) an async **Claude Science lane** with a pre-computed default + an optional live trigger — especially
the CS bidirectional-integration decision and the scope vs the 2026-07-13 deadline (solo builder)?
Hackathon = Researcher track ("a researcher who also builds"), judged Demo 30% / Claude Use 25% /
Impact 25% / Depth 20%.

**Novel claim to preserve.** **Claude Science must be an ASYNC deep-dive lane with a pre-computed
default — NOT the synchronous core.** The referee's <1s determinism is the interactive/demo core;
bidirectional *live* CS is an optional capability demonstration, deliberately off the demo's critical
path. Do not sand this into either "drop CS integration entirely" or "make the app wait on live CS."

## Position
1. **Tiered by latency, not by feature.** Referee = <1s (pandas over local CSVs) → the interactive hero.
   Claude Science = 5–20 min/task, only drivable via the Playwright automation (daemon + single-use auth
   nonce + full-auto approval) → cannot be synchronous. So: Tier-1 referee is the spine; Tier-3 CS is an
   async augmentation whose DEFAULT is the pre-computed evidence chain we already built, with the LIVE
   trigger as an honestly-labeled ("~several minutes") optional stretch, never on camera-critical path.
2. **LBD belongs on Streamlit as CACHED results, not a live sweep.** The 22-min sweep is pre-run; the app
   shows the funnel (22,039 → 30) + a browsable table of the 30 clean questions (`sweep_Stim8hr.json`),
   each click-through adjudicated live by Tier-1. This is the honest "the engine asked 22,039; the referee
   refused ~22,000" loop without pretending the sweep is instant.
3. **Everything REAL, calibrated, falsification-first.** Verdicts/receipts from `referee_triple`; funnel
   from the sweep JSON; CS panel from the real artifacts. The UNTESTED case **visibly halts at HOP-0**
   (the real contract). No Potemkin, no "discovered/proven/definitive."
4. **Scope fits the deadline.** Tiers 1 + 2 + 3-precomputed ≈ 1.5 days (demo-ready); live CS trigger is a
   post-demo stretch. Preflight gate (dep + 3 live triples + two-run screen-only smoke) precedes recording.

## Least sure of (debate targets)
- Does Tier-2 (LBD explorer) dilute the falsification-hero focus for the 3-min demo, or strengthen Impact?
- Is building the live CS trigger at all a deadline trap — is the pre-computed CS chain enough for the
  "genuine Claude Science use" credit?
- Check in the gitignored sweep JSONs (~48 KB) so the app doesn't depend on regen? Repo-hygiene concern?
- Streamlit + `referee_triple` snags: the dynamic import of `docs/perturbseq-qc_2026-07-07/
  pyzobot_referee.py`, `@st.cache_resource` holding the RefereeData object, screen-only drivability.

Plan: `docs/plans/streamlit_workbench_plan_2026-07-08.md`. Referee: `src/arbiter/lbd/referee_triple.py`.
Cached LBD: `data/lbd_out/sweep_Stim8hr.json`. CS artifacts: `docs/claude-science-evidence-chain_2026-07-08/`.
CS driver: `~/.claude/skills/drive-claude-science/`.
