# NEXT_SESSION — async handoff (canonical; written/read by session-closer & session-start)

## Next session priorities — written 2026-07-09 13:30 (full-close)

**Current state**: All threads complete + committed + pushed. The LBD instrument runs natively in Claude
Science (MVP Stage 0/1/3/5 + live from-scratch micro-sweep + 100%-live 3-condition loose sweep). The NAB2
finding is reproduced (Stim8hr rank 4, timepoint-specific) and stress-tested as a drug target: DepMap
negative-for-cancer (non-contradictory); GEO direction mining -> **association-backed NAB2-DOWN per-cell in
lesional skin -> the naive topical-knockdown is likely BACKWARDS; NAB2 reads as a Th2 BRAKE lost in disease ->
restore/UP-modulate** (ceiling: needs perturbation proof). Tree clean after this close.

**Next action**: **Two coupled deliverables** (operator stated intent): (1) **assemble everything into a
MANUSCRIPT** and (2) **derive the remaining-experiments list**. Start with `[CLAUDE]` a **manuscript-outline
decision** — pick the paper's spine (recommend: *method* paper = falsification-first LBD + native-in-CS
instrument, NAB2 as the worked exemplar, the timepoint-resolved 39-candidate table as the generalization),
then `[CODEX-DEBATE]` harden the outline via a repo-read debate. Then `[CLAUDE]` a **gap analysis**: map each
claim to its evidence tier (data-reproduced / association-backed / hypothesis) and list the wet-lab /
computational experiments to close each gap — especially the BRAKE hypothesis (does *restoring* NAB2 dampen
Th2?) and the disease link beyond GWAS-module enrichment.

**Prerequisites**: none blocking. CS daemon currently on **port 8000** (not 8765 — restarted this session;
`claude-science status` gives the live port; driver re-auths via nonce). Codex live-network recipe:
`codex exec -s workspace-write -c sandbox_workspace_write.network_access=true` + `NCBI_API_KEY` in env.

**Open questions**: (1) Manuscript spine — method-first, finding-first, or method+exemplar? (2) Target venue
(affects framing + figures). (3) Which experiments are in-scope for THIS paper vs future work — the
brake-hypothesis perturbation is the big one and may be "future directions," not required.

**Do not touch**: never commit `.env`, `data/*.csv`, `data/lbd_cache/`, `references/*.pdf`, `.claude/scratch/`,
`~/.claude-science/`, `docs/nab2-direction-geo_*/downloads/` (raw GEO, gitignored). Don't re-run completed
sweeps/arms (all archived). The referee direction-label is now CORRECT — don't "re-fix" it.

**Context to preload**:
`docs/cs-full-pipeline_2026-07-09/README.md` + `live-fullsweep-loose/CANDIDATES.md` (39 nominations +
timepoint-specificity); `docs/nab2-direction-geo_2026-07-09/SUMMARY.md` (NO-CALL->brake reversal) + `report.md`;
`docs/nab2-depmap-check_2026-07-09/README.md`; `docs/lbd-methods-explainer.md` (existing manuscript seed);
`docs/lbd_finding_nab2_2026-07-08.md`; `docs/plan.md` (S0 track framing); `WORK_PROGRESS.md`; `MEMORY.md`;
`docs/gotchas.md` (2026-07-09 entries).

**Estimated budget**: ~1 day for the manuscript outline + gap analysis; the full draft is multi-session.
Deadline 2026-07-13 EOD ET — submission MVP already exists, so the manuscript is upside, not gating.

---

## Mirror of this handoff is appended to memory/sessions/2026-07-09.md by session-closer.
