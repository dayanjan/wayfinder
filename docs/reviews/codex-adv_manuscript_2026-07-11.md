# Codex adversarial review — Wayfinder manuscript (2026-07-11 evening)

Cross-model hostile review (codex-cli 0.144.1, gpt-5.6-sol, read-only) of the compiled `.tex` after the
figure + related-work + evidence-strengthening + genomics revision. Verdict: **major revision** (but "the
concerns are substantially handled"; the blocker is the funnel arithmetic). Raw log:
`.claude/scratch/manuscript-finish/codex_review.log` (3,344 lines; trimmed here per doctrine §13.2).

| # | Sev | Location | Finding | Fix |
|---|-----|----------|---------|-----|
| 1 | **P0** | §4.1 funnel | "43 with a positive disease hop, of which 30…10…3…and 1" sums to **44**; funnel arithmetic doesn't close | State 43 supported = 30+10+3; 1 refuted-effect + 21,995 refuted-disease are separate (22,039 total). Matches Fig 2. |
| 2 | **P0** | §4.1 vs §4.1b | "referee supports **395**/47,220" vs "disease hop supports **406**" — two full-space counts disagree, no stated distinction | Reconcile: 395 full-chain support ⊆ 406 disease-hop-pass; the 11 difference fail QC/effect/program. |
| 3 | P1 | §5.2 | direction analysis (NAB2 down in lesional skin, exact FC/p) has no dataset accession / methods / n | Name the data source + note methods are in the project record; frame as exploratory. |
| 4 | P1 | §2.4 | "What none of them does…" universal novelty claim over-compresses heterogeneous systems (esp. Robin) | Soften to "we are not aware of"; sharpen the axis to *held/pre-existing substrate*. |
| 5 | P1 | §2.4 | "Their receipts are literature citations or model confidence" overgeneralizes (Robin/Coscientist run real experiments) | Make system-specific; contrast on *retrospective adjudication vs running new experiments*. |
| 6 | P1 | §4.4 | "cis-artifact **refuted**" is strong for one aggregate Stim8hr expression null | "no detectable STAT6-expression cis-effect at Stim8hr"; keep the scope. |
| 7 | P1 | §4.4 | "overlapping 3′ ends" as a cis-repression mechanism is a non sequitur (CRISPRi is TSS-targeted; STAT6 TSS ~43 kb away) | Drop the 3′-overlap mechanism; keep promoter-spreading (Lensch), note 43 kb makes it unlikely → empirical null decisive. |
| 8 | P1 | §4.3 | "not a 12q13 locus artifact" too strong — rejects colocated-gene-set artifact, not LD label | Qualify: "not a locally colocated gene-set artifact; LD provenance remains open (§4.4b)". |
| 9 | P1 | §4.6 | "strongest evidence the finding is a property of the data" — reproducibility ≠ biological validity | "…that the reported numbers are reproducible from the deposited tables, not our implementation." |
| 10 | P1 | §3.2/3.3/abstract | within-funnel hops 0–2 are selection criteria; referee mostly re-labels + applies disease test | Already foregrounded 3×; light touch — ensure abstract doesn't imply 4-hop within-funnel discrimination. |
| 11 | P2 | §4.1b | "label-dependent" risks sounding favorable | Already hedged both tails; minor wording. |
| 12 | P2 | references.bib | `{{PIP authors}}` placeholder; `\&amp;` HTML entity (cheng2021) | Fetch real authors; fix `\&amp;` -> `\&`. |
| 13 | P2 | §1/§2.1 | "three reviewers" blockquote is unsourced peer-review correspondence | Attribute explicitly to the authors' own proposal. |

**Overall:** major revision; the rejection-level item is the funnel non-reconciliation (43 vs 44; 395 vs 406).
Once the ledger is internally auditable, the "receipt-backed" thesis holds on the manuscript's own terms.
