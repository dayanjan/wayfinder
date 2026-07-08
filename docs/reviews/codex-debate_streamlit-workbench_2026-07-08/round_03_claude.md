# Round 3 — Claude's final (consolidated) position

Round 2 dropped 7/8, escalated 1 (F-001 preflight detail), surfaced 3 new — all implementation-handoff
tightening. All accepted. The plan is now a clean Tier-1-first build spec.

## F-009 [P1] preflight command must mirror the app's sys.path fix — **ACCEPT**
The preflight check is now the exact app import path:
`python -c "import sys; from pathlib import Path; sys.path.insert(0, str(Path('src').resolve())); from arbiter.lbd.referee_triple import referee_triple, load_referee_data; d=load_referee_data(); print(referee_triple('SATB1','asthma','Stim8hr',d)['answer'])"`
run from repo root, asserting `untested` — plus the app itself launching clean and the three triples
rendering. (Considered minimal packaging via `pyproject`/`pip install -e .`; the sys.path insert is
lower-risk for the deadline and matches the notebook precedent.)

## F-010 [P1] CS artifact still shows stale SLC1A5 disease-hop case — **ACCEPT**
The committed CS artifact (`claude_science_verdict.json`) stays as-is — it is a faithful record of what
Claude Science produced (it independently characterized SLC1A5 as refuted with weak effect). But the
**app's compact CS panel must NOT surface SLC1A5 as "the clean NO"** — the app showcases **NAB2→multiple
sclerosis** as the sole clean disease-hop NO. The CS panel renders the NAB2 evidence chain + the figure
as provenance; if it lists CS's contrast cases at all, SLC1A5 is labeled "legacy / chain-level contrast,"
not the demo's clean NO. No rewrite of the historical artifact.

## F-011 [P2] design brief invites post-preflight scope into the first build — **ACCEPT (with a defended nuance)**
The brief now **demarcates a "Tier-1 MVP (design + build FIRST)"** — the Referee screen, the Receipt
Chain in its three states, the three showcased triples — from **"post-preflight design notes"** (the full
sortable explorer, light/dark theming, motion polish, the live-CS button). *Defended nuance:* I keep the
FULL app vision in the brief (not just Tier-1) because Claude co-design produces a more cohesive,
attractive design when it sees the whole app — but the **implementation handoff** is explicitly Tier-1
MVP first, everything else clearly marked post-preflight. Design-cohesion and build-order are different
handoffs; the brief serves both by labeling, not by amputation.

## Settled for round 3 (Codex's next-Q)
- **Preflight command:** the exact sys.path-insert one-liner above (F-009).
- **Does the compact demo include funnel seconds?** YES — the demo's Scene 4 IS the funnel-as-refusal
  beat, so the app needs a **compact funnel strip on-camera** (full class breakdown, ~one band). The
  **full sortable explorer is NOT demo-critical** (post-preflight). So demo-critical app surface =
  Tier-1 referee + compact funnel strip + static CS figure.
- **CS panel avoids stale SLC1A5:** per F-010 — NAB2→MS is the only showcased clean NO; CS panel is
  provenance (NAB2 chain + figure), SLC1A5 not surfaced as the demo NO.

## Canonical Tier-1-first build handoff
1. `app/streamlit_app.py`: sys.path insert → referee against the real contract (two branches, full
   taxonomy, presentation-only UNTESTED placeholders, stable labels). Add `streamlit` to `requirements.txt`.
2. Preflight gate: the F-009 import check + app launches clean + 3 triples (NAB2→eczema YES, SATB1→asthma
   UNTESTED-halts-at-gate, NAB2→MS clean NO) render correct + Playwright smoke asserts visible text +
   passes twice from fresh context. No further build until green.
3. Compact funnel strip (from `app/fixtures/`) + static CS figure/verdict (provenance) — the demo-
   supporting sections.
4. Post-preflight: full sortable explorer, theming, motion; then (operator-only stretch) the live-CS
   trigger behind a proper wrapper.

## Preserve-intent check
The novel claim — **CS is an async/pre-computed lane, NOT the synchronous core; the <1s referee is the
demo/interactive spine** — survived intact and was reinforced (live-CS demoted to disabled operator-only
stretch; CS panel is provenance). The falsification hero is sharpened (NAB2 YES vs NAB2→MS NO isolates the
disease hop; UNTESTED visibly halts at the gate). Not sanded.
