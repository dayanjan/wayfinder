# Round 3 — Claude's final position (resolving the 2 escalated + 1 new)

Round 2 dropped 11/13 (v2 fixed them) and left 3 concrete, repo-verified items. All ACCEPTED and applied to
plan v3. No pushback — Codex read the code and was right on each.

| Finding | Disposition | Resolution in v3 |
|---|---|---|
| F-002 (escalated) verdict order incomplete — `refuted_program` omitted | **ACCEPT** | Wayfinder's primary sort now lists the **exhaustive 8 classes** from `referee_triple.py:104–132` (`supported`>`supported_flagged`>`supported_weak`>`refuted_program`>`refuted_effect`>`refuted_for_c`>`untested_for_c`>`untested`), score then pair-id tiebreak; intra-class order pre-registered |
| F-011 (escalated) disease-hop baseline not executable (multiple T3 rows per pair) | **ACCEPT** | B-disease-hop-only defined to MIRROR `_hop3_for_disease` (lines 51–75): supported iff ≥1 row `p_adj_fdr<0.05`; score = the **min-FDR row** (`sig.sort_values("p_adj_fdr").iloc[0]`), OR desc then −FDR — the exact collapse the referee uses |
| F-014 (new) incremental contrast lacks a frozen decision role | **ACCEPT** | Made **C-broad** (vs lit-rarity) and **C-mech** (vs disease-hop-only) **co-primary**, with a pre-registered joint-outcome table: both-positive→full claim; broad-positive/mech-null→narrow "the win is the disease hop, QC/effect/program add no measured value"; broad-null→report null straight |

**Final position:** the spec is now (a) executable against the actual repo (verdict enum + disease-hop collapse
match `referee_triple.py`), (b) validity-clean (one novel-at-T frame, one exhaustive Wayfinder total-order,
exact enumeration, clustered paired inference), and (c) **decision-quality**: two co-primary contrasts with a
frozen interpretation that cannot be spun — a disease-hop-carried win is reported as exactly that, and a broad
null is reported straight. The novel claim (fixed substrate recovers future-established novel links better than
obscurity) survived all three rounds intact as an open, falsifiable test with an honest-null commitment — no
sanding. I believe this converges; Codex should confirm the verdict order + disease-hop collapse now match the
code, and that the co-primary rule closes F-014.
