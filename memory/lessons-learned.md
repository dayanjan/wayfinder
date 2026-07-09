# Lessons Learned — PyZoBot Arbiter

Append-only. What worked / what to improve about the scaffolding, skills, workflows.
`session-closer` prompts for entries at close; this flows back to the generator template.

---
<!-- entries appended below, newest last, each with: date, category, detail -->

## 2026-07-07 — Claude Science stood up + driven headlessly; referee (Validator) built

### Claude Science access & install model (Windows)
- **UI-only; NO headless task CLI.** The `claude-science` CLI is lifecycle only (serve / open / url / status / logs / stop / update / import). Submitting tasks, approving code, and reading output ALL happen in the web UI → to automate, browser automation is the only path.
- **Windows = WSL-only, local app.** It runs INSIDE the WSL VM (data dir `~/.claude-science`, ext4); no native Windows build and no purely-hosted web option. Installer `curl -fsSL https://claude.ai/install-claude-science.sh | bash` → `~/.local/bin/claude-science` (158 MB, v0.1.16). Prereqs: Ubuntu 24.04+, bubblewrap >=0.8, socat. Runs on Opus 4.8; has an internal Sonnet-5 reviewer agent.
- **Entitlement self-proves at sign-in.** Docs don't list plans; the hackathon **Max** grant IS entitled (sign-in succeeded). Sign-in is the entitlement gate.
- **Sandbox works on the VCU-managed machine** — `bwrap --unshare-all` -> SANDBOX_OK. The endpoint does NOT block user-namespace sandboxing (the big Day-1 de-risk). CrowdStrike/KACE/Defender didn't interfere with `curl|bash` or the sandbox.

### WSL / machine operational gotchas (each cost real time today)
- **Backgrounded `sudo` in WSL hangs** (no tty for the password). Fix: `wsl -d Ubuntu -u root -- bash -lc 'apt-get install ...'` bypasses sudo entirely (root needs no password) — no interactive terminal. This unblocked the whole install after the operator hit the password wall. → Written up as a **standalone, paste-only, no-Linux-knowledge install guide for Windows scientists**: `docs/INSTALL-claude-science-on-windows.md` (most target scientists have Windows + zero Ubuntu experience — this is a real accessibility asset, potentially part of the submission).
- **`.wslconfig memory=8GB` was the "insufficient memory"** the operator remembered → raised to 32 GB (machine = 64 GB, 32 cores, RTX 3090 24 GB with CUDA 13.2 working in WSL). Applies only after `wsl --shutdown` (also stops Docker). Backup at `.wslconfig.bak`.
- **MSYS/Git Bash mangles spaced `/mnt/c` paths** passed to `wsl ... bash -lc`; a spaced Windows path assigned to a shell var inside `bash -lc` came back EMPTY repeatedly. Fixes: (a) `MSYS_NO_PATHCONV=1`; (b) BEST — do file ops from the Windows side via the `//wsl.localhost/Ubuntu/...` UNC path (copied artifacts cleanly); (c) inline the path, don't stash it in a var.
- **Windows Python can't read `/c/...` MSYS paths** — use `C:/...`.
- **Stage data into WSL ext4** (`~/pyzobot-data/`) for clean native Claude Science access, NOT `/mnt/c` (drvfs + spaces). Artifacts land as plain files under `~/.claude-science/orgs/<org>/workspaces/<ws>/`.
- **`claude-science logs --tail` follows/blocks** — don't run it expecting a return.

### Claude Science agent behavior
- **With no data uploaded it WANDERS** — it launched a generic breast-cancer demo instead of asking. Point it at data explicitly; stop + redirect works.
- **Self-recovers** from kernel resets and transient "Connection issue — retrying…" (daemon<->API) blips — but a blip can leave a turn idle; re-check rather than assume it's done.
- **Reproducible provenance-tracked artifacts** (code + env + history per output) = the Researcher-track "others can reproduce" evidence, for free.

### Strategic / product
- **Track committed: Researcher** -> Claude Science is critical path (no pandas fallback). See [[hackathon-track-and-facts]].
- **Referee (Validator) WORKS — P0 money-shot loop achieved Day 1.** 3-hop chain + knockdown-QC gate as HOP 0. Demonstrated with real receipts: **EGR2 = receipt-backed YES** (asthma OR 20.4, FDR 5e-5); **IL2 @ Rest = the UNTESTED artifact-catch** (barely expressed -> nothing to knock down -> not "no effect"); **SLC1A5 = receipt-backed REFUTED** (in 9 disease gene-sets but none FDR<0.05). Artifacts in `docs/perturbseq-qc_2026-07-07/`.
- **Caveat:** demo genes were AUTO-PICKED by the agent, not operator-vetted anchors — vet the biology + lock the two anchors (known-true + non-obvious) per plan §8. `pyzobot_referee.py` is a Claude-Science draft — read before trusting/promoting to `src/`.

### Process
- **The 3-round codex-debate on the install plan converged (17/17) but its FRAME was too narrow** — it optimized "how to install," never "whether / opportunity cost / track fit." The independent **Fable 5** review caught exactly that (plus systemd over-engineering + missing timebox/exit). Lesson: pair an execution-safety debate with an independent frame-challenging review; convergence inside a narrow frame is not the right call. See [[hardware-and-claude-science-placement]].

## 2026-07-08 — Playbook: multi-model adversarial replication + external-data validation loop

**Category:** finding-validation workflow (reusable across any high-stakes finding — grant, paper, submission).

**The pattern (what to do when a computational finding must survive scrutiny).** After you HAVE a
finding, do not self-check — run it through an escalating gauntlet where each stage is independent of
your own code and biased toward *falsification*:

1. **Independent literature audit (multi-agent).** Fan out N cold agents over a real literature corpus
   (built with a direct multi-source tool — Europe PMC + OpenAlex + Semantic Scholar) to answer "is this
   actually novel, and what's known?" One agent per facet; a disease/immunology agent tasked to judge
   novelty. Surfaced the STAT6-adjacency confounder we hadn't seen.
2. **In-data confounder checks (reproducible scripts).** For every confounder the audit raises, write a
   committed check script that tests it against your own tables. Each becomes provenance.
3. **N-agent ADVERSARIAL replication (the core).** Stand up an independent "lab": **cross-model** (Opus
   AND Codex — a bug both model families miss is rarer than one either misses), against a **frozen claim
   set** (exact numbers to reproduce), with an **adversarial mandate** ("a refuted claim with evidence is
   the most valuable output"), and **≥2 clean-room re-implementations** that import NONE of your code (a
   match is then genuine reproduction, not shared-code tautology). Run them blind/parallel — two agents
   independently finding the SAME bug is corroboration, not an echo.
4. **Source-paper read for METHOD provenance.** Have an agent read the dataset's own paper to learn HOW
   the load-bearing quantities were computed (here: disease labels = Open Targets GWAS-genetic evidence,
   no LD/coloc control) — this reframes which caveats are real and how to frame the claim (nomination vs
   causal, matching the authors' own stance).
5. **Close the last confounder with the AUTHORS' OWN deposited data.** When your in-house data can't
   settle a confounder, the original paper's deposited processed data usually can. Public repos (found via
   the GitHub README's "Data pointers") often expose it on a no-creds S3 bucket → **lazy partial read**
   (h5py+s3fs, anon) of one slice of a 16.8 GB file — no mega-download. Checking a finding against the
   source authors' gold-standard data is the strongest external validation available.
6. **Preserve the full raw provenance trail.** Commit the verbatim agent prompts + run-logs + scripts
   (the raw trace is the proof the work happened); strip third-party copyrighted text (abstracts →
   metadata only); secret-scan (values + patterns) before commit.

**Why it works.** Cross-model + clean-room independence makes reproduction meaningful; the adversarial
mandate makes agents *find real errors* instead of rubber-stamping; external gold-standard data closes
what in-house data cannot; full provenance makes every number auditable back to the run that produced it.

**Empirical result this session (NAB2 finding).** 5-agent replication returned **unanimous PASS** and
caught real errors a self-review missed (a cluster-ID misalignment found independently by TWO agents; an
"8×" stat that was effect-size not z; arguments defended with their weakest legs). The literature audit
surfaced the STAT6 confounder; the source-paper read located it precisely (GWAS-genetic disease labels,
no LD control); and the definitive check against the **authors' deposited genome-wide DE** moved the
STAT6 cis/shadow confounder from "flagged" to **DEFINITIVELY EXCLUDED** (NAB2 knockdown leaves STAT6
unmoved: log2FC +0.09, p 0.79). Net: a finding that survives this gauntlet is submission-grade.

**When to reach for it.** Any finding that will face expert scrutiny. Scale the agent count / round count
to the stakes. The cross-model + clean-room + adversarial + external-data combination is the load-bearing
part; the single-model self-check is what it replaces.

**Reusable assets built this session:** `src/arbiter/lit/` (multi-source lit search), the frozen-protocol
replication harness (`docs/replication/agent-prompts/00_shared_protocol.md`), and the lazy-S3-h5ad read
recipe (`docs/nab2_stat6_definitive_check.py`). Full record: `docs/replication/`, `docs/provenance/`.

---

## 2026-07-08 — Two reusable end-to-end workflows validated: Claude co-design → app (DesignSync), and the demo-video pipeline
*Category: workflow / tooling (flows to generator template)*

### A. DesignSync: Claude co-design → a real, honest app
**The loop that worked.** (1) Write a **self-contained** design brief (no repo jargon; include the real
example data values so the designer mocks accurate components) — `docs/plans/streamlit_design_brief_*.md`
is the template. (2) Operator runs it through **Claude co-design** (claude.ai/design); it asks a few
calibration questions (theme, accent, typography, layout, animation) — answer them consistent with the
plan. (3) Pull the design file into the session with the **DesignSync** tool: `/design-login` once
(needed even on an API-key session), then `get_project` → `list_files` → `get_file` on the `.dc.html`.
(4) **Implement it as the real app** — the co-design file ships with MOCK data; the win is wiring every
value to the real backend function (here `referee_triple`) so nothing is hardcoded. (5) Verify
screen-only with a Playwright smoke before trusting it.

**Why it's good.** The designer produces a cohesive, attractive system (colors/typography/components in
all states) far faster + better than hand-CSS; the engineer's job collapses to translation + real-data
wiring + a preflight. Demarcate a **Tier-1 MVP** in the brief so co-design invests in the hero component
first (here the Receipt Chain), everything else as "the frame."

**Gotchas.** DesignSync needs `/design-login`. Streamlit's `st.dataframe` is a **canvas** grid — row
clicks are NOT reliably screen-only-drivable; use a DOM `selectbox`+`button` for click-through. `arbiter`
wasn't installable → the app inserts `src/` on `sys.path` at startup.

### B. The demo-video pipeline (two-stage economy) end-to-end
**The flow.** `~/.claude/skills/demo-video/` harness + a 3-file pack (`demo.config`/`narration`/`scenes`).
Author narration FIRST (calibrated, falsification-first), then: **grep-gate → edge-tts DRAFT → record →
assemble → stitch → transcription gate PASS → operator review → flip TTS to ElevenLabs → RE-RUN the whole
pipeline → music mux**. Draft-in-cheap-edge-then-upgrade is the point: you never spend ElevenLabs on a
cut that might be re-cut.

**Load-bearing details.** (1) **No-auth app:** set the actor `user: ""` → the harness skips login; the
scene navigates to BASE itself. (2) **TTS-first pacing means a voice swap requires a RE-RECORD** — the
scenes are paced to the measured audio durations, so ElevenLabs durations ≠ edge → re-run `--stage=all`,
don't just re-tts+re-assemble. (3) **Music mux:** loop the track, `volume=-20dB` + fades, and
`amix ... normalize=0` so the **voice stays at full**; then **re-run the transcription gate on the music
version** — if coverage holds (held at 94% here) the bed provably doesn't drown the narration. (4) CC-BY
music (Kevin MacLeod / incompetech) is directly `curl`-able and license-clean; record attribution.

**Gotcha.** Backgrounding `node ... &` INSIDE a `run_in_background` Bash call double-detaches → the
harness reports "completed" prematurely while node runs on; **poll the log to true end** (look for the
gate `RESULT:`), don't trust the early notification.

**Assets:** `docs/demo-video-pack/` (the reproducible recipe), `app/DESIGN_SOURCE.md`,
`docs/plans/streamlit_workbench_plan_2026-07-08.md` + the two codex-debate records.

---

## 2026-07-08 — Claude Science capability audit: mine the demo, then VERIFY-FROM-DB (not UI)
*Category: research method / Claude Science knowledge (reusable for any CS-capability question)*

**What we did (overnight, autonomous).** (1) A 5-agent parallel pass over the 2026-07-08 CS product-demo
transcript → a `[DEMO]` capability catalog with a testable inventory (`docs/claude-science-demo-findings_2026-07-08.md`).
(2) A 2-round repo-read codex-debate turned that inventory into an executable test plan
(`docs/claude-science-test-plan_2026-07-08.md`). (3) Drove our own CS install headlessly and verified
each capability empirically (`docs/cs-capability-tests_2026-07-08/RESULTS.md`).

**THE load-bearing discovery — `operon-cli.db` is CS's readable receipt store.**
`~/.claude-science/orgs/<org>/operon-cli.db` (SQLite) opens read-only even while the daemon runs
(`file:<db>?mode=ro&immutable=1`; no `sqlite3` CLI in the image → use WSL `python3`). It records
EVERYTHING: `host_call_log` (every `host.*` call), `execution_log` (source/kernel_id/language/files),
`artifact_versions` (+ `extracted_code` repro block, `artifact_dependencies` graph), **`verification_checks`
(the Reviewer's findings, with `reviewer_model`)**, and `frames` (per-frame model/effort/tokens/cost).
**Method: drive CS with Playwright only to make it DO the work; verify from the DB + workspace files —
never scrape the UI** (doctrine §19; the scraped text tail is unreliable and the Reviewer/provenance are
UI-only). This makes reviewer + provenance capabilities verifiable with zero UI scraping.

**Empirically confirmed on our install (all DB- + artifact-verified):**
- **Actor-critic is real & on-thesis:** primary **OPERON = claude-opus-4-8 (effort high)**; **Reviewer =
  claude-sonnet-5**, forked as **3 checkpoint frames**; it **reads saved artifacts** and **caught a
  planted 4-vs-5 persona count inconsistency as a FAIL** (+ a WARN on a method substitution). This IS our
  referee/falsification thesis, validated by an independent product.
- **Real `host` SDK:** `host.llm_batch(...)` (inline cheap-model sampling — model **claude-haiku-4-5**),
  `host.mcp("<connector>","<tool>",{args})` (batched MCP/DB lookup — 5 genes in ONE call, MyGene-backed,
  returned **correct real Ensembl IDs**), `host.delegate(...)`, `host.artifacts/artifact_path`.
- **`host.delegate` is GATED** behind a session **Delegation ("ultra mode") toggle**, OFF by default in a
  driver-created project → agent falls back to `host.llm_batch`. To test true sub-agent delegation we must
  enable delegation (not exposed by the current headless driver).
- **Persistent kernel reuse, Python↔R interop** (separate processes, **CSV handoff**, real ggplot2),
  **figure self-sight self-correction** (z>3 outlier caught + v2) — all PASS.
- **Cost datapoint:** an ~8-min combined audit ≈ **$3.17** (Opus $2.08 + 3 Sonnet reviewers ~$1.05);
  OPERON input = 1.55M tokens (cache/folding). **The reviewer roughly doubles model spend.**
- **Async gotchas (matter for any CS automation):** the driver's "DONE" (Stop button gone) ≠ receipts
  landed — the **Reviewer commits findings ~10 min later**, and the **`extracted_code` repro block is
  deferred to frame/session completion** (didn't backfill for a headlessly-driven run; the OPERON frame
  stays `processing`). Poll `verification_checks`/`frames.status` after the run; immutable versioning +
  dependency graph ARE immediate.

**Driver hardening applied + live-validated** (`~/.claude/skills/drive-claude-science/cs-drive.js`):
broadened `APPROVE`/`PENDING` for the MCP-use / usage-velocity / snooze / network-domain cards revealed by
the demo; **deliberately never auto-clicks "Allow globally."** Auto-approved cleanly with no misfire.

**Reusable assets:** `docs/claude-science-{demo-findings,test-plan}_2026-07-08.md`,
`docs/cs-capability-tests_2026-07-08/` (RESULTS + extracted artifacts), and the DB verifier
`.claude/scratch/cs-capability-mining/verify_cs_capabilities.py` (promote to a real tool if we keep using it).

## 2026-07-09 — Tracer-first + repo-read-debate is a strong plan-hardening workflow
*Category: workflow (reusable for any "port an external result into a new tool" effort)*

De-risk a big rebuild by (1) a TRACER: drive the target tool to reproduce ONE known result end-to-end from
raw inputs, verified against known numbers (here CS re-derived the NAB2 receipt digit-for-digit + the IL2
untested hero catch, from raw tables, writing its own code) — this proves the substrate, connectors, and
verification path before any scale-up. Then (2) write the full plan and harden it with a **repo-read
codex-debate** (`-s read-only`, from the repo, Codex told it may open files to verify): findings arrive
repo-verified so acceptance is cheap and it converges fast (11→8→0 → SHIP). The debate's own accept/reject
log + per-round snapshots (`docs/reviews/codex-debate_*/`) are the audit trail. Net: the plan is executable
by a weaker model next session without re-derivation, and every claim is checked against reality first.
Pairs with the drive-CS-then-verify-from-`operon-cli.db` discipline (never UI-scrape).
