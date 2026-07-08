import pathlib
p = pathlib.Path("docs/lbd_finding_nab2_2026-07-08.md")
t = p.read_text(encoding="utf-8")

t = t.replace(
    "(ii) NAB2's program\n  effect is **~8× stronger than STAT6's own** (z 7.71 vs 2.66) and the KD is NAB2-specific → a real\n  regulator, not an echo.",
    "(ii) NAB2's program\n  effect exceeds STAT6's own (**~8× on effect size / ~3× on z**, 7.71 vs 2.66) and the KD is 2/2\n  on-target → a real regulator, not an echo.")

t = t.replace("members are FOXP1/GFI1/CD28/IRF4/IL4/IL10/IL22 from across the genome",
              "members (significant clusters 90 & 100) are BACH2/BCL6/IRF4/CD28/IL4/IL10 from across the genome")

anchor = 'axis STAT6 governs,"* not as a STAT6-independent discovery.'
add = anchor + (
    "\n\n  *(Independently replicated 2026-07-08 by a 5-agent lab — 3 Opus + 2 Codex, two clean-room\n"
    "  re-implementations: unanimous PASS; corrected the cluster IDs 74→90/100 and the 8×-vs-3× wording;\n"
    "  see docs/replication_report_2026-07-08.md.)*\n"
    "- **Funnel-framing honesty:** inside the A universe the PROGRAM hop is a tautology (all A genes pass\n"
    "  T2<0.05, so refuted_program=0) — it discriminates in the individual receipt, not in the funnel; and\n"
    "  the “30 clean supported” is a joint novelty-gate × referee product (referee alone supports 395/47,220),\n"
    "  so read it as “referee-supported among literature-eligible pairs.”")
assert anchor in t, "anchor not found"
t = t.replace(anchor, add, 1)

p.write_text(t, encoding="utf-8")
print("finding writeup patched OK")
