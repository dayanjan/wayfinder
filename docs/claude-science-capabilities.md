# Claude Science — fully curated capability list

**Compiled 2026-07-07** from five independent sources, cross-checked. Source tags per item:
`[UI]` live product Customize panel (this install, ground truth) · `[INSTALL]` filesystem/CLI probe
of the running install · `[DOCS]` official Anthropic/Claude docs (26 pages) · `[KEYNOTE]` the launch
keynote transcript · `[3P]` 52 third-party sources · `[OURS]` first-hand from driving it today.

> **Version probed:** `claude-science 0.1.16-dev.20260707` (public beta, launched 2026-06-30).
> **What Claude Science IS:** a local desktop AI workbench for scientists — Claude writes & runs
> Python/R/shell in an OS sandbox on your machine, queries 60+ scientific databases, runs GPU
> biomodels, and saves versioned artifacts with full provenance, with a background reviewer agent
> auditing every claim. Not web-hosted; not for clinical/diagnostic use.

---

## 1. Agent architecture & orchestration
- **Four bundled agent profiles** `[INSTALL]`: **OPERON** (main generalist — "compute, don't confabulate"; cites tool-returned IDs, never training memory), **REVIEWER** (mid-session fact-checker), **BOOKMARKER** (returns "breadcrumb" quotes for resuming), **ONBOARDING** (first-run interview → proposes 3 first tasks).
- **Plan → approve → execute** `[KEYNOTE][OURS]`: a one-sentence prompt yields a multi-phase plan (with a confidence estimate on scope/feasibility) that the user approves or iterates before execution. We saw "6 steps → Plan approved."
- **Natively multi-agent / sub-agents** `[KEYNOTE][DOCS][OURS]`: splits work into parallel sub-agents, each with its own brief + output schema + transcript. Keynote demoed **100 parallel sub-agents** across 100 diseases; "scale is no longer an issue."
- **Background Reviewer (actor-critic)** `[DOCS][INSTALL][OURS]`: an *independent* agent re-examines claims/artifacts at checkpoints — checks results were actually computed, value-vs-source consistency, citation/DOI accuracy, plan-step completion, conclusion-method alignment. Records "findings" on each artifact's **Review** tab; does **not** re-run analyses. Auto-review on by default (Max/Team/Ent; Pro since v0.1.16); user can "Request review" anytime; custom criteria via Settings › Specialists › Reviewer.
  - **⚠ Discrepancy (our data corrects the press):** some outlets `[3P]` claim the reviewer runs on the *same model* as the work (a criticism). Our first-hand run `[OURS]` + the separate `REVIEWER` agent profile `[INSTALL]` show it is a **distinct agent** — we observed it running **Sonnet 5** while the primary ran **Opus 4.8**.
- **Judgment-to-interrupt** `[KEYNOTE]`: long-running agents stop and flag the human when they need input (e.g. an unapproved dependency in a regulated task).
- **Scheduled/routine agent runs** exist as a first-class DB concept `[INSTALL]` (Drizzle migration names: routine scheduling, verification tables).

## 2. Skills (28 built-in) `[INSTALL]`; 16 shown as "Featured" in the UI `[UI]`
Loaded automatically when the work calls for it. Add your own via chat, from scratch, zip upload, or **GitHub import** (private repos via personal creds, v0.1.16).

- **Structure/sequence biomodels (GPU):** AlphaFold2, Boltz(-2), Chai-1, OpenFold3, ESMFold2 (+ESMC PLMs), ESM-2 (`fair-esm2`), Evo 2 (DNA foundation model), Borzoi (DNA→regulatory track / variant effect).
- **Protein design (inverse folding):** ProteinMPNN, LigandMPNN, SolubleMPNN, DiffDock (blind docking).
- **Single-cell:** scGPT, scvi-tools (scVI/scANVI batch correction, Bayesian DE).
- **Compute orchestration:** compute-env-setup, remote-compute-ssh, remote-compute-modal, managed-model-endpoints (NVIDIA-NIM-style), using-model-endpoint.
- **Writing/figures:** figure-style (pub-grade plot QA — this is the skill we saw its reviewer invoke), figure-composer (multi-panel, adversarial composite review), paper-narrative (manuscript arc judge), indication-dossier (5-phase therapeutic dossier).
- **Research/meta:** literature-review (Crossref/OpenAlex, anti-fabrication), pdf-explore, skill-creator, customize (author agents/skills programmatically), self-awareness (introspect its own session DB), product-self-knowledge.

## 3. Connectors / databases (24 in UI; ~55 client packages, 20 categories, ~150 MCP tools)
Wired over **MCP** (`bio-tools` bundled MCP server `[INSTALL]`). UI names `[UI]`: BioMart, Cancer Models, CellGuide, Chemistry, Clinical Genomics, Drug Regulatory, Expression, Genes & Ontologies, Genomes, Human Genetics, Ketcher Chemistry, Literature Graph, Omics Archives, Protein Annotation, Regulation, Research Resources, RNA, Structures & Interactions, Variants, ZINC + **Directory** (bioRxiv, ChEMBL, Clinical Trials, PubMed). Named underlying sources `[DOCS][INSTALL]`:

| Category | Sources |
|---|---|
| Literature | PubMed, Europe PMC, OpenAlex, arXiv, bioRxiv, Crossref, Semantic Scholar, Unpaywall |
| Genomics/genes | Ensembl (REST/BioMart/VEP), UCSC, GO, KEGG, UniProt, Reactome, InterPro, Pfam, STRING, MyGene |
| Variants/human-genetics | ClinVar, dbSNP, gnomAD, CADD, GWAS Catalog, eQTL Catalogue, PheWAS/FinnGen |
| Clinical/cancer | Open Targets, CIViC, ClinGen, cBioPortal, DepMap, openFDA, ClinicalTrials.gov |
| Expression/regulation | GTEx, PanglaoDB, ENCODE, JASPAR, UniBind |
| Structures | PDB, AlphaFold DB, EMDB, IntAct, ComplexPortal, Human Protein Atlas |
| Omics archives | GEO, ArrayExpress, PRIDE, MGnify, MetaboLights |
| Chemistry | PubChem, ChEBI, BindingDB, Rhea, ZINC, Ketcher (structure editor) |
| Other | CZ CellGuide, Antibody Registry, grants.gov, Rfam |

Custom connectors (Remote HTTPS or Local Command) + **any local/remote MCP** can be added `[DOCS][KEYNOTE]`. Partner connectors named at launch: Benchling, Latch Bio `[KEYNOTE]`.

## 4. Compute management `[DOCS][KEYNOTE]`
- **Local** (laptop / Linux box / HPC login node); **SSH hosts** (auto-reads `~/.ssh/config`, probes CPU/GPU/CUDA/schedulers); **SLURM** clusters (jobs via `sbatch`); **Modal** cloud (per-second billed, e.g. H100/8CPU/32GiB); **NVIDIA BioNeMo NIM** endpoints (hosted or local Docker).
- **Scales one GPU → hundreds**; keynote demoed 2,200 compounds across 80 GPUs, **fault-tolerant** (2 jobs failed, "no matter"), then a **second independent model** filtered survivors (built-in falsification step).
- **Modal limits** `[DOCS]`: 1 GiB input / 5 GiB output per job, 12h default (23h max) container, 10 concurrent default, **no spend ceiling**.
- **Local GPU** requires explicit enable (reduces sandboxing) `[DOCS]`.

## 5. Environment & code execution `[DOCS][INSTALL]`
- Languages: **Python, R, shell**, in **persistent kernels** (variables/dataframes survive across cells until ~30 min idle).
- **Lean base envs, specialized packages per-workspace on demand** `[INSTALL]`: base `python` (3.11: numpy/pandas/scipy/matplotlib/seaborn/sklearn/statsmodels) and `r` (tidyverse) are deliberately light; each workspace gets its own `uv`-managed `.venv` + `.r-libs` so GPU/bio stacks (torch, scanpy, ESMFold…) install without polluting the base. Package sources: conda (micromamba: conda-forge/bioconda/pytorch), pip/PyPI, CRAN/Bioconductor. Can compile from source in-sandbox and preserve builds as artifacts.

## 6. Artifacts, provenance & reproducibility `[DOCS][KEYNOTE][OURS]`
- **Artifact types:** figures, datasets, reports, notebooks, 3D protein structures, genome-browser tracks, chemical structures, MSAs, HTML dashboards, **manuscripts** (Markdown/LaTeX, with `\ref`/`\eqref` resolution).
- **Immutable versioning** — re-saving a filename makes a new version; each version has a 5-tab provenance panel: **Messages, Code, Execution Log (authoritative), Environment (lang+packages), Review (reviewer findings)**. "Reproducible by construction, years later." `[KEYNOTE]`
- **Vision-grounded annotations** `[KEYNOTE][DOCS]`: pin comments directly on a figure/PDF/report/transcript (Claude "sees" the annotation); ≤1,000 chars, no threading; drag-drop pins (v0.1.16).
- Built-in scientific renderers (proteins, alignments, genome tracks, chem structures, PDFs).
- **Local-first storage:** artifacts + history live only in `~/.claude-science` on the device; import/export up to 100 GB.

## 7. Models `[DOCS][KEYNOTE][OURS]`
- Primary agent runs **Claude Opus 4.8** (confirmed in our runs). Reviewer runs a **separate model (we saw Sonnet 5)**. Benchmarked (organic chem / bioinformatics / structural bio) "on par or above average PhD-level" per Anthropic — no numeric scores published.
- **Domain models via skills/BioNeMo:** Evo 2, Boltz-2, OpenFold3, AlphaFold2, ESM-2, etc. (NVIDIA BioNeMo Agent Toolkit).

## 8. Safety / sandbox / permissions `[DOCS][INSTALL][OURS]`
- **OS sandbox (bubblewrap on Linux/WSL)** — code reads/writes only the workspace + granted folders; verified it runs on this VCU-managed machine.
- **Permission "approval cards"** for: folder access (read / read+write), code execution, network hosts, connector tools, remote jobs. **Scopes: Once / This conversation / This project / Global**; all standing grants revocable under Settings › Permissions. (We auto-approved these headlessly.)
- **Network allowlist** of permitted outbound hosts. **Memory** local-only, off by default.
- **Dangerous CLI flags:** `--dangerously-no-sandbox`, `--dangerously-skip-approvals`.
- Data leaving device: only prompt/response API traffic (+ optional telemetry, disableable via `DO_NOT_TRACK`); files/connectors/compute stay local.

## 9. CLI reference `[INSTALL][DOCS]`
`serve · open · url · status · logs · stop · update · import · --version`. Global: `--data-dir`, `--here`, `--config`, `--assets-root`. `serve`: `--port`, `--sandbox-port`, `--no-browser`, `--detached`, `--host`, `--base-path`, `--allow-origin`, `--no-auto-update`, `--verbose` (+ the two dangerous flags). **No CLI for submitting tasks or granting permissions — the web UI is the only interface** (this is why we drive it via Playwright `[OURS]`).

## 10. Access, plans, OS `[DOCS]`
- **Plans:** Pro, Max, Team, Enterprise (Pro/Max self-serve; Team/Ent admin-enabled, off by default). **No free tier.** No API key (uses Claude sign-in). Discounted Team seats for academic/nonprofit labs.
- **OS:** macOS 13+ / Linux x64. **No native Windows — WSL2 + Ubuntu 24.04+ only** (bubblewrap ≥0.8; WSL1 can't sandbox). ~5 GB disk.
- **Grant program:** up to 50 "AI for Science" projects, up to $30k credits each (+ up to $2k Modal compute); applications through 2026-07-15, projects Sep–Dec 2026.

## 11. Admin / enterprise `[DOCS]`
SSO (SAML/OIDC), SCIM, domain capture, custom roles; org enablement (Owner-only); connector categories (Featured/Local/Directory, Directory needs allowlist); usage analytics (`science_metrics`: sessions, messages, delegations, remote-compute jobs, skills used); MDM via `~/.claude-science/config.toml` (`disable_telemetry`, `network_isolated`, `auto_update=false`). **Beta gaps:** no audit log / Compliance API yet; HIPAA usage **not** BAA-covered; partial skill/connector allowlisting; offboarding doesn't wipe local data.

## 12. Seed example projects (bundled demos) `[INSTALL]`
`example_crispr_screen` (kinome CRISPR-KO library design), `example_enzyme_engineering` (recombinase variant scoring via ESMFold/ESM-2/ProteinMPNN), `example_extremophile` (phylogeny + ancestral reconstruction), **`example_immunotherapy`** (scRNA-seq reanalysis of melanoma checkpoint data — closest to this project's T-cell domain).

## 13. Limitations & critiques `[DOCS][3P]`
- Not clinical/diagnostic; verify all results. Reviewer reduces but doesn't eliminate errors (checks claims, doesn't re-run). Residual hallucination ~5–15% reported by hands-on users `[3P]`; real hallucinated references seen on HN. Life-sciences only at launch. Beta HIPAA/audit/spend-ceiling gaps.
- **Rival benchmark `[3P]`:** OpenAI's *GeneBench-Pro* reportedly scored Opus 4.8 ~16% vs GPT-5.6 ~29–31% on scientific-judgment problems (adversarial, single source — cite with caution).
- Hands-on positives `[3P]`: a bioinformatician's 2-hr unattended run **caught its own artifact** (reclassification vs real trend) — echoing this project's UNTESTED thesis; a field-map for ~$26.

## 14. What WE demonstrated first-hand (not in any writeup) `[OURS]`
- **Installed it on Windows via WSL with a paste-only, no-password method** (`wsl -u root` for prereqs) — documented in `INSTALL-claude-science-on-windows.md`.
- **Drove it fully headless via Playwright** (create project → send task → auto-approve cards → poll-to-done → extract artifacts) — since it has no task CLI, this is the only way to script it. Packaged as the `drive-claude-science` skill.
- Confirmed the sandbox runs on a **managed/endpoint-secured corporate laptop**; the **reviewer is a genuinely separate model** (Sonnet 5); ran a real T-cell Perturb-seq referee pipeline end-to-end.

## 15. Sources not yet mined (for completeness)
- **Wednesday 2026-07-08 live session** (Alexander Terashansky's Claude Science overview) + hackathon **Discord** office hours — direct from the team; not yet occurred/captured.
- The **launch keynote video** itself (we have the transcript, not the on-screen UI frames).

---
*Note on the "NEW WORK ONLY" constraint:* Claude Science's data dir (`~/.claude-science/…/workspaces/`) holds our own session scratch from today (incl. a breast-cancer demo detour). That's the workbench's private storage, not the git repo — only the intended deliverables were committed. No pre-event reuse; git history remains the compliance proof.
