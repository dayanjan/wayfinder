# MEMORY.md — Wayfinder Session Index

Lean cross-session index. The narrative lives in `memory/sessions/YYYY-MM-DD.md`;
the live dashboard in `WORK_PROGRESS.md`; the handoff in `memory/NEXT_SESSION.md`.
This file is the fast scan: where we are, what's decided, what happened lately.

## Current Status
> **READ-FIRST:** `docs/CLAIMS_EVIDENCE_LEDGER.md` — the canonical living index (claim → status → evidence →
> source → critique). Any claim audit/review/revision reconciles against BOTH literature AND the experiments
> it indexes. Anti-amnesia protocol: `memory/NEXT_SESSION.md`.

**2026-07-12 (full-close) — CONTRIBUTION AUDIT + CLAIMS↔EXPERIMENTS RECONCILIATION + TRACEABILITY SPINE.**
A 13-agent mixed-model (Claude+Codex) literature novelty audit (`docs/reviews/contribution-novelty-audit_2026-07-12/`,
`VERDICT.md`) then a claims↔already-run-CS-experiments reconciliation (`docs/claims-vs-experiments_2026-07-12/`,
`RECONCILIATION.md` + 6 recon passes). **Verdict:** method is novel-but-NARROW **and UNEVALUATED** (no
precision/recall/baseline — the publish gate, gap G1); biology is stronger than the lit-audit implied — the
STAT6 "mistaken-identity" attack RETRACTED (2 of 3 confounder channels experimentally CLOSED: B3 cis, B4
cluster; only 12q13 disease-label B5 open); 9 honesty fixes catalogued. Built the canonical
**`docs/CLAIMS_EVIDENCE_LEDGER.md`** + `NEW_EXPERIMENTS.md` (G1–G3) + anti-amnesia protocol so audits never
again check literature-only. Committed `e626b4c`→`bba1e18`+. **Next = G1 held-out-eval de-risk spike.** See `memory/NEXT_SESSION.md`.
**2026-07-11 (OVERNIGHT autonomous, full-close) — MANUSCRIPT SUBMISSION-READY: 4 FIGURES + RELATED-WORK +
EVIDENCE-STRENGTHENING + 5-REVIEWER HARDENING; 32pp, 0 ERRORS.** Autonomous overnight run (operator asleep).
Built **4 deterministic figures** (architecture / funnel+ledger / diagnostics / NAB2 hero chain) from committed
JSON and wired them in (23pp→32pp). Added **§2.4 Related approaches** (honest positioning vs AI co-scientist /
FutureHouse Robin+PaperQA2 / SciAgents / Coscientist / The AI Scientist) + **§5.3b evidence-strengthening
program** (time-sliced held-out, external panel, colocalization, prospective perturbation); ~28 DOI-verified
refs. **Corrected a load-bearing genomics error** — NAB2 and STAT6 are convergent tail-to-tail neighbours
(~43 kb promoters, 3′ ends overlap; Ensembl GRCh38), NOT the "~1.9 kb" the draft claimed. Ran a **5-reviewer
critical pass (4 Claude agents + Codex adversarial)** then a **final repo-read Codex verification debate** →
all P0s fixed (funnel 43-not-44 matching Fig 2; 395/406 + 2,430/1,914 reconciliations) + substantive P1s
(STAT6 cis scoped to "no detectable expression-level cis-effect"; §2.4 de-strawmanned; abstract names the
un-dischargeable 12q13 confounder; §5.2 hedged on the Th2-shift sign; n=1 flagship limitation). Codex verdict:
**submission-defensible on its own terms.** Committed+pushed `62bb929`. **Deliverable to read:
`docs/manuscript/latex/main.pdf` (32pp). Next = read it → Frontiers formatting, or an offline strengthener
(held-out eval / coloc).** Review records in `docs/reviews/`. See `memory/NEXT_SESSION.md`.
**2026-07-11 (evening, full-close) — REVISION MVP: 4 SLICES LANDED (reframe + 12q13 + C10 + C2); MANUSCRIPT
23pp, 0 ERRORS.** Executed the converged revision roadmap. **Reframe** (`cde28b2`): retitled →
"Receipt-backed prioritization for literature-based discovery using Perturb-seq evidence"; top-line →
**prioritization + abstention + falsification diagnostics**; "calibrated"=language-only; CS→replicable-in-
principle; construction-vs-referee split sharpened. **12q13 foregrounding** (`24cefad`): new §4.4b separates
the 3 mechanisms (STAT6-cis falsified · cluster-membership rejected · GWAS-label LD = CANNOT discharge,
foregrounded). **C10 gate grid** (`0b612d5`, `gate_grid.py`+§4.1c): 27-cell ab_gate_pct×min_bc×tau; default
reproduces 30/rank-4; NAB2×eczema rank {1,4,5} median 4, verdict invariant, survives 18/27 (misses = exactly
pct=0.75). **C2 hard negatives** (`676fead`, `hard_negatives.py`+§4.2b): rebuts B1 — referee's OWN hops cull
16.9% of arbitrary genes + 15.7% of a frozen curated-association nominator's top-600 (IL36RN×psoriasis 0.82 →
untested), separated from the 67.3% substrate-inherited disease-hop cull. All run LOCALLY (repo code+cache,
§19), cache-free/deterministic. **Next = the 4 figures** (render locally from committed JSON, or CS kernel).
See `memory/NEXT_SESSION.md`.
**2026-07-11 (full-close) — FULL DRAFT (Abstract + §1–§5) IN LaTeX, COMPILES (21pp); 12-REF BIBLIOGRAPHY +
ZOTERO LIVE; TWO REFEREE REVIEWS → CONVERGED REVISION ROADMAP; CODEX → gpt-5.6-sol.** Drafted §4 (CS-
reproduced sensitivity panel, delta-0) + §5 + Abstract; 3-round §4 debate converged. Ported the LightsOut
**citation stack** (`tools/`) + `semantic_scholar.py`; `references.bib` 4→12 (resolved/audited/Zotero-synced,
wired into .tex). Built the **LaTeX manuscript** (LightsOut approach, `docs/manuscript/latex/`); fixed the
equation margin-bleed + colored headings. Two Major-Revision reviews → dossier + **converged 3-round revision
debate** (`docs/reviews/codex-debate_revision-plan_2026-07-11.md`) — top-line reframed to "**receipt-backed
prioritization + abstention + falsification diagnostics**" (not correctness/adjudication/calibrated). Upgraded
codex 0.141→0.144.1, default model **gpt-5.6-sol**. **Next = execute the revision MVP** (reframe + C6/C2/C10/
C3a diagnostics + 12q13 foregrounding + 4 figures). See `memory/NEXT_SESSION.md`.
**2026-07-10 (full-close, manuscript kickoff) — MANUSCRIPT STARTED: OUTLINE + SECTIONS 1-3 BUILD-READY.**
Target venue **FRMA** (Henry lineage — the template is **Henry, Wijesinghe, Myers, McInnes 2021**, 6:644728).
Headline = the agentic loop; **Wayfinder framed as an APPROACH, not a product**; title locked (*"Closing the
loop on literature-based discovery: receipt-backed adjudication of machine-generated hypotheses against
Perturb-seq data"*). Outline hardened by a 3-round repo-read codex-debate (10→5→1; DOI resolved to
**10.64898/2025.12.23.696273**). §1 Intro / §2 Background / §3 Methods drafted (§3.4 = the **no-API →
headless-UI-automation-from-Claude-Code** methods element), **CS actor-critic verified (16/18 exact)**, then a
3-round prose codex-debate (14→4→0, converged, zero sanding — caught a real factual error: `ac_known` is the
Open Targets *overall* score, not "genetic"). All committed+pushed (`a2d125e`). **Next = draft §4 Results**
(honor two promises: label-shuffle null distribution + rank-stability sensitivity). See `memory/NEXT_SESSION.md`.
**2026-07-10 (full-close) — SUBMISSION BUILT + REBRANDED "PyZoBot Arbiter" → "WAYFINDER"; FIRE-READY.**
Video re-cut in the operator's **cloned voice** (2:52, gate PASS 96%); **6-agent judge panel** (~8/10,
unanimous likely-top-6) + a **2-round frame-grounded codex-debate** (Codex "watched" a 12-frame storyboard);
judge-facing README + ~180w summary + builder bio; Tier-0 integrity fixes; **GitHub repo renamed
`dayanjan/wayfinder`** (PRIVATE, history preserved). One phrase from public — say **"scrub and flip"** →
`SUBMIT_CHECKLIST.md`. **Next working thread: write a MANUSCRIPT in Claude Science** (template
`references/frma-06-644728.pdf`, gitignored). Deadline: EOD ET Mon 2026-07-13. See `memory/NEXT_SESSION.md`.
**2026-07-09 (EVENING, full-close) — SUBMISSION PIVOTED TO A CS-NATIVE 3-MIN VIDEO; ALL DESIGN + DE-RISK +
DEBATE-HARDENING BANKED. DEADLINE MOVED UP TO EOD FRI 2026-07-10 (out of town Sat–Mon). Friday = capture +
assemble + submit only.** New spine: *when you don't know what to ask, use LBD to surface the data's implicit
hypotheses — built directly in Claude Science; the library and the lab on one bench.* Tonight: spine +
narration + 6-beat sheet + 100–180w summary; dataset attribution corrected to the **Marson lab** (Zhu, Dann,
… Marson; bioRxiv doi:10.64898/2025.12.23.696273), citation locked; **3 visual assets** (Swanson ABC
dual-scene graphic, two-floods + feature-matrix slides — 1920×1080, brand palette, QA'd); **capture path
de-risked** (Playwright + saved CS auth: screenshot + video) and **all 4 CS conversations opened** →
verified per-beat money shots + frame URLs + the two gotchas (opens-at-bottom, wheel-no-scroll → open the
receipt artifact) in `cs/CAPTURE_PLAN.md`; **CS-native demo pack** (`cs/*.mjs` + README + CAPTURE_PLAN;
harness drives CS via `STORAGE_STATE=cs_state.json`; gate PASS); **2-round repo-read codex-debate**
(`--preserve-intent`) → spine held (no sanding), 2 P0s fixed (money-shot receipts = release blockers;
live-vs-cached explicit on-screen), the confident NO made **visible**, calibration tightened — all applied to
the runnable artifacts (`docs/reviews/codex-debate_cs-native-video-plan_2026-07-09.md`). Streamlit app + prior
video remain the fallback MVP → this video is upside, not gating. All pushed (`49f9453`).
**2026-07-09 (PM, full-close) — CS INSTRUMENT EXTENDED (live micro-sweep + 100%-live 3-condition loose sweep)
+ NAB2 DRUG-TARGET & DIRECTION INVESTIGATED. Next session = MANUSCRIPT + remaining-experiments gap analysis.**
Thread A (CS instrument): CS AUTHORED its own LBD generator and ran it 100% live from scratch (liveness
independently verified); the full loose sweep ran 100% live over ALL genes × 3 conditions (9,557 live calls) —
**program-sig filter proven safe, NAB2→eczema reproduced digit-for-digit (Stim8hr rank 4, Stim8hr-SPECIFIC),
39 candidate nominations (34/39 timepoint-specific)** → `docs/cs-full-pipeline_2026-07-09/live-fullsweep-loose/`
(CANDIDATES.md). Also fixed an inverted Th1/Th2 direction LABEL in the referee (verdicts unaffected; NAB2 is
correctly Th2-associated). Thread B (NAB2 target): DepMap = negative-for-cancer-target (non-contradictory);
**GEO direction mining** (3-round live-verified codex-debate → execute → ARM-D scRNA) → **association-backed
NAB2-DOWN-in-lesional-skin (per-cell, not composition) → the topical-KNOCKDOWN idea is likely BACKWARDS; NAB2
reads as a Th2 BRAKE lost in chronic disease → restore/UP-modulate** (ceiling: needs perturbation proof).
`docs/nab2-direction-geo_2026-07-09/`, `docs/nab2-depmap-check_2026-07-09/`. All committed + pushed (f-series).
**2026-07-09 (full-close) — FULL PIPELINE REPRODUCED NATIVELY IN CLAUDE SCIENCE (MVP: Stage 0/1/3/5, all PASS).**
Implemented the solidified plan's §9 checklist. **Stage 0** proved all four external paths from the CS kernel
(Europe PMC=6, OT asthma=7403, **anon S3 lazy read opens headless — no download**, 24 connectors) → resolved
the open question (Stage 3 native, no fallback). **Stage 1** ran the real `arbiter.lbd.propose.sweep()`
unchanged over the full 3,935-gene universe under a **pure-replay guard** (cache delta 0) → funnel
3935/22039/43/30 + **NAB2→atopic eczema rank 4** exact, ALL_PASS. **Stage 3** native anon-S3 cis-check →
**STAT6 unmoved (+0.087/adj_p 0.79), cis-artifact refuted**. **Stage 5** CS-authored receipt chain +
**Sonnet-5 Reviewer verified every number AND enforced calibrated language** (flagged "validated"/"definitive",
fixed) — the falsification thesis, live in an independent product. Archived to `docs/cs-full-pipeline_2026-07-09/`
(16 files + provenance from `operon-cli.db`, ~$6.41). Codex brainstormed the Stage-1 design (Strategy B) and
honesty-eval'd the README (SHIP-WITH-EDITS, applied). Architecture: **CS = instrument; Codex = external auditor.**
**2026-07-08 (full-close) — M5 SHIPPED IN FULL. The finding + a submittable product both exist.**
On top of the replicated finding (NAB2 → Th1/Th2 → atopic eczema; STAT6 cis excluded), this session built
all three M5 artifacts: (1) the executable **evidence-chain notebook**
(`notebooks/pyzobot_arbiter_evidence_chain.ipynb`, imports the vetted modules, recomputes everything
live); (2) the **Claude Science evidence chain** (`docs/claude-science-evidence-chain_2026-07-08/`, an
independent CS agent reached the same verdict + 6-panel figure); (3) the interactive **Streamlit
"Researcher's Workbench"** (`app/streamlit_app.py` — Referee / Hypothesis Engine / Claude Science,
implementing a **Claude co-design** imported via **DesignSync**) + the **final demo video** (~112s,
ElevenLabs "Brian" + CC-BY music bed, transcription gate PASS 94%; recipe in `docs/demo-video-pack/`,
MP4 out-of-band). Two 3-round repo-read codex-debates hardened the demo + workbench plans. Track reframed
to **"Researcher who also builds"**. The demo/app are the **fallback MVP**.
**2026-07-08 (overnight, autonomous) — CLAUDE SCIENCE CAPABILITY DEEP-DIVE done.** Mined the CS product-demo
transcript (5-agent parallel pass), brainstormed tests with Codex (2-round repo-read debate), and
**empirically verified CS live against our own install** — all receipt-backed from CS's own audit DB
(**`operon-cli.db`**). Key: CS's **Reviewer (Sonnet 5) caught a planted inconsistency (fail)** — our
falsification thesis, live; **`host.mcp` batched DB lookups return real Ensembl IDs**; `host.delegate` is
gated behind a Delegation toggle. Docs: `docs/cs-capability-tests_2026-07-08/RESULTS.md`,
`docs/claude-science-{test-plan,demo-findings}_2026-07-08.md`. Driver hardened.
**Next:** EXPLOIT CS for the finding/product — the referee-inside-CS tracer is DONE (native digit-for-digit
reproduction); the **full-pipeline-in-CS plan is SOLIDIFIED (codex-debate SHIP)**. Next session = **implement
it** (Stage 0 probe → Stage 1 LBD proposer via kernel HTTP → Stage 3 S3 cis-check → Stage 5 provenance),
per the §9 runnable checklist in `docs/plans/full-pipeline-in-cs-plan_2026-07-09.md`. See `memory/NEXT_SESSION.md`.

## Hard constraints (never lose)
- **NEW WORK ONLY** — every file authored during the event (started 2026-07-07); git history is the compliance proof.
- **Deadline: 2026-07-13, 9:00 PM ET.** Solo builder; async, interruptible.
- **Open source, MIT.** Claude for reasoning; Voyage for embeddings. Never OpenAI.
- **Every causal edge traces to a data receipt.** Calibrated language only. See `CLAUDE.md`.

## Key decisions (ADRs)
ADRs live in `memory/decisions/adr-NNN-*.md`. None recorded yet — record the load-bearing
build decisions here as they're made (embeddings provider, agent boundaries, verdict UX).
- [Hardware + Claude Science placement](memory/decisions/hardware-and-claude-science-placement.md) — RTX 3090 works in WSL; runtime on C:(SSD), bulk data on D:(HDD), G:/H: are cloud. `.wslconfig` raised 8→32 GB.
- [Hackathon track + facts](memory/decisions/hackathon-track-and-facts.md) — **track committed: RESEARCHER** (finding-first via Claude Science); prizes/deadline/rules from kickoff transcript; Claude Science now critical path.
- [LBD question-engine reframe](memory/decisions/lbd-question-engine-reframe.md) — **the strategic heart:** LBD *generates the questions* (fills the "rich dataset, no question" cold-start gap), Claude Science + data *answers* them. Spec: `docs/lbd-proposer-spec.md`.

## Recent Sessions
| Date | Focus | Key outcome |
|------|-------|-------------|
| 2026-07-07 | PM tooling + repo | Session-lifecycle skills + doc scaffold; handoff → `memory/NEXT_SESSION.md`; API key verified active; private repo `dayanjan/pyzobot-arbiter` created & pushed |
| 2026-07-07 (PM) | Claude Science + Validator | Researcher-track commit; Claude Science installed on WSL + driven via Playwright; QC/join-map + referee (Validator) built through it — YES/UNTESTED/REFUTED demonstrated with receipts; 6 artifacts in `docs/perturbseq-qc_2026-07-07/`; hardware fully characterized; 3-round codex-debate + independent Fable review on the install plan |
| 2026-07-08 | LBD proposer + finding (autonomous) | Spec hardened v1→v2 (3-round repo-read codex-debate, 9→3→0); fresh tool layer `src/arbiter/lbd/` (verified); disease ids MONDO-resolved; `referee_triple` exact-disease adapter; Codex consult fixed scoring+full-chain bug; full Stim8hr sweep 22,039→30 clean supported; **finding NAB2→Th1/Th2→atopic eczema** (near-novel, receipt-backed) |
| 2026-07-08 | Validation + source-paper vetting | 4-agent literature audit (new `src/arbiter/lit/`) → both links 0-papers novel; STAT6/EGR/cis confounders stress-tested & argued-against; **5-agent independent replication unanimous PASS** (`docs/replication/`); source-paper read → **reframed as novel reproducible NOMINATION, disease link flagged**; paper in `references/` + analysis repo recorded; ~8 commits |
| 2026-07-08 | Definitive STAT6 check + provenance (full-close) | Preserved full raw provenance trail (`docs/provenance/`, 52 artifacts); **definitive STAT6 cis-check** via lazy S3 read of authors' genome-wide DE → **NAB2-KD leaves STAT6 unmoved → cis/shadow EXCLUDED**, verdict upgraded to genuine novel NAB2-specific regulator; decided M5 = evidence-chain notebook + Claude Science chain + demo video |
| 2026-07-08 (M5, full-close) | **M5 shipped in full** | Evidence-chain **notebook**; **Claude Science evidence chain** (independent same verdict + figure); 3-screen Streamlit **"Researcher's Workbench"** app implementing a **Claude co-design** (imported via **DesignSync**), all screens preflight-green; **final demo video** (~112s, ElevenLabs "Brian" + CC-BY music, gate PASS 94%; recipe `docs/demo-video-pack/`). Two 3-round repo-read codex-debates (demo + workbench plans). Track → **"Researcher who also builds"**. Demo/app = fallback MVP |
| 2026-07-08 (overnight, autonomous) | **Claude Science capability deep-dive** | 5-agent transcript mining → `[DEMO]` catalog + testable inventory; 2-round repo-read codex-debate → executable test plan; **live-verified CS on our install** via drive-then-verify-from-**`operon-cli.db`** (doctrine §19). Confirmed: Reviewer=**Sonnet 5** caught a planted inconsistency (**fail**); OPERON=**Opus 4.8**; inline=**Haiku 4.5**; `host.mcp` batched lookup → **real Ensembl IDs**; `host.delegate` **gated** behind Delegation toggle. Hardened `cs-drive.js`. Docs in `docs/cs-capability-tests_2026-07-08/` + `docs/claude-science-{test-plan,demo-findings}_2026-07-08.md` |
| 2026-07-09 | **Pipeline↔CS mapping + native tracer + solidified plan** | Exhaustive 30-step LBD→NAB2 pipeline reconstruction + per-step CS feasibility (**~25/30 CS-native**; gap = cross-model/Codex); **LBD methods explainer** (manuscript seed); **CS TRACER** reproduced the 4-hop referee + NAB2 finding **natively, digit-for-digit** (+IL2 untested hero); **full-pipeline-in-CS plan** hardened by a **3-round repo-read codex-debate → SHIP**. Architecture: **CS = instrument, Codex = external cross-model auditor.** Docs: `pipeline-inventory-and-cs-mapping_2026-07-09.md`, `lbd-methods-explainer.md`, `plans/full-pipeline-in-cs-plan_2026-07-09.md`, `reviews/codex-debate_full-pipeline-cs_2026-07-09/` |
| 2026-07-09 | **Full pipeline reproduced natively in CS (MVP Stage 0/1/3/5)** | Implemented the §9 checklist. Stage 0 (feasibility): all 4 external paths from the kernel, incl. **anon S3 lazy read opens headless** → Stage 3 native. Stage 1 (generation): real `sweep()` unchanged over 3,935 genes under a **pure-replay guard** (cache delta 0) → funnel 3935/22039/43/30 + **NAB2 rank 4** exact, ALL_PASS. Stage 3 (falsification): native anon-S3 → **STAT6 unmoved +0.087/0.79, cis refuted**. Stage 5: CS receipt chain + **Sonnet-5 Reviewer verified numbers + enforced calibrated language**. Codex: Stage-1 design (Strategy B) + README honesty-eval (SHIP-WITH-EDITS, applied). Archived `docs/cs-full-pipeline_2026-07-09/` (16 files, provenance, ~$6.41) |

| 2026-07-09 (PM) | **CS instrument extended + NAB2 target/direction** | Live from-scratch micro-sweep (CS authored its own generator, liveness-verified); 100%-live loose sweep all 3 conditions (9,557 live calls) → filter-safe + NAB2 reproduced (Stim8hr rank 4, timepoint-specific) + 39 candidates (34 timepoint-specific), `CANDIDATES.md`; fixed inverted referee direction label (verdicts safe). DepMap = negative-for-cancer-target. **GEO direction mining** (3-round live-verified codex-debate → NO-CALL → ARM-D scRNA) → **association-backed NAB2-DOWN per-cell in lesional skin; knockdown likely backwards → Th2 BRAKE → restore/UP-modulate** (needs perturbation proof). Docs: `nab2-direction-geo_2026-07-09/`, `nab2-depmap-check_2026-07-09/` |

| 2026-07-09 (evening) | **Submission → CS-native video (pivot) + full de-risk** | Spine decided + polished (LBD-in-CS; library+lab on one bench); dataset attribution → Marson lab, citation locked; 3 QA'd visual assets (Swanson ABC graphic + 2 slides); capture de-risked (Playwright+saved CS auth) + all 4 CS conversations opened → verified capture plan (`cs/CAPTURE_PLAN.md`); CS-native demo pack (`cs/*`, harness via STORAGE_STATE, gate PASS); **2-round repo-read codex-debate** → spine held, 2 P0s fixed + NO made visible + calibration tightened, all applied. Deadline pulled to EOD Fri. Friday = capture+assemble+submit. Streamlit MVP = fallback |

| 2026-07-10 | Submission built + rebranded → Wayfinder | Cloned-voice video re-cut (gate 96%); 6-agent judge panel + frame-grounded codex-debate; judge-facing README/summary/bio; GitHub repo renamed `dayanjan/wayfinder` (private); fire-staged (`SUBMIT_CHECKLIST.md`) |
| 2026-07-10 (cont.) | **Manuscript kickoff — outline + sections 1-3** | Template = **Henry et al. 2021** (FRMA); Wayfinder framed as an **approach**; title locked; **outline** hardened by 3-round repo-read codex-debate (10→5→1; DOI→10.64898); **§1/§2/§3 drafted** (§3.4 = no-API CS driver); **CS actor-critic verified 16/18**; **prose codex-debate 14→4→0 converged** (caught `ac_known`=overall-not-genetic via code read). 5 commits `ec68a23`→`a2d125e`. Next = §4 Results |

| 2026-07-11 | **Full draft + LaTeX + citations + review roadmap** | §4 Results (CS-reproduced sensitivity panel, delta-0; 3-round debate 10→1→1) + §5 + Abstract → full §1–§5 arc. Ported LightsOut **citation stack** + `semantic_scholar.py`; **references.bib 4→12** (DOIs resolved/audited, **Zotero 12 in-sync**), wired into .tex. Built **LaTeX manuscript** (LightsOut approach) → **21pp PDF, 0 errors**; fixed equation margin-bleed + colored→black headings. Two **Major-Revision reviews** → dossier + **converged 3-round revision debate** → top-line = "prioritization + abstention + falsification diagnostics". **Codex 0.141→0.144.1, default gpt-5.6-sol.** Next = revision MVP |
| 2026-07-11 (evening) | **Revision MVP: reframe + 12q13 + C10 + C2** | 4 tested commits (`cde28b2`→`676fead`), manuscript 23pp/0-err. Reframe (title + prioritization/abstention/falsification top-line, "calibrated"=language-only, CS→replicable-in-principle); §4.4b foregrounds the 12q13 GWAS-label confounder (3 mechanisms separated); **C10** gate grid (`gate_grid.py`+§4.1c: NAB2×eczema rank {1,4,5} med 4, survives 18/27, misses=pct=0.75); **C2** hard negatives (`hard_negatives.py`+§4.2b: referee own-hop cull 16.9% arbitrary / 15.7% of top-association noms, vs 67.3% substrate-inherited — rebuts B1). All LOCAL (repo code+cache, §19), cache-free. Next = 4 figures |

| 2026-07-11 (overnight) | **Manuscript: figures + related-work + review-hardening** | 4 deterministic figures wired (23pp→32pp, 0 err); §2.4 related-work + §5.3b strengthening; **genomics fix** (NAB2–STAT6 convergent ~43kb, not 1.9kb; Ensembl-verified); 5-reviewer pass (4 Claude + Codex) + final Codex debate → all P0/P1 fixed; ~28 DOI-verified refs; deliverable `main.pdf`; `62bb929` |

_Last updated: 2026-07-12 (manuscript polished: figures collision-audited, abstract/first-para indents, 'honest funnel'→'funnel', 'honest' prose thinned, STAT6 'falsified'→'ruled out' aligned; 32pp/0-err; operator reading main.pdf; continue next session)_
