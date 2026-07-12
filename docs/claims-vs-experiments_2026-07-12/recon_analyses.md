# Recon — MANUSCRIPT ANALYSES cluster (M8, M10, R2, R4, M6-byte-for-byte)

**Agent:** claims↔experiments reconciliation, analyses cluster · **Date:** 2026-07-12 · **Mode:** read-only.
**Artifacts opened:** `gate_grid.py` + `gate_grid_results.json`; `hard_negatives.py` + `hard_negatives_results.json`;
`sensitivity_results.json`; `cs-reproduction/sensitivity_results.cs.json` (hash/diff compared).
**Panel refs:** `contribution-novelty-audit_2026-07-12/{VERDICT,verify_prim,adversarial_codex}.md`.

---

## THE LOAD-BEARING ANSWER (read this first)

**No real evaluation-with-baseline exists.** Nothing in this cluster measures precision, recall, or
correctness against any ground truth, and nothing scores Wayfinder's ranking against a simpler-baseline
ranker on a metric. The panel's central FATAL — *"the method is DEMONSTRATED, NEVER EVALUATED; no precision,
recall, baseline, or held-out benchmark"* (VERDICT; adversarial_codex finding #1, severity **FATAL**) —
**still stands.** The §5.3b evaluation the VERDICT names as the single highest-value move (time-sliced
precision@k, OR an external known-true/known-false panel scored for false-refutation/false-abstention) has
**not** been run.

What this cluster *does* add — and it is real but narrower than "evaluation":
- **`gate_grid`** is a threshold-**robustness diagnostic**. It self-labels (docstring L13): *"a
  threshold-robustness DIAGNOSTIC of the machinery's behaviour, never a validation."* No baseline, no truth.
  This is *exactly* the object adversarial_codex pre-dismissed: *"Rank stability proves that similar
  hand-chosen weights produce a similar ranking, not that the ranking is scientifically useful."*
- **`hard_negatives`** is the closest thing to a baseline in the whole repo: Panel B builds a **frozen
  curated-association nominator** (top-50 genes/disease by Open Targets `ac_known`, chosen with zero referee
  input) and shows the referee culls a fraction of those association-plausible picks at its own hops. This is
  a genuine **comparator** (answers reviewer B1 "the referee's own no is thin", and satisfies F-012 "sample
  not chosen by the outcome"). **But it has no correctness metric** — the docstring guardrail (L26): *"a
  diagnostic of the referee's own discrimination, NOT a precision/recall or a 'confident-no accuracy'
  claim."* The culled genes (IL36RN, TREX1, PADI4) are "untested" because the *knockdown failed QC*, never
  because they were shown to be true negatives. It measures **how much** the referee additionally culls vs a
  DB nominator, not **whether** those culls are correct. Baseline-shaped, metric-free → **does not close the
  FATAL; softens it.**

Net: the FATAL is **partially answered on reviewer B1's narrow "thin-no" jab** (own-hop discrimination is now
quantified: ~15-17%, disease-independent) and now has a comparator the panel didn't have — but the FATAL as
written (precision/recall/baseline-beating) is **untouched**.

---

## PER-CLAIM

### M8 — balanced novelty+effect ranking objective (min-z bridge) · **SUPPORTS-with-COMPLICATE**
**Computed** (`gate_grid` + `sensitivity control3`): NAB2×eczema rank across 27 **gate** cells = **1–5**,
survives in **18/27** cells; across 27 **weight** cells = **1–8, median 4**, top-5 in 88.9%. Clean-survivor
count swings **7–74**; Jaccard-vs-default of the survivor SET = min **0.23**, median **0.41**.
- **vs CLAIM (objective is robust):** SUPPORTS the *rank*-robustness. **COMPLICATES** on two axes the paper
  under-reports: (a) NAB2 is **culled entirely (rank null)** in all 9 cells at the strict literature floor
  `ab_gate_pct=0.75` — flagship survival is gate-dependent; (b) the survivor *set* is unstable (Jaccard
  median 0.41, count 7→74), so "stable" holds for NAB2's *rank among survivors*, not for *who survives*.
- **vs PANEL:** does NOT answer the FATAL — this is precisely the rank-stability the panel called
  "not that the ranking is scientifically useful." V-PRIM separately grades M8 PARTIALLY-ANTICIPATED /
  *understated* (min-z + anti-obscurity is a reasonable novel combination the paper under-claims) — that
  under-claiming is untouched here.

### M10 — negative-control decomposition (label-shuffle) · **SUPPORTS**
**Computed** (`sensitivity control2`, 2,000 permutations): observed disease-hop supported = **406**; null
mean **467.7 ± 10.9**; **signed z = −5.645** (≈5.6 SD **below** null); fold-over-null **0.87**; upper-tail
p = **1.0**, two-sided p = **0.001**.
- **vs CLAIM:** SUPPORTS exactly. The disease-hop ~99% refutation stringency is **substrate-inherited** (the
  referee supports *fewer* pairs than the shuffled null), so it is correctly **not credited to the referee**;
  the paper declines the tempting "rarer-than-chance selectivity" reading (upper p=1.0). Self-limiting, as
  claimed.
- **vs PANEL:** V-PRIM grades this *understated / self-shrinking* — it actively **shrinks M3** (falsification
  claim). Honest. Not a baseline evaluation and not trying to be.

### R2 — "referee alone supports 395/47,220; novelty gate culls 395→43" · **PARTIAL (numeric tension to reconcile)**
- `47,220` = `pair_space_AxC` ✓ (control2). Post-gate endpoint `43` = **corroborated**: `gate_grid` default
  cell `disease_c_supported_total = 43` ✓ (clean=30).
- **The "395" is NOT in these JSONs** (it lives in the stage-1 sweep JSONs, outside this cluster). The
  closest analog here — control2 `observed_disease_hop_supported` = **406** — is the referee-alone
  disease-hop supported count over the same 47,220 pair space, and it is **406, not 395** (an 11-pair gap).
  Likely a definitional/version difference (clean-only vs clean+weak+flagged, or a re-run), but the
  manuscript's **395** and the JSON's **406** should be reconciled before either is cited. **Flag.**

### R4 — flagship rank stable: NAB2 rank 1–8 (median 4) over weights; 1–5 over gate cells · **SUPPORTS-with-COMPLICATE**
- `control3`: min 1 / max 8 / median 4 ✓ **exact**. `gate_grid`: rank min 1 / max 5 ✓ **exact**.
- **COMPLICATE / honesty:** "1–5 over gate cells" reports only the cells where NAB2 **survives** (18/27); in
  the other 9 (all `ab_gate_pct=0.75`) NAB2 is culled from the funnel entirely. The stated numbers are
  accurate; the caveat (flagship exits at the strict literature floor) is omitted from the claim.
- **vs PANEL:** same as M8 — pre-dismissed as characterization, not evaluation.

### M6 — sensitivity panel reproduced "byte-for-byte" · **REFUTES the literal wording / SUPPORTS the substance**
- **NOT byte-identical.** `sha256`: local `8f1ef9…` vs CS `0657bb…`; sizes **4055 vs 3838 bytes** (Δ217 =
  one newline char × 217 lines); local is **CRLF**, CS is **LF**.
- **After newline normalization (`tr -d '\r'`) the two hash IDENTICALLY (`0657bb…`) and diff is empty.** So
  **every number/value is digit-for-digit identical**; only line endings differ.
- **Classification:** the substantive reproduction claim (the CS run reproduces every sensitivity number
  exactly) is **TRUE and strong**. The literal phrase **"byte-for-byte" is FALSE** — the raw bytes differ by
  217 (CRLF vs LF). **Recommend** the manuscript say "value-identical / digit-for-digit," OR normalize line
  endings before asserting byte-equality. Intellectual-honesty flag, easily fixed.

---

## HONESTY FLAGS (surfaced for the reconciliation)
1. **M6 "byte-for-byte" is literally false** (CRLF vs LF; 217-byte delta). Substance holds; wording overclaims. **Fix wording or normalize.**
2. **R2 395 vs 406** — the manuscript's referee-alone count (395) does not match control2's observed disease-hop supported (406). **Reconcile.**
3. **M8/R4 flagship survival is gate-dependent** — NAB2 is culled in 9/27 gate cells (the `ab_gate_pct=0.75` floor); the "rank 1–5 over gate cells" claim silently conditions on the 18 cells where it survives. **Consider stating "survives 18/27; rank 1–5 where it survives."**
4. **CS-reproduction JSON confirmed self-consistent** — matches the local JSON on all values (only newline-format differs); no number was altered in the CS replay.

## Control-2 numbers (brief's request) — CONFIRMED
observed **406** vs null **467.7 ± 10.9**, **signed z −5.645** (5.6 SD below null). ✓ Exact match to the brief.
