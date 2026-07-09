# Round 2 — Claude's revision (explicit accept / push-back / defer per Codex finding)

Codex's round-1 critique is repo-grounded and largely correct. Disposition of each finding:

| ID | Disposition | What changes |
|---|---|---|
| **F-001** (b5/b6b receipts are Friday-critical, not "tuning") | **ACCEPT** | Reclassify b5 `receipt.md` funnel/NAB2 and b6b reviewer-overclaim from `//TODO tuning` to **release blockers**. New pre-assembly gate: **pre-capture those two exact receipt frames FIRST** (screenshot the artifact-open), confirm they're crisp, and only then assemble. If either won't capture cleanly, fall back to a static screenshot overlay of that artifact — never narrate the claim over generic UI. |
| **F-002** (live-vs-cached boundary too easy to misread) | **ACCEPT** | This is the honesty crux. Two moves: (a) scope the narration — beat 4 "had Claude Science **author and run** a generator **live, from scratch**" (= the micro-sweep, true); beat 5 "the referee **re-ran each against the data**" (avoids implying a fresh 22k-crawl); (b) an on-screen caption during beat 5: *"full sweep = CS-native cached-receipt replay · micro-sweep + STAT6 S3 = live."* Explicit, not buried. |
| **F-003** ("literature had never drawn" over-absolute) | **ACCEPT** | Rescope to the receipt: "**six stray co-mentions — but no paper drawing the NAB2→Th1/Th2→eczema chain.**" Self-consistent with `ac_lit=6`. |
| **F-004** (STAT6 line closes more than the evidence) | **ACCEPT** | "the **CRISPRi cis-artifact concern** was refuted live against the authors' own genome-wide data; the **GWAS disease label remains a nomination.**" |
| **F-005** (under-sells the falsification thesis — the moat) | **ACCEPT (strongly)** | This is the project's actual thesis (CLAUDE.md: "confident, receipt-backed NO"). Add a **visible NO receipt** in beat 5: show a **failed knockdown → *untested*** (or SBF2 **effect-refuted**) on screen, not just asserted. Refusal made visible. |
| **F-006** (CS-only may weaken Demo if receipts aren't crisp; hybrid fallback) | **DEFER (documented contingency)** | Keep CS-native as the primary cut (operator's explicit call). But record the contingency: if the F-001 pre-capture shows the receipts aren't crisp, fall back to **hybrid** (CS for method-proof + the working Streamlit app for the human-readable referee result). Not a plan change; a named escape hatch. |
| **F-007** (title/endcap over-claims product maturity) | **ACCEPT** | Ground the endcap: "**In this workbench, I built the missing generation half — beside the test.**" Keeps the one-platform novelty without implying a shipped product. |
| **F-008** (reviewer beat depends on hidden artifact, may be visually weak) | **ACCEPT** | Ties to F-001: source the reviewer beat from a **prepared `review.json` artifact view / static overlay** showing "validated"/"definitive" flagged — not live scrolling. |
| **F-009** (Swanson setup may over-consume time) | **ACCEPT (partial)** | Keep the Swanson graphic (it's the concept-carrier + a Demo asset), but **tighten beat 3** and reallocate the seconds to the live micro-sweep receipt + the NO receipt (per F-005). |
| **F-010** (stale status text; verify env var spelling) | **ACCEPT** | Clean the status language (built vs gated vs blocker) and **verify `ELLEVENLABS_API_KEY` spelling** against the real `.env` before the Friday run. |

## Preserve-intent check
The novel spine is **intact and strengthened**, not sanded: accepting F-005 (show the NO) and F-002
(scope live-vs-cached honestly) makes the "generation + testing on one platform, each answering the
other's criticism" claim *more* defensible, not less. Nothing here collapses it toward "we used Claude
Science" — the differentiator is precisely that the refusal + the generation both live in the workbench.

## Revised key narration (the load-bearing beats)
- **B4:** "…Claude Science. The generation half was capable but missing — so I built it, and had the
  workbench **author and run a literature-based-discovery generator live, from scratch.**"
- **B5:** "Now generation and testing run side by side. The generator posed twenty-two thousand
  gene-and-disease hypotheses; a deterministic referee **re-ran each against the data** with a receipt at
  every hop. **Watch it refuse** — a failed knockdown comes back *untested*, not a false negative. Thirty
  survive. The standout: **NAB2** — six stray co-mentions with eczema, but **no paper drawing the
  NAB2-to-Th1/Th2-to-eczema chain** — re-derived here, receipt-backed." *(on-screen caption: full sweep =
  cached-receipt replay · micro-sweep + STAT6 = live.)*
- **B6:** "Its hardest confounder — a possible **STAT6 cis-artifact** — refuted live against the authors'
  own genome-wide data; the GWAS label remains a nomination. And the platform checks itself: a reviewer
  model **flagged 'validated' and 'definitive' as overclaims, and I cut them.**"

## Open question for Codex round 3 [sic — final round]
Given these revisions: does the on-screen **caption** (full=cached / micro+S3=live) plus the scoped
narration fully resolve F-002, or does the *video* still risk a judge inferring a live 22k-crawl from the
visible funnel numbers? And is showing **one** NO receipt (F-005) enough to carry the moat, or does the
3-min budget demand it be the *centerpiece* rather than a beat?
