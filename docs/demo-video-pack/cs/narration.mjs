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
      "place: Claude Science. The generation half was capable but missing. So I built it." },
    { id: "b5_referee", text:
      "Now generation and testing run side by side, each covering the other's weakness. On the Marson lab's " +
      "CD4 T-cell Perturb-seq data, twenty-two thousand machine-generated hypotheses go in; a deterministic " +
      "referee culls them with a receipt at every hop — and confidently says no, flagging a failed knockdown " +
      "as untested, not a false negative. Thirty survive. The standout: NAB2 to the Th1/Th2 program to " +
      "atopic eczema — a connection the literature had never drawn, backed by a receipt in the data." },
    { id: "b6_selfcheck", text:
      "Its hardest confounder — refuted live against the original authors' own genome-wide data. And the " +
      "platform checks itself: a reviewer model caught and killed my overclaim, in real time. Swanson's ABC " +
      "was just the start — the first of several discovery methods we're bringing to the bench." },
  ],
};

export const CARDS = {
  title: { text:
    "PyZoBot Arbiter. When you don't know what to ask, let the data's implicit hypotheses surface — " +
    "and build literature-based discovery right where you test it. The library and the lab, on one bench." },
  endcap: { text:
    "Generate a hypothesis from the literature, test it on the data, in one platform. Receipt-backed, " +
    "willing to refute, and reproducible from public Perturb-seq data. That is PyZoBot Arbiter." },
};
