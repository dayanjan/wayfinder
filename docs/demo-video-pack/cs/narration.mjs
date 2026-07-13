// CS-native demo — narration (AUTHOR FIRST; calibrated language only —
// consistent with / re-derived / refuted / untested / flagged. Never discovered/proven/definitive).
// Spine: cold-open on the confident NO -> two floods -> core-facility pain -> Swanson ABC ->
// LBD+omics mirror weakness -> LBD built inside Claude Science -> NAB2 + the NO -> self-check.
// Scene ids MUST match sceneStart() ids in scenes.mjs.
//
// v4 (2026-07-10): renamed to Wayfinder; folds in the frame-grounded codex-debate + panel edits —
// IL2 cold-open (b0), spoken builder name (b2), "one key confounder" + "thirty clean candidates survive
// the referee gates" scoping, Anthropic's-workbench reviewer line. Held under the hard 3:00 max.
// v5 (2026-07-13): (1) b2 spoken surname respelled phonetically "Vijay-Sing-her" for the cloned voice —
// TRUE spelling is Wijesinghe (kept correct in the displayed lower-thirds/cards).
// (2) b6: dropped the "Swanson's ABC is just the start" flourish, added the honest held-out-null result
// (the manuscript's central measurement, cut 07-10 predated it). (3) endcap trimmed to hold the total
// under the hard 3:00 cap after (2)'s addition.
// RENDERED 2026-07-13 (this pipeline, live CS on :8765): final 2:57.97 (< 3:00), transcription gate PASS
// 94% mean WITH the CC-BY music bed. Master MP4: .tmp/demo-cs/out/wayfinder_v5.mp4 (out-of-band).

export const TURNS = {
  walk: [
    { id: "b0_hook", text:
      "Watch an AI referee refuse — a failed knockdown comes back untested, not a false negative. " +
      "An artifact caught, not a discovery missed." },
    { id: "b1_floods", text:
      "Every scientist is caught between two floods. The literature — over a million papers a year; " +
      "no one can read even their own field. And the data — one omics run, millions of measurements " +
      "per sample. The discoveries hide in the gap between them." },
    { id: "b2_matrix", text:
      "I felt this directly — I'm Shanaka Vijay-Sing-her. For years I ran a metabolomics core facility — " +
      "samples in, thousands of features out. The researcher always asked the one question that " +
      "mattered: what does it all mean? One hypothesis at a time doesn't scale to data like this." },
    { id: "b3_swanson", text:
      "What broke it open for me was literature-based discovery. Its simplest form is Swanson's ABC: " +
      "if the literature links A to B, and B to C, but no one has joined A to C, then A-to-C is a " +
      "hidden, testable hypothesis. Swanson's own case — fish oil, blood viscosity, Raynaud's." },
    { id: "b4_build", text:
      "But literature-based discovery has two burdens: it's a slog to collate, and it over-produces " +
      "hypotheses no one can test. Large-scale omics is the mirror problem: mountains of answers, no " +
      "questions. One platform can now generate a hypothesis and test it in one place — Claude Science. " +
      "The generation half was missing, so I had the workbench author and run a discovery generator live." },
    { id: "b5_referee", text:
      "Now generation and testing run side by side. On the Marson lab's CD4 T-cell Perturb-seq data, the " +
      "generator posed twenty-two thousand gene-and-disease hypotheses; a deterministic referee re-ran " +
      "each with a receipt at every hop, refusing whenever a knockdown failed. Thirty clean candidates " +
      "survive the referee gates. The standout: NAB2 — stray co-mentions with eczema, but no paper had " +
      "drawn the NAB2-to-Th1/Th2-to-eczema chain — re-derived here, receipt-backed." },
    { id: "b6_selfcheck", text:
      "One key confounder — a possible STAT6 cis-artifact — was refuted live against the authors' own " +
      "genome-wide data; the disease label stays a nomination. And Anthropic's scientific workbench " +
      "checked its own work — its reviewer model flagged the words validated and definitive, and I cut " +
      "them. Measured on links it had never seen, the referee itself came back null — reported straight." },
  ],
};

export const CARDS = {
  title: { text:
    "Wayfinder — the library and the lab, on one bench." },
  endcap: { text:
    "I built the missing generation half — back or refute, with a receipt. That's Wayfinder." },
};
