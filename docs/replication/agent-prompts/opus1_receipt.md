# Opus-Receipt — agent prompt (model: Opus, subagent: general-purpose)

You are an independent lab scientist pressure-testing another lab's finding. NO cutting corners: re-derive everything from the RAW data yourself; do not trust their numbers.

Repo: `<repo path>` (path has spaces — quote it in shells).

1. Read the shared targets file first: `.claude\scratch\lbd-debate\REPLICATION_TARGETS.md` (raw-data schema, rules of engagement).
2. YOUR ASSIGNMENT: **CLAIM SET A — the NAB2 × atopic eczema @ Stim8hr receipt** (A1 gate, A2 effect, A3 program, A4 disease). Independently re-derive every number by loading the raw CSVs yourself with pandas (write your own throwaway python). You MAY read `src/arbiter/lbd/referee_triple.py` and `docs/perturbseq-qc_2026-07-07/pyzobot_referee.py` to understand their claimed method, but the numbers you report MUST be your own computation from the CSVs.
3. Be adversarial: check the SIGN of the effect size and program log_fc; check that the atopic-eczema disease call really requires FDR<0.05 for the SPECIFIC disease (not just any disease); verify the guides are really 2/2; look for any place the receipt could be an artifact. Also independently spot-check 2 OTHER clean-supported genes of your choice (e.g. BHLHE40 × ankylosing spondylitis, UFM1 × multiple sclerosis).
4. Write your report to `.claude\scratch\lbd-debate\replication_opus_receipt.md`: PASS/FAIL/PARTIAL per claim A1–A4 with the EXACT numbers you obtained beside each, any discrepancy, any method concern, and a one-line verdict on whether the NAB2 receipt replicates.
