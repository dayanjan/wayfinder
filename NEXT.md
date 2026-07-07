# NEXT — async handoff (keep this current; solo, interruptible workflow)

**Updated:** 2026-07-07 (scaffold bootstrapped from Portfolio-Command planning session)

## State
Fresh repo scaffolded. Plan = `docs/plan.md` (v6). Data = 4 public Perturb-seq CSVs in `data/` (gitignored; `bash data/fetch_data.sh` to reproduce).

## The one thing that matters
Day-1 insurance (per plan section 7 + 11): stand up the deterministic **Validator tool** — the 3-hop CSV lookup (DE_stats -> polarization -> autoimmune enrichment, + KD-efficiency QC) — and prove the "receipt-backed NO/YES" loop end-to-end on ONE real gene. Capture the money-shot rough. Do this BEFORE the agent cast or UI polish.

## Next concrete actions
1. Set up venv + deps (`pandas`, `anthropic`; Streamlit + LlamaIndex when needed).  [CODEX-RESCUE]
2. Write `src/arbiter/validator.py` — deterministic 3-hop lookup returning a ProvenanceEdge per hop from the CSVs.  [CODEX-RESCUE]
3. Vet the TWO anchor hypotheses (known-true + non-obvious) — Claude to draft candidates from the tables, operator to confirm biology.  [CLAUDE + operator]
4. Minimal Streamlit page showing a verdict + receipts for one gene.  [CODEX-RESCUE]

## Do NOT
- Reuse any prior-project code (new-work-only). Assert biology from an LLM (receipts only). Use OpenAI. Commit data or secrets.
