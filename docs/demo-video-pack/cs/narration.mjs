// CS-native demo — narration (AUTHOR FIRST; calibrated language only —
// consistent with / re-derived / refuted / untested / flagged. Never discovered/proven/definitive).
// Spine: two floods -> the core-facility pain -> Swanson ABC -> LBD's + omics' mirror weaknesses ->
// one platform (LBD built inside Claude Science) -> NAB2 exemplar + the confident NO -> self-check.
// Scene ids MUST match sceneStart() ids in scenes.mjs.
//
// v3 (2026-07-09): tightened to hold the hard 3:00 max (event-details.mf: "3 minute maximum") with
// margin (~2:48 target). Spine + calibration vocabulary + every money-shot number preserved; only
// wordiness removed. b4/b5 cut hardest (they were the two longest beats).

export const TURNS = {
  walk: [
    { id: "b1_floods", text:
      "Every scientist is caught between two floods. The literature — over a million papers a year; " +
      "no one can read even their own field. And the data — one omics run, millions of measurements " +
      "per sample. The discoveries hide in the gap between them." },
    { id: "b2_matrix", text:
      "I felt this directly. For years I ran a metabolomics core facility — samples in, thousands of " +
      "features out. The researcher always asked the one question that mattered: what does it all mean? " +
      "One hypothesis at a time doesn't scale to data like this." },
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
      "each with a receipt at every hop. Watch it refuse — a failed knockdown comes back untested, not a " +
      "false negative. Thirty survive. The standout: NAB2 — stray co-mentions with eczema, but no paper " +
      "had drawn the NAB2-to-Th1/Th2-to-eczema chain — re-derived here, receipt-backed." },
    { id: "b6_selfcheck", text:
      "Its hardest confounder — a possible STAT6 cis-artifact — was refuted live against the authors' own " +
      "genome-wide data; the disease label remains a nomination. And the platform checks itself: a reviewer " +
      "model flagged the words validated and definitive, and I cut them. Swanson's ABC is just the start." },
  ],
};

export const CARDS = {
  title: { text:
    "PyZoBot Arbiter. When you don't know what to ask, surface the data's hidden hypotheses — right " +
    "where you test them. The library and the lab, on one bench." },
  endcap: { text:
    "I built the missing generation half, beside the test — generate a hypothesis, then refute or back " +
    "it with a receipt. Reproducible from public data. That's PyZoBot Arbiter." },
};
