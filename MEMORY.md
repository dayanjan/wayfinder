# MEMORY.md — PyZoBot Arbiter Session Index

Lean cross-session index. The narrative lives in `memory/sessions/YYYY-MM-DD.md`;
the live dashboard in `WORK_PROGRESS.md`; the handoff in `memory/NEXT_SESSION.md`.
This file is the fast scan: where we are, what's decided, what happened lately.

## Current Status
**2026-07-08 (full-close) — M5 SHIPPED IN FULL. The finding + a submittable product both exist.**
On top of the replicated finding (NAB2 → Th1/Th2 → atopic eczema; STAT6 cis excluded), this session built
all three M5 artifacts: (1) the executable **evidence-chain notebook**
(`notebooks/pyzobot_arbiter_evidence_chain.ipynb`, imports the vetted modules, recomputes everything
live); (2) the **Claude Science evidence chain** (`docs/claude-science-evidence-chain_2026-07-08/`, an
independent CS agent reached the same verdict + 6-panel figure); (3) the interactive **Streamlit
"Researcher's Workbench"** (`app/streamlit_app.py` — Referee / Hypothesis Engine / Claude Science,
implementing a **Claude co-design** imported via **DesignSync**) + the **final demo video** (~112s,
ElevenLabs "Brian" + CC-BY music bed, transcription gate PASS 94%; recipe in `docs/demo-video-pack/`,
MP4 out-of-band). Two 3-round repo-read codex-debates hardened the demo + workbench plans. Track reframed
to **"Researcher who also builds"**. The demo/app are the **fallback MVP**.
**Next:** deeper dive into **Claude Science**, driven by today's product-demo transcript (path in
`memory/NEXT_SESSION.md`). Read the transcript first.

## Hard constraints (never lose)
- **NEW WORK ONLY** — every file authored during the event (started 2026-07-07); git history is the compliance proof.
- **Deadline: 2026-07-13, 9:00 PM ET.** Solo builder; async, interruptible.
- **Open source, MIT.** Claude for reasoning; Voyage for embeddings. Never OpenAI.
- **Every causal edge traces to a data receipt.** Calibrated language only. See `CLAUDE.md`.

## Key decisions (ADRs)
ADRs live in `memory/decisions/adr-NNN-*.md`. None recorded yet — record the load-bearing
build decisions here as they're made (embeddings provider, agent boundaries, verdict UX).
- [Hardware + Claude Science placement](memory/decisions/hardware-and-claude-science-placement.md) — RTX 3090 works in WSL; runtime on C:(SSD), bulk data on D:(HDD), G:/H: are cloud. `.wslconfig` raised 8→32 GB.
- [Hackathon track + facts](memory/decisions/hackathon-track-and-facts.md) — **track committed: RESEARCHER** (finding-first via Claude Science); prizes/deadline/rules from kickoff transcript; Claude Science now critical path.
- [LBD question-engine reframe](memory/decisions/lbd-question-engine-reframe.md) — **the strategic heart:** LBD *generates the questions* (fills the "rich dataset, no question" cold-start gap), Claude Science + data *answers* them. Spec: `docs/lbd-proposer-spec.md`.

## Recent Sessions
| Date | Focus | Key outcome |
|------|-------|-------------|
| 2026-07-07 | PM tooling + repo | Session-lifecycle skills + doc scaffold; handoff → `memory/NEXT_SESSION.md`; API key verified active; private repo `dayanjan/pyzobot-arbiter` created & pushed |
| 2026-07-07 (PM) | Claude Science + Validator | Researcher-track commit; Claude Science installed on WSL + driven via Playwright; QC/join-map + referee (Validator) built through it — YES/UNTESTED/REFUTED demonstrated with receipts; 6 artifacts in `docs/perturbseq-qc_2026-07-07/`; hardware fully characterized; 3-round codex-debate + independent Fable review on the install plan |
| 2026-07-08 | LBD proposer + finding (autonomous) | Spec hardened v1→v2 (3-round repo-read codex-debate, 9→3→0); fresh tool layer `src/arbiter/lbd/` (verified); disease ids MONDO-resolved; `referee_triple` exact-disease adapter; Codex consult fixed scoring+full-chain bug; full Stim8hr sweep 22,039→30 clean supported; **finding NAB2→Th1/Th2→atopic eczema** (near-novel, receipt-backed) |
| 2026-07-08 | Validation + source-paper vetting | 4-agent literature audit (new `src/arbiter/lit/`) → both links 0-papers novel; STAT6/EGR/cis confounders stress-tested & argued-against; **5-agent independent replication unanimous PASS** (`docs/replication/`); source-paper read → **reframed as novel reproducible NOMINATION, disease link flagged**; paper in `references/` + analysis repo recorded; ~8 commits |
| 2026-07-08 | Definitive STAT6 check + provenance (full-close) | Preserved full raw provenance trail (`docs/provenance/`, 52 artifacts); **definitive STAT6 cis-check** via lazy S3 read of authors' genome-wide DE → **NAB2-KD leaves STAT6 unmoved → cis/shadow EXCLUDED**, verdict upgraded to genuine novel NAB2-specific regulator; decided M5 = evidence-chain notebook + Claude Science chain + demo video |
| 2026-07-08 (M5, full-close) | **M5 shipped in full** | Evidence-chain **notebook**; **Claude Science evidence chain** (independent same verdict + figure); 3-screen Streamlit **"Researcher's Workbench"** app implementing a **Claude co-design** (imported via **DesignSync**), all screens preflight-green; **final demo video** (~112s, ElevenLabs "Brian" + CC-BY music, gate PASS 94%; recipe `docs/demo-video-pack/`). Two 3-round repo-read codex-debates (demo + workbench plans). Track → **"Researcher who also builds"**. Demo/app = fallback MVP |

_Last updated: 2026-07-08 18:02 (full-close)_
