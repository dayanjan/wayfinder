# CS-native demo video — script, beat sheet & capture map (2026-07-09)

The **new spine** for the 3-min submission video: *when you don't know what question to ask, use
literature-based discovery to surface a dataset's implicit hypotheses — and build the LBD workflow
directly in Claude Science, so generation and testing live on one bench.* Researcher-who-builds angle.
Supersedes the Streamlit-app cut (`scenes.mjs`); the app stays in the repo as a supporting artifact,
not featured in the 3 minutes.

**Target:** 1920×1080, ElevenLabs "Brian", brand palette bg `#091314` / fg `#eaf3f1` / accent `#26c6c9`
(matches `demo.config.mjs` STITCH theme). **Deadline: submit EOD Fri 2026-07-10.**

---

## The spine narrative (director's cut — narration source)

> Every scientist today is caught between two floods. On one side, the literature — over a million new
> papers a year; no one can read their own field, let alone the one next door. On the other, the data —
> a single omics run returns millions of measurements per sample. The discoveries hide in the gap
> between them.
>
> I felt this directly. For years I ran a metabolomics and lipidomics core facility. Clinical samples
> came in; I generated the data and handed back a matrix of thousands of features — and the researcher
> asked the only question that mattered: *what does it all mean?* Testing one hypothesis at a time
> simply doesn't scale to data like this.
>
> What broke it open for me was literature-based discovery. Its simplest form is Swanson's ABC model:
> if the literature links A to B, and B to C, but no one has connected A to C — then A-to-C is a hidden,
> testable hypothesis. Swanson's own case: fish oil, blood viscosity, Raynaud's — a link no single paper
> had drawn, later confirmed.
>
> But LBD carried two burdens: it's a slog to collate, and it generates far more hypotheses than anyone
> can test. Large-scale omics has the mirror problem — mountains of answers with no questions. Now
> there's one platform that can generate a hypothesis *and* validate it in the same place: Claude
> Science. The generation half was capable but missing. So I built it.
>
> Now generation and testing run side by side, each covering the other's weakness. On the Marson lab's
> CD4 T-cell Perturb-seq data, 22,000 machine-generated hypotheses go in; a deterministic referee culls
> them with a receipt at every hop — and confidently says **no**, flagging a failed knockdown as
> *untested*, not a false negative. Thirty survive. The standout: **NAB2 → Th1/Th2 → atopic eczema** — a
> connection the literature had never drawn, backed by a receipt in the data. Its hardest confounder —
> refuted live against the original authors' own genome-wide data. And the platform checks itself: a
> reviewer model caught and killed my overclaim, in real time.
>
> Swanson's ABC was just the start — the first of several discovery methods we're bringing to the bench.
> *The library and the lab, on one platform.*

---

## Beat sheet + shot-by-shot narration (~380 words ≈ 2:45–2:55)

| # | Time | Narration (verbatim) | Visual |
|---|---|---|---|
| 1 | 0:00–0:25 | "Every scientist today is caught between two floods. On one side, the literature — over a million new papers a year; no one can read their own field, let alone the one next door. On the other, the data — a single omics run returns millions of measurements per sample. The discoveries hide in the gap between them." | Title card → CS b-roll (tables loading) |
| 2 | 0:25–0:52 | "I felt this directly. For years I ran a metabolomics and lipidomics core facility. Samples came in; I generated the data and handed back a matrix of thousands of features — and the researcher asked the only question that mattered: *what does it all mean?* Testing one hypothesis at a time simply doesn't scale to data like this." | **Framing slide** — feature matrix (TODO build) |
| 3 | 0:52–1:20 | "What broke it open for me was literature-based discovery. Its simplest form is Swanson's ABC model: if the literature links A to B, and B to C, but no one has connected A to C — then A-to-C is a hidden, testable hypothesis. Swanson's own case: fish oil, blood viscosity, Raynaud's — a link no single paper had drawn, later confirmed." | **Swanson graphic** `assets/swanson-graphic.html?scene=swanson` ✅ built |
| 4 | 1:20–1:55 | "But LBD carried two burdens: it's a slog to collate, and it generates far more hypotheses than anyone can test. Large-scale omics has the mirror problem — mountains of answers with no questions. Now there's one platform that can generate a hypothesis *and* validate it in the same place: Claude Science. The generation half was capable but missing. So I built it." | **CS capture** — micro-sweep authoring + live API calls |
| 5 | 1:55–2:38 | "Now generation and testing run side by side, each covering the other's weakness. On the Marson lab's CD4 T-cell Perturb-seq data, 22,000 machine-generated hypotheses go in; a deterministic referee culls them with a receipt at every hop — and confidently says **no**, flagging a failed knockdown as *untested*, not a false negative. Thirty survive. The standout: **NAB2 → Th1/Th2 → atopic eczema** — a connection the literature had never drawn, backed by a receipt in the data." | **CS capture** (funnel 22,039→30; a REFUTED example; NAB2 receipt chain) + Swanson graphic `?scene=nab2` overlay |
| 6 | 2:38–3:00 | "Its hardest confounder — refuted live against the original authors' own genome-wide data. And the platform checks itself: a reviewer model caught and killed my overclaim, in real time. Swanson's ABC was just the start — the first of several discovery methods we're bringing to the bench. **The library and the lab, on one platform.**" | **CS capture** (STAT6-unmoved table; Reviewer flags "definitive/validated") + end-card + credit |

---

## Beat → existing CS conversation (capture map)

All source material already exists as **Completed** CS conversations (de-risked 2026-07-09; saved auth
in `cs_state.json` valid, daemon on **port 8000**). No expensive re-runs needed.

| Beat | CS conversation title (on the home view) |
|---|---|
| 4 | "Live LBD Literature Question Generator" (microsweep) · "Timing Calibration Probe: Europe PMC & Open Targets" |
| 5 | "VALIDATED Bioinformatics LBD Pipeline Receipt Verification" (stage1) · "Literature-Based-Discovery Loose Gene Universe Sweep" |
| 6 | "Stage3: NAB2-STAT6 Cis-Artifact Verification" · "Assemble NAB2 Receipt Chain Synthesis" (stage5) |

**Capture ops:** navigate to each conversation frame with Playwright (headless, 1920×1080, saved auth),
scroll to the receipt/number, screenshot + short screen-record. **Do NOT restart CS** (an "Update
available" toast offers Restart — dismiss via ✕; restarting kills daemon pid 487 and may shift the UI).

---

## Written summary — required submission field (~180 words)

> Scientists are caught between two floods: over a million biomedical papers a year, and omics runs
> returning millions of measurements per sample. Discoveries hide in the gap — and the two classic
> tools each fail alone. Literature-based discovery (LBD) generates more hypotheses than anyone can
> test; large-scale omics generates answers with no questions attached.
>
> We built the missing half. Inside **Claude Science** — a platform that can already *validate* a
> hypothesis — we implemented **Swanson ABC** literature-based discovery, so hypothesis *generation* and
> *testing* run side by side. Every machine-generated hypothesis is culled immediately against real data
> by a deterministic referee that returns a receipt at every hop and confidently says **"no"** —
> flagging a failed knockdown as *untested*, not a false negative.
>
> On a public CD4+ T-cell Perturb-seq dataset (Zhu, Dann, … Marson; Gladstone/UCSF), 22,039 hypotheses
> funneled to **30 receipt-backed survivors**. The standout: **NAB2 → Th1/Th2 → atopic eczema** — a
> connection the literature had never drawn — plus other candidate leads. *The library and the lab, on
> one bench.*

---

## Citation & credit (locked)

> Zhu R, Dann E, Yan J, Reyes Retana J, Goto R, Guitche RC, Petersen LK, Ota M, Pritchard JK, Marson A.
> **Genome-scale perturb-seq in primary human CD4+ T cells maps context-specific regulators of T cell
> programs and human immune traits.** bioRxiv 2025. doi:10.64898/2025.12.23.696273

**End-card / README credit line:**
> Data: CD4+ T-cell Perturb-seq — Zhu, Dann, … Marson (Gladstone/UCSF), bioRxiv 2025,
> doi:10.64898/2025.12.23.696273. Used under the hackathon public-dataset provision; all analysis
> performed during the event. Analysis reference: `github.com/emdann/GWT_perturbseq_analysis_2025`.

---

## Calibration guardrails (do not overclaim in the cut)
- NAB2 stays a **nomination**: "candidate," "the literature had never drawn," "receipt in the data." Never "proven/discovered."
- Keep the **therapeutic direction** (brake / UP-modulate) OUT of the 3-min cut — association-backed, needs perturbation proof; belongs in the writeup caveats only.
- The **full 3,935-gene sweep in CS was a cached replay** — the "CS builds LBD live" beat uses the **micro-sweep** (genuinely live, independently re-verified). Never imply the full sweep was a live crawl.
- "over a million papers / millions of measurements" are context stats, kept soft — not receipt-claims.

### Debate-hardened additions (codex-debate 2026-07-09 — `cs/narration.mjs` is now authoritative)
- **Live-vs-cached ON SCREEN (F-002):** beat 5 carries a caption *"full 22,039 sweep = cached-receipt replay · micro-sweep + STAT6 = live"* — the boundary is explicit in the cut, not buried in docs. Beat-4 narration scopes "live" to "author and run a generator live, from scratch" (the micro-sweep).
- **Show the NO, don't assert it (F-005):** beat 5 includes a **visible refusal receipt** (IL2→untested or SBF2→effect-refuted) — verdict word + reason on screen. This is the moat.
- **Scoped calibration (F-003/F-004):** "six co-mentions, but no paper drawing the NAB2→Th1/Th2→eczema chain"; "a possible **STAT6 cis-artifact** refuted live; the GWAS label remains a nomination."
- **Grounded endcap (F-007):** "In this workbench, I built the missing generation half — beside the test" (no product-maturity overclaim).
- **4 REQUIRED FRAMES are release blockers (F-001/F-011)** — see `cs/CAPTURE_PLAN.md`: live micro-sweep proof · funnel+NAB2 receipt · one concrete NO receipt · reviewer overclaim flag. Pre-capture these FIRST; static artifact overlay if live capture is unreliable.

## Status (2026-07-09 PM)
- ✅ Spine, narration, beat sheet, summary, citation — this doc
- ✅ Swanson graphic (beats 3+5) — `assets/swanson-graphic.html`
- ✅ Capture path de-risked (auth + screenshot + video all confirmed)
- ✅ Framing slides (beats 1–2) — `assets/slide-two-floods.html`, `assets/slide-feature-matrix.html`
- ✅ **CS-native demo pack scaffolded** — `cs/{demo.config,narration,scenes}.mjs` + `cs/README.md`
  (screen-only gate PASS, syntax-clean; harness drives CS via `STORAGE_STATE`=cs_state.json). Friday runbook in `cs/README.md`.
- ✅ **On-screen capture plan VERIFIED** — all 4 CS conversations opened; frame URLs + money-shot sources + gotchas in `cs/CAPTURE_PLAN.md`.
- ✅ **Plan hardened via 2-round repo-read codex-debate** — `docs/reviews/codex-debate_cs-native-video-plan_2026-07-09.md`. Spine held (no sanding); accepted fixes applied to `cs/narration.mjs`, `cs/scenes.mjs`, `cs/CAPTURE_PLAN.md`, this doc.
- ⬜ Fri: pre-flight (CS port + refresh auth) → **pre-capture the 4 required frames (blockers)** → `run.mjs --stage=all` → gate PASS → mux music → repo public + scrub → submit
