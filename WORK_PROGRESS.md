# WORK_PROGRESS.md — Wayfinder

Live snapshot dashboard. Updated by `session-closer` at each session close and by
`freshen` on demand. The plan of record is `docs/plan.md` (v7 — Researcher-track reframe, §0).

## Snapshot
- **Phase:** Researcher-track finding COMPLETE + fully vetted — **NAB2→Th1/Th2→atopic eczema** replicated (5-agent lab, unanimous PASS) and **all confounders closed, incl. the DEFINITIVE STAT6 cis-check** (authors' genome-wide DE: NAB2-KD leaves STAT6 unmoved → cis/shadow EXCLUDED). Verdict = genuine novel NAB2-specific regulator (nomination re causality).
- **Active workstream:** **Submission → CS-native 3-min video (see the Working-target line below). Next session = capture + assemble + submit.** _(Manuscript + remaining-experiments gap analysis deferred — post-submission upside, not this week.)_ Prior finding state: CS proven to AUTHOR + run the LBD generator 100% live from scratch (micro-sweep) AND at full scale over all genes × 3 conditions (loose sweep: filter-safe, NAB2 reproduced Stim8hr-specific, 39 candidates in `CANDIDATES.md`). NAB2 drug-target verdict: DepMap negative-for-cancer; **GEO direction mining → association-backed NAB2-DOWN per-cell in lesional skin → knockdown likely backwards, NAB2 reads as a Th2 BRAKE → restore/UP-modulate** (needs perturbation proof). Referee direction-label bug fixed (verdicts safe). Only unbuilt CS stretch = Stage 2. Demo/app/notebook remain the **submission MVP**.
- **Working target: submit by EOD Friday 2026-07-10** (operator out of town Sat–Mon; official deadline still 2026-07-13). **Submission pivoted to a CS-native 3-min video**; tonight banked all design + de-risk + a 2-round codex-debate hardening (spine held). Friday = pre-capture 4 required frames (blockers) → assemble → gate → submit. Streamlit app + prior demo video = fallback MVP. Assets: `docs/demo-video-pack/cs/` + `assets/`.
- **Active thread:** **MANUSCRIPT** for FRMA — **revision MVP underway; manuscript now 23pp/0-errors.** DONE this session: **reframe** (title → "Receipt-backed prioritization…"; top-line = prioritization + abstention + falsification; "calibrated"=language-only; CS→replicable-in-principle), **12q13 foregrounding** (§4.4b, 3 mechanisms separated), **C10** gate grid (`gate_grid.py`+§4.1c), **C2** hard negatives (`hard_negatives.py`+§4.2b, rebuts B1) — all run LOCALLY (repo code+cache, §19), cache-free. **Next = the 4 figures** (Fig 1/2 schematics HTML/SVG; Fig 3 NAB2 chain + Fig 4 sensitivity/permutation panel — render locally from committed JSON, or CS kernel). Remaining MVP strengtheners: C6 refinement (low value — Control 2 covers it), C3c positive control, C3a temporal. Submission stays fire-ready in parallel.
- **Last updated:** 2026-07-11 (evening — revision MVP: reframe + 12q13 + C10 + C2 landed; manuscript 23pp; next = 4 figures)
- **Deadline:** 2026-07-13 (official EOD ET; operator personal stop 9:00 PM ET)
- **Repo:** `dayanjan/wayfinder` (private; renamed from pyzobot-arbiter, history preserved; flip public via `SUBMIT_CHECKLIST.md` — say "scrub and flip")
- **Claude Science:** installed on WSL, driven headless via the `drive-claude-science` skill (validated E2E, zero-click)

## Milestones (judging aims: Demo 30% · Claude Use 25% · Impact 25% · Depth 20% — WEIGHTS UNVERIFIED, confirm on CV form)
| # | Milestone | Status |
|---|-----------|--------|
| M0 | Repo scaffold + PM tooling | 🟢 done |
| M1 | Deterministic Validator (3-hop + KD-QC) proven on real genes | 🟢 done (built via Claude Science; `docs/perturbseq-qc_2026-07-07/`) |
| M2 | Receipt-backed YES / UNTESTED / REFUTED demonstrated (the moat) | 🟢 done (EGR2/GATA3 YES · IL2 UNTESTED · SLC1A5/CTLA4 REFUTED) |
| M3 | **LBD question-proposer** (generate untested questions → referee answers) | 🟢 done — v2 spec (debate-hardened) + fresh tool layer + full Stim8hr sweep; funnel 22,039→30 clean supported |
| M4 | Anchor lock + finding validation | 🟢 done — **NAB2→Th1/Th2→atopic eczema** replicated (5-agent lab, unanimous PASS: `docs/replication/`), STAT6+EGR+cis confounders stress-tested, source-paper-vetted → reframed as novel reproducible NOMINATION (disease link flagged) |
| M5 | Submission artifacts — evidence-chain notebook + Claude Science chain + demo video (+ interactive app) | 🟢 done — notebook (`notebooks/`); CS evidence chain (`docs/claude-science-evidence-chain_2026-07-08/`); 3-screen Streamlit **workbench** (`app/`) implementing a Claude co-design (via DesignSync); **final demo video** ~112s (ElevenLabs Brian + CC-BY music, gate PASS 94%; recipe `docs/demo-video-pack/`). Debate-hardened (2 × 3-round). Fallback MVP. |

Legend: 🟢 done · 🟡 in progress · 🔴 blocked · ⛔ off-track · ⚪ not started

## Active blockers
None. (Claude Science entitlement + sandbox verified; endpoint does not block it.)

## Progress log
### 2026-07-11 20:35 — Session close (full-close): revision MVP — reframe + 12q13 + C10 + C2
Executed the first four slices of the converged revision roadmap; 4 tested commits (`cde28b2`→`676fead`),
all pushed; manuscript **21pp→23pp, 0 errors**. **Reframe** (`cde28b2`): retitled → *"Receipt-backed
prioritization for literature-based discovery using Perturb-seq evidence"*; top-line everywhere →
**prioritization + abstention (untested) + falsification (refuted) diagnostics**; "adjudicate" softened
except QC+effect hops; **"calibrated" reserved for LANGUAGE only**; CS reproducibility →
replicable-in-principle (UI-dependent); self-audit = language-hygiene not epistemic verification;
construction-vs-referee split sharpened (§3.3); quick fixes (abstract split, −16.9/−16.88, 2025-preprint).
**12q13 foregrounding** (`24cefad`): new **§4.4b** separates the 3 mechanisms — STAT6-cis falsified (§4.4),
cluster-membership rejected (§4.6), **GWAS-label LD-inheritance = cannot discharge** (foregrounded as the
flagship's key open question); §4 intro + §5.3 cross-ref. **C10 gate grid** (`0b612d5`,
`docs/manuscript/analysis/gate_grid.py` + **§4.1c**): 27-cell ab_gate_pct×min_bc×tau; verdict+score
gate-independent → 47,220-pair census once + set arithmetic; default reproduces 30/rank-4; NAB2×eczema rank
{1,4,5} med 4, verdict invariant, survives 18/27 (misses = exactly pct=0.75, near-novelty at the literature
floor); Jaccard med 0.41. **C2 hard negatives** (`676fead`, `hard_negatives.py` + **§4.2b**): rebuts
reviewer B1 — Panel A (all 11,415 perturbed genes) own-edge cull 16.9% (~all QC-untested; effect gate
lenient), Panel B (frozen curated-association top-50/disease = 600) 15.7% own-hop cull vs 67.3%
substrate-inherited disease-hop cull, 17.0% supported; hard negatives incl. IL36RN×psoriasis (0.82),
TREX1×lupus, PADI4×RA — all UNTESTED. All analyses LOCAL (repo code+cache, doctrine §19), cache-free
(gate_grid measured +39 cached ac_lit lookups). Tree clean. **Next = the 4 figures.**

### 2026-07-11 — Session close (full-close): full draft in LaTeX + citations + converged revision roadmap
Big session. **Drafted §4 Results** (~1,900w) with a cache-free **sensitivity panel** (Control 1 QC 2,430→
untested; Control 2 label-shuffle 406/47,220 vs 467.7±10.9 → **substrate-inherited stringency**, lower-tail
p≈5e-4; Control 3 NAB2 rank 1–8) **reproduced byte-identical in Claude Science (delta-0, Reviewer-verified)**;
3-round §4 codex-debate converged (10→1→1). **Drafted §5 + Abstract** → full §1–§5 arc. **Ported the LightsOut
citation stack** (`tools/` + new `semantic_scholar.py`); **references.bib 4→12** (CrossRef/S2-resolved,
live-audited tier=OK, **pushed to Zotero, 12 in-sync**), wired \cite into the .tex. **Built the LaTeX
manuscript** (LightsOut approach, `docs/manuscript/latex/`) → **21-page PDF, 12 refs, 0 errors**. Visual
inspection caught + **fixed the equation margin-bleed (verbatim→amsmath display) and colored→black headings**.
Processed **two Major-Revision referee reviews** → consolidated **dossier** (22-item register) + resource-
tagged **revision roadmap**, hardened by a **3-round codex-debate that CONVERGED** (R1→R2→R3, 8→6→0) — top-line
reframed to "**receipt-backed prioritization + abstention + falsification diagnostics**". **Upgraded Codex
0.141.0→0.144.1; default model gpt-5.5→gpt-5.6-sol** (fixes large-artifact confabulation). ~15 commits
`2166257`→`94a40ea`, all pushed. **Next = execute the revision MVP.** Tree clean.

### 2026-07-10 — Session close (full-close, manuscript kickoff): outline + sections 1-3 build-ready
Started the **manuscript** (new thread). Confirmed the template is **Henry, Wijesinghe, Myers, McInnes 2021**
(FRMA 6:644728 — the operator's own LBD lineage). Locked: FRMA venue · agentic-loop headline · ledger+NAB2-hero
demo · **Wayfinder = an APPROACH not a product** (swept through outline+§1) · title *"Closing the loop on
literature-based discovery: receipt-backed adjudication of machine-generated hypotheses against Perturb-seq
data."* **Outline** (`docs/manuscript/OUTLINE.md` v1.2) hardened by a **3-round repo-read codex-debate**
(10→5→1, converged) — resolved the dataset **DOI → 10.64898/2025.12.23.696273** (Crossref; 10.1101 is a 404;
fixed `references/README`), dropped CTLA4 from the ledger (mis-sourced), repointed the claim inventory to
primary JSON. **Drafted §1 Intro / §2 Background / §3 Materials & Methods** — §3.4 carries the **no-API →
headless-UI-automation-from-Claude-Code** methods element. **CS actor-critic review** (dogfood, drove CS
headless): **16/18 claims MATCH, 0 mismatch**. **3-round prose codex-debate** (14→4→0, converged, zero sanding)
— caught **F-004, a real factual error**: `ac_known` is the Open Targets *overall* score, not "genetic" (Codex
read `sources.py`). Folded in operator edits (Cheng 2020 in-vivo cite; softened R01 framing; NAB2 RNA-seq-vs-
genetic resolved). 5 commits `ec68a23`→`a2d125e`, all pushed. Reviews under `docs/reviews/`. **Next = §4
Results** (honor: label-shuffle null distribution + rank-stability sensitivity). Tree clean.

### 2026-07-10 — Session close (full-close): submission BUILT + rebranded → Wayfinder; fire-ready
Recreated the demo video in the operator's **cloned ElevenLabs voice** + music (2:52, gate PASS 96%). Ran a
**6-agent independent judging panel** (~8/10, unanimous "likely top-6") then a **2-round frame-grounded
codex-debate** — Codex "watched" a 12-frame storyboard via `-i` (multimodal on images; audio boundary flagged)
→ runtime-discipline re-scope; records in `docs/reviews/{judging-panel,codex-debate}_cs-native-video_2026-07-10.md`
+ `EDIT_PLAN`. Verified the STAT6-cis claim (authors' own deposited genome-wide DE, lazy S3 read). **Renamed
PyZoBot Arbiter → Wayfinder.** Rewrote judge-facing README + summary + builder bio; Tier-0 integrity (purged
"validated", Th1→Th2 label, license wording). **Full video re-cut v4** (IL2 cold-open, Wayfinder cards + credit,
spoken name, split disease-label + de-number, new STAT6 callout, plain captions). **GitHub repo renamed
`dayanjan/wayfinder`** (PRIVATE, history preserved). Staged `SUBMIT_CHECKLIST.md` + `submission-fire-ready`
memory → say **"scrub and flip"** to submit. Next thread: **manuscript in Claude Science** (template
`references/frma-06-644728.pdf`). Housekeeping committed; tree clean.

### 2026-07-09 19:12 — Session close (full-close): submission pivoted to CS-native video + full de-risk + codex-debate
Interactive evening session. **Pivoted the submission to a CS-native 3-minute video** (skip the Streamlit
app in the cut; app stays as fallback MVP). New spine: *when you don't know what to ask, use LBD to surface
the data's implicit hypotheses — built directly in Claude Science; the library and the lab on one bench.*
**Deadline pulled to EOD Friday 2026-07-10** (out of town Sat–Mon). Banked ALL of: spine + narration +
6-beat sheet + 100–180w summary; dataset attribution corrected to the **Marson lab** (Zhu, Dann, … Marson;
bioRxiv doi:10.64898/2025.12.23.696273), citation locked; **3 QA'd 1920×1080 HTML assets** (Swanson ABC
dual-scene graphic + two-floods + feature-matrix slides); **capture path de-risked** (Playwright + saved CS
auth → screenshot + video) and **all 4 target CS conversations opened** → verified per-beat money-shot
sources + frame URLs + two gotchas (opens-at-bottom, wheel-no-scroll → open receipt artifact) in
`cs/CAPTURE_PLAN.md`; **CS-native demo pack** `cs/{demo.config,narration,scenes}.mjs` + `README.md` +
`CAPTURE_PLAN.md` (harness drives CS via `STORAGE_STATE=cs_state.json`; screen-only gate PASS; syntax-clean);
**2-round repo-read codex-debate** (`--preserve-intent`) → spine held (no sanding), fixed 2 P0s (money-shot
receipts = release blockers; live-vs-cached explicit on-screen), made the confident **NO visible**, tightened
calibration — ALL accepted fixes applied to the runnable artifacts. Record:
`docs/reviews/codex-debate_cs-native-video-plan_2026-07-09.md`. Friday = pre-capture 4 required frames
(blockers) → `run.mjs --stage=all` → gate → mux → repo public + scrub → submit. All committed + pushed
(`49f9453`). Tree clean.

### 2026-07-09 13:30 — Session close (full-close): CS instrument extended + NAB2 target/direction
Two threads. **A (CS instrument):** (1) live from-scratch **micro-sweep** — CS authored its OWN LBD generator
and ran it 100% live (liveness independently re-verified); (2) **calibration probe** (~1.29 s/call, throttle-free);
(3) **full 100%-live loose sweep** all 3 conditions, 9,557 live calls — program-sig filter SAFE, **NAB2→eczema
reproduced digit-for-digit (Stim8hr rank 4, Stim8hr-SPECIFIC)**, 39 candidate nominations (34/39 timepoint-
specific), `CANDIDATES.md`; (4) fixed an **inverted Th1/Th2 direction label** in the referee (marker-validated;
verdicts unaffected — NAB2 is correctly Th2-associated). **B (NAB2 target/direction):** DepMap =
negative-for-cancer-target (non-contradictory); **GEO direction mining** via a 3-round **live-verified**
codex-debate (11→10→0) → executed 4 arms + STAT6 → NO-CALL; then **ARM-D scRNA** resolved the composition
confound → **association-backed NAB2-DOWN per-cell in lesional skin (keratinocyte/T-NK) → topical KNOCKDOWN
likely BACKWARDS; NAB2 = Th2 BRAKE lost in disease → restore/UP-modulate** (ceiling: perturbation proof needed).
All committed + pushed. **Next:** manuscript assembly + remaining-experiments gap analysis.

### 2026-07-09 07:20 — Session close (full-close): full pipeline reproduced natively in Claude Science (MVP Stage 0/1/3/5)
Implemented the solidified plan's §9 runnable checklist; Claude drove CS headless + verified-from-DB, Codex
brainstormed + honesty-eval'd. **Stage 0 (feasibility)** — one driven run proved all four external paths from
the kernel: Europe PMC GET (`"NAB2" AND "atopic eczema"`→**6**), OT GraphQL POST (asthma→**7403**), **anon S3
lazy read of the 16.8 GB DE matrix opens headless, no download** (self-healed a proxy 403 via virtual
addressing), 24 `mcp-*` connectors → **resolved the open question: Stage 3 native, no fallback.** **Stage 1
(generation)** — Codex settled the fork → **Strategy B**; staged the real `arbiter.lbd` package + 4,675-response
cache into a repo-shaped `/home/dayanjan/pyzobot-cs-stage1`; ran `propose.sweep()` **unchanged** under a
**pure-replay guard** (cache 4685→4685, delta 0) → funnel **3935/22039/43/30**, ab_gate 26, **NAB2→atopic
eczema rank 4** (ab66/bc2184/ac_lit6/effect301/score −1.137/supported), all 16 checks ✅. **Stage 3
(falsification)** — native anon-s3fs+h5py lazy read → **STAT6 +0.0870/adj_p 0.7884 UNMOVED**, NAB2 self
−3.0783 → **cis-artifact refuted**. **Stage 5 (provenance)** — OPERON (Opus 4.8) wrote the HOP-0→3 receipt
chain; **3 Sonnet-5 Reviewer frames verified every number AND flagged "validated"/"definitive" (calibrated-
language), both fixed** — the falsification thesis live in an independent product; `verification_checks`
populated. Archived 16 artifacts + provenance to `docs/cs-full-pipeline_2026-07-09/` (~$6.41). A closing codex
honesty-eval → **SHIP-WITH-EDITS** (title scope, drop "definitive", soften "genuinely NAB2's", fix a cost
typo), all applied. **Next:** decide whether to surface this in the submission (notebook/app/demo) or keep as a
depth artifact; Stage 2 confounder checks are the only unbuilt stretch.

### 2026-07-09 06:15 — Session close (full-close): pipeline↔CS mapping + native tracer + solidified plan
Continued the CS deep-dive into an exploitation plan. **(1)** 3-agent exhaustive reconstruction of the full
LBD→NAB2 pipeline (30 steps) + per-step Claude Science feasibility → `docs/pipeline-inventory-and-cs-mapping_2026-07-09.md`
(**~25/30 CS-native**; the one gap = cross-model/Codex independence). **(2)** LBD methods explainer / manuscript
seed → `docs/lbd-methods-explainer.md`. **(3)** **CS TRACER** — drove CS to write its own 4-hop referee over
the raw tables and **reproduce the NAB2 finding digit-for-digit natively** (gate 2/2 1e-16; effect −16.88/301;
Ota z 7.708; eczema clusters 90&100 OR 3.899/3.43) + IL2 untested hero + SLC1A5 refuted; CS self-audited
unprompted → `docs/cs-capability-tests_2026-07-08/tracer-artifacts/`. **(4)** **full-pipeline-in-CS plan → SHIP**
via a 3-round repo-read codex-debate (11→8→0) → `docs/plans/full-pipeline-in-cs-plan_2026-07-09.md` (v3) +
`docs/reviews/codex-debate_full-pipeline-cs_2026-07-09/`. Architecture decided: **CS = instrument (generation →
referee → provenance); Codex = external cross-model auditor.** Prior commit c243840 landed explainer+inventory+tracer.
**Next:** implement the plan's §9 checklist in CS (Stage 0→1→3→5).

### 2026-07-08 (overnight, autonomous) — Claude Science capability deep-dive (mine → brainstorm → verify)
Executed the prior handoff's "deeper dive into Claude Science" as a 4-phase autonomous run:
**(1)** 5-agent parallel pass over the 2026-07-08 CS product-demo transcript → `[DEMO]` capability catalog +
testable inventory (`docs/claude-science-demo-findings_2026-07-08.md`; main capabilities doc updated).
**(2)** 2-round **repo-read codex-debate** turned the inventory into an executable test plan and surfaced
the load-bearing discovery: **`operon-cli.db` is CS's readable audit/receipt store**
(`docs/claude-science-test-plan_2026-07-08.md`). **(3)** Drove our own CS install headlessly (hardened
`cs-drive.js`) and **verified capabilities from the DB + artifacts** (drive-then-verify, doctrine §19),
`docs/cs-capability-tests_2026-07-08/RESULTS.md`. **Confirmed live:** actor-critic (OPERON **Opus 4.8** +
Reviewer **Sonnet 5** ×3 checkpoints) with the **Reviewer catching a planted count inconsistency (FAIL)** —
our falsification thesis, in an independent product; `host.mcp` **batched DB lookup → real Ensembl IDs**;
`host.llm_batch` inline sampling (**Haiku 4.5**); persistent kernel + Python↔R + self-sight all PASS;
`host.delegate` **gated** behind a Delegation toggle. **(4)** Memory + handoff updated; new docs uncommitted.
**Next:** exploit CS for the finding/product — top pick a **referee-inside-CS tracer**. See `memory/NEXT_SESSION.md`.

### 2026-07-08 18:02 — Session close (full-close): M5 SHIPPED IN FULL (notebook + CS chain + app + demo video)
Built all three M5 artifacts. (1) Executable **evidence-chain notebook** (`notebooks/`) — imports the
vetted `arbiter.lbd` modules, recomputes every headline number live, outputs baked. (2) **Claude Science
evidence chain** (`docs/claude-science-evidence-chain_2026-07-08/`) — drove CS headless on only the 4
tables + the question; it reached the identical receipt-backed verdict, weakened the STAT6 cis-artifact
by all 3 in-data checks, and emitted a 6-panel figure. (3) A 3-screen Streamlit **"Researcher's
Workbench"** (`app/streamlit_app.py`: Referee / Hypothesis Engine / Claude Science) implementing a
**Claude co-design** imported via the **DesignSync** integration; all screens preflight-green
(screen-only Playwright smokes). Then the **final demo video** (~112s): falsification-first arc,
ElevenLabs "Brian" narration, "Deliberate Thought" (Kevin MacLeod, CC-BY) music bed; transcription gate
**PASS 94%** with music. Recipe checked in at `docs/demo-video-pack/`; MP4/MP3 out-of-band (`.tmp/`, now
gitignored). Two **3-round repo-read codex-debates** (demo-video + workbench plans; both converged,
preserve-intent passed). **Track reframed** to "Researcher who also builds" across CLAUDE/AGENTS/README/
plan. The demo + app are the **fallback MVP**. Next = a deeper Claude Science dive driven by today's
product-demo transcript.

### 2026-07-08 HH:MM — Session close (full-close): definitive STAT6 check + provenance; notebook next
Preserved the full raw provenance trail (`docs/provenance/`, 52 artifacts, abstracts stripped,
secret-scanned). Ran the **definitive STAT6 cis-artifact check** against the authors' deposited
genome-wide DE (`GWCD4i.DE_stats.h5ad`, read lazily via h5py+s3fs from the public S3 — no download):
**NAB2 knockdown leaves STAT6 unmoved (log2FC +0.09, p 0.79)** → cis/shadow confounder **DEFINITIVELY
EXCLUDED**; verdict upgraded to a genuine novel NAB2-specific regulator. Decided M5 submission format:
executable evidence-chain **Jupyter notebook** (single source of truth) + **Claude Science evidence
chain** (reasoning layer) + 3-min demo video — to be built in a fresh session. Tree clean.

### 2026-07-08 (cont.) — Independent validation + source-paper vetting → nomination reframe
After the finding landed, hardened it against every challenge. **Independent literature audit**
(4-agent team via new `src/arbiter/lit/`): NAB2→Th1/Th2 and NAB2→atopic eczema BOTH novel (0 papers);
surfaced the **STAT6-adjacency** confounder. **In-data confounder checks** (`docs/nab2_stat6_confounder_
check.py`, `docs/nab2_egr_mechanism_check.py`): STAT6-locus and EGR-mediation both argued-against.
**5-agent independent replication** (3 Opus + 2 Codex, 2 clean-room re-impls; `docs/replication/` +
`docs/replication_report_2026-07-08.md`): **UNANIMOUS PASS** — every number reproduced; caught+fixed a
cluster-ID bug (74→90/100), a stat overstatement (8×→3× on z), and reframed the arguments.
**Source-paper read** (`docs/source_paper_read_eczema_2026-07-08.md`): paper never mentions NAB2
(novelty confirmed); disease labels are Open Targets GWAS-genetic (LD-susceptible, no coloc control);
sharpest concern = CRISPRi **cis-artifact** — tested (`docs/nab2_cis_artifact_check.py`): NAB2 & STAT6
don't co-cluster + NAB2 reproducible (cross-guide/donor R 0.74) → argues against cis (definitive
NAB2-KD→STAT6-mRNA check needs deposited DE matrix). **Reframed** to a novel, reproducible NOMINATION
with the disease link FLAGGED. Source paper in `references/` (gitignored); analysis repo
`github.com/emdann/GWT_perturbseq_analysis_2025` recorded. ~14 commits.

### 2026-07-08 — Autonomous overnight session: LBD proposer built + finding landed
Hardened the LBD spec v1→v2 via a **3-round repo-read codex-debate** (9→3→0 findings, build-ready)
and an independent Fable-5 read. Authored the **fresh tool layer** (`src/arbiter/lbd/`:
entity_maps, _http, sources, entities, referee_triple, cooccur, propose, verify_disease_ids) —
new-work-only, all verified live. Disease→id map resolved authoritatively (Open Targets/OLS4 →
**MONDO not EFO**; caught before it silently broke novelty). `referee_triple` = thin exact-disease
adapter (F-001/F-012), verified discriminating. A **Codex code consult** found the scoring rewarded
obscurity + a full-chain bug; both fixed. **Full Stim8hr sweep:** 22,039 candidate questions →
**30 clean full-chain referee-supported**. Headline finding **NAB2 → Th1/Th2 → atopic eczema**
(near-novel ac_lit=6, receipt-backed, Codex-vetted keep-with-caveat). 5 commits; finding writeup at
`docs/lbd_finding_nab2_2026-07-08.md`; process log `docs/lbd-build-log.md`.

### 2026-07-07 — Session close (checkpoint): PM tooling bootstrap
Pulled session-lifecycle skills (`session-start`, `session-closer`, `freshen`,
`atomic-planner`) from the sibling generator/Halcyon repos; instantiated the
`memory/` scaffold, `MEMORY.md`, this dashboard, and migrated the handoff to
`memory/NEXT_SESSION.md`. Product work not yet started.

### 2026-07-07 13:10 — Session close (full-close): PM tooling + repo live
Verified the `.env` Anthropic key is active (models 200 + minimal messages 200).
Created private GitHub repo `dayanjan/pyzobot-arbiter`, gitignored the local
`01-hackaton details/` folder, and pushed both commits. Secrets/data confirmed
absent from remote history. M0 complete; next up is M1 (deterministic Validator).

### 2026-07-07 19:30 — Session close (full-close): Claude Science + Validator + LBD reframe
Huge session. Committed to the **Researcher track** (plan v7). Installed **Claude Science** on WSL
(paste-only, no-password; sandbox verified on the managed laptop; entitlement confirmed) and built
a reusable **`drive-claude-science` skill** to drive it fully headless via Playwright — validated
end-to-end zero-click on a fresh project (auto-approves cards). Through it, built the **referee /
Validator** (3-hop + KD-QC gate) and demonstrated **YES / UNTESTED / REFUTED** with real receipts;
batch-ranked 602 genes for anchor candidates. Researched Claude Science exhaustively (4 agents + live
UI) → curated capability reference (`docs/claude-science-capabilities.md` + HTML + Artifact + a
Wednesday reminder). Reframed the project's strategic heart: **LBD generates the questions, Claude
Science + data answers them** — specced at `docs/lbd-proposer-spec.md`. All committed + pushed.
