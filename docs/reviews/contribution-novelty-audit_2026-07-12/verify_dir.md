# V-DIR — literature-novelty audit of the directional/therapeutic nomination (B6, B7)

Scope: §5.2 of `05_discussion.tex` ("The next experiment the approach nominates").
Both claims are framed in the manuscript as **exploratory nominations**, not findings —
graded here against *that* bar (is the hedge adequate?), plus the raw novelty question.
Tool: live `search_all` (OpenAlex-backed), 16 queries + 3 abstract pulls, run from repo root.
Cannot prove a negative; queries + retrieved evidence listed in the appendix.

---

## B6 — "NAB2 reads DOWN in lesional atopic-dermatitis skin"
(bulk log2FC −0.32 FDR 0.002; single-cell keratinocyte −0.51, T/NK −0.57)

**VERDICT: UNVERIFIABLE-BY-LIT (lean PARTIALLY-ANTICIPATED) — hedge ADEQUATE.**

Across ~7 queries aimed squarely at NAB2 in AD/eczema transcriptomes (lesional DE, keratinocyte,
single-cell, bulk) I retrieved dozens of AD DE / scRNA-seq papers — the compartment is heavily
mined (Guttman-Yassky-type signature studies, spatial, single-cell atlases, TWAS/eQTL) — but **not
one names NAB2** as a reported differentially-expressed gene in AD. So NAB2 is not a *reported/
headlined* AD-DE finding in the retrievable literature.

The decisive caveat: `search_all` indexes titles + abstracts, **not supplementary DE tables**. A
gene with a modest −0.32 log2FC is precisely the kind of entry that lives buried in a supplement of
one of these many studies, never surfacing to a title/abstract. Given how exhaustively these exact
datasets are re-analyzed, NAB2 very likely *appears* in some supplement — I simply cannot confirm or
deny it with this tool. Hence UNVERIFIABLE-BY-LIT, not NOVEL.

This does not wound the paper: §5.2 explicitly calls B6 an "*exploratory* mining … for the
*direction* of the association," used as directional support, not a headline discovery. It claims no
novelty for B6. **Against that bar the hedge is fully adequate** — arguably it could add one clause
("the gene may appear in prior DE supplements; we make no priority claim") to be bulletproof, but
the current framing does not overclaim.

**Moves science forward?** Marginally and only as intended — a direction-of-association check that
feeds B7. Not a standalone contribution, and not presented as one.

---

## B7 — "NAB2 = Th2 BRAKE lost/suppressed in chronic lesions → restore/up-modulate, not knockdown"

**VERDICT: PARTIALLY-ANTICIPATED (mechanism) + NOVEL (the specific AD nomination) — hedge ADEQUATE.**

Two layers, and they cut in opposite directions — which is why the hedge matters.

**The module-level premise is well-established (PARTIALLY-ANTICIPATED).** NAB2 is the obligate
transcriptional **corepressor of the EGR family**, and EGR2/EGR3 are canonical **negative regulators
of T-cell inflammation**:
- Egr2/3 deletion → lethal autoimmune syndrome; Egr2/3 induce SOCS1/3 and control inflammation
  (Immunity 2012, `10.1016/j.immuni.2012.08.001`).
- Egr2/3 directly inhibit T-bet → suppress Th1/IFN-γ (J Immunol 2017, `10.4049/jimmunol.1602010`).
- "Egr2 and Egr3 are unique regulators in immune system" (CEJI 2017, `10.5114/ceji.2017.69363`);
  Egr2/3 control homeostasis of PD-1^high memory CD4 T cells (Life Sci Alliance 2020,
  `10.26508/lsa.202000766`).

So "the EGR/NAB corepressor module can act as an inflammation brake in T cells" is **not novel** — it
is textbook. A reviewer *will* raise the EGR2/3 literature.

**But the specific directional nomination is unpublished (NOVEL), and the direction is genuinely
unsettled.** No paper proposes **NAB2 specifically as a Th2/type-2 brake**, nor **"restore NAB2" as a
therapeutic direction in atopic dermatitis / allergic disease**. My "Th2 brake TF in AD", "NAB
corepressor type-2 inflammation", "NAB2 asthma/allergy" and "NAB2 restore therapeutic target"
queries returned nothing on point. Moreover the module's directionality in *type-2* immunity is
messy, not clean-brake: EGR2 is a **direct STAT6 target and the linchpin of IL-4-driven alternative
(type-2) macrophage polarization** (Genes Dev 2020, `10.1101/gad.343038.120`) — i.e., in that axis
EGR2 is *pro*-type-2, which would make NAB2 (its repressor) anti-type-2 = a brake by one chain of
inference, while the Egr2/3-inhibits-T-bet result implies EGR2 is anti-Th1/permissive-to-Th2, which
routes the sign differently. The literature does **not** settle whether NAB2 is a Th2 brake.

That ambiguity is exactly what §5.2 says: "a reading whose concordance … turns on the *sign* … which
the substrate's directional metrics do not by themselves settle here, so we advance the brake model
as the directional *question* to test." **The hedge is not just adequate — it is precisely
calibrated to the real state of the literature.** The established EGR2/3-brake biology actually
*strengthens* the nomination (it is biologically grounded, not a guess), while the manuscript
correctly refuses to claim the sign is established.

**Moves science forward?** Yes, as a hypothesis. It is a testable, mechanism-grounded directional
nomination, and its sharpest value — flagging that the naive "topical knockdown" move may be
**backwards** — is a genuine, non-obvious contribution of the triage loop. That is the "point a bench
at one experiment" value the paper claims, delivered honestly.

---

## One caution for the operator (not a defect, a robustness note)
The EGR2-is-a-STAT6-target result (Genes Dev 2020) is a double edge: it ties NAB2's module directly
to STAT6 (the very gene the 12q13/`cis` confounder of B2/B3 concerns) **and** shows EGR2 can be
*pro*-type-2, so a determined reviewer could argue the brake sign should flip. The manuscript already
concedes the sign is unsettled, so this is survivable — but if §5.2 has room, a half-sentence
acknowledging "EGR2 is itself a STAT6-driven pro-type-2 factor in some compartments, so the module's
net sign is context-dependent" would pre-empt the objection and read as even-handed.

---

## Retrieved evidence (closest papers)

### NAB2 / EGR-NAB as negative regulator / corepressor (bears on B7)
- Zheng, Li et al. **"The transcription factors Egr2 and Egr3 are essential for the control of
  inflammation and antigen-induced proliferation of B and T cells."** *Immunity* 2012.
  `10.1016/j.immuni.2012.08.001` — Egr2/3 loss → autoimmunity; induce SOCS1/3; canonical brake.
- **"Egr2 and 3 Inhibit T-bet–Mediated IFN-γ Production in T Cells."** *J Immunol* 2017.
  `10.4049/jimmunol.1602010` — Egr2/3 suppress Th1/IFN-γ (directional, anti-Th1).
- Li et al. **"Early growth response 2 and Egr3 are unique regulators in immune system."**
  *Cent Eur J Immunol* 2017. `10.5114/ceji.2017.69363`.
- **"Egr2 and 3 control inflammation, but maintain homeostasis, of PD-1^high memory CD4 T cells."**
  *Life Sci Alliance* 2020. `10.26508/lsa.202000766`.
- **"EGR2 is the molecular linchpin connecting STAT6 activation to the late, stable [IL-4 type-2
  program]."** *Genes Dev* 2020. `10.1101/gad.343038.120` — EGR2 = STAT6 target, pro-type-2 in
  macrophages. **Directionally complicating for the brake model; ties module to STAT6.**
- **"Differential Expression of Fas Ligand in Th1 and Th2 Cells Is Regulated by Early Growth
  Response Gene."** *J Immunol* 2001. `10.4049/jimmunol.166.7.4534` — EGR in Th1/Th2.
- Egr3 induces Th17 via γδ T cells, *PLoS One* 2014, `10.1371/journal.pone.0087265`; EGR2 controls
  Th17 homing, *Nat Immunol* 2023, `10.1038/s41590-023-01553-7` — module is T-helper-active.
- **"The Transcriptional Cofactor Nab2 … Suppresses Fibroblast Activation."** *PLoS One* 2009.
  `10.1371/journal.pone.0007620` — NAB2 as a suppressive cofactor (non-immune, but the "brake"
  character of NAB2 itself).
- **"Differential regulation of NAB corepressor genes in Schwann cells."** *BMC Mol Biol* 2007.
  `10.1186/1471-2199-8-117` — establishes NAB1/NAB2 as EGR corepressors.
- (Context only — different disease axis) NAB2-STAT6 fusion drives Solitary Fibrous Tumor:
  eLife 2024 `10.1101/2024.04.15.589533`; the recurring cancer-context NAB2 hits are **not** about
  Th2/AD and do not anticipate B7.

### AD lesional transcriptomes (bears on B6 — none name NAB2)
- **"Atopic dermatitis displays stable and dynamic skin transcriptome signatures."** *JACI* 2020.
  `10.1016/j.jaci.2020.06.012` — canonical lesional-vs-nonlesional DE resource; NAB2 not surfaced.
- **"The molecular features of normal and AD skin in infants, children, adolescents and adults."**
  *JACI* 2021. `10.1016/j.jaci.2021.01.001`.
- **"Transcriptome-wide analyses delineate the genetic architecture of expression variation in AD."**
  *HGG Adv* 2024/25. `10.1016/j.xhgg.2025.100422`.
- **"Identification of DEGs in lesional versus nonlesional skin of patients with AD."** 2019.
  `10.35541/cjd.20190001`.
- **"Mapping the immune cell landscape of severe AD by single-cell RNA-seq."** *Allergy* 2024.
  `10.1111/all.16121`; **"Single-cell analysis of CD4+ TRMs in adult AD."** *Genomics* 2024,
  `10.1016/j.ygeno.2024.110870` — single-cell AD atlases; NAB2 not reported.
- Dozens more AD DE/scRNA papers retrieved (spatial, keratinocyte-focused, TWAS, drug-response);
  **zero** name NAB2 in title/abstract. Supplementary tables not searchable by this tool → the
  UNVERIFIABLE-BY-LIT grade for B6.
