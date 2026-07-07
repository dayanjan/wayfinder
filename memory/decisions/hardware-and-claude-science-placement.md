---
name: hardware-and-claude-science-placement
description: PHAR02325 hardware facts + where Claude Science / WSL data must live (SSD vs HDD vs cloud) and that the RTX 3090 works in WSL
metadata:
  type: project
---

Machine = **Alienware Aurora Ryzen R14 (PHAR02325)**, VCU-managed. Authoritative hardware doc:
`../PHAR02325-Hardware-Software-FileManager/docs/hardware-reference.md` + `phase0_environment.md`.
Verify before trusting across time gaps.

**Component facts (2026-07-07 cross-checked live):**
- CPU: Ryzen 9 5950X, 16C/32T (maxed; no upgrade).
- RAM: 64 GB (2×32 Kingston DDR4) @ 2667 MT/s (rated 3200, DOCP off — ~17% bandwidth left, BIOS-gated). 2 free DIMM slots (max 128 GB).
- GPU: **RTX 3090, 24 GB VRAM. CUDA 13.2 confirmed working INSIDE WSL2** (`nvidia-smi` OK, driver 595.95) — Claude Science can run folding/embedding/DL models LOCALLY instead of paying Modal GPU credits.
- **Storage topology (the load-bearing fact):**
  - **C: = NVMe SSD** (Micron 3400 Gen4), ~540 GB free, 97% health. The ONLY fast disk; single M.2 slot (filled).
  - **D: = SATA HDD** (Seagate Barracuda 2 TB), ~1.86 TB free, near-empty. Slow random I/O, fine sequential.
  - **G:/H: = Google Drive** mounts (cloud-synced, PROTECTED) — NOT storage candidates. P: = VCU network. OneDrive = cloud.

**Claude Science placement decisions:**
- **Runtime + Ubuntu distro → C: (SSD).** Small-file random I/O + bubblewrap sandbox demand SSD; sandbox won't run on `/mnt/d` (drvfs). Do NOT move the distro to D: (HDD would cripple it). ~5 GB fits easily in 540 GB free.
- **Bulk/cold scientific data (large raw matrices, model weights, tens-of-GB downloads) → D: (HDD) via `/mnt/d`.** Sequential reads, cheap capacity, keeps SSD free. Data files aren't executed so the sandbox caveat doesn't apply to them.
- This project's actual data (Perturb-seq aggregated CSVs, ~25 MB) is tiny → lives fine on C: with the repo; D: only needed if large raw data gets pulled.

**WSL config:** `.wslconfig` was `memory=8GB` (the "insufficient memory" the operator remembered) → raised to `memory=32GB, processors=16, swap=16GB, autoMemoryReclaim=gradual` (2026-07-07; backup at `.wslconfig.bak`). Ubuntu 24.04.1, WSL2, kernel 6.18 — meets Claude Science reqs (bubblewrap ≥0.8).

**Managed-machine caveats:** Windows elevates to `pharexec`/SYSTEM (broken winget) — but this does NOT affect WSL-internal `sudo apt` (that's a Linux password set at Ubuntu-user creation). Windows Terminal has a rare crash bug (microsoft/terminal#19231) → run `claude-science serve` detached so a terminal crash can't kill it. See [[hackathon-track-and-facts]].
