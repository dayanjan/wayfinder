FINDINGS: 8

POSITION: Claude's plan is directionally honest, but it still overestimates what the proposed analyses can prove. The feasible local work can move the paper from tool demonstration to a better-calibrated evidence-integration manuscript, but it will not establish correctness at scale unless the claims are narrowed and the C3/C6 analyses are reported as diagnostics rather than validation or joint FDR.

F-001 [P0] correctness nov=True - C3 is under-addressed: proposed baselines are mostly internal diagnostics, not external validation
  EVID: FEASIBLE but insufficient. Cross-condition artifacts exist at docs/cs-full-pipeline_2026-07-09/live-fullsweep-loose/{sweep_Stim8hr.json,sweep_Rest.json,sweep_Stim48hr.json,all_conditions_top.json}; local data support condition-specific referee checks via data/*.suppl_table.csv and src/arbiter/lbd/referee_triple.py. But these are the same Perturb-seq substrate, not external ground truth. Literature/OpenTargets baselin
  DO:   Run C3 anyway, but label it precisely: (1) internal temporal robustness across Rest/Stim8hr/Stim48hr, (2) random/literature-rarity/OpenTargets comparator for prioritization behavior, not accuracy. Add a small literature-curated positive-control panel of canoni

F-002 [P0] correctness nov=True - C6 'joint FDR' is statistically overclaimed; a permutation diagnostic is feasible, but not a true global null
  EVID: FEASIBLE as a bounded offline diagnostic from data/cluster_autoimmune_enrichment_results.suppl_table.csv, data/lbd_out/sweep_Stim8hr.json, data/lbd_cache/, and src/arbiter/lbd/propose.py. Existing Control 2 already permutes T3 disease labels and found observed 406 below null 467.7 +/- 10.9 in docs/manuscript/analysis/sensitivity_results.json. INFEASIBLE as a defensible 'whole-pipeline joint FDR' unless one specifies 
  DO:   Rename the C6 analysis to 'pipeline-level permutation diagnostic' or 'T3-label global-null diagnostic'. Report expected clean survivors under several constrained nulls: disease-label permutation within T3, gene-label permutation within condition, and eligible-

F-003 [P0] correctness nov=False - C4 cannot be resolved with current repo data; locus-wide neighbor check is useful but cannot discharge LD/colocalization
  EVID: PARTLY FEASIBLE. Existing evidence covers cis-expression and cluster co-membership: docs/lbd_finding_nab2_2026-07-08.md states NAB2 is ~1.9 kb from STAT6, ac_lit=6, zero mechanistic papers, and no colocalization/LD control; docs/cs-full-pipeline_2026-07-09/stage3/stage3_cis.json stores the STAT6 cis check; docs/replication_report_2026-07-08.md says corrected clusters 90/100 were re-derived and STAT6 was absent. NEEDS
  DO:   Promote C4 to a foreground limitation. Run the locus-wide neighbor check as a negative-control sanity check, not a resolution. Add a literature subsection on 12q13 atopic dermatitis/asthma GWAS and state explicitly that colocalization is unavailable here; phra

F-004 [P1] correctness nov=True - C2 random out-of-funnel discrimination is feasible, but the planned metric needs a real comparator and should not be sold as 'confident no' accuracy
  EVID: FEASIBLE offline from data/DE_stats.suppl_table.csv, data/guide_kd_efficiency.suppl_table.csv, data/cluster_autoimmune_enrichment_results.suppl_table.csv, and src/arbiter/lbd/referee_triple.py. Existing anecdotal out-of-funnel ledger exists at docs/perturbseq-qc_2026-07-07/pyzobot_referee_results.md for EGR2/IL2/SLC1A5. Existing Control 1 in docs/manuscript/analysis/sensitivity_results.json shows 2,430/2,430 failed-K
  DO:   Use two panels: (1) arbitrary genes for calibration of untested/refuted labels, clearly descriptive; (2) hard negatives from literature-plausible or proposer-eligible pairs that fail exact-C/effect gates. Compare against naive literature-only nomination and re

F-005 [P1] correctness nov=False - C10 threshold sensitivity is feasible but not with the current sensitivity panel alone
  EVID: FEASIBLE with existing repo/cache for Stim8hr, but it requires extending code. Existing docs/manuscript/analysis/sensitivity_panel.py only covers Control 1 QC, Control 2 label shuffle, and Control 3 beta/w/w2 rank stability. It does not sweep ab_gate_pct, min_bc, tau/ac_known, or alternative objectives. src/arbiter/lbd/propose.py exposes sweep(condition, min_bc, tau, ab_gate_pct, beta, w, w2). data/lbd_cache/ contain
  DO:   Add a small deterministic grid over ab_gate_pct, min_bc, and tau for Stim8hr, reporting clean survivor count, NAB2 survival/rank, and Jaccard overlap of supported sets. Keep it small; a full grid over all conditions is lower value than C3/C4/C6.

F-006 [P1] correctness nov=False - C9 reconciliation is feasible but needs fresh literature result inspection, not just restating ac_lit=6
  EVID: PARTLY FEASIBLE. The tension is documented in docs/lbd_finding_nab2_2026-07-08.md: ac_lit=6 but zero papers making the specific NAB2-Th1/Th2-eczema mechanistic claim. src/arbiter/lbd/sources.py computes Europe PMC hitCount with pageSize=1, so the cache may only preserve counts, not enough metadata for all six papers. tools/pubmed_fetch.py, tools/crossref_lookup.py, and tools/semantic_scholar.py exist for LIT work, bu
  DO:   Run a targeted LIT audit listing the six Europe PMC co-mentions with title, year, context, and whether each asserts NAB2->Th1/Th2, NAB2->eczema, or merely name co-occurrence. If network is unavailable, mark this NEEDS-FRESH-CS-RUN/LIT rather than claiming it i

F-007 [P1] correctness nov=False - The plan still needs a sharper hierarchy: C3/C4/C6 before extra figures and CS-workbench narrative
  EVID: FEASIBLE presentation fixes exist, but they are not load-bearing. Figure gap is real in the dossier; existing sensitivity outputs are at docs/manuscript/analysis/sensitivity_results.json; CS/browser artifacts are extensive under docs/cs-full-pipeline_2026-07-09/. Reviewer concerns C13/C16/C17 explicitly say CS overreaches. Conversely, C3/C4/C6 are the evidentiary objections that decide whether the manuscript moves be
  DO:   Minimum figure set: Fig 1 architecture with construction-vs-referee separation, Fig 3 or a compact ledger/funnel with C1/C2/C6 diagnostics, Fig 4 NAB2 chain with 12q13 caveat, and the sensitivity/null panel. Drop or supplement Fig 5 unless space remains. Keep 

F-008 [P1] correctness nov=True - Strategic answers: the honest reframe is necessary but not sufficient
  EVID: Repo-grounded answers to the five open questions: (1) reframe alone is not enough; C3 diagnostics plus a constrained C6 null are needed, but must be described as diagnostics. (2) C4 cannot be resolved from current files; docs/lbd_finding_nab2_2026-07-08.md already admits no LD/coloc, so foreground limitation. (3) CS should be Methods/appendix plus a short reproducibility note; docs/cs-full-pipeline_2026-07-09/ suppor
  DO:   Revise the plan order: first settle claims and limitations, then run C6/C3/C10, then build figures. Treat C2 random-panel as secondary unless it is designed around hard negatives. Do not claim wet-lab or LD validation; preserve the untested-vs-refuted and fals

NEXT: Which exact claim should the revised manuscript defend as its top-line result: calibrated receipt-backed prioritization with falsification diagnostics, or empirical correctness of supported calls? The analysis priority and wording differ substantially.
