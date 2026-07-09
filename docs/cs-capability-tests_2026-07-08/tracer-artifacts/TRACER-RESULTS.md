# CS tracer — clean-room reproduction of the referee + NAB2 finding, NATIVE in Claude Science

**2026-07-09.** De-risking tracer for "rebuild the pipeline inside CS" (see
`../../pipeline-inventory-and-cs-mapping_2026-07-09.md`). Driven via `drive-claude-science` into a
fresh project (`proj_774ded9efc2e`, 1 approval — the `~/pyzobot-data/` folder grant). CS was given our
referee **rules + table schema but NOT the expected numbers**; it wrote its own pandas `referee.py`,
ran it on the raw tables, and derived the verdicts. Artifacts here: `referee.py`, `verdicts.json`,
`receipt_chain.md`. Verified from `operon-cli.db` + these files.

## Result: digit-for-digit match to the external pipeline

| Hop | CS-derived (native) | Our known value | Match |
|---|---|---|---|
| **NAB2 @ Stim8hr** | **supported** ("validated gene→Th1/Th2→disease chain re-derived") | supported | ✅ |
| HOP0 gate | 2/2 signif, best adj-p 1e-16, expr 0.05603 vs NTC 0.5672 | 2/2, 1e-16, 0.056 vs 0.567 | ✅ exact |
| HOP1 effect | −16.8816, 301 downstream, off-target False | −16.9, 301, no off-target | ✅ exact |
| HOP2 program | Ota z **7.708** adj_p 1.95e-13 (Th1); Hollbacker n.s. (z 2.391) | Ota z 7.71 adj_p 1.96e-13; Höllbacher n.s. | ✅ exact |
| HOP3 disease | atopic eczema cl100 OR **3.899** FDR 0.0028; cl90 OR **3.43** FDR 0.0224 (+asthma) | clusters 90&100, OR 3.90/3.43, FDR 0.0028/0.0224 | ✅ exact |
| **IL2 @ Rest** | **untested** (gate: 0/2 signif, adj-p 0.32, expr 0.031≈NTC 0.036 → "nothing to knock down") | untested (hero catch) | ✅ exact |
| **SLC1A5 @ Stim8hr** | **refuted** (HOP1 no on-target KD, effect −3.46, n_downstream 1; HOP3 9 clusters none FDR<0.05, best T1D OR 2.732 FDR 0.0538) | refuted | ✅ exact |

The hero **UNTESTED** gate reproduced perfectly (IL2: a failed knockdown → unanswerable, not "no effect").

## What this de-risked (all green)
- **CS kernel reads our tables** natively from `/home/dayanjan/pyzobot-data/` (WSL ext4) — 1 auto-approved
  folder card, no `/mnt/c` pain. The referee needs **no connectors** (pure pandas), so zero connector risk.
- **CS wrote correct referee logic itself** — its own `referee.py` (16.8 KB) implements HOP-0 gate →
  effect → program (both contrasts) → disease, with calibrated vocabulary.
- **Provenance is free** — `operon-cli.db` logged every cell (`execution_log`), the immutable artifact
  versions, and the run cost (OPERON Opus-4.8; a Sonnet-5 REVIEWER frame ran, $0.30).
- **Bonus — CS self-audited unprompted:** it inspected `host.delegate`/`host.capabilities`, then ran an
  **independent adversarial re-derivation** of the referee in-kernel to cross-check its own writeup
  (execution_log cells 8–12). That is the falsification instinct, native.

## Caveats / learned
- The Sonnet-5 **Reviewer's `verification_checks` were still empty at capture** (async-lag: findings +
  provenance `extracted_code` backfill on frame completion, which headless driving doesn't trigger — same
  as 2026-07-08). A review frame DID run; re-poll the DB later or trigger an explicit review.
- SLC1A5's *overall* headlines HOP-1 (first-refuted-hop rule as I phrased it in the prompt); our original
  code headlined the disease hop. Both refute SLC1A5 on the same data — a wording nuance, not a science diff.

## Verdict
**The core instrument (data substrate + 4-hop referee + the NAB2 finding) runs natively in Claude
Science and reproduces the external result exactly.** Green light to scale to the full pipeline (add the
LBD proposer via CS's literature + Open Targets connectors, the confounder checks, and the S3 cis-check),
keeping Codex as the external cross-model auditor.
