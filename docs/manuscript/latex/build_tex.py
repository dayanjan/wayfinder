"""Convert the markdown manuscript sections to LaTeX \\input fragments (LightsOut approach).

For each body section (01..05): drop the leading H1 + draft-note blockquote (everything up to and
including the first '---'), map the manuscript's citation placeholders to raw-LaTeX \\cite spans, then
pandoc the body markdown -> a LaTeX fragment under sections/. The Abstract is handled separately in
main.tex frontmatter. Run:  python docs/manuscript/latex/build_tex.py
"""
from __future__ import annotations
import re, subprocess, sys
from pathlib import Path

LATEX_DIR = Path(__file__).resolve().parent
SECT_MD = LATEX_DIR.parents[0] / "sections"           # docs/manuscript/sections
OUT = LATEX_DIR / "sections"; OUT.mkdir(exist_ok=True)

BODY = ["01_introduction", "02_background", "03_methods", "04_results", "05_discussion"]

# citation placeholder (verbatim in the markdown) -> bib key
CITES = [
    ("[Swanson 1986]", "swanson1986"),
    ("[Henry et al. 2021]", "henry2021"),
    ("[Zhu, Dann, Yan, … Marson 2025]", "zhu2025"),
    ("[doi: 10.1016/j.biopha.2020.110970. Epub 2020 Nov 7. PubMed PMID: 33166763.]", "cheng2021"),
    # a couple of prose-form variants that also appear
    ("[cf. Henry et al. 2021, who forwent statistical\nevaluation on these grounds]", "henry2021"),
    ("[cf. Henry et al. 2021, who forwent statistical evaluation on these grounds]", "henry2021"),
]

def strip_frontmatter(md: str) -> str:
    """Drop everything up to and including the first line that is exactly '---'."""
    lines = md.splitlines()
    for i, ln in enumerate(lines):
        if ln.strip() == "---":
            return "\n".join(lines[i + 1:]).strip() + "\n"
    return md

def map_cites(md: str) -> str:
    for placeholder, key in CITES:
        md = md.replace(placeholder, f"`\\cite{{{key}}}`{{=latex}}")
    return md

def convert(name: str) -> None:
    md = (SECT_MD / f"{name}.md").read_text(encoding="utf-8")
    body = map_cites(strip_frontmatter(md))
    r = subprocess.run(
        ["pandoc", "--from", "markdown+raw_tex", "--to", "latex", "--wrap=preserve"],
        input=body, capture_output=True, text=True, encoding="utf-8")
    if r.returncode != 0:
        print(f"PANDOC FAIL {name}:\n{r.stderr}", file=sys.stderr); sys.exit(1)
    tex = r.stdout
    # unicode -> LaTeX (pdflatex-safe; covers every non-ASCII char the sections use)
    U = {
        "→": r"$\rightarrow$", "≤": r"$\leq$", "≥": r"$\geq$", "≈": r"$\approx$",
        "≡": r"$\equiv$", "×": r"$\times$", "…": r"\ldots{}", "β": r"$\beta$",
        "∈": r"$\in$", "−": "-", "±": r"$\pm$", "·": r"$\cdot$", "—": "---",
        "γ": r"$\gamma$", "ρ": r"$\rho$", "§": r"\S{}", "ö": r'\"{o}',
        "⁺": r"\textsuperscript{+}", "⁻": r"\textsuperscript{-}",
        "⁰": r"\textsuperscript{0}", "¹": r"\textsuperscript{1}", "²": r"\textsuperscript{2}",
        "³": r"\textsuperscript{3}", "⁴": r"\textsuperscript{4}", "⁵": r"\textsuperscript{5}",
        "⁶": r"\textsuperscript{6}",
        "₀": r"\textsubscript{0}", "₁": r"\textsubscript{1}", "₂": r"\textsubscript{2}",
        "₃": r"\textsubscript{3}", "₄": r"\textsubscript{4}",
    }
    for k, v in U.items():
        tex = tex.replace(k, v)
    # unnumbered sectioning (manual "4.1b"-style numbers in titles match the prose cross-refs)
    tex = re.sub(r"\\(sub)*section\{", lambda m: m.group(0)[:-1] + "*{", tex)
    (OUT / f"{name}.tex").write_text(tex, encoding="utf-8")
    print(f"  wrote sections/{name}.tex ({len(tex)} chars)")

if __name__ == "__main__":
    for n in BODY:
        convert(n)
    print("done.")
