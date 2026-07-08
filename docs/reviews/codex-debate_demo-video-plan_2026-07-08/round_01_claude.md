# Round 1 — Claude's opening position

**Framing question.** How best to improve the QUALITY of PyZoBot Arbiter's 3-minute demo video
before putting the pipeline into production — specifically: (1) the demo-surface decision (build a
REAL Streamlit referee UI [Option C, recommended] vs. just drive the executable notebook [Option A,
fallback]); (2) the 6-scene narrative arc and whether it maximizes Demo (30%) + Impact (25%) given the
thesis; (3) the production sequence and any pipeline / Potemkin / timing risks. Solo builder, deadline
2026-07-13 9:00 PM ET, ~5 days out.

**Novel claim to preserve (do not sand toward a safe feature-tour).** The strongest demo *leads with
falsification* — the confident, receipt-backed **NO** and the **UNTESTED** hero catch (a failed
knockdown → untested, not a negative). The willingness to refute IS the product. An interactive
referee that returns YES / UNTESTED / REFUTED live makes that tangible in a way a results scroll cannot.

## The position

1. **Surface = build a minimal REAL Streamlit UI wrapping `referee_triple` (Option C), not drive the
   notebook (A).** The referee (`src/arbiter/lbd/referee_triple.py`) already returns a full 4-hop
   verdict dict (`answer` ∈ supported / untested / refuted_for_c / supported_weak / supported_flagged)
   in <1s from local CSVs. A thin Streamlit wrapper (pick gene + disease + condition → Adjudicate →
   render the hop chain with PASS/UNTESTED/REFUTED badges + receipts) is honest (every value from
   `referee_triple`, no Potemkin), interactive, and product-feeling — the highest-value thing for
   Demo 30% + Impact 25%. Scope is modest (~half day) because the referee + data loader already exist.
   Notebook-driving (A) is the zero-scope fallback if the UI slips.

2. **Arc = 6 scenes, single actor, ~180s, leading with the funnel then the verdict range.** Title →
   (1) cold-start + funnel (22,039 generated → 30 culled) → (2) money-shot YES (NAB2→atopic eczema,
   4 green receipts) → (3) UNTESTED (SATB1, knockdown didn't take) → (4) REFUTED (SLC1A5) → (5) depth:
   STAT6 cis-confounder excluded vs the authors' genome-wide data → endcap. Calibrated language only;
   literal/warm/no-hype narration (per ALPINE). Author to scenes, render, trim to 180s.

3. **Production = reuse the proven `demo-video` skill unchanged.** Screen-only Playwright (ep5
   single-actor template), TTS-first pacing, edge-tts DRAFT → transcription gate PASS → operator review
   → ElevenLabs (Brian) final + music. PyZoBot's big advantage over the Halcyon reference: the referee
   is deterministic + read-only over local CSVs, so the #1 Halcyon effort sink (live-prod state
   accumulation / fixture re-runnability) is largely absent — re-records are trivially clean.

## What I am least sure of (debate targets)
- Is the Streamlit UI worth the scope vs Option A, given the deadline and that a bad/rushed UI could
  hurt more than a clean notebook scroll?
- Is 6 scenes right, or should it tighten to 5 and open cold on the money-shot?
- For Scene 5 depth: live-scroll a UI panel vs cut to the pre-rendered Claude Science figure — which is
  more honest AND higher-impact?
- Any Streamlit-specific screen-only/pacing gotcha (vs a normal SPA) to preempt.

Full plan: `docs/plans/demo_video_plan_2026-07-08.md`. Referee: `src/arbiter/lbd/referee_triple.py`.
Notebook: `notebooks/pyzobot_arbiter_evidence_chain.ipynb`. Depth assets:
`docs/claude-science-evidence-chain_2026-07-08/`. Pipeline: `~/.claude/skills/demo-video/`.
