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
