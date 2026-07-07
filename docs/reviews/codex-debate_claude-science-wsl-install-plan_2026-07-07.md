# Codex Debate synthesis -- Claude Science WSL install plan

**Date:** 2026-07-07 | **Rounds:** 3 (converged at 3) | **Model:** Codex (codex-cli 0.141.0), read-only
**Artifact:** `docs/claude-science-wsl-install-plan_2026-07-07.md` (regenerated post-debate)
**Framing question:** Is this the correct, safe, and complete plan to install Claude Science on
this exact hardware, with data placement optimal for the SSD/HDD/GPU topology -- what is wrong,
missing, or risky?

## Outcome

Converged cleanly at round 3: **17/17 findings resolved, 0 escalated, 0 new.** No
convergence-sanding (this is an operational runbook, no novel claims to protect). The plan was
regenerated so every accepted fix appears in the actual numbered steps (this was itself finding
F-014).

## Trajectory

- **Round 1 (12 findings).** Codex ran read-only probes against the machine. Its top concerns were
  NOT storage micro-optimization: (P0) whether WSL/Claude Science can launch at all on a managed
  host, (P0) whether the install source + entitlement are real/current, and (P1) a Builder-vs-
  Researcher track conflict. Also: blind `curl|bash`, GPU overstated, weak persistence, HDD rule
  too coarse, drvfs claim unproven, incomplete rollback, mojibake.
- **Key meta-finding:** three of Codex's probes (`wsl -l -v`, `Get-PhysicalDisk`, `free -h`)
  returned **access-denied inside Codex's own sandbox** -- which it read as "possibly blocked."
  The real user had already run those exact commands successfully this session.
- **Round 2.** Claude supplied the live user-shell transcript; Codex **dropped** the three
  sandbox-artifact findings (F-001/009/010) plus the track finding, **escalated** the eight real
  ones (correctly: an accept is not real until the runbook is rewritten), and added five
  sharpeners (F-013 gate ordering, F-014 stale artifact, F-015 managed-endpoint preflight, F-016
  persistence service contract, F-017 audit hygiene).
- **Round 3.** Claude presented the final phased-gate runbook shape. Codex dropped all remaining
  findings and declared convergence, noting the residual unknowns are correctly positioned as
  **stop gates, not plan defects.**

## What the debate changed (net value)

1. **Sequencing became gated.** GATE-0 (docs + entitlement) and a managed-endpoint PREFLIGHT now
   run *before any host change*; GATE-GPU (CUDA-in-sandbox) runs *before* any local-GPU/model-
   placement decision. This is the single biggest protection against wasting a hackathon day.
2. **Install is fetch-inspect-record-run**, not blind `curl|bash`; installer audit goes to a
   gitignored path.
3. **Persistence is a real service contract** (systemd user unit + linger + health check + reboot
   acceptance test), not just `--detached`.
4. **Placement rule sharpened** from size-based to **access-pattern-based**: hot data + mmap'd
   model weights on the SSD; HDD only for cold/sequential; drvfs behaviour is *tested*, not
   asserted; native-ext4 VHD is the escalation if C: gets tight.
5. **GPU claim downgraded** to "expected, unproven" pending CUDA-in-task.
6. **Rollback** now covers profile/packages/services/caches, not just `~/.local` + `.wslconfig`.
7. **Runbook normalized to ASCII**; track drift (Builder->Researcher+vehicle) flagged for
   doc reconciliation.

## Persistent disagreements

None. The only residual items are **genuinely unproven facts, not disagreements**: (a) Claude
Science entitlement for this Max account, and (b) VCU managed-endpoint behavior toward the
installer + sandbox + localhost port. Both are correctly the **first gates** in the runbook.

## Recommended next move

Execute **GATE-0** (re-read the live doc; confirm the installer command + that Claude Science is
enabled for the Max account) before any host change. It is cheap, and it is the one thing that,
if wrong, invalidates the rest. Then PREFLIGHT the managed endpoint, then GATE-1.

## Audit trail

Per-round artifacts: `round_0{1,2,3}_claude.md`, `round_0{1,2,3}_codex.json`,
`round_0{1,2,3}_preamble.md` under
`docs/reviews/codex-debate_claude-science-wsl-install-plan_2026-07-07/`. Raw Codex logs (gitignored)
under `.claude/scratch/codex-debate-cs-install/`.
