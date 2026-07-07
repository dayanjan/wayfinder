# Round 3 — Claude's final consolidated position

All five round-2 findings ACCEPTED. The eight escalations (F-002/004/005/006/007/008/011/012) are accepted precisely as escalated: they are not "done" until the runbook is regenerated, so F-014 is the meta-fix that resolves the rest. Below is the **final runbook shape** the regenerated document will take — critique the end-state, not the promise.

## Accept F-013..F-017
- **F-013 (gate ordering):** accept — gates are now phased and dependency-correct (below).
- **F-014 (stale artifact):** accept — the doc will be regenerated so every accepted fix appears in the actual numbered steps/validation/rollback; the current artifact is treated as superseded.
- **F-015 (managed-endpoint preflight):** accept — concrete preflight added.
- **F-016 (persistence service contract):** accept — full unit spec + reboot acceptance test added.
- **F-017 (audit hygiene):** accept — installer material to gitignored `memory/install-audit/`; only hash/URL/timestamp/version/inspection-summary in tracked docs.

## Final runbook — phased gates (each gate STOPs on failure)

**GATE-0 — Entitlement + docs (zero host changes).** Re-read live `claude.com/docs/claude-science/run-on-windows-wsl`; confirm exact installer command, CLI name, flags. Confirm Claude Science is enabled for THIS Max account (self-serve for Max; verify). STOP if not entitled or docs diverge from the plan.

**PREFLIGHT — Managed endpoint (VCU CrowdStrike/KACE/Defender).** (a) download-only fetch of the installer (no exec) — confirm it isn't quarantined; (b) confirm WSL process + bubblewrap sandbox aren't blocked by endpoint policy (run the `bwrap … echo ok` test first); (c) confirm `localhost:8765` is allowed; (d) if anything is blocked → escalation/fallback path (request policy exception, or use an approved host) BEFORE sinking install time.

**GATE-1 — Safe install.** `sudo apt update && sudo apt install -y curl bubblewrap socat` (Linux sudo). Then **fetch-inspect-run**: `curl -fsSL <verified-url> -o install-claude-science.sh`; `less install-claude-science.sh`; record `sha256sum` + URL + timestamp + resolved version to gitignored `memory/install-audit/`; `bash install-claude-science.sh`; `. ~/.profile`; `claude-science --version`.

**GATE-RUNTIME — Serve + sign-in + task works.** Launch serve; browser sign-in with Max; run a trivial Claude Science task that renders an artifact with provenance (proves the product actually runs, not just the CLI). Run sandbox smoke tests: `bwrap --ro-bind / / --unshare-all echo ok` AND a `/mnt/d` read+write+symlink+sandboxed-task test (settles F-008 by measurement, not assertion).

**PERSISTENCE — service contract (F-016).** systemd **user** service (`~/.config/systemd/user/claude-science.service`):
```ini
[Service]
ExecStart=%h/.local/bin/claude-science serve --port 8765 --no-browser
Restart=on-failure
RestartSec=5
[Install]
WantedBy=default.target
```
`systemctl --user enable --now claude-science`; `loginctl enable-linger wijesingheds` (survives logout); logs via `journalctl --user -u claude-science`; health check `curl -fsS localhost:8765`. **Acceptance test:** service auto-recovers after `wsl --shutdown` AND a full Windows reboot. Fallback if systemd-in-WSL misbehaves: Windows Task Scheduler at logon → `wsl -d Ubuntu -- systemctl --user start claude-science`.

**GATE-GPU — CUDA-in-task, gated BEFORE any local-GPU workflow or model placement (F-005/F-013).** From *inside a Claude Science task*: `python -c "import torch; print(torch.cuda.is_available(), torch.cuda.get_device_name(0))"` (or equivalent). PASS → local RTX 3090 is usable; FAIL (bubblewrap can't see `/usr/lib/wsl/lib`/CUDA libs) → local GPU is OUT, Modal is the path, and no model weights are placed for local use.

**PLACEMENT — pattern-not-size (F-007/F-008).** Runtime + hot cache + mmap'd/randomly-read model weights → **C: (SSD)** (540 GB headroom). Cold / archival / write-once-read-sequentially data → **D: (HDD) via `/mnt/d`**, and only after the `/mnt/d` smoke test passes. This project's 25 MB CSVs → C:. If C: pressure ever appears, a **native-ext4 VHD on D:** (not drvfs) is the escalation.

**ROLLBACK — full (F-011).** Pre/post inventory diff of `~/.profile`, `~/.bashrc`, `dpkg -l`, `~/.local`, `~/.config`, systemd user units, token/cache dirs. Uninstall = restore `.wslconfig.bak`; `systemctl --user disable --now claude-science` + remove unit; product uninstall per docs + remove inventory deltas; delete D: data dir.

**DOC HYGIENE.** Runbook regenerated in **ASCII** (`>=`, `!=`, `->`) — F-012. Track reconciliation (parallel, non-blocking): update `AGENTS.md`/`plan.md`/`CLAUDE.md` to **Researcher-primary + PyZoBot Arbiter as the vehicle + Gladstone-Special eligibility** (F-003).

## Position summary
The machine is verified-ready (WSL2/Ubuntu 24.04.1/RTX 3090+CUDA 13.2/31 GiB/SSD+HDD — live user transcript). The plan's real risk was never hardware or storage micro-optimization; it was **process discipline**: gated sequencing so a solo builder doesn't waste a hackathon day on an unentitled workbench or an ungated local-GPU assumption, safe install on a managed endpoint, and real persistence. Those are now specified. **Residual open item honestly flagged:** GATE-0 (entitlement) and the managed-endpoint preflight are genuinely unproven until run — they are the first actions, by design.

**For your final critique:** is this phased sequence complete and correctly ordered, or is there still a gap that would bite a solo builder under a 6-day clock?
