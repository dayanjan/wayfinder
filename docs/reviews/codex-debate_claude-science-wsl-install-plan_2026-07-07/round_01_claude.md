# Round 1 — Claude's opening position

**Framing question:** Is this the correct, safe, and complete plan to install Claude Science on this exact hardware (Alienware Aurora R14, PHAR02325), with data placement optimal for the SSD/HDD/GPU topology — what is wrong, missing, or risky?

**Position:** The plan at `docs/claude-science-wsl-install-plan_2026-07-07.md` is a correct and near-complete install-and-placement plan. Its load-bearing claims:

1. **Requirements met.** Claude Science runs under WSL2 / Ubuntu 24.04.1 on this machine. Prereqs = curl + bubblewrap + socat (bubblewrap & socat not yet installed; noble ships bubblewrap ≥ 0.8, which satisfies the sandbox floor). WSL2, kernel 6.18, unprivileged userns default-on — all satisfied. Plan needs a Pro/Max/Team/Enterprise account (the hackathon 20x Max grant covers this).

2. **Placement is dictated by topology.** Exactly one fast disk (C: NVMe, ~540 GB free) and one HDD (D: SATA, ~1.86 TB free). Therefore the runtime + Ubuntu distro **must** live on C: (SSD): the ~5 GB base is small-file random I/O and the bubblewrap sandbox will not run from `/mnt/d` (drvfs). Bulk/cold scientific data → D: (HDD) via `/mnt/d` (sequential reads, cheap capacity). This project's 25 MB CSVs stay on C:. G:/H: are Google Drive (cloud-synced, excluded).

3. **GPU is a local asset.** RTX 3090 (24 GB, CUDA 13.2) confirmed usable inside WSL2 → local GPU compute avoids Modal credit spend for the Researcher track (folding/embedding/DL models).

4. **Memory pre-fixed.** `~/.wslconfig` raised 8 → 32 GB (the historical "insufficient memory"), backup kept at `.wslconfig.bak`.

5. **Install path.** apt prereqs (Linux `sudo`, not Windows UAC), `curl … | bash` installer (URL to be re-verified vs the live doc), launch `serve --detached` (terminal-crash-safe), browser sign-in with Max.

The plan flags six risks (R1–R6) and four open questions (runtime size-cap on C:, `/mnt/d` vs a native-ext4 VHD on D: for bulk data, `--detached` vs a systemd user service, managed-machine AV interference).

**What I want settled:** whether the placement logic is sound, whether any step is unsafe or missing, and which open questions matter enough to resolve *before* install. I accept the plan is not yet execution-proven; I want the highest-value corrections — especially anything that would waste the hackathon week or silently break the sandbox/GPU path.
