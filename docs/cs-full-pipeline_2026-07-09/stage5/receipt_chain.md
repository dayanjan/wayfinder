# Receipt Chain — NAB2 as a Th1/Th2 Program Regulator

**A T-cell nomination whose receipt chain was reproduced natively across stages in this Claude Science workbench.**

This document assembles the end-to-end receipt chain for a single finding. Every number
below was produced by an earlier native run in this workbench and is cited, not recomputed
here. Language is deliberately calibrated: a step is *reproduced*, *re-derived*, *consistent
with*, *refuted*, or *untested* — never "discovered" or "proven".

---

## Origin of the question (Stage 1, LBD generator)

The literature-based-discovery (LBD) proposer asked:

> *"Does NAB2 regulate the Th1/Th2 program and thereby link to atopic eczema?"*

It surfaced as **rank 4** among **30 clean, full-chain-supported questions** distilled from
**3,935 candidate A-genes**. The funnel that produced it:

| Stage | Count |
|---|---|
| A-genes (candidate universe) | 3,935 |
| Eligible A–C pairs | 22,039 |
| Disease-C–supported | 43 |
| Clean full-chain-supported | 30 |

The NAB2 row receipt: **ab = 66**, **bc = 2,184**, **ac_lit = 6** (near-novel),
**ac_known = 0.0376**, **effect = 301 downstream genes**. The low `ac_lit` count is what
places this at the near-novel end of the ranked list.

---

## The 4-hop referee answer

The referee walks the chain hop by hop. Each hop carries its own receipt (the numbers below
were reproduced digit-for-digit in the native referee run).

### HOP-0 — KNOCKDOWN-QC GATE — **PASS**

The hero gate. Only a gene that was actually silenced yields an interpretable downstream
result; a failed knockdown would leave the chain **UNTESTED**, and must never be read as
"no effect."

- Receipt: **2/2 guides significant**, best **adj_p = 1e-16**, guide expression **0.056**
  vs NTC **0.567**.

### HOP-1 — EFFECT — **supported**

- Receipt: on-target **significant**, effect size **−16.88**, **301 downstream DE genes**,
  **no off-target flag**.

### HOP-2 — PROGRAM (Th1/Th2, both contrasts) — **supported**

- Receipt: **Ota 2021** z = **7.708**, adj_p = **1.95e-13** (Th2-associated).
- **Hollbacher** contrast: **n.s.** — reported as-is, not collapsed into the positive call.

Both contrasts are shown; the non-significant one is disclosed rather than dropped.

### HOP-3 — DISEASE (atopic eczema, condition-matched) — **supported**

- Receipt: **cluster 100** OR = **3.899**, FDR = **0.0028**; **cluster 90** OR = **3.43**,
  FDR = **0.0224**.

### Referee overall

**Consistent with** a gene → Th1/Th2 program → disease chain, re-derived from the
deposited tables.

---

## The confounder falsification (Stage 3, native S3 read)

**Cis-artifact check.** NAB2's CRISPRi guide sits **~1.9 kb from STAT6**, the master Th2
regulator. If the eczema signal were STAT6 bleed rather than genuine NAB2 biology, silencing
at the NAB2 locus should perturb STAT6 mRNA.

- Receipt (read live from the authors' deposited genome-wide DE matrix on public S3):
  NAB2 knockdown leaves **STAT6 mRNA UNMOVED** (log2FC ≈ **+0.09**, adj_p ≈ **0.79**), while
  **NAB2 self-knockdown is strong** (log2FC ≈ **−3.08**).

**Verdict:** the CRISPRi cis-artifact is **REFUTED**. The eczema effect is genuinely NAB2's,
not STAT6 bleed.

---

## Honesty framing

Claude Science ran the LBD generator natively over the full 3,935-gene Stim8hr universe using
the same deterministic code path, replaying previously captured Europe PMC / Open Targets JSON
receipts from a workbench-local cache, and reproduced the exact funnel and the NAB2 → atopic
eczema rank. A separate Stage 0 probe demonstrated the same kernel can make live Europe PMC GET
and Open Targets GraphQL POST calls, and Stage 3 read the authors' deposited genome-wide DE
matrix live from public S3. Cross-model replication (a second model family) is kept external as
an independent auditor.

---

## What ran where

| Layer | Component | Execution |
|---|---|---|
| Generation (Stage 1) | LBD generator over the full 3,935-gene Stim8hr universe | Native, deterministic code path replaying **cached** Europe PMC / Open Targets JSON receipts from a workbench-local cache; a separate **Stage-0 live-access proof** showed the same kernel making live Europe PMC GET and Open Targets GraphQL POST calls |
| Referee (4-hop) | HOP-0 → HOP-3 chain | **Native pandas** over the deposited tables; funnel and NAB2 rank reproduced digit-for-digit |
| Cis-check (Stage 3) | STAT6 cis-artifact falsification | **Live S3 read** of the authors' deposited genome-wide DE matrix |
| Provenance | Receipt audit store | This workbench's **audit store** |

---

## Calibrated overall verdict

A **novel, reproducible NOMINATION** that **NAB2 is a Th1/Th2 program regulator**. The
gene → program → disease chain is **consistent with** the deposited data and was re-derived
from the tables; the CRISPRi cis-artifact confound is **refuted**. The atopic-eczema disease
link is an **Open Targets GWAS-genetic** association and is flagged as such — it is a genetic
link carried through from Open Targets, not a disease effect experimentally re-derived in this
workbench. Nothing here is claimed as "discovered" or "proven"; cross-model replication remains
external as an independent audit.
