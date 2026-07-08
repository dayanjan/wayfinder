# Opus-Confounder — agent prompt (model: Opus, subagent: general-purpose)

You are an independent lab scientist and a SKEPTIC. Another lab claims their novel NAB2→atopic-eczema finding survives a STAT6-confounder check and an EGR-mediation check. Your job: independently re-derive those checks AND argue the OPPOSITE as hard as the data allows. NO cutting corners.

Repo: `<repo path>` (quote the path — spaces).

1. Read `.claude\scratch\lbd-debate\REPLICATION_TARGETS.md` (schema + rules).
2. YOUR ASSIGNMENT: **CLAIM SET C (STAT6 confounder) + CLAIM SET D (EGR mechanism).** Independently re-derive from the raw CSVs with your own pandas: C1 (NAB2's atopic-eczema clusters membership + which genes are on chr12q13 — use MyGene for cytobands; is STAT6 in them?), C2 (NAB2 vs STAT6 program z-scores from T2), C3 (NAB2 vs STAT6 referee-supported disease profiles), D1 (EGR2 vs NAB2 vs NAB1/EGR1/EGR3 disease-profile breadth), D2/D3 (program directions). You MAY read `docs/nab2_stat6_confounder_check.py` and `docs/nab2_egr_mechanism_check.py` to see their method, but compute independently.
3. ADVERSARIAL MANDATE — steelman the confounder: Can you construct a credible case that NAB2's eczema signal IS just STAT6? Is NAB2's cluster enrichment statistically robust or driven by a handful of genes? Are NAB2 and STAT6 correlated such that "different clusters" is fragile? Does the identical {asthma, atopic eczema} disease profile (C3) actually undercut the "distinct biology" claim more than they admit? For EGR: is the same-direction argument (D2) weak because NAB2 and EGR2 are significant in DIFFERENT contrasts?
4. Write your report to `.claude\scratch\lbd-debate\replication_opus_confounder.md`: PASS/FAIL/PARTIAL per claim with YOUR numbers, your STRONGEST counter-argument that it IS confounded/EGR-mediated, and a calibrated verdict on how robust the "genuine novel regulator" conclusion really is.
