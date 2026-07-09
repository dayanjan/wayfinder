# NEXT_SESSION — async handoff (canonical; written/read by session-closer & session-start)

## Next session priorities — written 2026-07-08 (overnight CS capability deep-dive, autonomous)

**Current state**: **M5 still complete** (notebook + CS evidence chain + Streamlit app + demo video).
On top of that, this overnight session did the **Claude Science capability deep-dive** the prior handoff
asked for — mined the 2026-07-08 CS demo, brainstormed tests with Codex (2-round repo-read debate), and
**empirically verified CS capabilities live against our own install**. All findings are receipt-backed
from CS's own audit DB. Tree has new docs + a hardened driver; **not yet committed** (see below).

**What we now KNOW about Claude Science (read these first):**
- `docs/cs-capability-tests_2026-07-08/RESULTS.md` — the empirical scorecard (start here).
- `docs/claude-science-test-plan_2026-07-08.md` — the method + the **`operon-cli.db` receipt-store** map.
- `docs/claude-science-demo-findings_2026-07-08.md` — the mined `[DEMO]` catalog (host SDK, folding
  compaction, reviewer/specialists/memory mechanics, roadmap, Q&A).
- `memory/lessons-learned.md` (2026-07-08 CS entry) — the reusable playbook.

**Headline findings that shape tomorrow:**
1. **CS's own Reviewer (Sonnet 5) is our thesis, live** — it forks at checkpoints, reads the saved
   artifacts, and **caught a planted count inconsistency as a FAIL**. Opus-4.8 primary + Sonnet-5 reviewer.
2. **`host.mcp(connector,tool,{args})` does batched deterministic DB lookups returning REAL Ensembl IDs**
   (one call for 5 genes, MyGene-backed) — CS can fetch our referee's receipts natively.
3. **`operon-cli.db`** is a fully-readable audit/receipt store → drive CS with Playwright, **verify from the
   DB**, never scrape the UI.
4. **`host.delegate` is gated** behind a session Delegation toggle (off by default) → to run a multi-agent
   referee *inside* CS we must enable delegation.

**Next action — decide how to EXPLOIT Claude Science for the finding/product (the whole point):**
1. **Referee-inside-CS tracer.** Rebuild a slice of our 3-hop referee natively in CS: `host.mcp` for the
   receipt lookups + `host.llm_batch`/delegation for the Skeptic/Adjudicator, with CS's Reviewer auditing
   it — then pull the whole receipt chain from `operon-cli.db`. Strongest "researcher who builds their
   instrument in the actual workbench" story. **[HYBRID]** (Claude designs; drive CS; verify-from-DB). First
   enable the **Delegation toggle** (needs a driver/UI step — small spike).
2. **Use CS's Reviewer as an independent corroboration of the NAB2 finding.** Feed the evidence chain in and
   let its Sonnet-5 reviewer adversarially audit our claims → another independent falsification pass, on
   the record. **[CLAUDE]** drive + capture `verification_checks`.
3. **Deepen the science with CS** — a new CS-driven analysis (e.g. the STAT6/cis question or a fresh LBD
   question) run end-to-end with the drive-then-verify-from-DB harness. **[HYBRID]**.
4. **Promote the tooling**: turn `verify_cs_capabilities.py` + the DB-read recipe into a small committed
   `src/` tool; extend `cs-drive.js` to toggle Delegation + open provenance if we want UI-side too. **[CODEX-RESCUE]**.

**Prerequisites / gotchas**: CS daemon up on **:8765** (was ~30h uptime). Auth state saved at
`~/.claude/skills/drive-claude-science/cs_state.json` (driver re-mints a nonce if needed). **Async:** after a
driven run, the **Reviewer commits findings ~10 min later** and the **`extracted_code` repro block is
deferred to frame completion** — poll `operon-cli.db` / `frames.status`, don't trust the driver's "DONE".
Read the DB via WSL `python3` (no `sqlite3` CLI). Two OPERON frames from tonight may still show `processing`.

**UNCOMMITTED — commit at session start:** new docs (`docs/claude-science-demo-findings_*`,
`docs/claude-science-test-plan_*`, `docs/cs-capability-tests_2026-07-08/`), edited
`docs/claude-science-capabilities.md`, `memory/lessons-learned.md`, this handoff, MEMORY.md,
WORK_PROGRESS.md. Scratch (`.claude/scratch/cs-capability-mining/`) is gitignored — the raw pass notes +
codex logs + probe scripts live there if needed. **Also commit the hardened `cs-drive.js` to `~/.claude`**
(separate repo; run the pre-push secret-grep).

**Do not touch**: never commit `.env`, `data/*.csv`, `data/lbd_*`, `references/*.pdf`, `.claude/scratch/`,
`.tmp/`. The CS store `~/.claude-science/` is CS's private data, not ours to commit (we copy only the
audit artifacts we produced into `docs/cs-capability-tests_2026-07-08/artifacts*`).

**Context to preload**: the four docs above; `WORK_PROGRESS.md`; `MEMORY.md`;
`~/.claude/skills/drive-claude-science/` (SKILL.md + cs-drive.js).

**Estimated budget**: ~0.5–1 day (pick one exploit path; the referee-inside-CS tracer is the highest-value).
