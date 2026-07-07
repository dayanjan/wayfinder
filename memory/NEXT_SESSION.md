# NEXT_SESSION — async handoff (canonical; written/read by session-closer & session-start)

## Next session priorities — written 2026-07-07

**Current state**: Day-1 insurance phase, no product code yet. Repo scaffolded, plan =
`docs/plan.md` (v6), data = 4 public Perturb-seq CSVs in `data/` (gitignored;
`bash data/fetch_data.sh` to reproduce). PM tooling just added — checkpoint, not full-close.

**Next action**: Write `src/arbiter/validator.py` — the deterministic 3-hop CSV lookup
(DE_stats → polarization → autoimmune enrichment, + KD-efficiency QC) returning a
`ProvenanceEdge` per hop, and prove the receipt-backed NO/YES loop end-to-end on ONE real
gene. Capture the money-shot rough. Do this BEFORE the agent cast or UI polish.

**Prerequisites**: venv + deps (`pandas`, `anthropic`); data CSVs present (`bash data/fetch_data.sh`).

**Open questions**: Which TWO anchor hypotheses (known-true + non-obvious)? Claude drafts
candidates from the tables; operator confirms the biology before they're locked.

**Do not touch**: Nothing in-flight. (No WIP artifacts on disk.)

**Context to preload**: `docs/plan.md`, `CLAUDE.md`, `AGENTS.md`, `data/README.md`,
`WORK_PROGRESS.md`, `MEMORY.md`.

**Estimated budget**: ~3–5 hours for the Validator + one-gene proof (M1).

## Do NOT (standing constraints)
- Reuse any prior-project code (new-work-only). Assert biology from an LLM (receipts only).
  Use OpenAI. Commit data or secrets.

## Delegation tags (per user doctrine §10)
1. venv + deps  — [CODEX-RESCUE]
2. `validator.py` 3-hop lookup  — [CODEX-RESCUE]
3. Anchor-hypothesis vetting  — [CLAUDE + operator]
4. Minimal Streamlit verdict page  — [CODEX-RESCUE]
