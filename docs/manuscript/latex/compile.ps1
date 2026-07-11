# Wayfinder manuscript — compile (LightsOut LaTeX approach, journal-adapted)
#   .\compile.ps1            # regenerate sections from markdown, then latexmk -> main.pdf
#   .\compile.ps1 -NoBuild   # compile only (don't re-run build_tex.py)
#   .\compile.ps1 -Docx      # also emit main.docx via pandoc (needs a Frontiers CSL for final)
#   .\compile.ps1 -Clean     # remove aux + pdf
param([switch]$NoBuild, [switch]$Docx, [switch]$Clean)

$dir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $dir
$env:PATH = "$env:LOCALAPPDATA\Programs\MiKTeX\miktex\bin\x64;$env:PATH"

if ($Clean) { latexmk -C main.tex; Remove-Item -Force main.pdf,main.docx -ErrorAction SilentlyContinue; exit }

if (-not $NoBuild) {
    Write-Host "Regenerating sections from markdown (build_tex.py)..." -ForegroundColor Cyan
    python build_tex.py
}

Write-Host "Compiling main.tex -> main.pdf (latexmk)..." -ForegroundColor Cyan
latexmk -pdf -interaction=nonstopmode main.tex
$pages = (Select-String -Path main.log -Pattern 'Output written on main.pdf \((\d+) pages?').Matches.Groups[1].Value
Write-Host "  main.pdf: $pages pages" -ForegroundColor Green
latexmk -c main.tex   # tidy aux, keep pdf

if ($Docx) {
    # NOTE: swap the CSL for a Frontiers author-year style before submission.
    Write-Host "Emitting main.docx (pandoc)..." -ForegroundColor Cyan
    pandoc main.tex --bibliography ../../../references/references.bib --citeproc -o main.docx
    Write-Host "  main.docx written (draft styling; apply Frontiers template for submission)" -ForegroundColor Green
}
