// CS-native demo — scenes. SCREEN-ONLY: mouse/keyboard only, no API reach.
// Slides + prepared CS-receipt overlays are our own file:// assets; live beats drive the LIVE
// Claude Science UI. Passes the screen-only gate (goto is WARN-only; no fetch/request/api/evaluate).
//
// v4 (2026-07-10): codex-debate + panel edits — B0 cold-open on the refusal; two plain honesty
// captions (live micro-sweep vs cached full sweep); STAT6 legibility callout in B6; frame-8 overlay
// carries the split disease-label + de-numbered receipt. Wayfinder rename lives in narration/cards.

const pg = (rec) => rec.page;

const ASSETS =
  "file:///C:/Users/wijesingheds/Documents/04%20Fun%20with%20Coding/2026-07-07%20PyZoBot-Arbiter/docs/demo-video-pack/assets/";
const CS = "http://localhost:8000/";   // confirm port via `claude-science status`

// VERIFIED frame URLs (2026-07-09 de-risk; see CAPTURE_PLAN.md).
const FRAMES = {
  b4:  CS + "projects/proj_64a5e671c715/frames/2b61c815-3e41-48fb-945c-618e8e94a190", // live micro-sweep
  b5:  CS + "projects/proj_fd9d7046d730/frames/681b75c5-64eb-48dc-a239-f8a45c1fcb88", // loose (cached) sweep
  b6a: CS + "projects/proj_ea76f1a08006/frames/fb886080-da06-492a-bfec-df1a972955bf", // stage3 STAT6
};

// Best-effort dismiss of CS UI chrome (update toast + "where you left off" tooltip) — real clicks.
async function dismissChrome(rec) {
  const p = pg(rec);
  for (const sel of ['button:has-text("Later")', '[aria-label="Close"]', 'button:has-text("×")']) {
    const b = p.locator(sel);
    if (await b.count().catch(() => 0)) await b.first().click({ timeout: 1500 }).catch(() => {});
  }
}

// Play one self-animating slide/overlay for the full narration beat.
async function playSlide(rec, file, id, caption) {
  await pg(rec).goto(ASSETS + file, { waitUntil: "load", timeout: 20000 });
  rec.sceneStart(id);
  if (caption) await rec.setCaption(caption);
  await rec.sceneEnd();
  await rec.setCaption("");
}

export const SCENES = {
  walk: async (rec) => {
    const p = pg(rec);

    // ── B0 · COLD-OPEN on the confident NO (F-015: distinctive behavior in the first seconds) ──
    await playSlide(rec, "overlay-no-il2.html", "b0_hook",
      "A failed knockdown → UNTESTED, not a false negative — the moat");

    // ── B1 · the two floods (slide) ──────────────────────────────────────────
    await playSlide(rec, "slide-two-floods.html", "b1_floods");

    // ── B2 · the core-facility pain (slide) ──────────────────────────────────
    await playSlide(rec, "slide-feature-matrix.html", "b2_matrix");

    // ── B3 · Swanson ABC (concept graphic) ───────────────────────────────────
    await playSlide(rec, "swanson-graphic.html?scene=swanson", "b3_swanson");

    // ── B4 · CS builds the LBD generator LIVE (liveness proof visible on load) ──
    await p.goto(FRAMES.b4, { waitUntil: "domcontentloaded", timeout: 30000 });
    await rec.sleep(1500); await dismissChrome(rec);
    rec.sceneStart("b4_build");
    // Plain honesty caption #1 (F-065): this is the genuinely LIVE proof.
    await rec.setCaption("Live micro-sweep — the generator it wrote, run on live literature + database calls");
    await rec.sceneEnd();
    await rec.setCaption("");

    // ── B5 · referee culls (22,039 -> 30) + NAB2 payoff ───────────────────────
    // Live b5 frame establishes "real Claude Science" (cached full sweep); funnel overlay carries the
    // de-numbered NAB2 receipt with the split disease-label. The refusal itself was front-loaded in B0.
    await p.goto(FRAMES.b5, { waitUntil: "domcontentloaded", timeout: 30000 });
    await rec.sleep(1500); await dismissChrome(rec);
    rec.sceneStart("b5_referee");
    const b5 = rec.durations["b5_referee"] || 30;
    // Plain honesty caption #2 (F-065): scope the full sweep as a cached replay (not a live crawl).
    await rec.setCaption("Full 22,039 sweep — cached replay of the same deterministic referee");
    await rec.untilT(Math.max(1, b5 * 0.42));
    // REQUIRED frame — funnel + de-numbered NAB2 receipt + split disease-label (F-095/F-035/F-115).
    await p.goto(ASSETS + "overlay-funnel-nab2.html", { waitUntil: "load", timeout: 20000 });
    await rec.setCaption("Thirty clean candidates survive — NAB2 → Th1/Th2 re-derived; eczema stays a nomination");
    await rec.untilT(Math.max(1, b5 * 0.80));
    await rec.setCaption("");
    await p.goto(ASSETS + "swanson-graphic.html?scene=nab2", { waitUntil: "load", timeout: 20000 }); // A->B->C payoff
    await rec.sceneEnd();

    // ── B6 · self-check: STAT6 refuted live -> legible callout -> Reviewer kills overclaim ──
    await p.goto(FRAMES.b6a, { waitUntil: "domcontentloaded", timeout: 30000 });
    await rec.sleep(1500); await dismissChrome(rec);
    rec.sceneStart("b6_selfcheck");
    const b6 = rec.durations["b6_selfcheck"] || 22;
    await rec.setCaption("A possible STAT6 cis-artifact — refuted live; the GWAS disease label stays a nomination");
    await rec.untilT(Math.max(1, b6 * 0.40));
    // F-025 — one legible callout of the STAT6 evidence (the live receipt is too small to read at scale).
    await p.goto(ASSETS + "overlay-stat6.html", { waitUntil: "load", timeout: 20000 });
    await rec.setCaption("STAT6 unmoved by NAB2 knockdown → the cis-artifact is refuted");
    await rec.untilT(Math.max(1, b6 * 0.70));
    // REQUIRED frame — reviewer flag via prepared CS-receipt overlay (stage5/review.json).
    await p.goto(ASSETS + "overlay-reviewer.html", { waitUntil: "load", timeout: 20000 });
    await rec.setCaption("...and the platform checks itself — a reviewer flagged 'validated' and 'definitive', and I cut them");
    await rec.untilT(Math.max(1, b6 * 0.78));
    // v5 — silent caption for the honest held-out null (no added spoken time; synced to the new b6 clause).
    await rec.setCaption("Held-out test (links unseen pre-2016): the referee's own ranking came back null — reported straight");
    await rec.sceneEnd();
    await rec.setCaption("");
  },
};
