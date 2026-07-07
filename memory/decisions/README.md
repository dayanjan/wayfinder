# Architecture Decision Records — PyZoBot Arbiter

One file per load-bearing decision: `adr-NNN-short-slug.md`. Keep them short —
**Context → Decision → Consequences**. Record the calls that would be expensive to
reverse or that a judge/reviewer would ask "why?" about. Index them in `MEMORY.md`.

Candidates worth an ADR as the build unfolds:
- Voyage (not OpenAI) for embeddings — the provider firewall.
- Data lookups as deterministic tools, not agents — where agency is spent.
- Knockdown-QC gate as a hero feature (untested vs. negative).
- Verdict UX + calibrated-language contract.
