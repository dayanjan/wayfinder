# Gotchas — PyZoBot Arbiter

Append-only running list of traps, surprises, and non-obvious fixes. `session-closer`
appends here at close; check it before debugging something that "should just work."

---
<!-- gotchas appended below, newest last, each with: Added: YYYY-MM-DD -->

## `freshen` references `ATOMIC_PLAN.md`, but this project uses `docs/plan.md`
**Added: 2026-07-07.** The `freshen` skill was copied from the generator and still names
`ATOMIC_PLAN.md` / `workstreams/` as task-state sources. This project has neither — it uses
`docs/plan.md` (plan of record) and `docs/plans/*_atomic.md` (from `atomic-planner`). Those
checks are guarded by "(if present)" so `freshen` degrades gracefully and still validates
`MEMORY.md`/`WORK_PROGRESS.md`. Not a bug; just don't expect the ATOMIC_PLAN checks to fire.

## Check an Anthropic key's validity without spending tokens
**Added: 2026-07-07.** `GET https://api.anthropic.com/v1/models` (with `x-api-key` +
`anthropic-version: 2023-06-01`) returns 200 + the model catalog and consumes zero tokens —
use it as the auth check. A key can list models yet still be blocked on inference, so also
fire one minimal `POST /v1/messages` (`max_tokens:5`) to confirm end-to-end before trusting it.

### Reading one cell of a huge deposited h5ad without downloading it — Added: 2026-07-08
The authors' genome-wide DE (`GWCD4i.DE_stats.h5ad`) is 16.8 GB on a public no-creds S3 bucket
(`s3://genome-scale-tcell-perturb-seq/marson2025_data/`). To read a single (perturbation, gene) value
(e.g. STAT6 under NAB2-KD) do NOT download it: `s3fs.S3FileSystem(anon=True).open(url)` → `h5py.File(fo)`
reads only the chunks needed (obs categoricals, var names, one matrix slice) via range requests. anndata
is NOT required (and its pin conflicts with typing_extensions here) — raw h5py suffices. See
`docs/nab2_stat6_definitive_check.py`. Raw single-cell matrices (`D*_*.assigned_guide.h5ad`, ~140 GB each)
are the off-limits big data; the DE results are the CPU-feasible slice.

### `offtarget_flag` in DE_stats already encodes a cis-neighbor check — Added: 2026-07-08
The DE_stats `offtarget_flag` = "a gene with TSS within 10 kb of the guide is significantly down-regulated."
So a False flag on a perturbation already means no 10 kb neighbor is cis-repressed — a cheap partial answer
to any "did the guide hit a neighbor?" (e.g. NAB2 guide vs STAT6 1.9 kb away) before pulling the full DE.

## Claude Science operational gotchas — Added: 2026-07-09
- **`host.delegate` is gated** behind a session Delegation ("ultra mode") toggle — OFF by default and NOT
  reachable via the headless driver. Programmatic sub-agent fan-out fails with "delegation is not enabled";
  use `host.llm_batch` (inline Haiku-4.5 sampling) instead. Real host API: `mcp`/`llm_batch`/`query_db`/
  `delegate`/`agent_list`/`list_artifacts`/`artifact_path`/`artifacts`. (`host.capabilities()` is NOT real.)
- **The driver's "DONE" ≠ receipts landed.** CS's Sonnet-5 Reviewer commits `verification_checks` and the
  `extracted_code` provenance block backfills only on FRAME COMPLETION — headless runs may leave the OPERON
  frame "processing" for 10+ min. Poll `operon-cli.db` after DONE; save receipts from the kernel, don't rely
  on DB backfill.
- **CS base env is lean** — `s3fs`/`h5py` (and other bio stacks) may need install into the workspace env;
  distinguish "missing package → install" from "S3/network blocked" when a data-access step fails.
- **LBD in CS = kernel HTTP, not connectors.** Europe PMC `hitCount` (GET) + Open Targets GraphQL (POST) are
  plain HTTP in `sources.py`; CS's `_mcp-*` connectors don't expose those exact scalars. Port `sources.py`/
  `_http.py` into the kernel with a workspace SHA1 cache (a fresh `--new` project resets the workspace → copy
  `lbd_cache/` in before replay).

## Claude Science full-pipeline-native gotchas — Added: 2026-07-09
- **Anon S3 in CS needs VIRTUAL addressing.** `s3fs.S3FileSystem(anon=True)` works headless for the public
  bucket, BUT path-style `s3.amazonaws.com` is proxy-denylisted (403). CS self-heals by switching to the
  bucket-qualified host `genome-scale-tcell-perturb-seq.s3.amazonaws.com` (virtual addressing); the driver
  auto-approves the network-domain card. So the 16.8 GB `GWCD4i.DE_stats.h5ad` opens + lazy-reads in-CS with
  NO download — the S3 cis-check runs natively (no external fallback). Proven Stage 0 + Stage 3 (2026-07-09).
- **A CS run's workspace dir == the OPERON frame id**, at
  `~/.claude-science/orgs/<org>/workspaces/<OPERON_FRAME>/`. Get the OPERON frame from `frames` WHERE
  project_id + agent_name='OPERON'. NOTE: `find` sometimes cannot traverse the workspace (overlay/perms);
  a DIRECT `wsl -d Ubuntu --cd "~" -- cat /abs/path/...` reads it fine.
- **Git-Bash → WSL nested-quote mangling (recurring, wastes runs).** A multi-line `wsl -- bash -c '...'`
  carrying `$VAR=` assignments, `$(...)` subshells, or heredocs silently yields EMPTY variables (symptom:
  `mkdir: cannot create directory '/src'` = `$DST` empty; or literal quotes in error paths). FIXES: (a) put
  the script in a FILE and run `MSYS_NO_PATHCONV=1 wsl -d Ubuntu --cd "~" -- bash /mnt/c/.../script.sh`;
  (b) for one-offs use a single direct command with NO shell vars (`wsl --cd "~" -- cat /abs/path`);
  (c) always `MSYS_NO_PATHCONV=1` when a `/mnt/c/...` arg is present (else Git-Bash prepends its install root).
- **CS `verification_checks` surface only when a review is EXPLICITLY requested AND the OPERON frame
  completes.** Stage 5 (which asked for a review) populated 4 rows; Stage 0/1/3 were async-empty at capture
  even though a REVIEWER frame ran — the driver-tail "Reviewer · No issues found" is the corroboration. To
  guarantee captured findings, end the prompt with an explicit "request a review of <file>" and poll the DB
  after "DONE".

## Codex + live network/API key, CS port drift, referee polarity — Added: 2026-07-09 (PM)
- **Codex CAN do live network + a scoped API key.** `codex exec -s workspace-write -c
  sandbox_workspace_write.network_access=true` with the key exported to env (`export NCBI_API_KEY=$(grep ...)`;
  fallback: tell Codex to read the ONE `NCBI_API_KEY` line in `.env`). Verified hitting NCBI E-utilities + GEO
  FTP live. This enables **live-verified codex-debates** (Codex checks each dataset's existence/groups/probe/
  matrix against real GEO during the debate) — §22 extended from "verify claims against the repo" to "against
  reality." Windows needs `[windows] sandbox="unelevated"` in `~/.codex/config.toml` for workspace-write.
- **CS daemon restart moves the port.** `claude-science stop && serve` picked **8000** (old 8765 pid was stale).
  The `cs-drive.js` driver re-auths via nonce on the new origin — just pass the new `claude-science url` nonce +
  `--url http://localhost:8000/`. Get the running port from `claude-science status` (JSON).
- **Killing the cs-drive.js driver does NOT stop the CS kernel** — the in-kernel sweep loop runs autonomously
  (no driver needed once the cell is executing). A fresh-context Stop-button click missed it. Reliable halt =
  `claude-science stop && serve` (the on-disk cache under a non-workspace path persists → resumable).
- **Referee Th1/Th2 direction label was INVERTED** (`log_fc>0` mislabeled "Th1-associated"). Validate signature
  polarity against canonical markers (GATA3/IL4/IL13 are +, TBX21/IFNG are − in the T2 signature ⇒ +log_fc=Th2),
  NOT against a coded convention. Verdicts were unaffected (HOP-2 status keys on significance, not direction).

## CS conversation UI opens at the bottom + mouse-wheel doesn't scroll the transcript — Added: 2026-07-09
Driving Claude Science conversation frames via Playwright: the frame loads scrolled to the LATEST message
(bottom), and `page.mouse.wheel(0, N)` does NOT scroll the transcript (CS scrolls an inner element, not the
window). Consequence for screen-capture: money shots earlier in a conversation (or inside artifacts) aren't
reachable by naive wheel. Fix: open the receipt ARTIFACT (thumbnail card, not inline text — `getByText`
matches inline code too) for a clean receipt view, or use a prepared static overlay. Verified opening all 4
PyZoBot CS conversations 2026-07-09. See `docs/demo-video-pack/cs/CAPTURE_PLAN.md`.

## demo-video harness supports STORAGE_STATE for pre-authed sessions — Added: 2026-07-09
`~/.claude/skills/demo-video/lib/record.mjs` injects `config.STORAGE_STATE` as the Playwright context
`storageState` (paired with `actor.user=""` to skip the Authentik login). So the harness can drive ANY
saved-session app (e.g. Claude Science via `cs_state.json`) through the normal pipeline — no separate
capture+manual-assembly path needed. This is what makes a fully CS-native demo video run through one pipeline.

## codex 0.141 exec: debate round via --output-schema + stdin works; review flags changed (not exec) — Added: 2026-07-09
Ran a 2-round codex-debate on codex-cli 0.141.0. `codex exec --ephemeral -s read-only --skip-git-repo-check
--output-schema <schema.json> --color never - < prompt.txt` works and returns schema-conforming JSON as the
final message (interleaved with narration; extract the last valid JSON object). The 0.141 flag tightening
(per doctrine §13.5) is on `codex review`, NOT `codex exec` — exec's schema+stdin path is unchanged.

## Codex/gpt-5.5 confabulates on large inline multi-part artifacts (Added: 2026-07-11)
When a codex-debate prompt inlines a large multi-part artifact (the 9k-word full manuscript; a dossier +
plan + re-inlined dossier), gpt-5.5 pattern-matches a generic prior and FABRICATES findings — quoting text
that does not exist (a grant number, "new discoveries wait", "genetic-association score"). **Always verify
every Codex quote against the actual file (grep) before acting.** Fix: (1) inline ONE focused artifact,
(2) require "verbatim-quote-or-drop", (3) reference big context by PATH (repo-read) not inline, (4) upgrade
to **gpt-5.6-sol** (codex ≥0.144.1) — it stayed grounded + file-cited where gpt-5.5 confabulated.

## pandoc markdown→LaTeX preamble fixes (Added: 2026-07-11)
`docs/manuscript/latex/main.tex` needs, for pandoc-generated fragments to compile: `\usepackage{amsmath}`
(display equations); `\usepackage{calc}` (pandoc longtable `\real{}` column widths); `\newcounter{none}` +
`\providecommand{\theHnone}` (caption-less longtable + hyperref reference a counter literally named `none`);
`\DeclareUnicodeCharacter{03C9}{...}` + `{2014}` (omega/em-dash from bib titles). `build_tex.py` maps all
other unicode → LaTeX and stars the sectioning. A fenced ``` block becomes `verbatim` (no wrap, no math) →
convert display equations to `equation*` manually or they bleed into the margin + show literal `$...$`.

## PDF visual inspection: use PyMuPDF, not pdftoppm (Added: 2026-07-11)
The Read tool renders PDF pages via poppler `pdftoppm`, which is NOT installed. Workaround: PyMuPDF (`fitz`)
is installed — `doc[p].get_pixmap(dpi=110).save('p.png')` then Read the PNG. Used to catch the equation
margin-bleed + colored headings.

## gpt-5.6-sol requires codex CLI ≥0.144 (Added: 2026-07-11)
On a ChatGPT-account, plain `gpt-5.6`/`gpt-5.6-codex`/`sol` are "not supported"; only **`gpt-5.6-sol`** is —
but codex 0.141 errors "requires a newer version". `codex update` (npm-global) → 0.144.1 fixes it. Set
`model = "gpt-5.6-sol"` in `~/.codex/config.toml`.

## `_http.py` fetches LIVE on a cache miss — no raise-on-miss guard (Added: 2026-07-11)
`src/arbiter/lbd/_http.py:cached_request` returns cached JSON on a hit but on a MISS sleeps 0.34s,
does `requests.request(...)`, and writes the response to `data/lbd_cache/`. There is **no pure-replay
guard in this layer** — the guard the Claude Science full-sweep used was EXTERNAL to the code. So any
`sources.cooccur_count` / `opentargets_*` / `propose.sweep()` with uncached inputs silently hits the
network (and needs the APIs live). For a DETERMINISTIC OFFLINE analysis, either keep every input
cache-complete, or MEASURE cache growth — count `data/lbd_cache/*.json` before/after and report it.
`docs/manuscript/analysis/gate_grid.py` does the latter (it added 39 live `ac_lit` lookups → now cached →
re-run is 0-growth); `hard_negatives.py` + `sensitivity_panel.py` touch no literature and are cache-free.

## Claude Science driver: port 8000 vs default 8765 (Added: 2026-07-12)
The running CS daemon is on **port 8000** (`claude-science status` → `"port": 8000`), but `drive-claude-science`'s
`cs-drive.js` + SKILL.md default to **8765**. Symptom (the 2026-07-11 "fragile"): driver can't reach CS / nonce
grep misses. Fix: pass `--url http://localhost:8000/` and mint the nonce on :8000 (`claude-science url` | grep
`localhost:8000`). Health-check PASSED with the override 2026-07-12.

## codex `exec --output-schema` logs contain many draft JSON objects (Added: 2026-07-12)
The reasoning trace emits multiple schema-shaped JSON drafts; the echoed prior-round JSON (from the prompt) can be
the LARGEST. Extract the **last** object with the expected `round_number`, not the largest.
