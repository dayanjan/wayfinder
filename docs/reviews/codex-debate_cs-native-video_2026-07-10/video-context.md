# The video you are judging — frame storyboard + transcript + audio metadata

You (Codex) have been given **12 attached image frames** — a storyboard of the actual rendered 2:52 demo
video, in order. Study them as if watching the video. Below is the exact narration transcript (what is
spoken), the on-screen captions (lower-thirds), per-beat durations (for pacing), and the audio metadata.

## IMPORTANT capability boundary (be honest about this in your critique)
The attached frames are the VISUAL track. The AUDIO track — the narration is the **researcher's own cloned
voice** (ElevenLabs voice clone), under a soft **CC-BY music bed** ("Deliberate Thought", Kevin MacLeod,
−20 dB, faded) — you CANNOT hear. So: judge the **visuals, on-screen text, narrative arc, pacing, A/V
legibility, and honesty of the framing** rigorously. Explicitly FLAG voice-timbre / naturalness / music-mix
as **not-assessable from frames** (do not guess these). Pacing you CAN infer from the per-beat durations +
transcript length.

## Frame map (attached, in order)
| # | file | beat | ~t | what it shows |
|---|---|---|---|---|
| 1 | 01-title.png | title card | 0:05 | "PyZoBot Arbiter — The library and the lab, on one bench" |
| 2 | 02-b1-floods.png | B1 (slide) | 0:18 | "two floods" animated slide |
| 3 | 03-b2-matrix.png | B2 (slide) | 0:35 | feature-matrix "what does it all mean?" slide |
| 4 | 04-b3-swanson.png | B3 (graphic) | 0:54 | Swanson ABC concept graphic |
| 5 | 05-b4-live-cs.png | B4 (LIVE CS) | 1:12 | live Claude Science UI: liveness proof + receipt.md artifact open |
| 6 | 06-b5-live.png | B5 (LIVE CS) | 1:35 | live CS loose-sweep conversation |
| 7 | 07-b5-IL2-untested.png | B5 (overlay) | 1:44 | "IL2 → UNTESTED" receipt overlay (the confident NO) |
| 8 | 08-b5-funnel-nab2.png | B5 (overlay) | 1:53 | funnel 3,935→22,039→30 + NAB2 receipt row |
| 9 | 09-b5-swanson-nab2.png | B5 (graphic) | 2:01 | Swanson A→B→C NAB2 payoff |
| 10 | 10-b6a-stat6-cis.png | B6 (LIVE CS) | 2:12 | live CS STAT6 cis-artifact "Cis-exclusion statement (calibrated)" |
| 11 | 11-b6b-reviewer.png | B6 (overlay) | 2:23 | "The platform checks itself" reviewer overclaim-flag overlay |
| 12 | 12-endcap.png | endcap card | 2:45 | "Generate a hypothesis. Test it. One platform." |

Total runtime 2:52 (under the 3:00 hard maximum). Order: title card → B1..B6 walk → endcap card.

## Narration transcript (verbatim, spoken in the researcher's own cloned voice) + durations
- **Title card (10s):** "PyZoBot Arbiter. When you don't know what to ask, surface the data's hidden hypotheses — right where you test them. The library and the lab, on one bench."
- **B1 floods (17.4s):** "Every scientist is caught between two floods. The literature — over a million papers a year; no one can read even their own field. And the data — one omics run, millions of measurements per sample. The discoveries hide in the gap between them."
- **B2 matrix (17.3s):** "I felt this directly. For years I ran a metabolomics core facility — samples in, thousands of features out. The researcher always asked the one question that mattered: what does it all mean? One hypothesis at a time doesn't scale to data like this."
- **B3 Swanson (20.6s):** "What broke it open for me was literature-based discovery. Its simplest form is Swanson's ABC: if the literature links A to B, and B to C, but no one has joined A to C, then A-to-C is a hidden, testable hypothesis. Swanson's own case — fish oil, blood viscosity, Raynaud's."
- **B4 build (27.1s):** "But literature-based discovery has two burdens: it's a slog to collate, and it over-produces hypotheses no one can test. Large-scale omics is the mirror problem: mountains of answers, no questions. One platform can now generate a hypothesis and test it in one place — Claude Science. The generation half was missing, so I had the workbench author and run a discovery generator live, from scratch."
- **B5 referee (33.9s):** "Now generation and testing run side by side. On the Marson lab's CD4 T-cell Perturb-seq data, the generator posed twenty-two thousand gene-and-disease hypotheses; a deterministic referee re-ran each with a receipt at every hop. Watch it refuse — a failed knockdown comes back untested, not a false negative. Thirty survive. The standout: NAB2 — stray co-mentions with eczema, but no paper had drawn the NAB2-to-Th1/Th2-to-eczema chain — re-derived here, receipt-backed."
- **B6 self-check (21.0s):** "Its hardest confounder — a possible STAT6 cis-artifact — was refuted live against the authors' own genome-wide data; the disease label remains a nomination. And the platform checks itself: a reviewer model flagged the words validated and definitive, and I cut them. Swanson's ABC is just the start."
- **Endcap card (11s):** "I built the missing generation half, beside the test — generate a hypothesis, then refute or back it with a receipt. Reproducible from public data. That's PyZoBot Arbiter."

## On-screen captions (lower-thirds, verbatim — these are the burned-in text a judge reads)
- B4: "Claude Science authored the LBD generator — live literature + database calls"
- B5 (held during live CS): "full 22,039 sweep = CS-native cached-receipt replay · live proof = micro-sweep · falsification = STAT6 S3"
- B5 (IL2 overlay): "Watch it refuse — a failed knockdown returns UNTESTED, not a false negative"
- B5 (funnel overlay): "Thirty survive — NAB2 → Th1/Th2 → atopic eczema, re-derived with a receipt at every hop"
- B6a (STAT6 live): "A possible STAT6 cis-artifact — refuted live; the GWAS disease label stays a nomination"
- B6b (reviewer overlay): "...and the platform checks itself — a reviewer flagged 'validated' and 'definitive', and I cut them"

## Overlay content (the prepared "Claude Science receipt" overlays, verbatim on screen)
- **IL2→UNTESTED** (frame 7): "HOP 0 · knockdown-QC gate FAILED · 0 of 2 guides reached signif_knockdown · best adj_p 0.32 · A guide is informative only if it actually silenced the gene. So a null downstream result is UNTESTED — never 'no effect.' An artifact caught, not a false negative. · By contrast, NAB2's gate passed — 2 of 2 guides, adj_p 1e−16 — so NAB2 can be judged." Eyebrow: "Claude Science receipt · tracer/receipt_chain.md".
- **Funnel + NAB2** (frame 8): "3,935 genes → 22,039 hypotheses posed → 30 clean, receipt-backed (21,995 refuted & culled). NAB2 → Th1/Th2 polarization → atopic eczema · Stim8hr · rank #4 · ab 66 · bc 2,184 · ac_lit 6 · ac_known 0.0376 · effect 301 · score −1.137 · referee verdict: supported · ALL_PASS · pure-replay cache Δ0 · re-derived, not discovered." Eyebrow: "Claude Science receipt · stage1/receipt.md".
- **Reviewer** (frame 11): "The platform checks itself · PASS_WITH_NOTES · numeric fidelity PASS — every number matched the source · ⚑ 'validated' flagged — a certainty upgrade akin to 'proven.' Not a sanctioned calibration term. · ⚑ 'definitive' flagged — unwarranted certainty beyond the plain 'REFUTED' status. · An independent reviewer model caught the overclaims — and I cut them." Eyebrow: "Claude Science reviewer · stage5/review.json".
