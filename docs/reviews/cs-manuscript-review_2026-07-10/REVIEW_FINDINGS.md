# REVIEW_FINDINGS — Wayfinder manuscript (§1 Introduction, §2 Background, §3 Methods)

**VERDICT:** Numbers hold. **18 quantitative/identity claims checked → 16 MATCH (1 by arithmetic derivation), 0 MISMATCH, 2 UNSUPPORTED; 1 calibrated-language flag; 0 receipt-class flags.** Every funnel count, gate parameter, and objective coefficient matches the primary artifacts exactly. The two UNSUPPORTED items are the specific "Claude Haiku 4.5" model identity (not in the provided provenance) and the external R01 grant/quote (out of artifact scope, expected). The two-receipt-class distinction (experimental vs. association/nomination) holds in every sentence.

Independent Reviewer (separate model, separate checkpoint) cross-checked all number verdicts against the parsed artifact fields: agreed on 17/18, disputed the "12 diseases" row (no direct field enumerates 12) — reclassified below as MATCH* (derived) with a caveat.

---

## Task 1 — Number & identity verification

Ground truth read directly from: `sweep_Stim8hr.json` (params/funnel), `lbd_questions_Stim8hr.json` (NAB2 + ranking), `stage3_cis.json`, `README.md` (model cast).

| Section | Location | Claimed value | Artifact source (file → field/line) | Status |
|---|---|---|---|---|
| 01_introduction.md | L61 (~body) | 22,039 gene→program→disease hypotheses | sweep_Stim8hr.json → funnel.eligible_pairs = 22039 | **MATCH** |
| 01_introduction.md | L65-66 | NAB2 highest-ranked near-novel survivor; Th1/Th2 → atopic eczema; genetic link | lbd_questions_Stim8hr.json → NAB2×atopic eczema at index 4; ac_lit=6 (near-novel), ranks 1-2 UFM1/BHLHE40 ac_lit 43/26 (not novel), rank3 NUDT1 ac_lit 0 (trivial effect) | **MATCH** |
| 03_methods.md | L47 / L75 / L126 | A contains 3,935 genes | sweep → funnel.a_genes = 3935 | **MATCH** |
| 03_methods.md | L75 | → 22,039 eligible (gene,disease) pairs | sweep → funnel.eligible_pairs = 22039 | **MATCH** |
| 03_methods.md | L76 | → 43 disease-supported | sweep → funnel.disease_c_supported_total = 43 | **MATCH** |
| 03_methods.md | L76 | → 30 clean full-chain nominations | sweep → funnel.clean_supported = 30 (chain_classes.supported = 30) | **MATCH** |
| 03_methods.md | L45 | significant Th1/Th2 shift: T2 adjusted p < 0.05 | params.program_significant = True; finding md: 'all A genes pass T2<0.05' | **MATCH** |
| 03_methods.md | L58 | bc ≥ 3 | sweep → params.min_bc = 3 | **MATCH** |
| 03_methods.md | L58 | ac_known ≤ 0.1 (no established genetic link) | sweep → params.tau = 0.1 | **MATCH** |
| 03_methods.md | L56 | ab ≥ ab_gate = universe percentile, default the median | sweep → params.ab_gate_pct = 0.5 (ab_gate_value = 26) | **MATCH** |
| 03_methods.md | L66 | β = 1 | sweep → params.beta = 1.0 | **MATCH** |
| 03_methods.md | L66 | w = 1 | sweep → params.w = 1.0 | **MATCH** |
| 03_methods.md | L66 | w2 = 3 | sweep → params.w2 = 3.0 | **MATCH** |
| 03_methods.md | L25 | 12 immune diseases (disease set C) | DERIVED: finding md + replication md state 'referee alone 395/47,220'; 47,220 ÷ a_genes 3,935 = 12 exactly. No artifact field literally enumerates 12 diseases; clean set surfaces only 10 distinct diseases (2 had no clean survivors). | **MATCH*** |
| 03_methods.md | L33-34 | author = Opus-class (Claude Opus 4.8) | README.md L28/L87 → 'OPERON = Opus 4.8' | **MATCH** |
| 03_methods.md | L34 | reviewer = Sonnet-class (Claude Sonnet 5) | README.md L28/L87 → 'REVIEWER = Sonnet 5' | **MATCH** |
| 03_methods.md | L35 | inline sampling = Haiku-class (Claude Haiku 4.5) | NOT PRESENT in README.md or any provided artifact (grep 'haiku' → 0 hits) | **UNSUPPORTED** |
| 01_introduction.md & 02_background.md | intro L29 / bg L28 | NIH grant 1R01LM015392-01 + reviewer quote | Not in provided artifacts (external R01 critique; out of artifact scope) | **UNSUPPORTED** |

\* **MATCH\*** = confirmed by arithmetic derivation, not a direct field. The disease universe "12" is not literally enumerated in any artifact; it follows from `referee alone 395/47,220` (finding + replication md) with 47,220 ÷ 3,935 (a_genes) = 12 exactly. The clean survivor set spans only **10** distinct diseases (the other 2 produced no clean full-chain nomination). Independent Reviewer flagged this; retained as MATCH because the quotient is exact and both operands are stated figures.

**Notes on the number checks**
- **Funnel (3,935 → 22,039 → 43 → 30)** matches `funnel.a_genes / eligible_pairs / disease_c_supported_total / clean_supported` to the unit; `chain_classes` = supported 30 · supported_weak 10 · supported_flagged 3 · refuted_effect 1 · refuted_for_c 21,995 (consistent with §3.3 demotion scheme).
- **Objective coefficients β=1, w=1, w2=3** = `params.beta/w/w2`; **ab_gate = median (0.5 pct → value 26)** = `params.ab_gate_pct/ab_gate_value`; **bc ≥ 3** = `params.min_bc`; **ac_known ≤ 0.1** = `params.tau`. All exact.
- **NAB2** is the highest-ranked *near-novel* survivor: rank 4 overall in `lbd_questions` (ac_lit 6); ranks 1–2 (UFM1, BHLHE40) have ac_lit 43/26 (not novel), rank 3 (NUDT1) has ac_lit 0 but a trivial effect (4 downstream DE, read from lbd_questions_Stim8hr.json effect field; the finding md's prose says "4 downstream DEs"). NAB2×atopic-eczema signals (ab 66, bc 2184, ac_lit 6, ac_known 0.0376, effect 301, score −1.137) all match the artifact — though the section drafts cite only the qualitative "Th1/Th2 … genetic link to atopic eczema," not the numeric signals.
- **STAT6 cis numbers** (log2FC +0.087, adj_p 0.788, rank 5444/10282, 302 moved) are internally consistent (`stage3_cis.json`, ALL_PASS=true) but are **not cited in these three sections** — they belong to §4.

---

## Task 2 — Calibrated-language scan (BODY prose only; DRAFT blockquotes and reviewer meta-descriptions excluded)

**1 flag.**

| Section | Location | Offending phrase | Calibrated rewrite |
|---|---|---|---|
| 02_background.md | L53 (§2.2) | "…experimental **oracle** for the first three hops…" | "…direct experimental measurement source for the first three hops…" |

Detail: "oracle" is on the overclaim list and Task 3 names it explicitly for the substrate. The word connotes an infallible ground-truth machine; the substrate is aggregated supplementary tables carrying QC caveats. **This is a word-choice flag only** — the sentence correctly restricts "oracle" to the first three (experimental) hops and contrasts an association signal for the fourth, so it does not blur the receipt classes.

**Correctly excluded (not flagged):**
- **Intro L5 DRAFT blockquote** — "proven/definitive/validated/genuine" (rule a: inside `> DRAFT …`).
- **Bg L74–75 "validated"/"definitive"; Methods L120 "validated","definitive"** — meta-descriptions of the reviewer *flagging and removing* those words (rule b). These are consistent with README.md L82 (reviewer flagged "validated" title + "definitive" heading; both edited out) — a supported provenance claim, not an overclaim.
- **"literature-based discovery" / "open/closed discovery" / "discovery-informatics"** (intro L19,23; bg L10,12,15,16,59) — field terminology and the hedged "*candidate* discovery," not a claim of having discovered something.
- **"established in the literature" (bg L12), "no established genetic link" (methods L58)** — mean *documented/absent-from-curation*, not causal establishment; not flagged.
- **"demonstrate/demonstrates"** — deliberately chosen calibrated verb per the outline ("ledger *demonstrates*, not proves"); not on the overclaim list.

---

## Task 3 — Receipt-class consistency (experimental vs. association/nomination)

**0 flags — the distinction holds everywhere.**

- **Intro L48–51:** knockdown/effect/program hops = "*experimental* measurements"; disease hop = "an *association* receipt (genetic enrichment), a nomination rather than a claim of experimental causality." ✓
- **Bg §2.2 (L44–53):** first three hops = "**experimental receipts**"; fourth hop = "**association receipt** … a *nomination*, not a claim of experimental disease causality," with GWAS/no-coloc/no-LD caveat stated. ✓
- **Methods §3.3:** Hop 3 (disease) reads T3 odds-ratio/FDR enrichment; never called experimental; "supported" verdict is a chain re-derivation, not causal proof. ✓

No sentence calls the disease hop experimental, and no sentence calls the whole substrate an oracle (the single "oracle" use is scoped to the three experimental hops — see Task 2).

---

## Task 4 — Other correctness / internal-consistency notes

1. **UNSUPPORTED model identity (medium):** §3.1 L35 names "Claude **Haiku 4.5**" for inline sampling. No provided artifact records a Haiku model — README.md lists only Opus 4.8 (author) + Sonnet 5 (reviewer); `grep haiku` across all six artifacts = 0 hits. Cite the audit-store row or soften to "a lightweight model."
2. **External citation, not a defect (info):** the NIH grant **1R01LM015392-01** and the three-reviewer quote (intro L29 / bg L28) are not in the six artifacts. The draft header states the quote is verbatim from the funded critique — verify against that source separately; out of artifact scope.
3. **Gate-vs-referee framing (low):** intro L61 says the referee "culled" the 22,039 hypotheses. Accurate (the referee does reduce 22,039→43→30), but the 47,220→22,039 reduction is done first by the literature/known-association **gate**, not the referee. §3.2 (L74–76) states this precisely; intro could mirror it to avoid conflation.
4. **Five-signal names (info):** §3.2 names ab / bc / ac_known / ac_lit / effect — identical to the `lbd_questions` record fields. ✓
5. **Objective formula (info):** the §3.2 score equation with β=1, w=1, w2=3 is consistent with the README micro-sweep form `min(z_ab,z_bc)+z(effect)−log1p(ac_lit)−3·ac_known`. ✓

---

*Method: every value read from the parsed JSON field / artifact line named in the table — no values recalled. Independent Reviewer (distinct model, distinct checkpoint) confirmed the number verdicts before finalization.*
