import pathlib
p = pathlib.Path("docs/lbd_finding_nab2_2026-07-08.md")
t = p.read_text(encoding="utf-8")

section = """
## Source-paper cross-check (independent read of the original paper)
An independent read of the dataset's own paper (`docs/source_paper_read_eczema_2026-07-08.md`;
bioRxiv 2025.12.23.696273) sharpened the finding's honesty:
- **Novelty confirmed.** The paper **never mentions NAB2** — its own top Th2 regulators are IL4R,
  STAT6, GATA3, RARA, FBXO32. NAB2→Th1/Th2→eczema is entirely our finding, not a paper claim.
- **Disease-label provenance (new caveat).** The disease enrichment tags a gene to "atopic eczema"
  via **Open Targets *genetic* evidence (GWAS + gene-burden + ClinVar, score ≥0.1), NOT co-expression**,
  and the paper runs **no colocalization / LD control**. So NAB2's atopic-eczema *label* is
  GWAS-locus-based and could in principle be LD-inherited from the STAT6 12q13 atopy locus.
- **Sharpest concern = a CRISPRi cis artifact**, and we tested it: a guide targeting NAB2 (1.9 kb from
  STAT6) could cis-repress STAT6. Evidence **against** the artifact (`docs/nab2_cis_artifact_check.py`):
  (i) NAB2 and STAT6 share **zero** perturbation-effect clusters → NAB2-KD does **not** phenocopy
  STAT6-KD; (ii) NAB2 clears the paper's own reproducibility bar (**cross-guide R 0.74, cross-donor R
  0.74**) and is *more* reproducible than STAT6 itself (0.51); (iii) on-target, no off-target flag.
  **Definitive test not possible from our 4 tables:** does NAB2-KD lower STAT6 mRNA? — needs the
  deposited per-perturbation×gene DE matrix (authors' repo, `github.com/emdann/GWT_perturbseq_analysis_2025`).
- **Framing = nomination, not causation** (matching the paper, which calls all module→disease
  enrichment "guilt-by-perturbational association … can nominate").
- **Citation fix:** the CSV's contrast label "Hollbacker 2021" is really **Höllbacher et al. 2020**
  (ImmunoHorizons); "Ota 2021" (Cell) is correct.

**Net honest verdict after the paper read:** a *novel, reproducible* NAB2→Th1/Th2 functional
**nomination**; the →atopic-eczema disease link is **flagged** — the STAT6 genomic/cis shadow is
argued-against (non-phenocopy + reproducibility) but **not fully excluded** (the GWAS-locus disease
label + the missing direct STAT6-mRNA readout). This more-conservative verdict is on-thesis: a
confident, receipt-backed, caveat-aware call, not an overclaimed discovery.
"""

anchor = "## The cull is real (honesty examples from the same run)"
assert anchor in t, "anchor not found"
t = t.replace(anchor, section.strip() + "\n\n" + anchor, 1)
p.write_text(t, encoding="utf-8")
print("finding writeup: source-paper cross-check section added")
