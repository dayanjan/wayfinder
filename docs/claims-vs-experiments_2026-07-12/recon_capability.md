# Recon — CS CAPABILITY & SELF-AUDIT (M5, M6-driving, tracer→M1/M4)

**Step 2 reconciliation, cluster: CS capability & self-audit.** Read from PRIMARY artifacts
(`docs/cs-capability-tests_2026-07-08/{RESULTS.md,artifacts/*,tracer-artifacts/*,artifacts-mcp/*}`,
`docs/claude-science-evidence-chain_2026-07-08/*`), not manuscript summaries. Cross-classed vs the
CLAIMS_LEDGER and the panel (`docs/reviews/contribution-novelty-audit_2026-07-12/{verify_audit.md,VERDICT.md}`).

**Governing distinction (the task's core ask):** separate **"is this a real, useful capability?"** (largely
YES on the evidence) from **"is this a novel scientific contribution?"** (NO — panel-confirmed, and the
manuscript already concedes it). Both are true simultaneously. The evidence lets the manuscript make a
*stronger capability* statement than the panel's "engineering, not novel science" dismissal implies — but
NOT a stronger *novelty* statement. Where the manuscript keeps M5/M6 scoped to method/vehicle, the evidence
backs it. The honesty risk is not overstatement of what was *observed*; it is the temptation to promote
these from craft to contribution (which the manuscript, so far, resists).

---

## M5 — Actor–critic self-audit (independent reviewer enforces calibrated language)

**(1) Experiment + key finding.** Two live runs. **Combined-audit run 1** (`proj_f73a77807d02`, ~$3.17):
an inconsistency was *planted* in `final_summary_with_planted_inconsistency.md` — line 14 says "The
delegation used exactly four personas" while the table immediately below lists **five**. An **independent
Sonnet-5 Reviewer** (separate REVIEWER frames, actor=Opus-4.8) **CAUGHT it**: `verification_checks` (DB)
holds a **FAIL** — *"final_summary… asserts 'exactly four personas' while the table lists five"* — plus a
WARN on the delegation→`host.llm` substitution. The reviewer **read the actual saved artifacts** to ground
the finding; the FAIL committed **~10 min after** the driver's "DONE" (reviewer is genuinely async, not a
scripted inline step). **The catch is real and model-independent** — a Sonnet critic finding an Opus
actor's planted error by reading files, not a hardcoded assertion.

*Second, weaker data point (tracer run):* the calibration reviewer **flagged the word "validated"** in
NAB2's verdict as stronger than the per-hop `supported` statuses warrant — but the wording was **RETAINED
by design** (it is prescribed verbatim by the referee spec; the disagreement was noted, not fixed;
`receipt_chain.md` §"Language audit"). So the language critic fires, but here it was *overruled*, not
obeyed.

**(2) vs CLAIM (M5).** **PARTIAL / SUPPORTS-with-caveat.** The claim "an independent reviewer model flagged
& removed 'validated'/'definitive'" is only half-borne: the **independence + catch** are strongly supported
(the four-vs-five FAIL); the **"removed"** half is NOT uniformly true — in the one language-hygiene instance
captured, "validated" was **flagged and retained**. The catch demonstrated is a *consistency/numeric* catch
(4≠5), not a *language-calibration removal*. The manuscript should not cite this as "the critic removed
overclaiming language"; it is "the critic independently caught a planted inconsistency, and separately
flagged (did not remove) a calibration word."

**(3) vs PANEL.** Panel (verify_audit M5) = "PARTIALLY-ANTICIPATED as method; NOT OVERSTATED as written…
disciplined authorship hygiene via a second model… n=1 anecdote." The evidence **supports a stronger
*capability* framing than the panel grants**: this is not merely "plumbing" — a genuinely independent
cross-model critic (Sonnet auditing Opus), running async, reading artifacts, and catching a real seeded
error is a *demonstrated working critic*, useful and non-trivial. But it does **NOT** rebut the panel's
*novelty* verdict: LLM-as-judge + overclaiming-detection are mature fields; this is application, n=1. Both
hold: real capability, not novel science.

**(4) HONESTY FLAG.** (a) The catch is real, NOT scripted — but it is a **planted** inconsistency in a
capability *test*, an n=1 designed demonstration, not a spontaneous catch inside the production manuscript
pipeline. Don't let it read as "the critic routinely polices our paper." (b) "flagged **& removed**
'validated'/'definitive'" overstates the observed behavior — the one language flag captured was **retained
by design**. Recommend the manuscript say "flagged" and describe the retain-with-note outcome honestly.

---

## M6 — Headless scripting of an API-less workbench (the *driving* capability + the tracer reproduction)

**(1) Experiment + key finding.** Two capability strands, must be kept distinct:

- **Driving is real.** The hardened `drive-claude-science` Playwright driver ran a full CS analysis
  headlessly, auto-approved sandbox cards ("allow for this conversation") with **no hang/misfire**, polled
  to a correct DONE, and pulled artifacts + the `operon-cli.db` receipt store (per-`host.*`-call log,
  per-cell `execution_log`, `artifact_versions`, `verification_checks`, per-frame cost/model). CS exposes
  **no task-submission API**, so browser automation is the only scripting path — confirmed. **MCP-as-skill**
  also drove programmatically: one batched `host.mcp("genes-ontologies","query_genes",{5 genes})` returned
  5 correct real Ensembl IDs, none fabricated (`mcp_lookup_method.md`).

- **The tracer reproduction is GENUINE native re-computation, not a cache replay.** In a fresh CS project
  (`proj_774ded9efc2e`), CS was given the referee **rules + schema but NOT the expected numbers**; it wrote
  its own `referee.py` (16.8 KB) that `pd.read_csv`s the raw supplementary tables from `~/pyzobot-data/` and
  computes each hop — **"nothing is hardcoded"** (verified in `referee.py`: lines 44–60 load + aggregate the
  raw T1–T4). Output `verdicts.json` matches the external pipeline **digit-for-digit**: NAB2 effect
  **−16.88158589** (vs −16.9), Ota **z 7.7077** (vs 7.71), eczema **OR 3.898532 / 3.43040** (vs 3.90/3.43),
  IL2 gate **0/2 signif → UNTESTED** (the hero catch, reproduced), SLC1A5 **refuted at HOP1**. This is a
  real independent re-derivation on the same data.

**(2) vs CLAIM.** For **M6** (the *driving* claim): **SUPPORTS** — headless scripting of an API-less
workbench works end-to-end, with the DB as a full audit receipt. For the tracer's bearing on **M1/M4**:
**SUPPORTS** — the deterministic non-LLM referee (M1's wedge) and the division of labour "LLM assembles,
code computes the receipt" (M4) both **reproduce natively inside CS** with the LLM writing correct
`pandas` and the numbers copied from tables, not asserted by the model. The QC-gated abstention (M2's hero
UNTESTED) reproduced exactly.

**(3) vs PANEL.** Panel (verify_audit M6) = "engineering plumbing, unambiguously… a driver + auto-approver
+ poller + artifact-puller." The evidence backs a **stronger capability** statement (it genuinely works,
zero-click, with a full receipt store) — but confirms it is **instrumentation, not a scientific method**.
Panel's sharpest caveat is **correct and important**: the panel's "byte-for-byte" worry applies to the
**full-pipeline sensitivity-panel** claim (M6 as worded in the ledger: "sensitivity panel byte-for-byte"),
which is a **cache replay under a raise-on-live-call guard, cache delta 0** — the *weaker* "recompute
identical outputs from cached inputs" sense. **That is a different artifact from this tracer.** The tracer
IS a genuine native re-derivation; the full-pipeline byte-for-byte is a cache replay. The manuscript must
not let the tracer's genuineness launder the full-pipeline replay into sounding live.

**(4) HONESTY FLAG.** (a) **Two senses of "reproduce" must stay separated:** tracer = genuine native
computation from raw tables (strong); full-scale sensitivity panel = deterministic replay of cached inputs,
no live calls (honestly labeled in RESULTS/panel, but weaker — do not conflate). (b) **`host.delegate`
failed** — it is gated behind a session "ultra-mode" Delegation toggle (off by default); the agent fell
back to `host.llm_batch` parallel fan-out and **disclosed the substitution** (`final_summary` provenance
note + the reviewer's WARN). So "multi-persona **delegation**" is really parallel single-shot `llm()`
sampling, not true sub-agent delegation — honestly disclosed, but the word "delegation" overstates the
mechanism. (c) Provenance `extracted_code` repro-block **did not backfill** for headless-driven runs
(0/14; tied to frame completion which headless driving doesn't trigger) — the durable repro receipt is
`artifact_versions.extracted_code` + the dependency graph, and it lands async, not at DONE.

---

## Cross-claim summary table

| Claim | Experiment (primary) | vs CLAIM | vs PANEL ("engineering, not novel") | Honesty flag |
|---|---|---|---|---|
| **M5** self-audit | Sonnet-5 reviewer caught planted 4-vs-5 (FAIL, async, read artifacts) | **PARTIAL/SUPPORTS** — catch real; "removed" half not borne out | Capability stronger than panel grants; novelty verdict (mature LLM-judge, n=1) stands | "flagged & **removed**" overstated (one flag was **retained** by design); catch is a *planted test*, not production |
| **M6** driving | Headless Playwright drove CS full-auto; DB receipt store; MCP batched lookup | **SUPPORTS** (driving works) | Real, working instrumentation — but instrumentation, not method (panel correct) | Full-pipeline "byte-for-byte" = cache replay (≠ tracer); `host.delegate` gated→fell back to `llm_batch` (disclosed) |
| **tracer → M1/M4** | CS wrote own `referee.py`, computed from raw tables, digit-for-digit match; IL2 UNTESTED reproduced | **SUPPORTS** — native non-LLM referee + code-computes-receipt reproduce inside CS | Confirms M1 wedge (deterministic referee over held substrate) runs natively; does not raise M1 novelty | Genuine re-computation, NOT hardcoded/cache — this is the *strong* repro; keep it distinct from M6 replay |

**Bottom line.** The capability evidence is real and, in places (the independent critic's catch; the
digit-for-digit *native* tracer re-derivation), **stronger than the panel's "plumbing" framing suggests** —
these are working, receipt-backed capabilities, not just claims. But nothing here elevates M5/M6 to novel
science, and the manuscript's own scoped framing (method/vehicle) is the correct and defensible posture.
Three specific honesty corrections for the manuscript: (i) M5 "removed" → "flagged (retained-with-note in
the one language case)"; (ii) keep tracer *native* reproduction rigorously separate from full-pipeline
*cache-replay* "byte-for-byte"; (iii) call `host.llm_batch` fan-out what it is, not "delegation."
