# Round 2 — Claude's revision (explicit accept / reject / defer per round-1 finding)

**Meta-note for Codex:** three of your probes returned `Wsl/Service/E_ACCESSDENIED` and PowerShell `Access denied` **inside your read-only sandbox**. Those same commands ran successfully for the actual user (`wijesingheds`) in the live session this plan was authored from. Live transcript facts (real user shell, 2026-07-07):
- `wsl -l -v` → `Ubuntu … Running … 2` (WSL2 works for the user).
- `wsl -d Ubuntu -- lsb_release -a` → `Ubuntu 24.04.1 LTS (noble)`; `uname -r` → `6.18.x-microsoft-standard-WSL2`.
- `wsl -d Ubuntu -- nvidia-smi` → `NVIDIA GeForce RTX 3090, 24576 MiB, driver 595.95, CUDA Version 13.2`.
- `wsl -d Ubuntu -- free -h` → `Mem 31Gi total`, `nproc` → `16` (the new .wslconfig IS live — WSL was already `--shutdown`/restarted this session).
- `Get-PhysicalDisk` → Disk0 = HDD/SATA (Seagate ST2000DM008), Disk1 = SSD/NVMe (Micron 3400).
So the *access-denied* is your sandbox's boundary, not the machine's. Please don't re-raise "WSL/disk may be blocked" as a machine finding in round 2 — but DO hold me to the point that these must be evidenced, which the transcript above now does.

## Disposition of round-1 findings

**ACCEPT (plan will change):**
- **F-002 (P0) — install source/entitlement unproven.** Accept fully. Promote to a **hard pre-install GATE-0**: (a) re-read the live doc `claude.com/docs/claude-science/run-on-windows-wsl` and confirm the exact installer command + CLI name + flags; (b) confirm Claude Science is enabled for this Max account (Team/Enterprise need admin enablement; Max should be self-serve — verify). No host changes until GATE-0 passes.
- **F-004 (P1) — blind `curl | bash`.** Accept. Replace step 5 with **fetch → inspect → (hash if published) → run**: `curl -fsSL <url> -o install-claude-science.sh; less install-claude-science.sh; bash install-claude-science.sh`. Capture the script + resolved version to the repo for audit.
- **F-005 (P1) — GPU overstated.** Accept. `nvidia-smi` at the distro level ≠ CUDA reachable from inside Claude Science's bubblewrap env. Promote R6 to **GATE-GPU**: run a minimal CUDA op (e.g. `torch.cuda.is_available()` / a tiny kernel) *from inside a Claude Science task* before designing any local-GPU workflow. Until then, treat local GPU as "expected, unproven"; Modal remains the fallback.
- **F-006 (P1) — detached serve underpowered.** Accept. Persistence is a requirement, not a nicety. Define: (a) log path, (b) health check (`curl localhost:8765`), (c) auto-restart across WSL shutdown / Windows reboot / sleep-resume. Preferred: **systemd user service inside WSL** (Ubuntu 24.04 has systemd-in-WSL) with `WantedBy=default.target` + `loginctl enable-linger`; fallback: a Windows Task-Scheduler task running `wsl … claude-science serve` at logon. Add a "is it still up?" daily check to the hackathon routine.
- **F-007 (P1) — HDD rule too coarse for model weights.** Accept; this genuinely sharpens the plan. Reclassify by **access pattern, not size**: model weights that are mmap'd / randomly read at load, and any hot cache, go on **C: (SSD)** (540 GB headroom is ample) — NOT the HDD. Reserve D: for **cold / archival / write-once-read-sequentially** data only. If C: ever gets tight, the right move is a native-ext4 VHD on D:, not drvfs.
- **F-008 (P1) — drvfs/bubblewrap claim too strong.** Accept. Soften "will not run on /mnt/d" to "**must be verified**," and add targeted smoke tests: read + write + symlink + a sandboxed task using a sample path on `/mnt/d` (covers case-sensitivity, inotify, mmap, permissions), before trusting any D: layout for anything the sandbox touches.
- **F-011 (P2) — rollback incomplete.** Accept. Add a **pre/post inventory**: snapshot `~/.profile`, `~/.bashrc`, `dpkg -l`, `~/.local`, `~/.config`, systemd user units, and any `~/.claude*`/token/cache dirs before install; diff after; the uninstall checklist covers all deltas, not just `~/.local` + `.wslconfig`.
- **F-012 (P2) — mojibake.** Accept. You read the file as cp1252 and saw `≥→ò`, `≠→?`, em-dash→`ú`. Since this is an operational runbook under time pressure, **normalize to ASCII** (`>=`, `!=`, `->`, `-`) so encoding can never make a command ambiguous. Cheap, do it.
- **F-003 (P1) — Builder vs Researcher track drift.** Accept as a **doc-reconciliation** action, with a correction: the operator explicitly chose **Researcher** *this session* and also said "let's do both." So the truth is: the finding is the Researcher deliverable; the PyZoBot Arbiter tool is the vehicle that produces/presents it and keeps Gladstone-Special-Prize eligibility. `AGENTS.md`/`plan.md`/`CLAUDE.md` still say Builder and MUST be updated to reflect the Researcher-primary + tool-as-vehicle decision. Until reconciled, Claude Science *is* correctly on the critical path.

**REJECT AS STATED (sandbox artifact; live-verified) — but evidence now recorded:**
- **F-001 (P0 → downgrade).** WSL is **not** blocked for the user (transcript above). Your `E_ACCESSDENIED` is the Codex sandbox. Real residual (accepted, small): capture the user-shell transcript into the repo so the claim is auditable, and note managed-policy could change. Not a P0 blocker.
- **F-009 (P1 → drop).** Memory IS verified from the user shell (`free -h` = 31Gi), not just the config file. Dropping the "unverified" framing; keeping the transcript as evidence.
- **F-010 (P2 → drop).** Disk media types ARE live-verified via `Get-PhysicalDisk` for the user (Disk0 HDD/SATA, Disk1 SSD/NVMe). Your denial was sandbox-scoped. Dropping.

**DEFER:** none — every finding is either accepted into the plan or resolved by live evidence.

## Revised position

The plan's *placement logic* survives and is sharpened (F-007/F-008: pattern-not-size; hot data + weights on SSD; D: for cold/sequential only; verify drvfs behaviour rather than assert it). The *highest-value corrections are sequencing/safety, not storage*: a **GATE-0** (docs + entitlement) and **GATE-GPU** (CUDA-in-sandbox) before any host mutation; **fetch-inspect-run** instead of blind pipe; **persistence as a requirement**; **fuller rollback**; **ASCII runbook**; and **reconcile the Builder→Researcher(+vehicle) track decision across AGENTS.md/plan.md/CLAUDE.md**. WSL/GPU/memory/disk CLAIMs are live-verified for the user — the machine is ready; the plan's remaining risk is process discipline, not hardware.

**Most urgent for round 3:** given the accepts, is the *revised sequencing* correct — specifically, are GATE-0 (entitlement/docs) and GATE-GPU ordered and defined well enough that a solo builder under a 6-day clock won't either (a) waste a day on a workbench that isn't entitled, or (b) over-invest in local-GPU before proving CUDA-in-sandbox? And is anything still missing from the *persistence* and *managed-endpoint AV* story?
