# AGENTS.md — cross-agent brief (Codex & other agents)

Companion to `CLAUDE.md`. Read both. This project is a hackathon **Researcher-track** entry framed as *a researcher who also builds*: **Wayfinder**, a hypothesis referee that validates T-cell mechanistic claims against real Perturb-seq data, returning a verdict with a receipt per hop. The deliverable is a **reproducible finding + how Claude Science reached it**; the referee / LBD engine / Claude-Science automation are instruments the researcher built to *ask and answer* the research questions (the tool is the method/vehicle, not a product to adopt).

## Stack
- Python >=3.11. Package/dep tooling: `uv` (or `pip` + venv). Data: `pandas` over local CSVs.
- LLM reasoning: Anthropic Claude (Claude SDK). Embeddings (if needed): Voyage AI. **Never OpenAI.**
- Retrieval/graph (as needed): LlamaIndex / on-disk. UI: Streamlit. Deploy: a simple managed host (written fresh).

## Never do
- **Never reuse pre-existing project code** (new-work-only hackathon). Author everything fresh. The old PyZoBot POC is a *mental reference only* — do not copy files.
- **Never let an LLM assert biology.** Every causal edge must trace to a data receipt (odds ratio / p-value / effect size) from the Perturb-seq tables.
- **Never use uncalibrated language** ("discovered/proven"). Use "consistent with / re-derived / refuted / untested / flagged."
- Never commit raw data or secrets (see `.gitignore`). Never add OpenAI as a provider.

## Working agreement
- Data-validation lookups are **deterministic functions/tools**, not LLM calls. Reserve LLM/agent calls for genuine judgment.
- Keep changes small and testable; the builder works in short async bursts. The live handoff is `memory/NEXT_SESSION.md` (dashboard: `WORK_PROGRESS.md`, index: `MEMORY.md`) — leave it updated.
- The 3-hop validation substrate + the DTO/tool contract are in `docs/plan.md` (sections 3 and 5). Follow it.

## How to run
Fetch data: `bash data/fetch_data.sh`. (Build/run commands land as the app is written.)
