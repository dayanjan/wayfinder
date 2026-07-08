// Screen-only preflight for the Tier-1 Referee. Requires the app serving (default :8533) and Playwright's
// chromium (resolved from the demo-video skill; override via DEMO_NODE_MODULES). Usage:
//   streamlit run app/streamlit_app.py --server.port 8533   # in one shell
//   node app/smoke_referee.mjs [screenshotDir]              # in another
import { createRequire } from 'module';
const require = createRequire(import.meta.url);
const NM = process.env.DEMO_NODE_MODULES || 'C:/Users/wijesingheds/.claude/skills/demo-video/node_modules';
const { chromium } = require(`${NM}/playwright`);

const URL = process.env.APP_URL || `http://localhost:${process.env.PORT || 8533}/`;
const SHOT = process.argv[2] || '.';

const cases = [
  { chip: 'SATB1 → asthma',             expect: 'UNTESTED', wantWatermark: true },
  { chip: 'NAB2 → atopic eczema',       expect: 'SUPPORTED', wantWatermark: false },
  { chip: 'NAB2 → multiple sclerosis',  expect: 'REFUTED',  wantWatermark: false },
];

const browser = await chromium.launch({ headless: true });
const page = await browser.newPage({ viewport: { width: 1440, height: 940 } });
let fails = 0;
try {
  await page.goto(URL, { waitUntil: 'networkidle', timeout: 30000 });
  await page.getByRole('button', { name: 'Adjudicate' }).first().waitFor({ timeout: 20000 });
  for (const c of cases) {
    await page.getByRole('button', { name: c.chip }).first().click();
    await page.locator('.pz-badge').first().waitFor({ timeout: 10000 });
    await page.waitForTimeout(2600);
    const badge = (await page.locator('.pz-badge').first().innerText()).trim();
    const ntoks = await page.locator('.pz-tok').count();
    const wm = await page.locator('.pz-wm').count();
    const ok = badge.startsWith(c.expect) && (c.wantWatermark ? wm >= 3 : ntoks >= 3);
    console.log(`${ok ? 'PASS' : 'FAIL'}  ${c.chip.padEnd(30)} badge="${badge}" tokens=${ntoks} watermark=${wm}`);
    if (!ok) fails++;
    await page.screenshot({ path: `${SHOT}/smoke_${c.expect}.png` });
  }
} catch (e) {
  console.log('ERROR', e.message); fails++;
} finally {
  await browser.close();
}
console.log(fails === 0 ? 'SMOKE: ALL PASS' : `SMOKE: ${fails} FAIL`);
process.exit(fails === 0 ? 0 : 1);
