// CS-native demo — narration (AUTHOR FIRST; calibrated language only —
// consistent with / re-derived / refuted / untested / flagged. Never discovered/proven/definitive).
// Spine: two floods -> the core-facility pain -> Swanson ABC -> LBD's + omics' mirror weaknesses ->
// one platform (LBD built inside Claude Science) -> NAB2 exemplar + the confident NO -> self-check.
// Scene ids MUST match sceneStart() ids in scenes.mjs.

export const TURNS = {
  walk: [
    { id: "b1_floods", text:
      "Every scientist today is caught between two floods. On one side, the literature — over a million " +
      "new papers a year; no one can read their own field, let alone the one next door. On the other, the " +
      "data — a single omics run returns millions of measurements per sample. The discoveries hide in the " +
      "gap between them." },
    { id: "b2_matrix", text:
      "I felt this directly. For years I ran a metabolomics and lipidomics core facility. Samples came in; " +
      "I generated the data and handed back a matrix of thousands of features — and the researcher asked the " +
      "only question that mattered: what does it all mean? Testing one hypothesis at a time simply doesn't " +
      "scale to data like this." },
    { id: "b3_swanson", text:
      "What broke it open for me was literature-based discovery. Its simplest form is Swanson's ABC model: " +
      "if the literature links A to B, and B to C, but no one has connected A to C, then A-to-C is a hidden, " +
      "testable hypothesis. Swanson's own case: fish oil, blood viscosity, Raynaud's — a link no single " +
      "paper had drawn, later confirmed." },
    { id: "b4_build", text:
      "But literature-based discovery carried two burdens: it's a slog to collate, and it generates far more " +
      "hypotheses than anyone can test. Large-scale omics has the mirror problem — mountains of answers with " +
      "no questions. Now there's one platform that can generate a hypothesis and validate it in the same " +
      "place: Claude Science. The generation half was capable but missing — so I built it, and had the " +
      "workbench author and run a literature-based-discovery generator live, from scratch." },
    { id: "b5_referee", text:
      "Now generation and testing run side by side, each covering the other's weakness. On the Marson lab's " +
      "CD4 T-cell Perturb-seq data, the generator posed twenty-two thousand gene-and-disease hypotheses; a " +
      "deterministic referee re-ran each against the data with a receipt at every hop. Watch it refuse — a " +
      "failed knockdown comes back untested, not a false negative. Thirty survive. The standout: NAB2 — six " +
      "stray co-mentions with eczema, but no paper drawing the NAB2-to-Th1/Th2-to-eczema chain — re-derived " +
      "here, receipt-backed." },
    { id: "b6_selfcheck", text:
      "Its hardest confounder — a possible STAT6 cis-artifact — was refuted live against the authors' own " +
      "genome-wide data; the GWAS disease label remains a nomination. And the platform checks itself: a " +
      "reviewer model flagged the words validated and definitive as overclaims, and I cut them. Swanson's " +
      "ABC was just the start — the first of several discovery methods we're bringing to the bench." },
  ],
};

export const CARDS = {
  title: { text:
    "PyZoBot Arbiter. When you don't know what to ask, let the data's implicit hypotheses surface — " +
    "and build literature-based discovery right where you test it. The library and the lab, on one bench." },
  endcap: { text:
    "In this workbench, I built the missing generation half — beside the test. Generate a hypothesis from " +
    "the literature, then refute it or back it with a receipt, in one place. Reproducible from public " +
    "Perturb-seq data. That is PyZoBot Arbiter." },
};
