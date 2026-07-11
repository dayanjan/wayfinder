# 5. Discussion

> **DRAFT v1 — authored from OUTLINE v1.2 §5 + the finding/direction docs, consistent with §1–§4 (incl.
> the codex-debate-hardened §4).** Editorial "we"; calibrated language throughout (never
> proven/definitive/validated/genuine/discovered). Honors: R01 answer scoped to *triage/adjudication* not
> follow-up replacement (F-010); Limitations consolidate the §4 caveats including the debate-sharpened
> reading that the disease-hop stringency is substrate-inherited. ~1,450 words.

---

## 5.1 What the agentic loop changes

We opened with a critique the field has leveled at itself — that literature-based discovery "generates an
enormous number of hypotheses, almost none of which ever get followed up." Wayfinder is a response to that
critique, and it is worth being exact about *which* part of it we answer. We do not claim to have solved
experimental follow-up; the wet-lab confirmation of any surviving hypothesis remains future work, as it
must. What the approach changes is the step immediately before that: **triage**. Of 22,039
machine-generated gene→program→disease hypotheses, the deterministic referee reduced the set to a few
receipt-backed survivors — and, crucially, attached to each survivor a per-hop receipt and to each
rejection a reason. "Which of these thousands is worth a bench's time?" stops being a question answered by
literature-rarity heuristics (which, as we showed, track obscurity as readily as importance) and becomes a
question answered by a data test with a verdict a reader can inspect. That is a narrower claim than
"closing the LBD loop," and we prefer the narrower claim because it is the one the evidence supports.

Two properties of the loop do the work. The first is the willingness to answer *no*, and to distinguish a
*refuted* hypothesis from an *untested* one. A generator with no discriminating filter turns one flood into
another; a filter that only ever confirms is not a filter. The knockdown-QC gate is the sharpest expression
of this — a failed perturbation is reported as *untested*, never as a false "no effect" — and it is why the
approach can be trusted to reject as well as to nominate. The second is that the entire loop, generation
through self-audit, ran inside an agentic workbench in which an independent reviewer model enforced
calibrated language on the platform's own output. The paper's own thesis — that machine-generated science
must carry receipts and calibrated verdicts — was applied to the machine that generated it.

There is a reproducibility dividend here that we did not anticipate at the outset. The workbench exposes no
programmatic interface, so an analysis run in it is ordinarily a one-off, hand-paced web session. By driving
it headlessly and pulling its own provenance, we turned that one-off into a re-runnable, audited pipeline —
and the sensitivity analyses in §4.1b make the point concrete: the same panel, run locally and then inside
the workbench, reproduced byte-for-byte, verified by the workbench's own reviewer. An agentic analysis that
would otherwise be irreproducible-by-construction became reproducible. This is a small step, but a real one,
toward reproducible *agentic* science rather than merely reproducible code.

## 5.2 The next experiment the approach nominates

The value of an adjudication loop is not only that it culls, but that its survivors come with a sharp,
falsifiable next question. For NAB2, that question is directional. The Perturb-seq substrate tells us that
knocking NAB2 *down* reshapes the Th1/Th2 program; it does not tell us whether, in disease, one would want
more NAB2 or less. We pursued that question orthogonally — outside the Perturb-seq substrate — and report the
result as a nomination for the next experiment, not as a finding.

Two lines of evidence bear on it. First, NAB2 is not a cancer dependency in the DepMap screens, which is
consistent with (though not proof of) a regulatory rather than an essential role — non-contradictory context
rather than support. Second, and more informative, mining public expression data for the *direction* of the
NAB2–atopic-eczema association: in lesional atopic-dermatitis skin, NAB2 is **down** relative to non-lesional
(bulk log₂FC −0.32, FDR 0.002; anti-correlated with Th2 activity, ρ −0.34), and a single-cell analysis
confirmed this is a genuine per-cell reduction in the disease-relevant compartments (keratinocyte −0.51,
paired *p* 0.027; T/NK −0.57) rather than a shift in cell-type composition. Read together, these are more
consistent with NAB2 acting as a **Th2 brake that is lost or suppressed in chronic lesions** than as a Th2
driver — a reading that reconciles with the perturbation data (the brake is engaged during acute
polarization and lost in chronic disease; knocking it down removes it). If that reading holds, the naive
therapeutic move — topical knockdown — is likely *backwards*, and the direction to test is
**restoration or up-modulation** of NAB2.

We are candid about the ceiling on this. Expression tracks the direction of *association*, not the
distinction between an effector and a brake; the voting-arm evidence was mixed (one significant arm, others
ambiguous or null); and only a perturbation — showing that *restoring* NAB2 dampens the Th2 program — can
convert this brake hypothesis into a directional therapeutic claim. That perturbation is the experiment the
loop nominates. This is exactly the shape we argue for: the approach does not end the inquiry, it points a
bench at the one experiment most worth running.

## 5.3 Limitations

We inherit the LBD tradition of a candid limitations section, and there is a great deal to be candid about.

**The verdicts are nominations, not causal claims.** Every "supported" verdict means the chain held with a
receipt at each hop, not that the biology is established. This is sharpest at the disease hop, which is an
*association* receipt: the module–disease labels derive from genetic (GWAS-based) evidence with no
colocalization or linkage-disequilibrium control, so NAB2's atopic-eczema label could in principle be
LD-inherited from the adjacent 12q13 atopy locus. We falsified the *cis*-effect on STAT6's expression, which
addresses the perturbation signal; it does not settle the provenance of the GWAS label, which we leave open.

**The disease hop's stringency is substrate-inherited, not the referee's own discrimination.** Our
label-shuffle control (§4.1b) is the most important honesty check in the paper, and it returned a result we
report straight: the disease hop supports fewer than 1% of arbitrary gene×disease pairs, but so does a
random relabeling of the enrichment data — the near-total refutation rate is a property of the enrichment
study's FDR family, inherited by the referee, not a discrimination the referee itself supplies. The
referee's genuine confident-*no* edge lies in the knockdown-QC gate and the effect/program demotions, which
are its own computations; the disease hop's contribution is a stringent, label-dependent nomination filter,
and we claim no more for it.

**The funnel numbers are conditioned, not free-standing.** Within the pre-gated universe the program hop is
a tautology (`refuted_program ≡ 0`), so it discriminates in an individual receipt, not as a funnel filter;
and "43 supported" is a joint product of the literature-novelty gate and the referee (the referee alone
supports 395 of 47,220 pairs). We restate these in Results rather than burying them here.

**The substrate is bounded, and singular.** The adjudication is retrospective against one Perturb-seq
resource, one program (Th1/Th2), one cell type, and one set of aggregated tables; we ran no new wet-lab
experiment. The approach is only as good as the held substrate for a given claim, and it stays silent —
returning *untested* — where the substrate cannot speak, which is a feature, but also a boundary on scope.

**The determinism boundary, and where model judgment enters.** Every data receipt is deterministic code; the
language model interprets receipts and never computes one. But the objective's weights are a human design
choice (we showed the headline is robust to them, §4.1b), and the model's interpretive and provenance-writing
roles are judgment, not computation — so the calibrated-language discipline, and the independent critic that
enforces it, are load-bearing rather than cosmetic.

**The self-audit is within-family, and the automation depends on an unstable surface.** The workbench's
reviewer is an independent *role, model, and checkpoint*, but within a single model family; cross-family
independence is supplied externally (§4.6), not natively. And the headless driver depends on the workbench's
web front-end, for which there is no stable public contract — a reproducibility bridge over an API-less
platform, honestly, not a durable interface. If the front-end changes, the driver must be re-fitted.

## 5.4 Conclusion

Literature-based discovery has never lacked for hypotheses; it has lacked a disciplined way to decide which
ones to believe, and the candor to say *no*. Wayfinder pairs a machine hypothesis-generator with a
deterministic referee that adjudicates each proposal against a held experimental substrate and returns a
verdict with a receipt at every hop — supporting, refuting, or declining to test — and runs the whole loop,
including an audit of its own language, inside an agentic workbench whose work we can reproduce and inspect.
Applied to a genome-scale CD4⁺ T-cell resource, it culled tens of thousands of machine-generated hypotheses
to a small set of receipt-backed survivors, of which NAB2 → Th1/Th2 → atopic eczema is the worked example: a
literature-novel regulatory nomination whose sharpest artifactual confounder we falsified against the study
authors' own data, and which points to a concrete, falsifiable next experiment. The contribution is the
method and what it found — receipt-backed adjudication of machine-generated hypotheses, and the confident,
calibrated *no* that makes such adjudication worth trusting.
