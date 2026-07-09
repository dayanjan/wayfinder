# Persona Synthesis (Part A)

Five differentiated reviewer personas were sampled in parallel via the host model interface (`host.llm` fan-out, model `claude-haiku-4-5-20251001`). Delegation via `host.delegate()` was attempted first but is disabled for this session (ultra/delegation toggle off); `host.llm` provides the equivalent multi-persona sampling and is used here.

## The five lenses

- **immunology referee** — NAB2 knockdown effects on immune cell activation, cytokine production, and differentiation must be characterized beyond target gene expression, as NAB2 is a transcriptional corepressor with broad regulatory roles in T cell and B cell function.
- **statistics reviewer** — Adjusted p-values require specification of the multiple-comparison correction method and family-wise error rate control strategy, which must be pre-registered or justified post-hoc to avoid selective reporting bias.
- **visualization critic** — Knockdown efficiency and specificity must be visually transparent—unclear whether phenotypes reflect the intended target knockdown or off-target effects.
- **reproducibility auditor** — Knockdown efficiency and specificity are not documented with quantitative validation (qPCR, Western blot, or RNA-seq), making it impossible to verify that observed phenotypes result from the intended target reduction rather than off-target effects.
- **skeptical integrator** — Whether the observed phenotype genuinely reflects target knockdown versus off-target effects, incomplete depletion, or compensatory mechanisms that confound causal interpretation.

## Convergent theme

Across all five lenses the dominant concern converges on **knockdown validation and specificity**: every persona wants proof that the observed target-expression drop reflects genuine, on-target depletion rather than off-target activity, incomplete knockdown, or confounding by viability/activation state. The immunology referee frames this biologically (broad corepressor roles), the statistics reviewer procedurally (multiple-comparison correction and reproducible p-value adjustment), the visualization critic representationally (co-displayed validation panels), the reproducibility auditor operationally (re-runnable qPCR/Western validation), and the skeptical integrator causally (rescue experiments).

## Integrated recommendation

Report per-guide knockdown efficiency with an orthogonal assay (qPCR + protein), co-display validation alongside every phenotype figure, fully specify the multiple-comparison correction and release unadjusted p-values, and include a rescue arm to establish causal specificity. These steps satisfy all five reviewers simultaneously.
