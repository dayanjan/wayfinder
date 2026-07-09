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

    // ── B4 · CS builds the LBD generator, live ───────────────────────────────
    await openConversation(rec, "Live LBD Literature Question Generator");
    rec.sceneStart("b4_build");
    await rec.setCaption("Claude Science authored the LBD generator — live literature + database calls");
    await rec.wheel(0, 520, 3, 1300);   //TODO Fri: land on the live Europe PMC / Open Targets calls
    await rec.sceneEnd();
    await rec.setCaption("");

    // ── B5 · the referee culls (22,039 -> 30) + NAB2 payoff ──────────────────
    await openConversation(rec, "Literature-Based-Discovery Loose Gene Universe Sweep");
    rec.sceneStart("b5_referee");
    await rec.setCaption("22,039 questions in — 30 receipt-backed survivors; a confident NO on the rest");
    await rec.wheel(0, 520, 3, 1300);   //TODO Fri: land on the funnel + a REFUTED example
    // cut to the NAB2 A->B->C graphic for the "NAB2 -> Th1/Th2 -> atopic eczema" clause
    const b5 = rec.durations["b5_referee"] || 22;
    await rec.untilT(Math.max(1, b5 - 8));
    await rec.setCaption("");
    await p.goto(ASSETS + "swanson-graphic.html?scene=nab2", { waitUntil: "load", timeout: 20000 });
    await rec.sceneEnd();

    // ── B6 · self-check (STAT6 refuted live + Reviewer kills the overclaim) ───
    await openConversation(rec, "Stage3: NAB2-STAT6 Cis-Artifact Verification");
    rec.sceneStart("b6_selfcheck");
    await rec.setCaption("Hardest confounder refuted live; a reviewer model killed the overclaim");
    await rec.wheel(0, 520, 3, 1300);   //TODO Fri: land on STAT6 unmoved + the Reviewer calibrated-language flag
    await rec.sceneEnd();
    await rec.setCaption("");
  },
};
