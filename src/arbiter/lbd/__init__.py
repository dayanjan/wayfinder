"""LBD question-proposer for the PyZoBot Arbiter.

Literature-based discovery (Swanson ABC) as a QUESTION-GENERATION engine: mine the
literature for the highest-value UNTESTED A(gene)->B(program)->C(disease) triples the
CD4+ T-cell Perturb-seq dataset can resolve, then hand each to the referee to answer.
Build spec: docs/lbd-proposer-spec.md (v2). Process log: docs/lbd-build-log.md.

All code authored during the Built with Claude: Life Sciences hackathon (July 2026),
new-work-only; MIT. Sibling projects informed the *pattern* only -- zero file copy.
"""
