# Master claim register — merged from 3 independent extractors + orchestrator read

Sources: `extract_claude_1.md` (16), `extract_claude_2.md` (16), `extract_codex.md` (23 finer-grained).
The three converged on the same map and the same risk ranking. Below = deduplicated claims,
each tagged with the Phase-B verification agent that owns it and the pre-search novelty-risk
consensus. **Risk = probability a real literature search finds it already known / overstated.**

## METHOD claims
| ID | Claim | §  | Risk (consensus) | Verifier |
|----|-------|----|--------|----------|
| **M1** | **The headline conjunction**: LBD generation + a **deterministic, non-LLM referee** scoring each hypothesis against a **held, pre-existing** experimental substrate + **per-hop experimental receipt** for every edge + **QC-gated abstention** + **falsification** as first-class verdicts. Claimed distinct from AI co-scientist, Robin/PaperQA2, SciAgents, Coscientist, AI Scientist, PerturbQA. **The load-bearing novelty.** | 2.4, abs, 1, 5.4 | MEDIUM | V-GAP |
| M2 | QC-gated **abstention** (failed knockdown = *untested*, not negative) as a first-class verdict primitive | 3.3, 4.2 | MEDIUM (selective-prediction prior art) | V-PRIM |
| M3 | **Falsification / "confident receipt-backed no"** as the deliverable (vs plausibility-optimizing generators) | 4.2, 5.1 | MEDIUM (self-bounded by M10) | V-GAP |
| M4 | Deterministic-tools-only division of labour: LLM = judgment/provenance only, never computes a receipt | 2.3, 3.1 | **HIGH** (standard grounded tool-use) | V-PRIM |
| M5 | Actor–critic **self-audit that enforces calibrated LANGUAGE** on the platform's own output (removed "validated"/"definitive") | 3.4, 4.5 | **HIGH-ish** (LLM-as-judge prior art) | V-AUDIT |
| M6 | **Headless scripting of an API-less agentic workbench** (Claude Science) → replicable-in-principle agentic science; byte-for-byte native reproduction | 3.4, 4.5, 5.1 | LOW prior-art / but "is it *science*?" risk | V-AUDIT |
| M7 | **Cross-family adversarial clean-room replication lab** (5 agents incl. cross-vendor Codex) as a verification method | 4.6 | LOW prior-art / reads as good practice | V-AUDIT |
| M8 | Balanced novelty+effect ranking objective (min-z bridge, no obscurity reward) | 3.2 | LOW (understated) | V-PRIM (light) |
| M9 | Disease-answer-free / leakage-free candidate-universe construction | 3.2, 4.1 | **HIGH** (standard leakage avoidance) | V-PRIM |
| M10 | Negative-control **decomposition**: label-shuffle shows disease-hop stringency is *substrate-inherited*, referee's own edge = QC gate (~1 in 6). Self-limiting honesty result. | 4.1b, 4.2b | MEDIUM (as a method) / it *shrinks* M3 | V-PRIM (light) |

## BIOLOGY claims
| ID | Claim | §  | Risk (consensus) | Verifier |
|----|-------|----|--------|----------|
| **B1** | **NAB2 is a Th1/Th2 (Th2) regulator** — literature-novel regulatory nomination. Threat: EGR2/NAB2 axis (EGR2/3 are established Th regulators). | abs, 4.3 | MEDIUM — **high-value search** | V-TH2 |
| **B2** | **NAB2 → atopic eczema** — literature-novel disease nomination. Threat: NAB2 sits IN the 12q13 atopy locus next to STAT6; may already be a named locus candidate in AD GWAS/eQTL/TWAS. | abs, 4.3 | **HIGH — highest-value search** | V-ECZEMA |
| B3 | STAT6 *cis*-effect **ruled out at expression level** (STAT6 unmoved under NAB2-KD, log2FC +0.087/p 0.788) | 4.4 | LOW novelty / needs **correctness + cis-spread lit** check | V-ECZEMA |
| B4 | NAB2 eczema modules are genome-wide functional immune modules (STAT6 absent from clusters 90/100), not a 12q13 artifact | 4.3, 4.4b | LOW (dataset-specific) | V-ECZEMA |
| B5 | The **12q13 LD-inheritance confounder cannot be discharged** — foregrounded, not claimed resolved | 4.4b, 5.3 | honesty claim (audit for adequacy) | V-ECZEMA |
| B6 | **NAB2 reads DOWN in lesional AD skin** (per-cell: keratinocyte −0.51, T/NK −0.57) | 5.2 | **HIGH** (AD transcriptomes heavily mined) | V-DIR |
| B7 | **NAB2 = "Th2 brake"** lost in chronic lesions → restore/up-modulate, not knockdown (directional nomination) | 5.2 | MEDIUM (exploratory, well-hedged) | V-DIR |

## Phase-B verifier assignments (each runs REAL search_all queries, cites papers, verdicts)
- **V-GAP** — M1, M3 (the §2.4 conjunction + each named neighbor; the crux)
- **V-PRIM** — M2, M4, M8, M9, M10 (method-primitive prior art: selective prediction, grounded tool-use, LBD ranking, leakage, permutation controls)
- **V-AUDIT** — M5, M6, M7 (LLM-as-judge language critic, agentic reproducibility, cross-model replication)
- **V-TH2** — B1 (NAB2↔Th1/Th2 polarization; EGR/NAB axis)
- **V-ECZEMA** — B2, B3, B4, B5 (NAB2↔atopic dermatitis/eczema; 12q13 fine-mapping; STAT6 cis; CRISPRi spread lit)
- **V-DIR** — B6, B7 (NAB2 DE in lesional AD; Th2-brake / EGR-NAB negative regulation)

## Verdict vocabulary (Phase B)
NOVEL · PARTIALLY-ANTICIPATED · NOT-NOVEL · OVERSTATED · FALSE · UNVERIFIABLE-BY-LIT
Every verdict must cite specific papers (title/year/DOI). Each finding file ends with a
**"Retrieved evidence"** appendix (the actual papers + abstract snippets) so a different-model
cross-checker (Phase D) can independently re-adjudicate the same evidence.
