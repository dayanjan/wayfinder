# NEXT_SESSION — async handoff (canonical; written/read by session-closer & session-start)

## Next session priorities — written 2026-07-08 (full-close)

**Current state**: **M3+M4 DONE, tree clean, all committed.** The LBD question-proposer is built
end-to-end; the finding **NAB2 → Th1/Th2 → atopic eczema** is replicated (5-agent lab, unanimous PASS)
and every confounder is closed — **including the definitive STAT6 cis-artifact check** against the
authors' deposited genome-wide DE (NAB2 knockdown leaves STAT6 unmoved → cis/shadow **excluded**).
Verdict: a genuine, novel, NAB2-specific Th1/Th2 regulator (a nomination re causality, per the paper).
Full provenance trail committed (`docs/provenance/`). Next = **M5 submission artifacts**.

**Next action**: Build the **executable evidence-chain Jupyter notebook** (the operator's chosen
submission format). Steps: (1) `pip install jupyterlab ipykernel nbformat`; (2) scaffold
`notebooks/pyzobot_arbiter_evidence_chain.ipynb` that **imports the vetted modules** (`arbiter.lbd`,
`arbiter.lit`) and runs the FAST decisive checks **live** with narrative markdown between cells:
build the A universe → NAB2 receipt via `referee_triple` → (funnel = cached load, it's the ~22-min
step) → the 4 confounder checks (`nab2_stat6_confounder_check`, `nab2_egr_mechanism_check`,
`nab2_cis_artifact_check`) → the **definitive STAT6 S3 read** (`nab2_stat6_definitive_check`) → the
honest verdict. Notebook = single source of truth. THEN capture the **Claude Science evidence chain**
(via `drive-claude-science`) as the "how Claude Science got us there" reasoning layer that mirrors it.

**Prerequisites**: `pip install -r requirements.txt` (pandas/requests/h5py/s3fs) + the jupyter stack.
The definitive-check cell needs network (public S3, no creds). The full sweep is cached in
`data/lbd_out/` (gitignored) — regenerate with `PYTHONPATH=src python -m arbiter.lbd.propose --condition Stim8hr` if absent.

**Open questions**: which notebook cells run live vs cached (the ~22-min sweep should be cached/shown,
not re-run); notebook ↔ Claude Science division of labor (notebook = executable; Claude Science =
reasoning provenance); then the **3-min demo video** (heavily weighted by judges) — narrative/format TBD.

**Do not touch**: never commit `.env`, `data/*.csv`, `data/lbd_cache/`, `data/lbd_out/`,
`references/*.pdf`, `.claude/scratch/`, `docs/provenance/` is already committed (don't regenerate).

**Context to preload**: `docs/lbd_finding_nab2_2026-07-08.md` (the finding + verdict),
`docs/lbd-build-log.md`, `docs/replication/README.md`, `docs/nab2_stat6_definitive_check.py`,
`src/arbiter/lbd/referee_triple.py`, `src/arbiter/lbd/propose.py`, `references/README.md`,
`WORK_PROGRESS.md`, `MEMORY.md`.

**Estimated budget**: ~0.5 day for the notebook; then the Claude Science evidence chain + the 3-min demo video.
