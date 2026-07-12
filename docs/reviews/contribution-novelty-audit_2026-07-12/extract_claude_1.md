# Contribution / Novelty claim register — Extractor 1 (independent, uncontaminated)

Manuscript: *Receipt-backed prioritization for literature-based discovery using Perturb-seq evidence* (Wayfinder). Files read: main.tex (title+abstract), 01_introduction, 02_background, 03_methods, 04_results, 05_discussion.

Scope: every claim the paper presents as NOVEL or as a CONTRIBUTION (METHOD + BIOLOGY). Characterization only; no lit search, no final verdict.

---

## METHOD claims

### C1-01 — The headline method: receipt-backed prioritization with explicit abstention + falsification diagnostics
- **Type**: METHOD
- **Claim**: "The contribution is the method and what it found: **receipt-backed prioritization of machine-generated hypotheses, with explicit abstention and falsification diagnostics**." The core packaged contribution.
- **Location**: abstract; §1 (repeated verbatim); §5.4 conclusion.
- **Paper's own hedge**: "not a demonstration of predictive correctness"; "a prioritization method... none of these [validation steps] is gating for the present contribution"; explicitly narrower than "closing the LBD loop."
- **Novelty test**: Does any prior LBD/AI-scientist system combine (a) machine hypothesis generation, (b) a data-grounded prioritization verdict, (c) first-class *abstention*, and (d) first-class *falsification/refutation*, all with per-item receipts? Search: "literature-based discovery hypothesis prioritization experimental grounding", "hypothesis triage abstention refutation LLM", "evidence-grounded LBD ranking". Prior art defeating it = any single system already offering abstain+refute+receipt as a package.
- **Novelty-risk prior**: MEDIUM — the *packaging* is plausibly novel, but each ingredient (grounding, ranking, abstention) exists separately; a reviewer may see it as recombination.

### C1-02 — The specific gap: a deterministic (non-LLM) referee scoring each hypothesis against a HELD, pre-existing experimental substrate with per-hop experimental receipts
- **Type**: METHOD
- **Claim**: "We are not aware... of a system that does the specific combination Wayfinder targets: a **deterministic, non-LLM referee** that scores each hypothesis against a **held, pre-existing** experimental substrate and returns a per-hop **experimental** receipt... for every causal edge, with a quality-control-gated **abstention**... and a **falsification** as first-class verdicts." Contrasted against AI co-scientist, FutureHouse/Robin, SciAgents, PaperQA2, PerturbQA.
- **Location**: §2.4 (the novelty crux); Figure 1 caption.
- **Paper's own hedge**: "We are not aware, however" (claims novelty in *surfaced* systems, not proven absence); "narrow and specific." Careful not to strawman named neighbors.
- **Novelty test**: The load-bearing distinction is HELD/pre-existing substrate + deterministic referee. Candidate defeaters: (i) Robin (Bimson/FutureHouse) — does it adjudicate against *pre-existing* assay data rather than new experiments? (ii) any system using Perturb-seq/CRISPR screens as a retrospective validation oracle for LBD/LLM hypotheses; (iii) "knowledge-graph + experimental evidence scoring" systems. Search: "AI co-scientist held-out experimental substrate", "Robin FutureHouse assay data hypothesis", "CRISPR screen validate LLM hypothesis retrospective", "Perturb-seq hypothesis adjudication referee". Also check PerturbQA (perturbqa2025) framing.
- **Novelty-risk prior**: MEDIUM — the "held pre-existing substrate + deterministic (non-LLM) scorer" carve-out is genuinely specific and the paper defends it carefully; risk is that a retrospective-screen-grounding paper (esp. in the 2025-26 wave) already exists.

### C1-03 — QC-gated abstention: failed knockdown reported as *untested*, not *negative* (the "hero feature")
- **Type**: METHOD
- **Claim**: A knockdown that fails QC returns **untested**, distinguishing a *refuted* from an *untested* hypothesis — "an artifact caught rather than a false negative recorded." Framed as the moat / hero feature.
- **Location**: abstract; §1; §3.3 (hop 0); §4.2 (IL2); §5.1.
- **Paper's own hedge**: none on the concept; scoped by acknowledging within-funnel hops 0–2 are pre-gated so this edge is shown out-of-funnel (§3.3, §4.2b).
- **Novelty test**: Is "distinguish untested from negative via perturbation QC" a novel adjudication primitive, or standard practice in CRISPR-screen QC / three-way-classification ML? Search: "knockdown efficiency QC untested vs negative", "abstain uncertain gene knockdown screen", "selective prediction reject option biomedical hypothesis". The *reject option* / selective prediction literature is the real threat to novelty of the abstraction.
- **Novelty-risk prior**: MEDIUM — the biological framing (failed knockdown ≠ no effect) is sound and well-executed, but "abstain rather than assert on low-confidence input" is a known selective-prediction idea; novelty is in the LBD/perturb-seq application, not the primitive.

### C1-04 — Two distinct receipt classes (experimental vs genetic-association) kept explicit throughout
- **Type**: METHOD
- **Claim**: Knockdown/effect/program hops are **experimental receipts**; disease hop is an **association receipt** (GWAS-based nomination, not experimental causality) — the distinction is enforced textually and visually (Fig 1, Fig 4).
- **Location**: abstract; §2.2; §3.3; §4.3.
- **Paper's own hedge**: this IS the hedge apparatus; presented as epistemic discipline, not a strong novelty claim.
- **Novelty test**: Weak standalone novelty claim; more a calibration practice. Search only if audit wants: "receipt provenance experimental vs association hypothesis grounding".
- **Novelty-risk prior**: LOW-as-a-contribution — likely uncontested but also not a strong independent novelty claim (it's good hygiene, not a new method).

### C1-05 — Division of labor: LLM visible agency reserved for judgment/provenance; all data receipts from deterministic non-model code
- **Type**: METHOD
- **Claim**: "Every data receipt... is produced by deterministic code... the language model interprets receipts and assembles the verdict, but it never asserts a biological fact that a table value does not support. Visible agency is reserved for judgment, not for data retrieval." Positioned as what makes agentic LLMs "usable as an instrument."
- **Location**: §2.3; §3.1 ("no model computes a receipt"); §5.3.
- **Paper's own hedge**: acknowledges objective weights + interpretive role are human/model judgment (§5.3 determinism boundary).
- **Novelty test**: Is "deterministic tools for retrieval, LLM only for judgment" a novel architectural principle or standard tool-use / RAG-with-deterministic-tools doctrine? Search: "LLM deterministic tool grounding no hallucinated facts agent", "retrieval deterministic vs generative reasoning agent architecture".
- **Novelty-risk prior**: HIGH — this is essentially disciplined tool-use / grounded-RAG; the principle is widely stated. Novelty is application-specific at best.

### C1-06 — Actor–critic self-audit that enforces calibrated language on the platform's OWN output (flagged + removed "validated"/"definitive")
- **Type**: METHOD
- **Claim**: An independent reviewer model, at separate checkpoints, verified every number and enforced calibrated language on the manuscript-facing output — concretely flagging "validated" (title) and "definitive" (heading) as calibration violations, which were then removed. "The platform corrected its own overstatement."
- **Location**: abstract; §1; §2.3; §3.4; §4.5.
- **Paper's own hedge**: "role, model, and checkpoint independence... within a single model family, not cross-vendor"; "language hygiene plus receipt-consistency... not an independent epistemic verification that the underlying biology is correct."
- **Novelty test**: Is intra-family actor–critic review / LLM-as-judge enforcing calibrated hedging novel? Search: "LLM critic calibrated language scientific claims overstatement", "actor critic self-audit hypothesis language hedging", "LLM-as-judge overclaiming detection manuscript". Threat: extensive LLM-as-judge / self-critique literature.
- **Novelty-risk prior**: HIGH — actor–critic and LLM-as-judge are heavily prior-arted; the specific "remove overstated words from science output" application is a thin novelty slice.

### C1-07 — Headless scripting of an API-less agentic workbench (Claude Science) for replicable-in-principle agentic science
- **Type**: METHOD
- **Claim**: Claude Science exposes no programmatic task API; driving its web UI headlessly (auto-approving sandbox/working-dir/code/network cards for zero-click unattended operation) converts a one-off hand-paced web session into a "re-runnable, audited pipeline" — "an under-appreciated route to replicable-in-principle (UI-dependent) agentic science."
- **Location**: §3.4; §5.1 ("replicability dividend we did not anticipate").
- **Paper's own hedge**: "browser automation against a user interface with no stable public contract"; "replicable in principle — subject to the platform's UI remaining stable"; auto-approval "replaces a click, not a safety boundary."
- **Novelty test**: Is headless browser-driving of an LLM agent platform a novel methodological contribution or just Playwright automation? Search: "headless automation agentic workbench reproducibility", "browser automation LLM agent platform scripting science reproducibility". Likely no direct prior-art paper, but reviewers may deem it engineering not contribution.
- **Novelty-risk prior**: MEDIUM — probably no exact prior paper, but the "contribution" status is fragile (may read as tooling); low risk of being *already published*, higher risk of being *dismissed as not a scientific contribution*.

### C1-08 — The balanced novelty+effect ranking objective (min(z_ab,z_bc) + β·effect − w·ac_lit − w2·ac_known)
- **Type**: METHOD
- **Claim**: A ranking objective that balances the two literature legs (min term prevents one strong axis rescuing a weak other), rewards data-loudness, and pushes novel-yet-bridged candidates up *without* hard-gating zero co-mention (avoids rewarding obscurity). "The design of this objective is the only human judgment in an otherwise mechanical pipeline."
- **Location**: §3.2.
- **Paper's own hedge**: weights set priority not verdict; verdict is weight-independent; rank shown robust (§4.1b, §4.1c). Not loudly claimed as novel.
- **Novelty test**: Is the min-of-z balanced-bridge scoring novel vs classical LBD ranking (Arrowsmith, mutual information, min-of-strengths)? Search: "LBD ranking balanced ABC min strength z-score novelty penalty", "avoid rewarding obscurity understudied gene ranking".
- **Novelty-risk prior**: MEDIUM — bespoke formula, but structurally similar to existing LBD scoring; understated by the authors, low audit priority.

### C1-09 — Cross-family adversarial clean-room replication lab (5 members incl. cross-vendor Codex agents) as a verification method
- **Type**: METHOD
- **Claim**: A five-member replication lab (3 Opus-class + 2 different-vendor Codex agents), adversarial mandate, two clean-room re-implementations importing no pipeline code, unanimously reproduced every headline number AND caught real errors (cluster-ID misalignment, effect-size overstatement). Positioned as cross-family independence + evidence of computational robustness.
- **Location**: §2.3, §3.4 (iii); §4.6.
- **Paper's own hedge**: "evidence of computational robustness, not of biological validity."
- **Novelty test**: Is multi-agent cross-model clean-room replication a novel verification methodology? Search: "multi-agent adversarial replication reproducibility LLM clean-room", "cross-model verification computational reproducibility agents". Likely no direct prior paper; risk it reads as good practice rather than a contribution.
- **Novelty-risk prior**: MEDIUM — novel-ish as a described practice; weak as a headline scientific contribution.

---

## BIOLOGY claims

### C1-10 — NAB2 is a Th1/Th2 (Th2) regulator — a re-derived regulatory role the literature has not made
- **Type**: BIOLOGY
- **Claim**: Perturbation data support NAB2 as a Th1/Th2 regulator with a receipt at every experimental hop (2/2 guides, effect −16.9, 301 downstream DE, Ota z=7.71). "Consistent with a re-derived NAB2 → Th1/Th2 → atopic-eczema chain the literature has not made." NAB2's only prior described T-cell role is EGR-family coregulator (Egr-1/NAB2 tuning T-cell activation), distinct from Th1/Th2 polarization.
- **Location**: abstract; §1; §4.3; §5.4.
- **Paper's own hedge**: "consistent with / re-derived," never "discovered/proven"; novelty from a "targeted agent search, not an exhaustive systematic review — novelty in the surfaced literature rather than proven absence."
- **Novelty test**: THE central biology novelty. Search hard for any prior NAB2–Th2/Th1/T-helper-polarization link. Queries: "NAB2 Th2 polarization", "NAB2 Th1 Th2 T helper differentiation", "NGFI-A binding protein 2 T cell polarization", "NAB2 GATA3 IL4", "NAB2 EGR2 Th2". Also check whether NAB2's known EGR2/EGR3 partnership (EGR2/3 are established Th differentiation regulators) already implies a polarization role — if EGR2/NAB2 → Th2 is documented, novelty is weakened.
- **Novelty-risk prior**: MEDIUM — NAB2 is understudied in polarization specifically, but its tight coupling to EGR2/EGR3 (known Th differentiation factors) means an existing NAB2/EGR2→Th link is plausible; this is the single highest-value item to search.

### C1-11 — NAB2 → atopic eczema is a literature-novel nomination
- **Type**: BIOLOGY
- **Claim**: An independent four-agent literature audit surfaced no papers connecting NAB2 to atopic eczema; the eczema link is a genetic-association nomination (Open Targets GWAS-based label, no coloc/LD control). "Literature-novel regulatory nomination."
- **Location**: abstract; §1; §4.3; §5.4.
- **Paper's own hedge**: heavily hedged — nomination not causal claim; "novelty in surfaced literature"; foregrounds the unresolved 12q13 LD-provenance confounder as the key open question (§4.4b, §5.3).
- **Novelty test**: Is NAB2 already associated with atopic dermatitis/eczema in GWAS/literature? CRITICAL: NAB2 sits in the 12q13 atopic-dermatitis locus adjacent to STAT6 — so a NAB2–eczema *association* may ALREADY be reported (as a locus gene) in AD GWAS papers (e.g. Paternoster 2015). Search: "NAB2 atopic dermatitis GWAS", "12q13 atopic dermatitis NAB2 STAT6 locus genes", "NAB2 eczema association". If NAB2 is already a named candidate at the 12q13 AD locus, the "novel disease link" claim is substantially weakened (though the authors partly pre-empt this via the LD-inheritance caveat).
- **Novelty-risk prior**: HIGH — the gene is literally in a known AD GWAS locus; a prior NAB2–eczema *association* mention is quite likely. The paper's own LD-confounder framing implicitly concedes the association may not be NAB2-specific.

### C1-12 — The STAT6 cis-effect confounder is ruled out at the expression level (STAT6 unmoved under NAB2 KD)
- **Type**: BIOLOGY (also a method demonstration)
- **Claim**: Against the study authors' genome-wide DE matrix, STAT6 is unmoved under NAB2 knockdown (log2FC +0.087, adj p 0.788; ranks 5,444/10,282). "No detectable STAT6-expression cis-effect" — signal consistent with NAB2 perturbation, not STAT6 bleed.
- **Location**: abstract; §1; §4.3; §4.4; §4.4b(i).
- **Paper's own hedge**: "ruled out *at the expression level*"; "one aggregate Stim8hr expression null excludes a detectable expression-level cis-effect, not every conceivable cis channel"; does not prove the disease link.
- **Novelty test**: This is a novel *analysis result* on public data, not a literature claim — hard to defeat by prior art (nobody else ran this specific check). Audit relevance: confirm the data reading is defensible, not that it's "already known." Minimal external search.
- **Novelty-risk prior**: LOW — a bespoke re-analysis result; unlikely to be "already published." Risk is analytical correctness, not novelty.

### C1-13 — NAB2 as a "Th2 brake" lost/suppressed in chronic atopic-dermatitis lesions (directional nomination)
- **Type**: BIOLOGY
- **Claim**: Exploratory mining of lesional-vs-non-lesional AD expression shows NAB2 reads *down* in lesional skin (bulk log2FC −0.32, FDR 0.002; ρ −0.34 with Th2 activity; single-cell keratinocyte −0.51, T/NK −0.57) — "more consistent with NAB2 acting as a Th2 brake that is lost or suppressed in chronic lesions than as a Th2 driver." Implies naive topical-knockdown therapy is "backwards"; restoration is the direction to test.
- **Location**: §5.2.
- **Paper's own hedge**: strongly hedged — "report as a nomination for the next experiment, not as a finding"; "exploratory mining... outside the referee substrate"; "advance the brake model as the directional *question* to test rather than an established concordance"; concordance turns on an unsettled sign.
- **Novelty test**: Is NAB2 downregulation in lesional AD already reported? Search: "NAB2 expression lesional atopic dermatitis skin", "NAB2 downregulated eczema keratinocyte", GEO AD lesional datasets for NAB2. Also: is a "Th2 brake" role for NAB2/EGR2 known?
- **Novelty-risk prior**: MEDIUM — AD lesional transcriptomes are heavily mined; a prior NAB2-differential-expression observation in AD is possible, though the "brake" interpretation is the authors' own and well-hedged.

### C1-14 — Verdict-ledger biology exemplars (EGR2→asthma supported; NUDT1→T1D supported-weak; IL2 untested; SLC1A5→T1D refuted)
- **Type**: BIOLOGY (used as method demonstrations, not asserted as novel findings)
- **Claim**: Five genes span the verdict space with per-hop receipts, demonstrating the referee discriminates. Explicitly "drawn to span the verdict space, not sampled to estimate a rate."
- **Location**: §4.1 (Table 2); §4.2 (IL2, SLC1A5).
- **Paper's own hedge**: strong — "a demonstration that the referee discriminates... not as a measured precision or recall"; not claimed as novel biology.
- **Novelty test**: Not asserted as novel biology, so low audit priority. Only relevant if a claim (e.g. EGR2→asthma) is implicitly presented as a discovery — it is not.
- **Novelty-risk prior**: LOW — explicitly framed as illustrative, not novel findings.

### C1-15 — Hard-negative out-of-funnel discriminations (IL36RN×psoriasis, TREX1×lupus, PADI4×RA returned *untested* for failed knockdown)
- **Type**: BIOLOGY-adjacent METHOD demonstration
- **Claim**: Strongly database-associated flagship pairs are returned *untested* because their knockdown failed QC in this screen — the referee's own edge over a curated-association nominator. ~1 in 6 top nominations flagged.
- **Location**: §4.2b; Fig 3C.
- **Paper's own hedge**: framed as demonstration of the referee's own-hop discrimination, scoped to "in this screen."
- **Novelty test**: Not a biology-novelty claim (these are well-known disease genes); it's a demonstration that DB association ≠ measurability. Low audit priority. Confirm the QC-failure calls are correct in the source data.
- **Novelty-risk prior**: LOW — no novelty asserted; the value is methodological.

### C1-16 — Replicability dividend: an agentic analysis that is "irreproducible-by-construction" made "replicable in principle" (byte-for-byte native reproduction)
- **Type**: METHOD (repeat/refinement of C1-07, but distinct claim)
- **Claim**: The sensitivity panel reproduced byte-for-byte and the funnel digit-for-digit when the workbench was driven programmatically; "a small step, but a real one, toward replicable-in-principle agentic science rather than merely reproducible code."
- **Location**: abstract; §5.1; §4.5.
- **Paper's own hedge**: "subject to the platform's UI remaining stable"; "replicable in principle."
- **Novelty test**: Overlaps C1-07. Search: "reproducibility agentic AI science pipeline byte-for-byte", "replicable agentic analysis workbench".
- **Novelty-risk prior**: MEDIUM — as a framed contribution it's distinctive but modest; treat with C1-07.

---

## Extractor 1 — honest first read

Pre-search impression, clearly labeled. This reads as a *genuine but modest* recombination contribution rather than a breakthrough. The strongest and most defensible novel move is the specific architectural carve-out (C1-02): a deterministic, non-LLM referee adjudicating LLM/LBD hypotheses against a *held, pre-existing* experimental substrate with abstention and refutation as first-class verdicts — the §2.4 related-work framing is careful and non-strawman, which is a good sign, but the whole claim rests on "we are not aware of," and the 2025-26 AI-scientist wave is crowded, so a near-neighbor could exist. Several method claims (C1-05 deterministic-tools-only, C1-06 actor–critic language critic, C1-03 abstention-as-reject-option) are individually well-worn ideas from tool-use/selective-prediction/LLM-as-judge literatures; their novelty is application-specific and a skeptical reviewer could deflate them. The biology is honestly the weakest novelty flank: NAB2 sits *inside* a known 12q13 atopic-dermatitis GWAS locus next to STAT6, so a prior NAB2–eczema association mention is quite plausible (the authors half-concede this via the LD-inheritance confounder they foreground) — C1-10 (NAB2 as Th2 regulator) and C1-11 (NAB2–eczema novelty) are the two items a searcher must hit hardest, especially checking whether NAB2's established EGR2/EGR3 coupling already implies a polarization role. The paper's hedging is unusually disciplined and largely pre-empts overclaiming; the audit's real job is (a) find a prior held-substrate-referee system, and (b) confirm/deny prior NAB2–Th2 and NAB2–eczema links.
