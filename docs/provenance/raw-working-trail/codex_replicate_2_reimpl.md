You are an INDEPENDENT lab, read-only in this repo, RE-IMPLEMENTING another lab's key result FROM
SCRATCH to see if it reproduces. No cutting corners — write your OWN fresh analysis; do NOT import
their `arbiter.lbd` modules for the numbers.

Read first: `.claude/scratch/lbd-debate/REPLICATION_TARGETS.md` (claims A–E + raw-data schema).

Repo path has spaces — quote it. pandas is installed. You are read-only (read CSVs, print to stdout;
no file writes needed).

## Task 1 — re-derive the NAB2 receipt (CLAIM SET A) with your OWN pandas code
Load the four raw CSVs directly and independently compute, for NAB2 @ Stim8hr:
- GATE (T4): how many NAB2 guides have signif_knockdown=True, best adj_p, mean guide vs NTC expr.
- EFFECT (T1): ontarget_significant, ontarget_effect_size, n_downstream, offtarget_flag.
- PROGRAM (T2): NAB2's log_fc/zscore/adj_p in BOTH contrasts; which are significant + direction.
- DISEASE (T3): explode intersecting_genes; find NAB2's rows for disease=="atopic eczema" AND
  gene_set=="downstream_Stim8hr"; report every (cluster, odds_ratio, p_adj_fdr); is ≥1 FDR<0.05?
Report PASS/FAIL vs claims A1–A4 with YOUR exact numbers.

## Task 2 — re-implement the full-chain classifier (CLAIM SET B3) FROM SCRATCH
Write your own function that, for a (gene, disease, condition) triple, returns one of
{supported, supported_weak(effect n_downstream==0), supported_flagged(offtarget), refuted_effect,
refuted_program, refuted_for_c, untested} using ONLY the raw CSVs and the same rules (gate: ≥1
signif guide; effect: ontarget_significant OR n_downstream>0, flagged if offtarget; program: ≥1 T2
contrast adj_p<0.05; disease: exact disease FDR<0.05). Then build the A universe yourself (KD-gate ∩
effect ∩ program-significant T2 adj_p<0.05), run your classifier over A × the 12 eligible diseases
(read the 12 from T3, excluding the 2 umbrella terms "autoimmune disease" + "inflammatory bowel
disease"), and report YOUR chain-class counts. Compare to claim B3 (43 disease-C-supported; 30 clean;
10 weak; 3 flagged; 1 refuted-effect). Note: for the disease-C gate you can consider ALL A genes ×
12 diseases (skip the literature/OpenTargets pre-gate) — so your disease-C-supported total may be
LARGER than 43; what matters is whether the CLEAN-vs-weak-vs-flagged PROPORTIONS and the NAB2 result
reproduce.

## Task 3 — sanity the novelty framing (CLAIM SET E, light)
Confirm NAB2 & STAT6 genomic adjacency (E3): note chr12q13.3 for both. (You need not re-run the full
literature audit; just state whether the "0 direct papers" claim is plausible given NAB2's known
role.)

OUTPUT (plain prose, tight): PASS/FAIL/PARTIAL per claim set with YOUR numbers beside the claim; any
place your independent re-implementation DISAGREES with theirs (most valuable); and a final verdict:
does the NAB2 receipt + the funnel proportions reproduce under a clean-room re-implementation?