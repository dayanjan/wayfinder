# NEXT_SESSION — async handoff (canonical; written/read by session-closer & session-start)

## Next session priorities — written 2026-07-07 19:30

**Current state**: Full-close, tree clean, all pushed. Researcher track (plan v7). Referee/Validator BUILT + demonstrated (receipt-backed YES / UNTESTED / REFUTED). Claude Science installed + drivable fully headless (the `drive-claude-science` skill, validated E2E zero-click). Strategic reframe locked: **LBD generates the questions → Claude Science + data answers them**. Anchors ranked but NOT yet biology-vetted.

**Next action**: Explore + build the **thin LBD question-proposer** per `docs/lbd-proposer-spec.md`. Start by pinning the disease→EFO/MeSH and program→keyword maps (the one non-mechanical step), then the API clients (PubTator3 / Europe PMC / OpenAlex + Open Targets / GWAS Catalog exclusion) + the co-occurrence/novelty logic; emit `lbd_questions.json` that the existing referee consumes unchanged. [HYBRID: Claude pins maps + scoring; Codex builds clients/logic; Claude reviews.]

**Prerequisites**: none blocking — CPU/API only, no GPU/Colab. Optional NCBI API key raises PubMed to 10 req/s. Referee already at `docs/perturbseq-qc_2026-07-07/pyzobot_referee.py`.

**Open questions**: (1) vet the biology on ranked anchor candidates (GATA3/STAT4/ITK known-true; ZBTB25/CRIM1/IGSF9B/SLAMF1/ANXA4 non-obvious) before locking; (2) confirm the judging weights on the CV submit form (currently unverified — only "demo video super important" confirmed); (3) scope discipline vs July 13 — the referee alone is already a complete finding, so keep the LBD proposer thin and let it be the generate→answer upgrade.

**Do not touch**: never commit `.env`, data CSVs, `01-hackaton details/`, `.claude/scratch/`, `memory/install-audit/`. Claude Science's data dir (`~/.claude-science/.../workspaces/`) is scratch/reference, not the repo.

**Context to preload**: `docs/lbd-proposer-spec.md`, `memory/decisions/lbd-question-engine-reframe.md`, `docs/plan.md` (§0 v7), `docs/perturbseq-qc_2026-07-07/pyzobot_referee_results.md`, `docs/claude-science-capabilities.md`, `memory/decisions/hackathon-track-and-facts.md`, `WORK_PROGRESS.md`, `MEMORY.md`.

**Estimated budget**: ~0.5–1 day for the thin LBD proposer (fresh build; delegatable to Codex after the maps are pinned).
