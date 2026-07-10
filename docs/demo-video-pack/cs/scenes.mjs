// CS-native demo — scenes. SCREEN-ONLY: mouse/keyboard only, no API reach.
// Slides (beats 1-3) are our own file:// assets that auto-animate; CS captures (beats 4-6)
// drive the LIVE Claude Science UI (real front door -> click a conversation card -> scroll).
// Passes the screen-only gate (goto is WARN-only; no fetch/request/api/evaluate here).
//
// FRIDAY TODOs are marked //TODO — they need the live CS on screen to tune (scroll targets,
// exact card titles). Everything else runs as-is.

const pg = (rec) => rec.page;

// Absolute file URL to the committed slide assets (spaces %20-encoded). //TODO if repo moves.
const ASSETS =
  "file:///C:/Users/wijesingheds/Documents/04%20Fun%20with%20Coding/2026-07-07%20PyZoBot-Arbiter/docs/demo-video-pack/assets/";
const CS = "http://localhost:8000/";   //TODO Fri: confirm port via `claude-science status`

// VERIFIED frame URLs (2026-07-09 de-risk; see CAPTURE_PLAN.md). Robust fallback to home->click.
const FRAMES = {
  b4:  CS + "projects/proj_64a5e671c715/frames/2b61c815-3e41-48fb-945c-618e8e94a190", // live micro-sweep
  b5:  CS + "projects/proj_fd9d7046d730/frames/681b75c5-64eb-48dc-a239-f8a45c1fcb88", // loose sweep
  b6a: CS + "projects/proj_ea76f1a08006/frames/fb886080-da06-492a-bfec-df1a972955bf", // stage3 STAT6
  b6b: CS + "projects/proj_99ccc044f003/frames/4473ddef-0858-47f8-a4f8-408ce5ecfdcf", // stage5 reviewer
};

// Best-effort dismiss of CS UI chrome (update toast + "where you left off" tooltip) — real clicks.
async function dismissChrome(rec) {
  const p = pg(rec);
  for (const sel of ['button:has-text("Later")', '[aria-label="Close"]', 'button:has-text("×")']) {
    const b = p.locator(sel);
    if (await b.count().catch(() => 0)) await b.first().click({ timeout: 1500 }).catch(() => {});
  }
}

// Play one self-animating slide for the full narration beat (slides carry their own captions).
async function playSlide(rec, file, id) {
  await pg(rec).goto(ASSETS + file, { waitUntil: "load", timeout: 20000 });
  rec.sceneStart(id);
  await rec.sceneEnd();
}

// Open a CS conversation from the real home screen by its visible title (screen-only click).
async function openConversation(rec, title) {
  const p = pg(rec);
  await p.goto(CS, { waitUntil: "domcontentloaded", timeout: 30000 });
  await rec.sleep(1800);
  await rec.act(p.getByText(title, { exact: false }).first());   //TODO Fri: confirm the card lands in the transcript
  await rec.sleep(2600);
}

export const SCENES = {
  walk: async (rec) => {
    const p = pg(rec);

    // ── B1 · the two floods (slide) ──────────────────────────────────────────
    await playSlide(rec, "slide-two-floods.html", "b1_floods");

    // ── B2 · the core-facility pain (slide) ──────────────────────────────────
    await playSlide(rec, "slide-feature-matrix.html", "b2_matrix");

    // ── B3 · Swanson ABC (concept graphic) ───────────────────────────────────
    await playSlide(rec, "swanson-graphic.html?scene=swanson", "b3_swanson");

    // ── B4 · CS builds the LBD generator, live (Liveness proof visible on load) ──
    await p.goto(FRAMES.b4, { waitUntil: "domcontentloaded", timeout: 30000 });
    await rec.sleep(1500); await dismissChrome(rec);
    rec.sceneStart("b4_build");
    await rec.setCaption("Claude Science authored the LBD generator — live literature + database calls");
    // Money shot on the bottom view: ranked table + "Liveness proof" (ab->7, bc->30473, ac_lit->82, OT->3000).
    //TODO Fri: optional — open the executed_code.py thumbnail to show "the generator it wrote".
    await rec.sceneEnd();
    await rec.setCaption("");

    // ── B5 · referee culls (22,039 -> 30) + a VISIBLE NO + NAB2 payoff ────────
    // REQUIRED money shots (release blockers — CAPTURE_PLAN.md F-015) via prepared CS-receipt
    // overlays: live scroll is unreliable (CS opens at bottom + wheel doesn't scroll the transcript).
    // Live b5 frame establishes "real Claude Science"; the overlays render the exact on-disk
    // artifacts (stage1/receipt.md, tracer/receipt_chain.md) — verdict word + receipt reason on screen.
    // Visual order tracks the narration: referee context -> the refusal -> 30 survive + NAB2 -> payoff.
    await p.goto(FRAMES.b5, { waitUntil: "domcontentloaded", timeout: 30000 });
    await rec.sleep(1500); await dismissChrome(rec);
    rec.sceneStart("b5_referee");
    const b5 = rec.durations["b5_referee"] || 30;
    // Honesty caption — scope live-vs-cached ON SCREEN (F-002/F-012), not buried in docs:
    await rec.setCaption("full 22,039 sweep = CS-native cached-receipt replay · live proof = micro-sweep · falsification = STAT6 S3");
    await rec.untilT(Math.max(1, b5 * 0.28));
    // The MOAT made visible (F-005/F-013): one concrete refusal receipt — verdict word + reason.
    await p.goto(ASSETS + "overlay-no-il2.html", { waitUntil: "load", timeout: 20000 });
    await rec.setCaption("Watch it refuse — a failed knockdown returns UNTESTED, not a false negative");
    await rec.untilT(Math.max(1, b5 * 0.52));
    // REQUIRED frame — funnel + NAB2 receipt (ab66/bc2184/ac_lit6/ac_known0.0376/effect301/supported).
    await p.goto(ASSETS + "overlay-funnel-nab2.html", { waitUntil: "load", timeout: 20000 });
    await rec.setCaption("Thirty survive — NAB2 → Th1/Th2 → atopic eczema, re-derived with a receipt at every hop");
    await rec.untilT(Math.max(1, b5 * 0.82));
    await rec.setCaption("");
    await p.goto(ASSETS + "swanson-graphic.html?scene=nab2", { waitUntil: "load", timeout: 20000 }); // NAB2 A->B->C payoff
    await rec.sceneEnd();

    // ── B6 · self-check: STAT6 refuted live (b6a, screen-only) -> Reviewer kills overclaim (overlay) ──
    await p.goto(FRAMES.b6a, { waitUntil: "domcontentloaded", timeout: 30000 });
    await rec.sleep(1500); await dismissChrome(rec);
    rec.sceneStart("b6_selfcheck");
    const b6 = rec.durations["b6_selfcheck"] || 22;
    // b6a "Cis-exclusion statement (calibrated)" is visible on load (screen-only, no overlay needed).
    await rec.setCaption("A possible STAT6 cis-artifact — refuted live; the GWAS disease label stays a nomination");
    await rec.untilT(Math.max(1, b6 * 0.55));
    // REQUIRED frame — reviewer flag via prepared CS-receipt overlay (stage5/review.json, not raw JSON).
    await p.goto(ASSETS + "overlay-reviewer.html", { waitUntil: "load", timeout: 20000 });
    await rec.setCaption("...and the platform checks itself — a reviewer flagged 'validated' and 'definitive', and I cut them");
    await rec.sceneEnd();
    await rec.setCaption("");
  },
};
