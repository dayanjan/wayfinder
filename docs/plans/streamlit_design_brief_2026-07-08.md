# Design brief — PyZoBot Arbiter (the Researcher's Workbench)

*Self-contained brief for a UI/UX designer. No codebase knowledge needed — everything is here.
We'll implement in **Streamlit** (Python), so favor layouts expressible with columns / containers /
cards + a modest amount of custom CSS. Deliver a component + layout design: colors, typography, the
signature Receipt Chain component in all three states, the funnel, and the three screens, in light AND
dark themes.*

---

## What the product is

**PyZoBot Arbiter** is a hypothesis referee for T-cell immunology. A scientist poses a mechanistic
claim — *"gene G regulates T-cell program P, implicated in autoimmune disease D"* — and the app returns a
**verdict with a receipt (a real data value) for every step**, and it is **willing to say a confident
*no*, or *untested*** when an experiment failed. The whole personality is **"receipts, not hype"**: it
refutes plausible-sounding claims and honestly flags failed experiments instead of pretending.

**Tone / visual language.** A modern computational-biology instrument — clean, data-dense but calm,
trustworthy; a cross between a lab notebook and a clinical decision tool. Primary accent should evoke
molecular biology (a deep teal or indigo). A clear **semantic status palette** (below) is central. Provide
a polished **light and dark** theme. It must look like a real instrument a scientist would trust — never a
toy or a marketing page.

**What to optimize for (in order).**
1. The **Receipt Chain** must be gorgeous and instantly legible — it is the brand.
2. The **UNTESTED "halt at the gate"** state must feel *intentional and honest*, not like an error.
3. The **funnel** must make "the referee refused ~22,000 questions" land emotionally.
4. Overall: an instrument a scientist trusts.

---

## Build order — please design in this priority

The full app vision is below so your design is cohesive, but we implement in stages, so please make the
**Tier-1 MVP gorgeous first** and treat the rest as the cohesive frame around it:

- **Tier-1 MVP (design first, we build first):** **Screen 1 (Referee)** + the **Receipt Chain** component
  in all three states (supported / untested / refuted) + the three "Try these" example queries.
- **Everything else — later:** Screen 2's full sortable table, Screen 3's "run live" button, motion
  polish. Design them as part of the whole, but they're the frame, not the centerpiece.

---

## The signature component — the Receipt Chain

A 4-step chain (vertical on narrow screens, horizontal on wide): **GATE → EFFECT → PROGRAM → DISEASE**.
Each step is a **card** with three things: a **status pill**, a **one-line plain-English claim**, and its
**receipt** — the actual numbers. Above the chain sits a prominent **overall verdict banner** (one
calibrated sentence). Three states to design:

**State 1 — SUPPORTED (a confident YES).** All four cards green/check. Example content (use verbatim as
mock data):
- Verdict banner: *"Consistent with a re-derived NAB2 → Th1/Th2 → atopic-eczema chain."*
- GATE ✓ "Knockdown verified" — *2 of 2 guides significant · adj-p 1e-16 · guide expr 0.056 vs control 0.567*
- EFFECT ✓ "Real on-target effect" — *effect −16.9 · 301 downstream genes · no off-target flag · reproducibility R 0.74*
- PROGRAM ✓ "Shifts the Th1/Th2 program" — *Ota 2021: z 7.71, adj-p 2e-13 · Höllbacher: same direction, not significant*
- DISEASE ✓ "Enriched in atopic-eczema modules" — *odds ratio 3.90 · FDR 0.003 · 2 significant clusters*

**State 2 — UNTESTED (the hero moment — the chain HALTS at the gate).** The GATE card is **amber,
"UNTESTED"**; EFFECT / PROGRAM / DISEASE render **greyed and struck-through** with a subtle watermark
*"not evaluated — knockdown unverified."* This must read as a *deliberate, honest stop*, not a crash or an
error. Example:
- Verdict banner: *"Untested — the knockdown failed QC; downstream results are not interpretable."*
- GATE ⚠ "Knockdown did not take" — *0 of 2 guides significant · adj-p 0.70 · guide expr 2.40 vs control 2.35 (barely moved)*
- EFFECT / PROGRAM / DISEASE → greyed, struck, "not evaluated."
*(This is the product's signature feature: a failed experiment is honestly "untested," never a false
negative. Make it feel trustworthy and intentional.)*

**State 3 — REFUTED (a confident NO, disease-specific).** Upstream cards stay green; the failing hop is
**red/×**. Example — note this is the SAME gene (NAB2) as State 1, but a different disease, to show the
referee adjudicates the *specific disease*:
- Verdict banner: *"Refuted for multiple sclerosis — the chain holds until the disease hop, where it doesn't."*
- GATE ✓ · EFFECT ✓ · PROGRAM ✓ (same greens as State 1)
- DISEASE ✗ "Not enriched in multiple-sclerosis modules" — *not a member of any MS-enriched cluster at FDR<0.05*

**Full status palette (for badge design).** green = *supported*; amber (with a small caveat chip) =
*supported-weak* / *supported-flagged*; grey = *untested*; red = *refuted*. The app **never** uses the
words "discovered / proven / definitive" — calibrated language only (consistent with / re-derived /
refuted / untested / flagged).

---

## Screen 1 — Referee (the hero)

A clean **query bar**: a **gene** picker + a **disease-module** picker + a small **condition** toggle
(Rest / Stim 8 hr / Stim 48 hr) + a prominent **Adjudicate** button. Below it, a **"Try these"** row of
three chips that tell the whole story at a glance:
- **NAB2 → atopic eczema** — a confident **YES**
- **SATB1 → asthma** — the **UNTESTED** catch (halts at the gate)
- **NAB2 → multiple sclerosis** — a confident **NO**

The YES and NO deliberately **share the gene (NAB2)** — same real knockdown and effect, opposite verdicts
by disease. Make that disease-specificity visually obvious (it's a key "aha"). Result area = the Receipt
Chain + verdict banner. Design an inviting **empty state** that nudges the user toward the three chips.

## Screen 2 — Hypothesis Engine (the funnel) *[frame, design after Tier-1]*

Top: a **funnel** visualization that makes a dramatic cull land instantly:
**3,935** knockdown-gated regulators → **22,039** literature-eligible gene–disease questions → **43** held
at the disease hop → **30 clean, receipt-backed findings.** The story to convey: *the engine generated
22,039 questions from a dataset that came with none, and the referee refused all but 30 it could back with
a receipt.* Below the funnel: a **sortable table** of the 30 surviving questions (gene · disease · novelty
· effect size · score · verdict); clicking any row opens it in the Receipt Chain (Screen 1). One honest
callout: the single "novel-but-weak" survivor (NUDT1 → type-1 diabetes — zero prior literature but a tiny
effect), illustrating *why the engine ranks rather than blindly trusting novelty*.

## Screen 3 — Claude Science *[frame, design after Tier-1]*

An **evidence-chain reasoning panel**: a short narrative (reusing the Receipt Chain motif) + a
**publication-style scientific figure** (a 6-panel figure exists) + a verdict card. A header frames it:
*"An independent Anthropic scientific agent, given only the data and the question, reasoned to the same
verdict."* One **clearly-secondary** button — *"Run a fresh Claude Science analysis"* — with an honest
"~several minutes" affordance and an async progress state (queued → reasoning → done). This is an optional
deep-dive, not the default view.

## Global chrome

A slim left nav (or top tabs): **Referee · Hypothesis Engine · Claude Science**. A compact header with the
product name + a one-line honest tagline (*"Receipt-backed. Willing to refute."*). A footer with the
calibrated-language note + *"Reproducible: every number re-derived live from public Perturb-seq tables."*
Motion is subtle — nice touch: on **Adjudicate**, the Receipt Chain steps can resolve **sequentially**
(gate → effect → program → disease), which also reads beautifully on video.

---

*Context: this app anchors a 3-minute demo video and a hackathon submission (Anthropic × Gladstone "Built
with Claude: Life Sciences"). The falsification story — the confident NO and the UNTESTED catch — is the
whole point, so the Receipt Chain (especially its untested-halt and refuted states) is where the design
investment should go.*
