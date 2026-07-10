# Independent hackathon-judging panel — CS-native demo video + submission

**Date:** 2026-07-10 · **Artifact judged:** the 2:52 CS-native demo video (author's cloned voice + CC-BY
music bed) + the ~180-word written summary + the public-facing repo. **Method:** six independent Claude
judge agents (cold context, no cross-contamination), each on a distinct lens tied to the rubric, then a
synthesized register. Each judge was given the exact narration + per-beat on-screen visuals + the summary,
and repo file access for depth. **This doc is the input to the follow-on codex-debate** (which additionally
watches the rendered MP4 for A/V — voice, music, pacing — the panel could not assess).

Rubric (working model): **Demo 30% · Claude Use 25% · Impact 25% · Depth 20%.** Async first round selects
top 6 from video+repo+summary; live final round reacts to the top-6 videos.

---

## Scorecard

| Lens | Score | Gut call |
|---|---|---|
| Demo & watchability (30%) | **7.5/10** | Likely top-6 — best moment (the refusal) buried ~1:00 deep |
| Claude Use (25%) | **8/10** | Likely — CS as the real instrument + reviewer model caught its own overclaim |
| Impact (25%) | **8/10** | Likely to place; borderline-likely for the Gladstone disease prize |
| Depth (20%) | **8.5/10** | Top-tier rigor; verified against the actual code |
| Skeptical scientist | **trust-with-caveats** | Calibration genuine; protect the on-screen visuals |
| Submission compliance | **ready-after-checklist** | Secrets/new-work clean; stale README is the own-goal |

Rubric-weighted ≈ **8.0/10.** Unanimous "in contention." Gaps are almost entirely presentation +
repo-hygiene, not substance — the science held up even when a judge read the code.

---

## Converged strengths (raised by multiple judges)

- **The confident NO** (failed knockdown → *untested*, not false negative; IL2→UNTESTED overlay) — a rare,
  legible, on-thesis money moment. Most demos show what a tool finds; almost none show it correctly declining.
- **Claude Science as the actual lab bench** — Stage 0/1/3/5 ran natively; OPERON=Opus 4.8 author +
  Reviewer=Sonnet 5 critic; the reviewer **flagged "validated"/"definitive" and they were cut** (verifiable
  in `stage5/review.json` / `operon-cli.db`). "Anthropic's own reviewer model enforced the project's own
  falsification thesis on its own output" — the strongest Claude moment.
- **STAT6 cis-falsification against the authors' own genome-wide DE** — external, gold-standard, real
  refutation (STAT6 unmoved +0.09/adj_p 0.79; NAB2 self −3.08, z≈−17).
- **End-to-end calibrated language** + **clean new-work git trail** + **5-agent independent replication** (the
  best defense against any "did you just assert this?" attack).
- **The knockdown-QC gate is genuinely rigorous** (Depth verified in `pyzobot_referee.py` / `referee_triple.py`)
  — the distinction most hackathon "validators" get wrong.

---

## Prioritized fix register (synthesized, deduplicated)

### Tier 0 — before the repo goes public (integrity own-goals; cheap, non-negotiable)
1. **Rewrite the stale README.** It still describes the old Streamlit vision, has a placeholder "build
   instructions to follow," and never states the finding, Claude Science role, or the video link. Async
   judges land here first; it's the "judges analyze the code" round. `[moderate]` *(Compliance — #1 own-goal)*
2. **Kill the "validated" contradiction in shipped artifacts.** The word still appears in
   `pyzobot_referee.py` (`_synthesize_overall`, ~line 314) and `receipt_chain.md:13`, contradicting the
   "never validated/proven/definitive" calibration claim. Change to "re-derived." `[quick]` *(Depth — verified)*
3. **Fix the stale direction label** in `receipt_chain.md:39` — "Th1-associated" → "Th2-associated" (the
   inverted-label fix never propagated to that artifact). `[quick]` *(Depth)*
4. **Scrub personal Windows paths** (`C:/Users/wijesingheds/…`, the `.env` + `cs_state.json` signposts) from
   `docs/demo-video-pack/{demo.config.mjs, cs/demo.config.mjs, cs/scenes.mjs}` + `app/smoke_referee.mjs`.
   No secret leaks (files untracked) but it signposts them and leaks the username. `[quick]` *(Compliance R1)*
5. **Reconcile the data-license wording.** README + `data/README.md` call the *dataset* "MIT-licensed," which
   is likely wrong (that's the analysis-reference repo). Align to the "public-dataset provision" language +
   verify actual terms. Rights-round risk. `[quick]` *(Compliance R2/R3)*
6. **At publish:** paste the CC-BY music credit ("Deliberate Thought" — Kevin MacLeod, CC-BY 4.0) + the full
   data citation into the **video description** (CC-BY isn't discharged by in-repo credit alone); final
   secret-grep → flip public. `[quick]` *(Compliance B3)*

### Tier 1 — high-ROI edits to win points (video is re-renderable)
7. **Surface the R01-rejection hook** — *"Three NIH reviewers killed the grant behind this: 'LBD generates
   hypotheses almost none of which get followed up.' I built the answer to that critique."* Two judges
   independently called this the strongest opener + strongest impact sentence; it's only in the README today.
   `[quick]` *(Demo + Impact)*
8. **Cold-open on the refusal** — front-load the IL2→UNTESTED moment into the first ~8s (before the title).
   Triage judges decide in 30s; the coolest/most-legible frame is currently ~1:00 deep. `[moderate — re-render]` *(Demo)*
9. **Protect the beat-6 visual** — caption the STAT6 result *"cis-artifact refuted · eczema label = GWAS
   nomination,"* never "confounder cleared"; soften "hardest." The narration threads it; the on-screen text is
   the exposure. The STAT6 check refutes the *cis-expression* artifact, NOT the LD-inherited GWAS-label
   confound (no colocalization run). `[quick]` *(Skeptical — top risk)*
10. **Keep the "cached full sweep" caption on-screen through the entire funnel shot** + tag b4 "live
    micro-sweep" vs b5 "cached full sweep." The genuinely-live micro-sweep used a 12-gene universe where NAB2
    didn't even rank; the headline 22,039→30 + NAB2 are the cached replay. Keep the live glow off the cached
    result. `[quick]` *(Skeptical + Claude Use)*
11. **Rewrite the summary to lead with significance, not machinery** — open with the confident-NO / R01
    answer; add an honesty line (*"eczema link = GWAS nomination, no colocalization; the perturbation-backed
    claim is NAB2 as a Th1/Th2 regulator"*); reframe "30 survivors" as illustrative and lean on NAB2.
    `[quick]` *(Impact + Skeptical + Demo)*
12. **De-number the NAB2 overlay** — cut the 8-figure receipt row to 3 (novelty ac_lit=6, effect 301, verdict
    "supported"); let 22,039→30 be the number that carries. `[quick]` *(Demo + Depth)*
13. **Name CS as "Anthropic's own scientific workbench" + give the reviewer-catch its own beat** — one spoken
    clause + one standalone moment turns your best Claude moment from a blur into a trophy. `[quick]` *(Claude Use)*
14. **Say the disease hop is an inherited nomination out loud** — HOP-3 reads Open-Targets/enrichment stats,
    it's not the referee's own inference; one sentence pre-empts the top depth+credibility critique and reads
    as sophistication. `[quick]` *(Depth + Impact + Skeptical)*

### Tier 2 — skip before deadline
Threshold-sensitivity sweep · a second non-immune triple · autoimmune-broad disease reframe · burned-in captions.

---

## Per-judge detail

### Demo & watchability (30%) — 7.5/10, likely top-6
Best-in-class on "findings you trust"; the "cool to watch" half is dragged by a ~60s abstract preamble before
the first live screen and a number-dense money shot. Fixes: cold-open on the refusal; swap the "two floods"
open for the R01 stakes; de-number the NAB2 overlay to 3 figures; reframe the honesty caption as
*reproducibility* ("pre-computed with receipts, re-run live") not "not-live"; lead the summary with the
differentiator. Flagged the cloned-voice quality as an unverified delivery bet (the codex-debate resolves this).

### Claude Use (25%) — 8/10, likely
CS is the instrument not a wrapper; genuine multi-model actor-critic; the reviewer-catches-overclaim is the
trophy moment. Ceiling capped because the load-bearing scientific compute is deterministic pandas (by design)
— be crisp that Claude reasons in the *generation + critique*, the referee is deterministic on purpose. Fixes:
name CS as Anthropic's workbench (one clause); give the reviewer-catch its own beat; tighten the "22,000" so it
doesn't imply CS authored 22k live; put the actor-critic (OPERON=Opus, Reviewer=Sonnet, caught overclaim) into
the summary/README.

### Impact (25%) — 8/10, likely to place; borderline-likely Gladstone disease prize
The method is the impact — a reusable "generate-and-cull on one bench" instrument that fixes LBD's 40-year
follow-up problem (the R01 critique). Headline result is honestly a *nomination*, which reads preliminary to a
disease-prize judge. Fixes: put the R01 line in the summary; rewrite the summary's last third to lead with "so
what" not counts; concede+claim the boundary in the endcap ("demonstrated on T-cell Perturb-seq; the referee
generalizes to any gene→program→disease triple"); frame disease story as autoimmune-broad with eczema as the
worked example.

### Depth (20%) — 8.5/10, top-tier (verified against code)
GENUINELY RIGOROUS: the knockdown-QC gate (untested vs false-negative), the STAT6 cis-falsification, the
receipt-at-every-hop chain (none hardcoded), self-caught cluster-ID bug + replication, pure-replay cache guard.
COSTS POINTS: HOP-3 disease receipt is an *inherited* Open-Targets lookup (not the referee's own statistic);
ac_lit=6 novelty is a raw co-mention count (ranks obscurity); the program hop is tautological *inside the
funnel* (`refuted_program ≡ 0` by construction); calibrated-language is a convention + reviewer pass, not a
code gate — and the word **"validated" still lives in shipped code + `receipt_chain.md`**; stale Th1/Th2 label
in that artifact. Fixes: say the disease hop is inherited out loud; reconcile "validated" in code; patch the
stale label; show the gate contrast (NAB2 2/2 passes, IL2 0/2 stops) long enough to read.

### Skeptical scientist — trust-with-caveats
Unusually honest work; calibration is real, not decorative. Ranked risks: **(1)** "hardest confounder refuted"
conflates the *cis-expression* artifact (refuted) with the *LD-inherited GWAS-label* confound (only hedged, no
colocalization) — narration is scoped correctly, protect the VISUAL/caption and the word "hardest"; **(2)** the
"live" glow is borrowed — the live micro-sweep never produced NAB2 (12-gene universe); keep the cached caption
on-screen through the funnel; **(3)** "22,039→30" credits the referee with the literature filter's culling
(referee alone supports 395/47,220) and has no threshold-sensitivity check — reframe "30" as illustrative, lean
on NAB2; **(4)** domain-optics (metabolomics builder, T-cell claim) — defensible because tool-attributed +
replicated, be ready to say it crisply; **(5)** anthropomorphizing "referee" — low risk, honest metaphor;
**(6)** reproducibility is a STRENGTH — make the NAB2 receipt one-command reproducible from a fresh clone.
Genuine credit: novelty is real and understated; therapeutic direction correctly EXCLUDED from the cut.

### Submission compliance — ready-after-checklist
BLOCKERS: repo still private (flip last); **README stale** (old Streamlit vision + placeholder build
instructions + no finding/CS/video-link — the #1 own-goal); music CC-BY must land in the video description.
OWN-GOALS: personal Windows paths in build scripts; dataset-license mislabel ("MIT" vs public-dataset
provision). VERIFIED CLEAN (call these strengths): no secrets in the full git history; `.env`/`cs_state.json`
never tracked; first commit 2026-07-07 (new-work proof); "PyZoBot POC reference-only" boundary clean and not
muddied into the README; MIT LICENSE present; video 2:52 (< 3:00) + summary present.

---

## Panel provenance
Six parallel `general-purpose` Claude sub-agents, cold context, one per lens above; each given the verbatim
narration + per-beat on-screen visuals + the ~180w summary + repo file access. Independent (no shared state);
synthesized by the main thread. Follow-on: codex-debate with the rendered MP4 (A/V) — the cross-model +
multimodal hedge the panel could not provide.
