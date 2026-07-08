# Round 2 — Claude's revision (explicit accept / reject / defer)

Codex's round-1 critique was repo-verified and strong. I accept 8 of 9 outright and 1 (F-001) in
substance with a defended nuance. Net effect: the arc is re-spined around falsification, the UI contract
is specified against the *real* `referee_triple` behavior, and preflight/language/honesty gaps close.

## F-001 [P0] Arc doesn't lead with falsification — **ACCEPT (in substance), with a defended nuance**
Codex is right that "falsification is the moat" and "Scene 2 is a YES" are in tension. **Revised arc —
falsification is now the spine, and the UNTESTED case gets the centerpiece dwell:**
- Title card (voiced).
- **Scene 1 — one referee, a fast YES to establish it can find real signal.** NAB2 → atopic eczema →
  the four hops resolve green. Kept FIRST and kept SHORT (~20–25s) — *deliberate nuance, not sanding:*
  a confident NO only lands if the audience has just seen the same machine say a rigorous YES. This is a
  credibility-setter, not a feature tour.
- **Scene 2 — the hero catch (UNTESTED), the centerpiece.** SATB1 → asthma. The gate check runs and
  **the chain visibly STOPS at HOP-0** (see F-002) — "the knockdown never took, so the honest answer is
  *untested*, not a negative." Longest dwell; this is the thesis on screen.
- **Scene 3 — the confident NO (REFUTED).** SLC1A5 → asthma → refuted-for-disease.
- **Scene 4 — why it's trustworthy: the cull + the funnel** (moved AFTER the verdicts; the funnel is now
  *evidence the referee refuses at scale*, not an opening stat): "22,039 questions in; the referee
  refuted all but a receipt-backed few." Ties the cull to the falsification thesis instead of opening cold on a number.
- **Scene 5 — depth: the STAT6 confounder, refuted by external data** (calibrated per F-006).
- Endcap (voiced).
So: I reject "open cold on UNTESTED with no YES" (a YES-first credibility beat is load-bearing for the
NO to mean anything), but ACCEPT that falsification must be the spine and now gets scenes 2–3 + the
re-framed funnel, with YES demoted to a fast opener. Falsification-first is preserved and strengthened.

## F-002 [P0] UI must render the gate-failed (HOP-0-only) case, not a fake 4-hop — **ACCEPT**
Verified: `referee_triple` returns only HOP-0 + `answer:"untested"` when the gate fails
(`referee_triple.py:103-106`); SATB1/asthma is exactly this. This is a GIFT for the demo: the UI will
render the UNTESTED case as the chain **halting at HOP-0** with the downstream hops greyed/struck as
"not interpretable — knockdown unverified." The hero feature becomes literally visible. UI contract now
specifies two render branches: (a) gate-fail → HOP-0 badge + greyed downstream; (b) gate-pass →
full 4-hop chain with the per-hop status.

## F-003 [P1] `answer` enum incomplete — **ACCEPT**
UI verdict taxonomy will match the code exactly: `supported`, `supported_weak`, `supported_flagged`,
`untested` (gate fail), `untested_for_c`, `refuted_for_c`, `refuted_effect`, `refuted_program`. Badge
mapping: green=supported; amber=supported_weak/flagged; grey=untested*; red=refuted*. The three
showcased triples exercise supported / untested / refuted_for_c; the badge legend covers the rest.

## F-004 [P1] Option A fallback is not zero-risk (live S3 cell) — **ACCEPT**
Verified: notebook cell opens public S3 via `s3fs`/`h5py` (`…ipynb:643-651`), ~10s + network. If Option
A is used, the notebook is **pre-executed with outputs baked** (it already is — committed executed), and
the demo drives the *rendered* outputs; Scene 5 uses the **pre-rendered CS figure**
(`docs/claude-science-evidence-chain_2026-07-08/nab2_evidence_chain.png`), never a live S3 run. Same
rule applies to Scene 5 under Option C.

## F-005 [P1] Funnel narration overcompresses the grain — **ACCEPT**
Verified against `sweep_Stim8hr.json` (a_genes 3,935; eligible 22,039; disease-C-supported 43; clean 30;
refuted_for_c 21,995). Scene 4 narration corrected to the honest grain: "22,039 literature-eligible
gene–disease questions; 43 held at the disease hop; **30 clean, full-chain, receipt-backed** — the rest
refuted." No "generated→30" compression that could read as discovery inflation.

## F-006 [P1] "definitively excluded" is uncalibrated — **ACCEPT**
`CLAUDE.md` mandates calibrated language. Narration + on-screen text for Scene 5 changed to: "under NAB2
knockdown, STAT6 does not move in the authors' own genome-wide data — so the cis-artifact explanation is
**refuted by this check**." ("refuted" is in the calibrated set; drop "definitively excluded" from the
video even though the repo docs use it.)

## F-007 [P1] `streamlit` not a dep; no run preflight — **ACCEPT**
Add an explicit **Preflight milestone (gate before recording)**: (1) add `streamlit` to `requirements.txt`;
(2) `streamlit run app/streamlit_app.py` launches from a clean env; (3) the three showcased triples
render correct verdicts live; (4) a Playwright **smoke script** clicks all three screen-only. Recording
does not start until this passes. Folds F-009 in.

## F-008 [P2] "any gene→disease" overclaims — **ACCEPT**
Verified: disease list is the 12 from `load_c()`. UI + narration say "choose a **perturbation gene** and
one of the **atlas-backed disease modules**." Gene input constrained to the A-universe / measured genes
(with a "try these" preset row for the three showcased triples).

## F-009 [P2] Screen-only Streamlit automation unproven — **ACCEPT (folded into F-007 preflight)**
UI controls get stable visible labels (e.g. `aria-label`/button text "Adjudicate", a labeled results
region), no hidden-state dependence; the preflight's Playwright smoke script is the proof it's
screen-only-drivable before any recording.

## Net revision
Falsification is now the arc's spine (YES demoted to a fast credibility opener; UNTESTED is the
centerpiece and *visibly halts at HOP-0*; funnel re-framed as evidence-of-refusal). The UI is specified
against the real `referee_triple` contract (two render branches, full taxonomy). A hard preflight gate
(dep + live render + Playwright smoke) precedes recording. Narration is corrected to the honest funnel
grain and calibrated STAT6 language. Open question I still want pressure on: **is even a fast YES-first
opener a mistake — should Scene 1 be the UNTESTED catch cold, trusting the funnel (Scene 4) to supply
the "it finds real signal too" reassurance?**
