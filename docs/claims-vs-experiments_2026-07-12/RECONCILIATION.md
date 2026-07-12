# RECONCILIATION — manuscript claims × already-run CS/experiments × literature-panel critique
**Step 2 (2026-07-12).** Synthesis of six primary-artifact recon passes (`recon_{pipeline,capability,
replication,confounders,direction,analyses}.md`) against `CLAIMS_LEDGER.md` and the literature audit
(`docs/reviews/contribution-novelty-audit_2026-07-12/`). Method: recon agents read the *actual* JSON/
receipt/code artifacts, not the manuscript's retellings.

## Headline — the reconciliation runs in BOTH directions
1. **The experiments RESCUE biology the literature panel under-credited.** The panel searched abstracts;
   it never opened the confounder or direction data. Those experiments materially strengthen B1/B3/B4/B6.
2. **The experiments CONFIRM the panel's central method FATAL.** Every CS run is *execution/reproduction*,
   not *evaluation*. No precision/recall, no baseline-beating metric exists. "Demonstrated, never measured" stands.
3. **The experiments SURFACE fresh honesty flags neither the panel nor the manuscript currently has right**
   — small but real wording/number defects to fix before any submission.

## The matrix
| Claim | Already-run experiment → key result | Panel had said | Reconciled status |
|-------|-------------------------------------|----------------|-------------------|
| **M1** | Stage1 sweep + tracer re-derived the pipeline natively (digit-for-digit); live cold-cache full sweep recovered NAB2 rank 4 | NOVEL-but-narrow integration | **SUPPORTS** execution; novelty verdict unchanged |
| **M2** | 2,430/2,430 failed-KD genes → *untested* (100%, no leakage) | known primitive, app-only | **SUPPORTS** (behavioral) |
| **M3** | Referee's own "no" fires ~1-in-6; disease-hop "no" substrate-inherited | self-bounded; partly-anticipated | **SUPPORTS-but-self-COMPLICATES** (as the paper already says) |
| **M4** | Deterministic sweep under replay guard; tracer referee reads raw tables, nothing hardcoded | known (grounded tool-use) | **SUPPORTS** |
| **M5** | Independent Sonnet-5 critic genuinely CAUGHT a planted 4-vs-5 inconsistency (async, DB-logged) | LLM-as-judge prior art | **SUPPORTS (real catch)** — ⚠ but "flagged & **removed**" overstates: one word ("validated") was flagged and **retained by design** |
| **M6** | Headless driving real; tracer = genuine native re-derivation; full-pipeline repro = cache replay | engineering, not novel science | **SUPPORTS capability** — ⚠ "**byte-for-byte**" is literally FALSE (CS vs local differ 217 B, CRLF/LF; value-identical after newline-normalize) |
| **M7** | 5-agent cross-vendor lab, 2 clean-room; unanimous PASS; caught 74→90/100 + "8×→3×" | QA, not novel science | **SUPPORTS** — ⚠ "reproduced every number" vs "caught real errors" in tension (2 were *corrected*) |
| **M8/R4** | gate_grid: NAB2 rank 1–8 (med 4) weights, 1–5 gate cells | rank-stability pre-dismissed as not-validation | **SUPPORTS numbers / COMPLICATES**: silently conditions on NAB2 surviving the gate (culled in 9/27 cells) |
| **M9** | Universe built pre-disease-table | known (leakage avoidance) | **SUPPORTS** |
| **M10** | Control 2: observed 406 vs null 467.7±10.9, z −5.645 | the honest self-limit | **SUPPORTS exactly** |
| **B1** | Replicated exactly (2/2, −16.9, 301 DE, Ota z 7.71); distinct from EGR (NAB1 paralog opposition) | novel-for-polarization | **SUPPORTS** — add EGR2/3 adjacency + "polarization-scoped" wording |
| **B2** | Enrichment reproduced; disease link is the GWAS label | thin, LD-plausibly STAT6, but honestly scoped | **SUPPORTS-as-scoped** (a nomination, not a discovery) |
| **B3** | stage3_cis.json: STAT6 +0.087/p0.79, NOT in the 302 moved, rank 5444/10282; NAB2 −3.08/p7e-60 | cis-test "competent, survives" (adversary: "cannot attack") | **SUPPORTS — definitively.** Panel's "LD-passenger" headline over-generalized (see below) |
| **B4** | Corrected clusters 90/100 are genome-wide, STAT6 absent | dataset-specific, uncontradicted | **SUPPORTS-after-correction** (the 74→90/100 catch is its only verifier) |
| **B5** | — none — needs variant-level colocalization | the genuine open confounder | **NO-EXPERIMENT (real gap)**; paper foregrounds it correctly |
| **B6** | Bulk NAB2 −0.32/FDR 0.002, ρ −0.34; scRNA keratinocyte −0.51/p0.027, myeloid −0.59/p0.049; proportion↑ (not dilution) | "unverifiable by literature" | **SUPPORTS, under-credited** (a re-derived DE result) — ⚠ T/NK −0.57 is n.s. (p0.11); "per-cell confirmed" mildly overstated |
| **B7** | Direction mixed: 1 of 4 voting arms significant; cytokine arm: IL-4/13 do NOT induce NAB2 | mechanism partly-anticipated (EGR2/3 brake) | **PARTIAL/COMPLICATES** — sign unsettled; manuscript's hedge is correct, keep it; add EGR2-is-STAT6-driven sign-flip caveat |
| **R1** | Funnel 3,935→22,039→43→30 reproduced exactly | — | **SUPPORTS exactly** |
| **R2** | Referee-alone supported count | "395" | **PARTIAL — ⚠ number discrepancy: ledger/text 395 vs sensitivity_results.json 406; reconcile** |
| **R5** | NAB1 paralog opposition (both contrasts sig) = the load-bearing anti-EGR fact | — | **SUPPORTS-with-reframe** (lead with D3, not D2 cross-cohort p0.049) — ⚠ no frozen output receipt |

## The STAT6 "mistaken identity" correction, made precise
The panel's sharpest biology attack ("NAB2→eczema is likely a STAT6 LD-passenger") conflated **three
separable channels**; the experiments **close two and leave one open**:
- (i) **Expression cis-artifact** → CLOSED (B3: STAT6 unmoved in the authors' own genome-wide data).
- (ii) **Cluster-membership / 12q13 co-location artifact** → CLOSED (B4: modules 90/100 genome-wide, STAT6 absent).
- (iii) **GWAS disease-LABEL LD-inheritance** → OPEN (B5: needs external variant-level colocalization).
So the *functional* NAB2→Th2 finding is experimentally defended; only the *disease-label attribution*
remains open — and the paper already says exactly that. "Probably mistaken identity" was wrong; "a
receipt-backed regulatory nomination with one unresolved disease-label confounder" is right.

## What the experiments CONFIRM (the panel critique that STANDS)
- **The method is never EVALUATED.** gate_grid self-labels "a robustness diagnostic, never a validation";
  hard_negatives is baseline-*shaped* (a frozen curated-association comparator) but **metric-free** (no
  precision/recall, culls not validated as true negatives). Nothing measures decision quality vs a baseline.
  → The audit's #1 FATAL is real and unanswered. (Held-out eval already scoped — Step 3.)
- M5/M6/M7 are real, useful capabilities but not novel *science* — both the panel and the experiments agree.

## Honesty flags the manuscript MUST fix (from the primary artifacts — new)
1. **M6 "byte-for-byte" → false.** Say "value-identical / digit-for-digit" (or normalize newlines).
2. **M5 "flagged and removed" → half-true.** "validated" was flagged and *retained by design* in one case; reword.
3. **R2 funnel number: 395 vs 406** — reconcile the referee-alone supported count across text/JSON.
4. **M8/R4 rank stability conditions on survival** — state that NAB2 is culled in 9/27 gate cells (already in §4.1c; keep it honest in the headline).
5. **B6 T/NK −0.57 is non-significant (p0.11)** — call it partial, not "confirmed per-cell."
6. **Confounder script bug** (`[74,90]` hardcoded, 74 non-significant) — self-caught & fixed (→90/100); cite only the corrected derive-clusters script; retire the buggy one.
7. **Stale "1.9 kb"** in old script headers vs corrected "~43 kb" (cosmetic; B3 rests on the empirical null, not geometry).
8. **M7 framing:** "reproduced every headline number" alongside "caught real errors" — say "reproduced all but two, which it corrected."
9. **B7:** keep the unsettled-direction hedge; add the EGR2-is-STAT6-driven-pro-type-2 sign-flip caveat to §5.2.

## Genuine gaps → Step 3 (`NEW_EXPERIMENTS.md`)
- **G1 (method) — evaluation with a baseline.** The held-out eval (scoped in `docs/plans/heldout-eval-scope_2026-07-12.md`) OR promote hard_negatives to a real precision/recall metric. Highest value; closes the FATAL.
- **G2 (biology) — B5 12q13 colocalization.** External variant-level genetics (coloc/SMR) vs the 12q13 AD GWAS; the one open confounder. May exceed CS's reach (needs GWAS sumstats + eQTL).
- **G3 (cheap) — R5 frozen receipt.** Re-run the EGR-distinctness (NAB1-opposition) analysis and save the output as a committed receipt; currently script-only.

## Net effect on the audit verdict
The overall call is **unchanged but re-balanced**:
- **Method:** "novel-but-narrow AND unevaluated" — CONFIRMED by the experiments. The publish-blocker is real and is G1.
- **Biology:** **materially stronger and better-defended than the literature panel conveyed.** The confounder + direction experiments rescue B1/B3/B4/B6 from the panel's abstract-only pessimism; the "mistaken identity" dismissal is retracted (2 of 3 STAT6 channels closed). What remains is one honestly-flagged open confounder (B5) — a nomination, not a debunk.
- **Honesty:** the manuscript's calibration is largely accurate, with 9 specific fixes above (mostly wording/number, one real self-caught bug).
Bottom line: still not publishable *as an evaluated discovery paper* (G1 is the gate), but the path is
narrower and more concrete than the literature audit alone implied — and the biology is real.
