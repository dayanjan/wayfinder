# App design — source & provenance

The Tier-1 Referee UI (`app/streamlit_app.py`) implements a design produced with **Claude co-design**
(claude.ai/design), imported via the DesignSync integration on 2026-07-08.

- **Design project:** "PyZoBot Arbiter Design Brief" — claude.ai/design project
  `563180df-c301-4129-a3b0-bbe5188f9a76`, file `PyZoBot Arbiter.dc.html` (the source of truth for the
  visual system; owner: Dayanjan Wijesinghe).
- **Brief handed to co-design:** `docs/plans/streamlit_design_brief_2026-07-08.md`.
- **Design tokens implemented** (from the co-design file): dark instrument-console theme (default);
  IBM Plex Sans (UI) + IBM Plex Mono (all receipt numbers); teal `#26c6c9` + indigo `#8285f2` brand;
  semantic status palette — ok `#4fd08a` / warn `#f2b64c` / bad `#f26d63` / mute `#7d9095`; the
  slim-left-nav + Receipt Chain (4-across), evidence rail ("gene-level · identical across diseases" vs
  "disease-specific"), sequential gate→effect→program→disease reveal, caveat chips, and the
  "not evaluated — knockdown unverified" halt watermark.

## What is REAL (not mock)
The co-design file used mock data; this app wires every verdict + receipt to the live
`arbiter.lbd.referee_triple` over the four public Perturb-seq tables. The three showcased triples are
verified at Stim8hr: **NAB2 → atopic eczema = SUPPORTED**, **SATB1 → asthma = UNTESTED** (halts at the
gate), **NAB2 → multiple sclerosis = REFUTED** (clean disease-hop NO; same gene as the YES).

## Preflight (screen-only) — run before recording / shipping
1. `python -c "import sys; from pathlib import Path; sys.path.insert(0, str(Path('src').resolve())); from arbiter.lbd.referee_triple import referee_triple, load_referee_data; d=load_referee_data(); print(referee_triple('SATB1','asthma','Stim8hr',d)['answer'])"` → `untested`
2. `streamlit run app/streamlit_app.py` (from repo root)
3. `node app/smoke_referee.mjs` (with the app serving) → clicks all three chips screen-only and asserts
   the rendered verdict + receipts (SMOKE: ALL PASS). Run twice from a fresh browser context.

## Not yet built (post-preflight / stretch, per the debate)
Screen 2 (Hypothesis Engine / funnel + explorer), Screen 3 (Claude Science lane), light-theme toggle,
and the operator-only live Claude Science trigger. See `docs/plans/streamlit_workbench_plan_2026-07-08.md`.
