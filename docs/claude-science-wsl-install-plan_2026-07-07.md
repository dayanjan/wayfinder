# Claude Science on WSL -- install & data-placement runbook (PHAR02325)

**Date:** 2026-07-07 | **Machine:** Alienware Aurora Ryzen R14 (PHAR02325), VCU-managed
**Status:** INSTALLED 2026-07-07 -- claude-science 0.1.16 running (daemon pid, port 8765, data dir
on ext4). Prereqs installed via `wsl -u root` (password bypassed). **SANDBOX SMOKE TEST PASSED**
(`SANDBOX_OK`) -- VCU endpoint does NOT block the sandbox; the big Day-1 de-risk is cleared.
**Only remaining step:** browser sign-in with the hackathon **Max** account (interactive). Install
audit: `memory/install-audit/claude-science_2026-07-07.md` (gitignored). Debate-hardened (3-round
Claude<->Codex, converged -- `docs/reviews/codex-debate_claude-science-wsl-install-plan_2026-07-07.md`).
**Encoding:** ASCII only (`>=`, `!=`, `->`) so no command is ever ambiguous under time pressure.

**Goal:** Install Anthropic **Claude Science** (beta) under WSL2, placed correctly for this
hardware, to support the **Researcher-track** hackathon deliverable (a reproducible T-cell
Perturb-seq finding derived *through Claude Science*). The PyZoBot Arbiter tool remains the
vehicle that produces/presents the finding and keeps Gladstone-Special-Prize eligibility.

> Execution is **gated**. Each GATE STOPs on failure -- do not proceed to the next until it
> passes. This ordering exists so a solo builder on a 6-day clock does not waste a day on an
> unentitled workbench, an ungated local-GPU assumption, or a managed-endpoint block.

> **TIMEBOX + EXIT.** Because the operator is committed to the **Researcher track**, Claude Science
> is REQUIRED -- there is no "drop it and use plain pandas" fallback. So the exit is NOT "abandon
> Claude Science"; it is **"escalate a managed-endpoint block hard and fast."** Timebox getting a
> real Claude Science task running to **~half a day**. If GATE-1/PREFLIGHT is blocked by VCU
> endpoint policy, STOP and escalate to VCU IT the same day (the block could take days to clear --
> discover it on Day 1, not Day 5), or move to a non-managed host. Everything past GATE-RUNTIME
> (persistence, GPU, tiering) is deferrable; getting ONE task to run is the Day-1 goal.

> **GATE-(-1) -- access path: RESOLVED 2026-07-07.** Claude Science is a LOCAL app that runs
> *inside* the WSL VM; Windows has no native build and there is NO purely-hosted web option, so a
> local WSL install is the only path. There is no hosted shortcut that would moot this runbook.

---

## 1. Verified system state (live user-shell transcript, 2026-07-07)

All confirmed for the real user `wijesingheds` this session (NOT assumed):

| Fact | Value | Verified by |
|---|---|---|
| WSL | WSL2, distro `Ubuntu` running | `wsl -l -v` |
| Distro | Ubuntu 24.04.1 LTS (noble); kernel 6.18 WSL2 | `lsb_release -a`, `uname -r` |
| Prereqs | bubblewrap + socat NOT yet installed (noble bubblewrap >= 0.8 OK); curl TBD | `bwrap --version` fails now |
| GPU (distro) | RTX 3090, 24576 MiB, driver 595.95, CUDA 13.2 | `nvidia-smi` in WSL |
| Memory | 31 GiB RAM, 16 GiB swap, 16 CPUs (new .wslconfig live) | `free -h`, `nproc` |
| Disks | C: = Micron 3400 NVMe **SSD** (~540 GB free); D: = Seagate ST2000DM008 SATA **HDD** (~1.86 TB free) | `Get-PhysicalDisk` |
| Excluded | G:/H: = Google Drive (cloud, protected); P: = VCU network | `phase0_environment.md` |

The machine is hardware-ready. The remaining risk is **process discipline + two genuinely
unproven items (entitlement, managed-endpoint), which are the FIRST gates.**

## 2. Pre-req already applied

`~/.wslconfig` raised from `memory=8GB` (the historical "insufficient memory") to
`memory=32GB, processors=16, swap=16GB, autoMemoryReclaim=gradual`. Backup at
`C:\Users\wijesingheds\.wslconfig.bak`. Applied via `wsl --shutdown` (done); `free -h` = 31 GiB.

---

## 3. GATE-0 -- Entitlement + docs (ZERO host changes) -- DONE (docs) 2026-07-07

1. **CONFIRMED against the live doc** `claude.com/docs/claude-science/run-on-windows-wsl`:
   installer = `curl -fsSL https://claude.ai/install-claude-science.sh | bash`; CLI = `claude-science`;
   launch = `claude-science serve --port 8765 --no-browser` (`--detached` exists; `claude-science url`
   reprints the sign-in token). Prereqs = Ubuntu 24.04+, bubblewrap >= 0.8, socat (all satisfied).
   Access path = LOCAL WSL only (see GATE-(-1)).
2. **OPERATOR CHECK (self-proves at sign-in):** the docs do not enumerate plans, but the launch
   announcement lists Pro/Max/Team/Enterprise, and the hackathon grants **20x Max** -- a qualifying
   plan. Entitlement is confirmed the moment sign-in succeeds at GATE-RUNTIME. Sign in with the
   **hackathon Max account**, not a personal free/Pro account.

**STOP if** sign-in is rejected (not entitled) -> resolve account/entitlement before proceeding.

## 4. PREFLIGHT -- Managed endpoint (VCU CrowdStrike / KACE / Defender)

1. **Download-only** fetch of the installer to a file -- do NOT execute yet. Confirm AV does not
   quarantine it.
2. Confirm WSL + the bubblewrap sandbox are not blocked by endpoint policy: run
   `wsl -d Ubuntu -- bash -lc 'bwrap --ro-bind / / --unshare-all echo ok'` (expect `ok`) AFTER
   GATE-1 installs bubblewrap -- if endpoint policy blocks user namespaces, this fails here.
3. Confirm `localhost:8765` is reachable from a Windows browser (no endpoint firewall block).
4. **If any step is blocked** -> escalation/fallback: request a managed-device policy exception,
   or move to an approved host. Resolve BEFORE sinking install time.

## 5. GATE-1 -- Safe install

```bash
# 5.1 Prereqs (Linux sudo password set at Ubuntu-user creation -- NOT Windows UAC;
#     the managed-machine pharexec/winget quirks do NOT apply inside WSL)
sudo apt update && sudo apt install -y curl bubblewrap socat

# 5.2 Fetch -> inspect -> record -> run (NOT a blind curl | bash)
curl -fsSL <VERIFIED-URL-FROM-GATE-0> -o install-claude-science.sh
less install-claude-science.sh                       # eyeball it
sha256sum install-claude-science.sh                  # record hash
#   -> append hash + source URL + timestamp + resolved version to the gitignored
#      memory/install-audit/ (only hash/URL/timestamp/version + a 1-line inspection
#      summary go into any tracked doc; never commit the raw installer)
bash install-claude-science.sh
. ~/.profile
claude-science --version                             # expect a version string
```

## 6. GATE-RUNTIME -- Serve + sign-in + a real task renders

1. Launch (persistence comes in section 7; for the first run a foreground serve is fine):
   `claude-science serve --port 8765 --no-browser` then open the printed `localhost:8765`
   URL in a **Windows** browser; sign in with the **Max** account.
2. Run a trivial Claude Science task that **renders an artifact with provenance** (code +
   environment attached). This proves the *product* runs, not just the CLI.
3. Sandbox smoke tests (settle the drvfs question by measurement, not assertion):
   - `bwrap --ro-bind / / --unshare-all echo ok` -> `ok`
   - Create `/mnt/d/claude-science/` and test **read + write + symlink + a sandboxed task**
     using a file there (covers case-sensitivity, inotify, mmap, permissions).

## 7. PERSISTENCE -- keep it simple (Fable trim: no gold-plating)

For a week you are ACTIVELY driving the tool, a **detached serve is sufficient** -- do NOT build a
systemd service + reboot-acceptance test (gold-plating that burns time for zero deliverable value):

```bash
claude-science serve --port 8765 --no-browser --detached
curl -fsS localhost:8765                 # health check
claude-science url                        # reprint sign-in URL if needed
```

Reality of the week: after any `wsl --shutdown` or Windows reboot, just re-run the one-line
`serve --detached`. That is a 5-second manual step you will do a handful of times, not a service to
engineer. ONLY escalate to a systemd user service (`~/.config/systemd/user/`, `Restart=on-failure`,
`loginctl enable-linger`) IF you find yourself restarting it constantly or need unattended
overnight runs -- deferred, not Day-1.

## 8. GATE-GPU -- CUDA-in-task (BEFORE any local-GPU workflow or model placement)

`nvidia-smi` at the distro level does NOT prove CUDA is reachable from inside Claude Science's
bubblewrap sandbox. From **inside a Claude Science task**, run a minimal CUDA op:

```python
import torch; print(torch.cuda.is_available(), torch.cuda.get_device_name(0))
```

- **PASS** -> the local RTX 3090 (24 GB) is usable; local folding/embedding/DL work is on the
  table and avoids Modal credit spend.
- **FAIL** (sandbox cannot see `/usr/lib/wsl/lib` / CUDA libs / device) -> local GPU is OUT;
  Modal is the path; do NOT place model weights for local use. Treat local GPU as
  "expected, unproven" until this gate passes.

## 9. PLACEMENT -- by access pattern, NOT by size

- **C: (SSD)** -> runtime + Ubuntu distro (already there) + hot cache + any model weights that
  are mmap'd / randomly read at load. 540 GB free is ample; the SSD is where random I/O belongs.
- **D: (HDD) via `/mnt/d`** -> cold / archival / write-once-read-sequentially data ONLY, and only
  after the section-6 `/mnt/d` smoke test passes. Large raw single-cell matrices (if ever pulled)
  live here.
- **This project's data** (Perturb-seq aggregated CSVs, ~25 MB) -> stays on C: with the repo.
- **If C: pressure appears** -> a **native-ext4 VHD on D:** mounted into WSL (`wsl --mount --vhd`),
  NOT drvfs. Do not put the runtime or sandboxed workloads on `/mnt/d`.

## 10. Rollback -- full (pre/post inventory)

Before install, snapshot: `~/.profile`, `~/.bashrc`, `dpkg -l`, `~/.local`, `~/.config`, systemd
user units, token/cache dirs. Diff after. Uninstall = restore `.wslconfig.bak` (+ `wsl --shutdown`);
`systemctl --user disable --now claude-science` + remove the unit; product uninstall per docs +
remove inventory deltas; delete the D: data dir. Nothing on D: is created before section 6.

## 11. Parallel (non-blocking) -- track reconciliation

The operator chose **Researcher-primary** this session (with "do both" = the Arbiter tool as the
vehicle). **DONE 2026-07-08:** `CLAUDE.md`, `AGENTS.md`, `docs/plan.md`, and `README.md` updated to
**Researcher — a researcher who also builds** (tool-as-vehicle + builder-craft as evidence of a
scientist who builds to get the science done; Gladstone-Special eligibility noted).

---

## Provenance

Hardened by a 3-round Claude<->Codex debate (2026-07-07), converged with 17/17 findings resolved,
0 escalated, 0 new at round 3. Per-round artifacts + synthesis under
`docs/reviews/codex-debate_claude-science-wsl-install-plan_2026-07-07/`.
Hardware facts: `../PHAR02325-Hardware-Software-FileManager/docs/hardware-reference.md`.
