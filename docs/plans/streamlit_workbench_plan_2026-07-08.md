# PyZoBot Arbiter — the Researcher's Workbench (Streamlit app) — plan v1 (for codex-debate)

**What.** A real, interactive Streamlit app that is the demo hero AND the "researcher who also builds"
artifact: a scientist's instrument that generates untested hypotheses, adjudicates them against real
Perturb-seq receipts (including the confident NO / UNTESTED), and can hand a question to **Claude Science**
for a deeper reasoning pass. Backs the 3-min demo video (`docs/plans/demo_video_plan_2026-07-08.md`).

**Thesis it must serve.** Falsification is the moat — the confident, receipt-backed NO and the UNTESTED
hero catch (a failed knockdown → *untested*, not *negative*, visibly halting at HOP-0). Calibrated
language only. Everything shown is REAL (from `referee_triple` / cached sweep / real CS artifacts) — no
Potemkin.

---

## 0. Architecture — a 3-tier workbench (the load-bearing design decision)

The core constraint is **latency**: the referee is <1s (deterministic pandas over local CSVs); Claude
Science is 5–20 min/task and only drivable via the Playwright automation (daemon + auth nonce + full-auto
approval). So CS cannot be the synchronous core. The resolution is tiered:

| Tier | What | Latency | Data source | Demo role |
|---|---|---|---|---|
| **1 · Referee** | Choose a perturbation gene + an atlas-backed disease module + condition → **Adjudicate** → receipt-backed 4-hop verdict (or HOP-0-halt for UNTESTED) | **<1s** | `referee_triple(gene, disease, condition, d)` live | **HERO** — drives the demo |
| **2 · LBD explorer** | The engine's generate→cull funnel (22,039 → 30) + a browsable/rankable table of the generated questions; click any question → Tier-1 adjudicates it live | **instant** (cached) | `data/lbd_out/sweep_Stim8hr.json` + `lbd_questions_Stim8hr.json` | supporting — the "it asked 22,039 questions" beat |
| **3 · Claude Science lane** | DEFAULT: the pre-computed CS evidence chain (narrative + figure + verdict). OPTIONAL: "Run a fresh Claude Science analysis" that genuinely triggers a live CS task via `drive-claude-science` and displays the returned artifacts | default **instant**; live trigger **minutes (async)** | `docs/claude-science-evidence-chain_2026-07-08/` (default); the CS driver (live) | supporting — "how CS got us there" + the bidirectional wow, OFF the critical path |

**The Claude Science bidirectional decision (the big open question).** YES, build it — but as an **async
deep-dive lane with the pre-computed view as the reliable default**, NOT the synchronous core. Rationale:
CS's minutes-long latency + daemon/auth/Playwright fragility would wreck an interactive demo and is a
live-failure risk on camera; but a genuine "app hands a question to Claude Science and shows its reasoning
back" is a strong Researcher-track ("genuine Claude Science use") + "researcher who builds" signal. So:
show the pre-computed CS chain instantly by default; make the LIVE trigger a clearly-labeled
("~several minutes") optional capability that is **not** on the demo's critical path (demo uses the
pre-computed view or a pre-warmed run). Live-trigger is a **stretch**, not demo-critical.

---

## 1. Scope & sequencing (re-sequenced per debate R1/F-004 — Tier-1 spine passes preflight FIRST)

1. **Tier 1 referee — THE SPINE (demo-critical, ~half day).** The hero, and the ONLY thing that must pass
   **screen-only preflight FIRST** (real verdicts, the two render branches, the three showcased triples,
   the `import arbiter` sys.path fix, two clean fresh-context runs). Nothing else is built until this is
   demo-ready.
2. **Compact funnel strip (demo-supporting, ~2–3h) — build AFTER Tier-1 smoke passes.** A single funnel
   band (full chain-class breakdown, F-008) + a small clickable list of a few generated questions → each
   adjudicated by Tier-1. (The full sortable explorer is post-preflight polish, not demo-critical.)
3. **Static CS figure + verdict (demo-supporting, ~2h) — after Tier-1.** Render the pre-computed
   `docs/claude-science-evidence-chain_2026-07-08/` figure + narrative as PROVENANCE (F-007), not as the
   referee verdict object.
4. **Post-preflight polish:** the full sortable LBD explorer, theme work, motion.
5. **Tier 3 live CS trigger (STRETCH, fragile, operator-only).** DISABLED by default; built only behind a
   proper wrapper (daemon-status, nonce mint, prompt-file, artifact copy, timeout, error surface) AFTER
   everything above is demo-ready; **never on the demo's critical path** (F-003).

Demo-critical minimum = Tier-1 + compact funnel strip + static CS figure (~1 day). Everything else is
post-demo. Fits the 2026-07-13 deadline with margin.

---

## 2. Data contracts (what feeds each panel — verified against the repo)

- **Referee:** `import arbiter` is NOT installable from repo root (no package metadata — F-001, confirmed
  live). The app MUST insert the repo `src/` on `sys.path` at startup:
  `sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))` BEFORE
  `from arbiter.lbd.referee_triple import referee_triple, load_referee_data` /
  `from arbiter.lbd.entities import build_a_universe, load_c`. `d = load_referee_data()` once
  (`@st.cache_resource`). `referee_triple(gene, disease, condition, d)` → dict with `answer`, `overall`,
  `hops` (each `{hop,name,status,claim,receipt,caveats}`). **Gate-fail → only HOP-0 returned** (the greyed
  downstream cards are presentation-only placeholders labeled "not evaluated," NOT returned hops — F-005).
  Gene options = `build_a_universe(program_significant=True).symbol`; disease options = `load_c()` (12).
  The referee dynamically imports `docs/perturbseq-qc_2026-07-07/pyzobot_referee.py` via an absolute path
  it computes itself (`parents[3]`), so it works regardless of cwd once `src/` is on the path. **A bare
  `import arbiter` fails** (confirmed) — the preflight import check MUST insert `src/` first (see the
  exact one-liner in §4 step 2), never a plain `import arbiter`.
- **LBD explorer:** reads from a checked-in **`app/fixtures/`** (F-006) — a curated copy of
  `sweep_Stim8hr.json` (35 KB) + `lbd_questions_Stim8hr.json` (13 KB) + a short `PROVENANCE.md` (condition,
  gen date, regen command). `data/lbd_out/` stays gitignored as regenerable scratch. Fields: `funnel`
  (a_genes 3,935; eligible 22,039; disease_c_supported 43; clean_supported 30; full `chain_classes`
  breakdown — 21,995 refuted_for_c · 1 refuted_effect · 10 weak · 3 flagged · 30 clean, F-008) +
  `ranked_clean_supported` (30 rows). Narrate "about 22,000 did not become clean full-chain findings."
- **CS lane (pre-computed):** `docs/claude-science-evidence-chain_2026-07-08/`
  {`claude_science_evidence_chain.md`, `claude_science_verdict.json`, `nab2_evidence_chain.png`}.
- **CS lane (live):** subprocess `node ~/.claude/skills/drive-claude-science/cs-drive.js` with a prompt
  file; poll; read artifacts from the CS workspace. (Reuses this session's proven mechanism.)

---

## 3. DESIGN BRIEF (self-contained — hand this to Claude co-design)

> *Design an attractive, credible scientific web app. It does not need repo context; everything needed is
> here. Tone: a modern computational-biology instrument — clean, data-dense but calm, trustworthy,
> "receipts not hype." Think a cross between a lab notebook and a clinical decision tool. Light and dark
> themes. Primary accent evokes molecular biology (a deep teal/indigo), with a semantic status palette.*
>
> **Build order for the design (F-011).** The full vision is below so the design is cohesive — but the
> **Tier-1 MVP (design + implement FIRST): Screen 1 (Referee) + the Receipt Chain component in all three
> states + the three "Try these" triples.** Everything marked *[post-preflight]* — Screen 2's full
> sortable explorer, Screen 3's live-CS button, light/dark theming polish, motion — is designed as part
> of the whole but implemented only after the Tier-1 MVP passes screen-only preflight. Prioritize making
> the Tier-1 MVP gorgeous; treat the rest as the cohesive frame around it.

**Product in one line.** *PyZoBot Arbiter* — a hypothesis referee for T-cell immunology: pose a
gene → program → disease claim and it returns a **verdict with a receipt for every step**, and it is
willing to say a confident *no* or *untested*.

**The signature component — the Receipt Chain.** A vertical (or horizontal on wide screens) 4-step chain:
**GATE → EFFECT → PROGRAM → DISEASE**. Each step is a card with: a status pill, a one-line plain-English
claim, and its **receipt** (the actual numbers — e.g. "2/2 guides, adj-p 1e-16, expr 0.03 vs 0.57").
Status semantics + palette:
- **supported** → green/check.
- **untested** (knockdown failed the gate) → the chain **visibly HALTS at GATE**: the GATE card is amber
  "UNTESTED", and EFFECT/PROGRAM/DISEASE render **greyed and struck through** with a subtle "not
  interpretable — knockdown unverified" watermark. *(This halt is the product's hero moment — design it
  to feel deliberate and honest, not like an error.)*
- **refuted** (for the specific disease) → the failing hop is red/×, prior hops stay green.
- A prominent **overall verdict banner** above the chain (the calibrated one-liner).
Full verdict taxonomy for badge design: `supported` (green), `supported_weak` / `supported_flagged`
(amber, with a caveat chip), `untested` / `untested_for_c` (grey), `refuted_for_c` / `refuted_effect` /
`refuted_program` (red). Never uses the words "discovered/proven/definitive."

**Screen 1 — Referee (the hero).** A query bar: **gene** picker + **disease-module** picker + condition
toggle (Rest / Stim8hr / Stim48hr) + a big **Adjudicate** button. A **"Try these"** row of 3 chips that
tell the whole story in one glance: *NAB2 → atopic eczema* (a confident **YES**), *SATB1 → asthma* (the
**UNTESTED** catch — halts at the gate), *NAB2 → multiple sclerosis* (a confident **NO**). Note the YES
and NO deliberately share the gene (NAB2): same real knockdown and effect, but the referee adjudicates
the *specific* disease — a confident yes for atopic eczema, a confident no for multiple sclerosis. This
disease-specificity is a key story the chips should make obvious. Result area = the Receipt Chain +
verdict banner.
Design the empty state to invite the "Try these" chips.

**Screen 2 — Hypothesis Engine (LBD explorer).** Top: a **funnel** visualization — 3,935 knockdown-gated
regulators → 22,039 literature-eligible gene–disease questions → 43 held at the disease hop → **30 clean,
receipt-backed** — designed so the dramatic cull (the referee *refused* ~22,000) reads instantly. Below:
a sortable **table of the 30 clean questions** (gene, disease, novelty, effect size, score, verdict), each
row clickable → opens that question in the Receipt Chain (Screen 1). One honest highlight callout: the
single "pure-novel but weak" survivor (NUDT1 → type-1 diabetes, zero prior literature, tiny effect) — the
"why we rank, not hard-gate" story.

**Screen 3 — Claude Science.** Shows an **evidence-chain reasoning panel**: a narrative with the same
Receipt Chain motif, plus a publication-style **figure** (a 6-panel scientific figure exists), plus a
verdict card. A header explains: *"An independent Anthropic scientific agent, given only the data and the
question, reasoned to the same verdict."* A secondary, clearly-secondary button: **"Run a fresh Claude
Science analysis"** with an honest "~several minutes" affordance and an async progress state (queued →
reasoning → done) — this is an optional deep-dive, not the default.

**Global chrome.** A slim left nav (Referee · Hypothesis Engine · Claude Science) or top tabs; a compact
header with the product name + a one-line honest tagline ("Receipt-backed. Willing to refute."); a footer
with the calibrated-language note + "reproducible: every number re-derived live from public Perturb-seq
tables." Provide a light AND dark theme. Motion: subtle — the Receipt Chain steps can resolve
sequentially (gate→effect→program→disease) on adjudicate, which also reads great on camera.

**What to optimize for.** (1) The Receipt Chain must be gorgeous and instantly legible — it is the brand.
(2) The UNTESTED halt-at-gate must feel intentional and trustworthy. (3) The funnel must make "refused
~22,000" land emotionally. (4) It must look like a real instrument a scientist would trust, not a toy.

*(Deliver: a component/layout design — colors, typography, the Receipt Chain component in all three
states, the funnel, the three screens. We implement in Streamlit, so favor layouts expressible with
columns/containers/cards + a modest amount of custom CSS.)*

---

## 4. Build plan
1. `app/streamlit_app.py` (+ maybe `app/components.py`): Tier 1 referee against the real contract (two
   render branches, full taxonomy, stable visible labels, run-from-repo-root). Add `streamlit` to
   `requirements.txt`.
2. **Preflight gate (before any further build or recording) (F-009):** the import check MUST mirror the
   app's sys.path fix, run from repo root:
   `python -c "import sys; from pathlib import Path; sys.path.insert(0, str(Path('src').resolve())); from arbiter.lbd.referee_triple import referee_triple, load_referee_data; d=load_referee_data(); print(referee_triple('SATB1','asthma','Stim8hr',d)['answer'])"`
   → asserts `untested`. Then: app launches clean → the **3 showcased triples** render correct
   (NAB2→atopic eczema YES; SATB1→asthma **UNTESTED, halts at gate**; NAB2→multiple sclerosis **clean NO**,
   GATE/EFFECT/PROGRAM green + DISEASE red) → Playwright smoke asserts visible result text → passes
   **twice from a fresh browser context**. No further build until green.
3. Compact funnel strip + a few click-through questions from **`app/fixtures/`** (curated `sweep` +
   `questions` JSON + `PROVENANCE.md`; `data/lbd_out/` stays gitignored). Demo-supporting.
4. Static CS view (F-010): render the pre-computed NAB2 evidence chain + figure as **provenance** — do
   NOT surface SLC1A5 as the clean NO (NAB2→MS is the sole showcased clean NO); if CS contrast cases are
   listed, SLC1A5 is labeled "legacy / chain-level," not the demo NO. The committed CS artifact is
   unchanged.
5. Post-preflight polish: full sortable explorer, light/dark theming, motion.
6. (Operator-only STRETCH) live CS trigger behind a proper wrapper; never on the demo path.
7. Wire into the demo-video pack (`docs/plans/demo_video_plan_2026-07-08.md`) as the screen-only surface.

## 5. Risks
- **Scope vs deadline.** Tiers 1+2+3-precomputed is ~1.5 days; live CS is a fragile stretch. Timebox;
  the demo never depends on live CS.
- **Potemkin.** Every verdict/receipt from `referee_triple`; every funnel number from the sweep JSON; CS
  panel from the real artifacts. No hardcoding.
- **Data availability.** `data/lbd_out/*` is gitignored → check in a small copy for the explorer (step 3).
- **CS live fragility.** daemon/auth/Playwright/full-auto — acceptable ONLY because it's optional + async.
- **Repo-root import.** `referee_triple` dynamically loads the base referee; the app must run from repo
  root (document + assert on startup).

## 6. Resolved by the debate (3 rounds, converged) — decisions of record
1. **Scope:** tiered by latency. Tier-1 referee is the demo spine + passes preflight FIRST; compact funnel
   strip + static CS figure are demo-supporting; full explorer / theming / live-CS are post-preflight.
2. **Claude Science:** async deep-dive lane, **pre-computed view as the reliable default** (carries the
   "genuine CS use" credit); the **live trigger is a disabled operator-only stretch behind a proper
   wrapper**, never on the demo path (the driver's daemon/nonce/full-auto/artifact-copy realities make a
   casual live integration a deadline+demo risk).
3. **LBD on Streamlit = cached results** (the funnel + the 30 clean questions, each click-adjudicated by
   the live referee). No live sweep on camera. Fairly represents the engine (generate→cull) honestly.
4. **Fixtures:** curated `app/fixtures/` (sweep + questions JSON + PROVENANCE.md); `data/lbd_out/` stays
   gitignored scratch.
5. **Integration:** the app inserts `src/` on `sys.path` at startup (the `import arbiter` fix, F-001/F-009);
   `load_referee_data()` behind `@st.cache_resource`; UNTESTED downstream cards are presentation-only
   placeholders; the three showcased triples are NAB2→atopic eczema (YES) / SATB1→asthma (UNTESTED) /
   NAB2→multiple sclerosis (clean NO).

**Production watchpoint:** does the Tier-1 MVP pass screen-only preflight (import fix + 3 triples + two
fresh-context runs) BEFORE any Tier-2/3 work begins? That gate is the discipline that keeps scope honest.
