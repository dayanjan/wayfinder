# 4. Results

> **DRAFT v1 — authored from repo-verified finding docs + OUTLINE v1.2 §4.** Editorial "we" (FRMA
> convention; solo author). Calibrated language throughout — never "proven / definitive / validated /
> genuine / discovered". Honors: ledger *demonstrates* discrimination, not an accuracy benchmark (F-003);
> program hop is a within-funnel tautology and "43 supported" is a joint gate×referee product (F-004);
> three liveness claims kept distinct (F-005); manuscript-facing verdicts cite post-critic receipts (F-007);
> two receipt classes (F-008); self-audit = role/model/checkpoint independence (F-009). ~1,850 words.
> **Sensitivity numbers (§4.1b) are computed** by `docs/manuscript/analysis/sensitivity_panel.py`
> (cache-free, deterministic) and were **independently reproduced inside Claude Science — byte-identical
> (delta 0, identical sha256), Reviewer-verified** (`analysis/cs-reproduction/COMPARE.md`), the same
> dogfood gate §4.5 describes. All other numbers are repo-verified (claim inventory C1–C21). **Note:**
> Control 2 returned a nuanced result — the disease hop's near-total refutation rate is largely *inherited
> from the enrichment FDR family* (observed pass count is 5.6 SD *below* the label-shuffle null, not above)
> — reported honestly rather than forced into the anticipated "rarer-than-chance" story.

---

We report six results. The funnel and verdict ledger show the referee discriminating across a spread of
worked examples (§4.1), and two negative controls plus a rank-stability check probe how much of that
discrimination is a property of the data versus an artifact of the setup — with one control returning a
deliberately honest, non-obvious answer (§4.1b). The confident *no* and the quality-control
catch are examined on their own (§4.2), because they are the point. NAB2 is then followed hop by hop as the
worked hero (§4.3), and its sharpest artifactual confounder is falsified against the study authors' own
genome-wide data (§4.4). Finally we show the entire loop reproduced natively inside the agentic workbench,
audited by an independent critic model (§4.5), and replicated by a second vendor's models (§4.6).

## 4.1 The funnel and the verdict ledger

At the 8-hour stimulation condition, the generator built a disease-answer-free universe of **3,935**
knockdown-gated, program-significant genes, from which the gate admitted **22,039** eligible
(gene, disease) pairs. Running the deterministic referee over those pairs returned **43** with a positive
disease hop, of which **30** held the full chain cleanly (nonzero positive effect); the remainder split into
10 effect-zero *supported-weak*, 3 off-target *supported-flagged*, and 1 *refuted-effect*, with the other
**21,995** pairs *refuted for the specific disease* (Table 3). The generate-to-cull ratio is the headline
shape: 22,039 machine-generated questions reduced by data receipts to 30 clean survivors, none asserting
more than a table value supports.

We are deliberately careful about what this funnel does and does not demonstrate, and we restate the two
honesty caveats here rather than defer them to Limitations. First, the universe **A** is preselected on
program-significance, so *within the funnel* the program hop cannot fail (`refuted_program ≡ 0` by
construction); the dominant cull among eligible pairs is therefore disease-specificity, not broad four-hop
falsification. The program hop discriminates in an individual triple's receipt (a reported quantity — NAB2's
Ota *z* = 7.71), not as an independent filter on funnel survivors. Second, the "43" is a **joint** product
of the literature-novelty gate and the referee, not a referee-only count: the referee alone supports
**395 of 47,220** pairs, and the novelty gate culls 395 → 43. The honest reading is "referee-supported
*among literature-eligible* pairs." Accordingly we present the ledger below as a **demonstration that the
referee discriminates** — that on worked examples it will support, decline to test, and refute, each with a
receipt — not as a measured precision or recall.

The verdict ledger (Table 2) places five genes across the full verdict spectrum, each with its per-hop
receipt:

| Gene → disease (condition) | Verdict | Deciding receipt |
|---|---|---|
| **NAB2** → atopic eczema (Stim8hr) | **supported** | full chain holds; eczema clusters OR 3.90 / FDR 0.0028 and OR 3.43 / FDR 0.0224 (§4.3) |
| **EGR2** → asthma (Stim8hr) | **supported** | 2/2 guides signif; effect −11.06, 854 downstream DE; member of 34 disease clusters, asthma OR 20.4 / FDR 5×10⁻⁵ |
| **NUDT1** → type 1 diabetes (Stim8hr) | **supported-weak** | full chain holds but a trivial effect (4 downstream DE) — the *only* pure-disjoint (zero-literature) survivor |
| **IL2** → (Rest) | **untested** | knockdown-QC fails: 0/2 guides significant; target barely expressed at Rest, nothing to knock down |
| **SLC1A5** → type 1 diabetes (Stim8hr) | **refuted** | in 9 disease cluster gene-sets, but none reach FDR < 0.05 (best FDR 0.054, OR 2.73) |

Two features of the ledger carry the thesis. The *untested* verdict (IL2) is not a missing entry or a
failure to compute — it is the referee refusing to read an uninterpretable knockdown as a biological
result. And the *refuted* verdict (SLC1A5) is a plausible metabolite-transporter → autoimmunity link that
the enrichment data decline to support: a confident, receipt-backed *no*. NUDT1 illustrates the opposite
edge — a hypothesis that clears every hop yet is foregrounded only weakly, because its effect is trivial;
this is exactly why the pipeline *ranks* by a novelty-plus-effect score rather than hard-gating on
zero-literature absence, which would reward obscurity (§3.2). We note that these examples are drawn to span
the verdict space, not sampled to estimate a rate; §4.1b supplies a disease-hop support-*rate* control over
the full A×C space — not a ledger accuracy rate, nor a claim of precision or recall.

## 4.1b Sensitivity: two negative controls and rank stability

To move "the referee discriminates" from assertion to a small measured result, we ran three checks as a
bounded kernel analysis inside the workbench (§3.4).

**Control 1 — the QC gate does its job.** We applied the referee to every gene whose knockdown *fails* QC
at the 8-hour condition (no guide reaching a significant knockdown call in T4): **2,430** genes. All 2,430
returned *untested* at hop 0 — a **100%** rate, with no leakage into a spurious *refuted* or *supported*
verdict. The gate converts failed experiments into an honest "cannot say," exactly as designed, and does so
without exception across the full failed-knockdown set.

**Control 2 — the disease hop's stringency is substrate-inherited, and its pass count is label-dependent.**
Across the referee's native pair space of all **47,220** (gene ∈ A) × (disease ∈ C) combinations at the
8-hour condition, the disease hop supports only **406 (0.86%)** and refutes the remaining **99.14%**. That
stringency, however, is not the referee's own doing: under **2,000** permutations of the disease labels
across the enrichment rows, the null still passes only **467.7 ± 10.9** pairs — a null pass rate of
**0.99%** — so even randomly-labelled pairs clear FDR < 0.05 barely more than one percent of the time. The
near-total refutation is therefore **inherited from the enrichment study's FDR family** — a
substrate-provenance property we flag in Limitations (§5.3), and one an adversarial replication
independently noted — not a discrimination we should credit to the referee. What the permutation *does*
establish is that the pass count is **label-dependent**: the observed 406 sits **5.6 standard deviations
below** the null mean (lower-tail permutation *p* ≈ 5×10⁻⁴; the *upper*-tail *p* is 1.0 — that is, the hop
does **not** pass *more* often than chance, so we explicitly do not claim a "rarer-than-chance"
selectivity). The direction — observed *below* null — is a feature of this restricted twelve-disease
permutation setup; the one component we actually measured, a per-gene concentration effect, is small (a
passing gene carries **2.39** distinct disease labels under the true assignment versus **2.44** under
shuffling), so we report the figures but do not interpret the mechanism of the direction further. The load-bearing reading is the
one we can defend on both tails: the disease hop is a **stringent, label-dependent nomination filter whose
stringency is substrate-inherited** — not a demonstration of the referee's own discriminating power. (This
control speaks to the disease hop; it does not re-open the program-hop tautology of §3.3, which is a
construction property, not a chance one.)

**Rank stability under alternative objective weights.** The ranking objective (§3.2) has three free weights
(β on effect, *w* on direct co-mention, *w₂* on curated association; default β = 1, *w* = 1, *w₂* = 3). The
weights set *priority* among eligible survivors, not the supported/refuted verdict, which is
weight-independent by construction — but a headline example that is rank-4 only at one weight setting would
be a fragile choice of hero. We recomputed the ranking over a **27-point grid** crossing β ∈ {0.5, 1, 2},
*w* ∈ {0.5, 1, 2}, and *w₂* ∈ {1, 3, 5}, recovering each survivor's weight-independent score component from
its default-weight value and re-ranking under every setting (the default setting reproduces NAB2's rank of
4, confirming the recovery). NAB2's rank ranged from **1 to 8** across the grid, with a **median of 4**, and
it stayed within the top five survivors under **24 of the 27** settings (89%). No survivor's *verdict*
changed, since verdicts do not depend on the weights. The worked hero is robust to the one human judgment
(§3.2) in an otherwise mechanical pipeline.

## 4.2 The confident *no*, and the quality-control catch

The moat of this approach is a referee that will answer *no* — and that distinguishes a *refuted*
hypothesis from an *untested* one. Both behaviors appear in the ledger, and both are worth stating plainly.

IL2 is the quality-control catch. IL2 is a canonical, biologically central T-cell gene that appears in both
the Th program and the disease gene-sets; a naive pipeline that read the empty downstream result of a
failed knockdown would call it "no effect" and record a false negative. The referee instead halts at hop 0:
0 of 2 guides reach a significant knockdown (guide mean expression 0.031 vs. non-targeting-control 0.036 —
the target is barely expressed at Rest, so there is nothing to knock down), and the verdict is *untested —
knockdown failed QC*. An artifact is caught, not mistaken for biology.

SLC1A5 is the correctly-sourced refutation. A metabolite transporter with a plausible metabolic-gene →
autoimmunity story, SLC1A5 clears the QC gate (1/2 guides significant) and shifts the Th1/Th2 program, yet
its disease hop *refutes*: it appears in nine autoimmune-disease cluster gene-sets but none reaches
FDR < 0.05 (best FDR 0.054, type 1 diabetes, OR 2.73). The enrichment data decline the link. This is the
verdict a confirmation-shaped pipeline never produces, and it is deterministic — the *no* is computed, not
argued.

## 4.3 NAB2 → Th1/Th2 → atopic eczema, hop by hop

The highest-ranked near-novel survivor is **NAB2**, near-novel by an operational criterion — low direct
literature co-mention (`ac_lit` = 6) and no curated Open Targets association (`ac_known` = 0.038) — rather
than strict Swanson-style A–C absence. The data support NAB2 as a Th1/Th2 regulator with a receipt at every
hop (Figure 4):

- **Hop 0 — knockdown QC.** 2/2 guides significant, best adjusted *p* ≈ 1×10⁻¹⁶ (guide expression 0.056
  vs. non-targeting control 0.567). The perturbation worked.
- **Hop 1 — effect.** On-target knockdown, effect −16.9, **301 downstream differentially expressed genes**,
  no off-target flag. A large, clean transcriptional consequence.
- **Hop 2 — program.** Th2-associated in the Ota contrast (*z* = 7.71, adjusted *p* = 1.96×10⁻¹³,
  log-fold-change +0.63; polarity marker-checked); not significant in the Höllbacher contrast — one of
  two contrasts, reported rather than hidden.
- **Hop 3 — disease.** Member of two atopic-eczema-enriched modules: OR 3.90 (FDR 0.0028) and OR 3.43
  (FDR 0.0224). These are genome-wide functional immune modules (significant clusters 90 and 100 —
  BACH2, BCL6, IRF4, CD28, IL4, IL10), not a 12q13 locus artifact.

The calibrated claim is: *consistent with a re-derived NAB2 → Th1/Th2 → atopic-eczema chain the literature
has not made.* We keep the two receipt classes explicit even for the hero — the knockdown, effect, and
program hops rest on experimental perturbation measurements; the atopic-eczema link is a **genetic-
association nomination** (an Open Targets GWAS-based disease label, without colocalization or LD control),
not an expression claim or a proof of disease causality. An independent four-agent literature audit found
zero papers connecting NAB2 either to Th1/Th2 polarization or to atopic eczema — the finding is novel in
the literature — and the same audit surfaced the confounder we take up next.

## 4.4 Falsifying the hardest confounder: the STAT6 *cis*-effect

NAB2 sits ~1.9 kb from *STAT6*, the master type-2/atopic regulator, so the sharpest artifactual explanation
of NAB2's *perturbation* signal is a CRISPRi *cis*-effect: a guide targeting NAB2 could inadvertently
repress the adjacent STAT6, and the observed Th2/eczema signal could be STAT6's, not NAB2's. We test this
directly against the study authors' own deposited genome-wide differential-expression matrix (the 16.8 GB
`GWCD4i.DE_stats.h5ad`, read lazily from public object storage by byte-range, no download). Under NAB2
knockdown at Stim8hr:

| Gene (under NAB2-KD) | log₂FC | adj. *p* | moved? |
|---|---:|---:|:--:|
| **STAT6** (neighbor under test) | **+0.087** | **0.788** | no — **unmoved** |
| **NAB2** (self / on-target) | **−3.078** | 7.2×10⁻⁶⁰ | yes — knockdown worked |

Of 10,282 measured genes, 302 are significantly moved by NAB2 knockdown (≈ the referee's effect count of
301); STAT6 is not among them, ranking 5,444/10,282 by absolute log-fold-change — the less-affected half. A
*cis*-artifact would push STAT6 *down*; it does not move. Three further checks corroborate this — drawn from
the study's own QC fields and our finding analysis rather than the genome-wide DE row above: NAB2 and STAT6
share zero perturbation-effect clusters (their knockdowns are not equivalent); NAB2 clears the study's own
reproducibility bar (cross-guide/donor R 0.74); and the authors' own off-target flag — a transcription
start site within 10 kb showing significant down-regulation — is False for NAB2, meaning their pipeline
already found no *cis* down-regulation of any near neighbor, STAT6 included. We therefore report the
*cis*-artifact as **refuted**: the signal is consistent with NAB2 perturbation rather than STAT6 bleed. We
scope the claim precisely — this strengthens the case that the *perturbation* signal is NAB2-specific; it
does not prove the disease link, which remains a genetic-association nomination.

## 4.5 Native reproduction and self-audit in Claude Science

The entire loop — generation, adjudication, and the assembly of its own provenance — was run inside the
agentic workbench, at a total run cost of ~$6.41, with the model identities, per-step costs, and reviewer
checks drawn from the workbench's own audit store. We keep the three liveness claims distinct (§3.4). *Full-
scale reproduction*: the real generator ran unchanged over the entire 3,935-gene universe inside the
workbench and reproduced the exact funnel (3,935 → 22,039 → 43 → 30) and NAB2's rank of 4, but against a
workbench-local cache of previously captured literature/association responses under a guard that raises on
any live network call (cache delta zero) — a faithful recomputation, not a live crawl. *Live authorship*: a
separate 12-gene from-scratch run, given only the method, had the workbench write its own generator and make
live Europe PMC and Open Targets calls; NAB2's effect was too low to rank in that small run's top twelve, so
it did not appear — nothing was cherry-picked — and independent re-querying of the workbench's recorded
queries against the live APIs returned identical counts. *Cross-family independence* is kept external by
design (§4.6).

The self-audit is the part that mirrors the paper's own thesis (Figure 5). The author model (an Opus-class
model) assembled the end-to-end receipt chain; an independent reviewer model (a Sonnet-class model),
invoked at separate checkpoints, verified every reported number against the underlying artifacts and
enforced calibrated language on the manuscript-facing output. It produced four verification checks: two
confirming that every cited receipt and the final "what ran where" table matched the source of truth, and —
the telling one — a check that **flagged the words "validated" (in a title) and "definitive" (in a heading)
as calibrated-language violations, both of which were then removed**. The platform corrected its own
overstatement. We characterize this independence honestly: it is *role, model, and checkpoint* independence
— a distinct reviewer model at distinct verification points within a single model family — not independence
across vendors. It is also why manuscript-facing verdicts cite the post-review receipt rather than the raw
generation log, which still carries a pre-critic "validated" string in a free-text field: that pre- to
post-critic difference *is* the self-audit.

## 4.6 Independent cross-model replication

Cross-family independence was supplied from outside the workbench, by a five-member replication lab: three
Opus-class agents and two Codex (a different vendor's) agents, each re-deriving the finding from the raw
supplementary tables under an adversarial mandate, with two members performing clean-room re-
implementations that imported none of our pipeline code. The verdict was a **unanimous pass**. Across the
lab, every headline number was independently reproduced to the unit — not every member re-checked every
number, but each number was re-derived from the raw CSVs by at least one clean-room member: the NAB2 receipt (2/2 guides,
effect −16.88, 301 downstream DE, Ota *z* +7.71, eczema clusters OR 3.90/3.43), the full funnel
(3,935 → 22,039 → 43 → 30, with the 30/10/3/1 class split and the single pure-disjoint survivor), and the
answer-free construction of the universe.

The replication is worth reporting precisely *because* it was not silent agreement: the adversarial pass
caught and corrected real errors. It found a cluster-ID misalignment in our confounder script — sorted
cluster IDs printed against row-order FDRs had mislabeled NAB2's significant eczema modules as 74/90 when
the true significant modules are 90 and 100 (cluster 74 is non-significant, FDR 0.52), and the locus test
had been run on the wrong cluster; the corrected run confirms modules 90 and 100 are genome-wide functional
immune modules with STAT6 absent, which rejects the *cluster-membership* locus artifact — though not the
distinct question of whether the GWAS disease *label* is LD-inherited from the 12q13 atopy locus, which the
substrate cannot settle and which we leave open (§5.3). It corrected an effect-size overstatement ("~8× stronger" is the
log-fold-change ratio; the *z*-ratio is ~3×). And it reframed the distinctness argument onto its strongest
support — cluster co-membership, magnitude, and guide-specificity — rather than the shared disease profile,
which if anything *aids* the confounder. That a hostile independent re-derivation reproduced every number
and improved the framing is the strongest available evidence that the finding is a property of the data,
not of our implementation.
