# HACKATHON — Built with Claude: Life Sciences (canonical fact sheet)
> Single source of truth for the hackathon this project was built for. Consolidates the kickoff-transcript
> ADR (`memory/decisions/hackathon-track-and-facts.md`), `docs/plan.md` (§0, §12), and `SUBMIT_CHECKLIST.md`.
> Facts are transcript-grounded unless marked **[UNVERIFIED]**. Referenced from `CLAUDE.md`.

## Event
- **Name:** *Built with Claude: Life Sciences*.
- **Hosts:** **Anthropic × Gladstone Institutes**, run by **Cerebral Valley** (organizer contact: Ivan Pirello).
- **Format:** global **virtual** hackathon.
- **Kickoff:** Tue **2026-07-07, 12:30 PM ET**. Effective build window ≈ 6.5 days.
- **Source of truth:** kickoff transcript (gitignored: `01-hackaton details/…_plain-text.txt`).

## Track — RESEARCHER (committed 2026-07-07)
Framed as **"a researcher who also builds."** Two tracks (transcript-verbatim):
- **Researcher (ours):** start from a biological question, use an existing dataset/tool, produce a **discrete
  finding / trained model / reproducible analysis**, and show **how Claude Science got you there**.
- **Builder:** engineers use Claude Code, start from a *user* (lab/clinic/biotech), build a tool that outlasts the event.

**History/resolution (so the stale `plan.md` "Build track" language doesn't confuse):** early plan versions
(v1–v6) aimed Builder; a Fable-5 review argued Builder fit the referee *tool* better. **v7 committed to
Researcher** and does not hedge — the referee / LBD engine / Claude-Science automation are *instruments built to
get the science done*, so the builder-craft is evidence of a scientist who can build, not a separate Builder
pitch. Track is technically set at the **Submit Project** button, not locked at application.
**Implication:** Claude Science is **required + on the critical path** (no pandas-only fallback).

## Deliverable & submission requirements
Submit via the Cerebral Valley "Submit Project" flow:
1. **3-minute demo video** — transcript stressed this is "**super important**" (the one confirmed judging signal).
2. **Open-source repository** — judges analyze the code (must be OSS-licensed; MIT here).
3. **Written summary.**
Our deliverable: a **reproducible CD4⁺ T-cell Perturb-seq finding** (NAB2 → Th1/Th2 → atopic eczema,
receipt-backed) reached **through Claude Science**, with Wayfinder (the referee) as the method/vehicle.

## Timeline
- **Submissions due:** **Monday 2026-07-13, end of day ET** (official). Operator personal hard stop **9:00 PM ET** (travels 7/14).
- **Judging:** async **Tue–Wed 7/14–15** → top 6.
- **Results:** final livestream reactions **Thu 2026-07-16, noon ET** → 1st/2nd/3rd per track + special prize.

## Prizes
- **Per track:** 1st **$30k** / 2nd **$10k** / 3rd **$5k** in **API credits**. *(Transcript stated the $30/10/5k
  explicitly under Builder; Researcher has its own top-3 — exact Researcher amounts **[UNVERIFIED]**, assume parallel.)*
- **Gladstone Special Prize** (track-agnostic): "most potential to advance science overcoming disease" —
  hand-picked, can go to a non-top-3 project. Very reachable for a real autoimmune gene→program→disease result.

## Rules & eligibility
- **NEW WORK ONLY (strict):** everything submitted built from scratch during the event; the analysis must happen
  during the event. **Git history is the compliance proof** (`git init` after kickoff). PyZoBot POC = reference
  only, zero file reuse.
- **Open-source** with an OSS license (MIT).
- **Team:** solo or 2 people (operator = **solo**).
- **Allowed:** third-party OSS libraries (LangChain/LlamaIndex/Streamlit/pandas/Voyage SDK, pyzotero, Biopython)
  and public datasets. **Rights violations disqualify.**

## Credits provided to all participants
- **20× Max plan** + **$200 API credits** per participant.

## Judging criteria (weights + our answer)
**[UNVERIFIED WEIGHTS]** — the specific weights below are from `docs/plan.md` §12, **not** in the kickoff; the
only transcript-confirmed signal is "the demo video is super important." Confirm against the CV details page / submit form.
- **Demo — 30%:** the live **NO-with-a-receipt** money shot; "cool to watch" + "findings you trust" (3-min video).
- **Claude Use — 25%:** the adversarial **agent cast** (Skeptic refutes, Adjudicator calibrates); "capabilities that surprised even us."
- **Impact — 25%:** the **named user** (an immunologist refereeing claims against 22M cells) + "could people use this."
- **Depth & Execution — 20%:** falsification rigor, the knockdown-QC gate, calibrated language, two anchors; "real craft."

## Project constraints (self-imposed, aligned to the event)
- **Claude for reasoning/generation; Voyage for embeddings** (Anthropic has no embedder). **Never OpenAI** in the product.
- **CPU-only** (pandas over aggregated CSVs; no GPU, no raw 22M-cell matrices).
- Calibrated language only; every causal edge traces to a data receipt (see `CLAUDE.md`).

## Substrate / data
CD4⁺ T-cell genome-scale CRISPRi **Perturb-seq** — **Zhu, Dann, … Marson** (Gladstone/UCSF), bioRxiv 2025,
**doi:10.64898/2025.12.23.696273**; analysis repo `github.com/emdann/GWT_perturbseq_analysis_2025`. Full source
map: `docs/CLAIMS_EVIDENCE_LEDGER.md` (S1–S11).

## Submission status & how to submit
**BUILT + FIRE-READY.** Repo `dayanjan/wayfinder` (private until flip). Say **"scrub and flip"** → run
`SUBMIT_CHECKLIST.md` (gitignored, repo root): scrub personal paths → add video link → leak grep → commit →
`gh repo edit dayanjan/wayfinder --visibility public`. Deliverable video: `.tmp/demo-cs/out/wayfinder_demo.mp4`.

## Support
Office hours daily **Tue–Fri 5–6 PM ET** (Discord). Live sessions: **Wed** = Alexander Terashansky (Claude
Science); **Fri** = Sukrit Silas (Gladstone).

## Sources of truth (for updates/verification)
- `memory/decisions/hackathon-track-and-facts.md` — the kickoff-transcript ADR (ground truth).
- `docs/plan.md` §0 (Researcher reframe) + §12 (judging map).
- `SUBMIT_CHECKLIST.md` (gitignored) — the submission runbook.
- Kickoff transcript (gitignored). **To verify the [UNVERIFIED] items, check the Cerebral Valley details/submit page.**
