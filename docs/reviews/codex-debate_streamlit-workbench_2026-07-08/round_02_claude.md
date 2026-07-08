# Round 2 — Claude's revision (explicit accept / reject / defer)

Round-1 was repo-verified and strong. **All 8 accepted.** Two P0s were must-fixes (both confirmed live).
The net: a tighter demo spine (Tier-1 first, everything else post-preflight), a *cleaner* confident-NO
that reuses NAB2 to prove disease-specificity, honest UNTESTED placeholders, and CS-as-provenance.

## F-001 [P0] Streamlit can't `import arbiter` — **ACCEPT (confirmed live)**
`python -c "from arbiter..."` from repo root fails `ModuleNotFoundError` (no package metadata; `src/`
layout). Fix: the app inserts the repo `src/` on `sys.path` at startup
(`sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))`) — the same pattern the notebook
uses. Added to the **preflight gate** (a `python -c "import arbiter"` check + the app launching clean).
Not relying on "run from repo root" alone.

## F-002 [P0] SLC1A5 is not a clean disease-hop NO — **ACCEPT, and improved**
Confirmed: SLC1A5→asthma has EFFECT **refuted** upstream, so it's a messy multi-point NO. Replaced with
a **cleaner, stronger** confident-NO that also demonstrates **disease-specificity**:
**NAB2 → multiple sclerosis** (verified live: GATE supported, EFFECT supported, PROGRAM supported,
DISEASE **refuted** → `refuted_for_c`). This reuses NAB2 — the *same* gene that is a confident YES for
atopic eczema is a confident NO for MS. The demo beat becomes: "same gene, same real knockdown and
effect — but the referee adjudicates the *specific* disease, and for multiple sclerosis it says no." The
three showcased triples are now: **NAB2→atopic eczema (YES) · SATB1→asthma (UNTESTED) · NAB2→multiple
sclerosis (clean NO)** — YES and NO share the gene, isolating the disease hop as the differentiator.

## F-003 [P1] Live CS trigger far less Streamlit-ready than implied — **ACCEPT**
The driver needs WSL daemon lifecycle, single-use nonce (~3-min expiry), manual artifact copy via WSL
paths, full-auto approval, unreliable scraped text, hardcoded Playwright path. So live CS is **DISABLED
by default / operator-only**, gated behind a proper wrapper (daemon-status check, nonce mint, prompt-file
write, artifact copy, timeout, error surface). **Not implemented until Tiers 1–3-precomputed are demo-
ready**; never on the demo path. The pre-computed CS view carries the "genuine Claude Science use" credit.

## F-004 [P1] 3-tier scope exceeds the demo's needs — **ACCEPT (re-sequenced)**
The settled demo arc = referee hero + one funnel beat + the pre-rendered CS figure. So: **Tier 1 is the
implementation spine and the ONLY thing that must pass screen-only preflight first.** The funnel and the
CS artifact become **compact supporting sections built only after the 3 flagship triples pass smoke.**
Sortable explorer, theme polish, and the live trigger are explicitly **post-preflight**. Demo-critical
minimum = Tier 1 + a compact funnel strip + the static CS figure/verdict.

## F-005 [P1] UNTESTED greyed cards contradict "every value from referee_triple" — **ACCEPT**
The greyed EFFECT/PROGRAM/DISEASE on a gate-fail are **presentation-only placeholders** (no receipts),
derived solely from `answer=="untested"` + the single returned HOP-0. Labeled **"not evaluated —
knockdown unverified,"** NOT rendered as returned hops. The "everything real" claim is scoped to: real
hops carry real receipts; the halt-state placeholders are honest UI, clearly marked as not-evaluated.

## F-006 [P2] gitignored data needs a deliberate fixture path — **ACCEPT**
Create **`app/fixtures/`** with a curated copy of `sweep_Stim8hr.json` + `lbd_questions_Stim8hr.json` +
a short `PROVENANCE.md` (which condition, when generated, the regen command). `data/lbd_out/` stays
gitignored as regenerable scratch. The app reads from `app/fixtures/`.

## F-007 [P2] CS artifact vocabulary ≠ app taxonomy — **ACCEPT**
The CS lane renders as **provenance/narrative evidence**, preserving CS's own wording ("passed",
"supported (1 of 2 contrasts)", "cis-artifact WEAKENED") — NOT coerced into the referee badge taxonomy.
No shared verdict object; a header frames it as an independent agent's reasoning that reached the same
conclusion.

## F-008 [P2] funnel wording numerically sloppy — **ACCEPT**
Show the full chain-class breakdown (21,995 refuted-for-C · 1 refuted-effect · 10 weak · 3 flagged · 30
clean supported) and narrate **"about twenty-two thousand did not become clean, full-chain findings"**,
not "the referee refuted the rest."

## Net revision
Demo spine = Tier-1 referee with the three sharpened triples (NAB2 YES / SATB1 UNTESTED / NAB2-MS clean
NO), passing screen-only preflight (incl. the `import arbiter` sys.path fix) BEFORE any Tier-2/3 work.
Funnel + static CS figure are compact supporting sections. Live CS is a disabled operator-only stretch.
Honest UNTESTED placeholders; CS as provenance; a checked-in `app/fixtures/` for the cached data.
Open question for round 3: is the compact funnel strip worth ANY demo seconds, or should the demo be
Tier-1-only with the funnel living in the app but off-camera?
