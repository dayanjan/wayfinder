# Codex-2 (clean-room re-implementation) — extracted results

Codex-2 wrote a from-scratch classifier importing **none** of our `arbiter.lbd` modules and ran it
directly over the raw CSVs. Absolute counts are larger than our 43 because it ran over ALL A × diseases
without our literature/OpenTargets pre-gate (the task permitted this) — so what reproduces is the
**A-universe size, the NAB2 result, and the clean/weak/flagged proportions**, not the gated absolute total.

Key results extracted from its run:

```
A universe: {'A_intersection': 3935, 'NAB2_in_A': True}         # matches our 3,935 exactly
Eligible diseases (umbrella + negative-controls removed): 12    # matches our load_c()
NAB2_atopic_classifier: supported                               # clean full-chain, matches
NAB2 supported diseases: [('asthma','supported'), ('atopic eczema','supported')]   # matches C3
chain classes over A × diseases:  supported_total 411; clean 312 / weak 87 / flagged 12
supported proportions: {supported: 0.759, supported_weak: 0.212, supported_flagged: 0.029}
```

Our gated funnel proportion (30 clean / 43 disease-C-supported ≈ 0.70 clean) is consistent with
Codex-2's un-gated 0.76 clean. **Verdict: PASS** — the A universe, the NAB2 clean-supported result,
and the chain-class proportions reproduce under an independent clean-room re-implementation. Codex-2
also independently derived the correct 12-eligible-disease set (excluding the 2 umbrella terms AND the
3 negative-control diseases). Full run log: `.claude/scratch/lbd-debate/codex_replicate_2_reimpl.log`.
