# manuscript/latex — LaTeX manuscript (LightsOut approach)

The manuscript is authored in LaTeX, mirroring the `2026-03-05-LightsOut-R01` workflow: a master
`main.tex` with a journal-adapted preamble (helvet, colored section headers, `natbib` numbered-super
citations) that `\input`s one `.tex` per section, compiled with `latexmk` and MiKTeX.

## Layout
```
main.tex            master: preamble + title/abstract frontmatter + \input sections + \bibliography
sections/*.tex      one file per section (1 Intro … 5 Discussion) — the AUTHORITATIVE prose source
build_tex.py        one-time migration: markdown (../sections/*.md) -> sections/*.tex (pandoc + fixups)
compile.ps1         build helper (latexmk -> main.pdf; -Docx for a pandoc DOCX)
```
Bibliography: `../../../references/references.bib` (CrossRef-resolved, live-audited, Zotero-synced).

## Source-of-truth note
`build_tex.py` performed the **one-time** markdown→LaTeX migration (2026-07-11). **Going forward, edit
the `.tex` files directly** — they are the authoritative manuscript source. The markdown in
`../sections/*.md` is retained for its debate/CS-verification lineage (it is what §1–§5 were hardened
against) but is no longer the edit surface. Do NOT re-run `build_tex.py` over hand-edited `.tex` — it
would overwrite them from the (now-frozen) markdown.

## Build
```powershell
.\compile.ps1 -NoBuild        # compile the .tex as-is -> main.pdf (the normal path now)
.\compile.ps1 -Docx -NoBuild  # also emit main.docx (swap in a Frontiers CSL before submission)
.\compile.ps1 -Clean          # remove aux + pdf
```
Or directly: `latexmk -pdf -interaction=nonstopmode main.tex`. Current build: **19 pages**, 0 errors,
4 references resolved.

## Preamble notes (why the fixups exist)
- `\usepackage{calc}` — pandoc longtables use `\real{}` column-width arithmetic.
- `\newcounter{none}` + `\theHnone` — pandoc caption-less longtables + hyperref reference a counter named `none`.
- `\DeclareUnicodeCharacter` for `ω`/em-dash — appear in a bib title; declared so `references.bib` stays pristine unicode (matching Zotero).
- Sections are **starred** (`\section*`) so the manual "4.1b"-style numbers in the titles match the prose's literal cross-references.

## Still to do for Frontiers submission
- Swap `natbib` numbered-super + `unsrtnat` for a **Frontiers author-year** style (and a Frontiers CSL for the DOCX path).
- Add figures (Fig 4 hero chain + §4.1b panel; schematics) via `\includegraphics`.
- Apply the Frontiers article template / Word template at submission.
