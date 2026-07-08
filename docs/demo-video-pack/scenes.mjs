// demo-video PACK — scenes.mjs  (PyZoBot Arbiter — one actor, one journey across three screens)
// Screen-only: mouse/keyboard only, no API reach. Drives the live Streamlit app on BASE.
const pg = (rec) => rec.page;
const BASE = "http://localhost:8501/";

// wait for the referee verdict badge to show the EXPECTED word (survives Streamlit rerun churn)
async function waitBadge(rec, word) {
  await pg(rec).locator(".pz-badge", { hasText: word }).first().waitFor({ timeout: 12000 });
}

export const SCENES = {
  walk: async (rec) => {
    const p = pg(rec);
    await p.goto(BASE, { waitUntil: "networkidle", timeout: 45000 });
    await p.getByRole("button", { name: "Adjudicate", exact: true }).first().waitFor({ timeout: 25000 });
    await rec.sleep(900);

    // ── S1 · confident YES (credibility-setter) ──────────────────────────────
    rec.sceneStart("s1_yes");
    await rec.act(p.getByRole("button", { name: /NAB2 → atopic eczema/ }).first());
    await waitBadge(rec, "SUPPORTED");
    await rec.setCaption("NAB2 → Th1/Th2 → atopic eczema — a receipt at every hop");
    await rec.sleep(2300);                                   // let the chain reveal gate→effect→program→disease
    await rec.moveTo(p.locator(".pz-chain").first()).catch(() => {});
    await rec.sceneEnd();

    // ── S2 · UNTESTED (the centerpiece — halts at the gate) ──────────────────
    await rec.setCaption("");
    rec.sceneStart("s2_untested");
    await rec.act(p.getByRole("button", { name: /SATB1 → asthma/ }).first());
    await waitBadge(rec, "UNTESTED");
    await rec.untilT(3);
    await rec.setCaption("The knockdown never took — untested, not a negative");
    await rec.sleep(2300);
    await rec.moveTo(p.locator(".pz-wm").first()).catch(() => {});   // point at the "not evaluated" halt
    await rec.sceneEnd();

    // ── S3 · confident NO (disease-specific) ─────────────────────────────────
    await rec.setCaption("");
    rec.sceneStart("s3_no");
    await rec.act(p.getByRole("button", { name: /NAB2 → multiple sclerosis/ }).first());
    await waitBadge(rec, "REFUTED");
    await rec.setCaption("Same gene — a confident no at the disease hop");
    await rec.sleep(2300);
    await rec.moveTo(p.locator(".pz-chain").first()).catch(() => {});
    await rec.sceneEnd();

    // ── S4 · the cull / funnel ───────────────────────────────────────────────
    await rec.setCaption("");
    rec.sceneStart("s4_funnel");
    await rec.act(p.getByRole("button", { name: "Hypothesis Engine" }).first());
    await p.locator(".pz-funnel").first().waitFor({ timeout: 12000 });
    await rec.setCaption("22,039 questions generated — the referee kept only 30, receipt-backed");
    await rec.untilT(5);
    await rec.moveTo(p.locator(".pz-funnel").first()).catch(() => {});
    await rec.sceneEnd();

    // ── S5 · Claude Science depth ────────────────────────────────────────────
    await rec.setCaption("");
    rec.sceneStart("s5_depth");
    await rec.act(p.getByRole("button", { name: "Claude Science" }).first());
    await p.locator(".pz-callout").first().waitFor({ timeout: 12000 });
    await rec.setCaption("An independent Claude Science agent — same verdict; the STAT6 confounder refuted");
    await rec.untilT(5);
    await rec.moveTo(p.locator(".pz-conf").first()).catch(() => {});
    await rec.sceneEnd();
    await rec.setCaption("");
  },
};
