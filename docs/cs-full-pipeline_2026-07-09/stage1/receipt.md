# Stage 1 — LBD Proposer Sweep: Receipt Verification

Native port with receipt verification. The real pipeline code (`arbiter.lbd.propose.sweep`) was imported and run **unchanged**, replaying entirely from the staged HTTP receipt cache (`data/lbd_cache/`). No pipeline logic and no statistics were modified. The numbers below were **reproduced / re-derived** by executing that code, not discovered.

**ALL_PASS = True**

## Pure-replay guard

- Cache files before sweep: 4685
- Cache files after sweep:  4685
- Delta: 0 (0 == every sweep response came from cache; the HTTP layer was monkeypatched to raise on any live call)

## Funnel (as produced by the code)

```json
{
  "a_genes": 3935,
  "eligible_pairs": 22039,
  "chain_classes": {
    "refuted_for_c": 21995,
    "supported": 30,
    "supported_weak": 10,
    "supported_flagged": 3,
    "refuted_effect": 1
  },
  "clean_supported": 30,
  "disease_c_supported_total": 43,
  "pure_disjoint_clean": 1
}
```

- ab_gate_value (params): 26

## NAB2 → atopic eczema row (from res['ranked_supported'])

- Rank (1-based): 4
```json
{
  "a_gene": "NAB2",
  "b_program": "Th1_Th2_polarization",
  "c_disease": "atopic eczema",
  "condition": "Stim8hr",
  "ab": 66,
  "bc": 2184,
  "ac_lit": 6,
  "ac_known": 0.0376,
  "effect": 301,
  "pure_disjoint": false,
  "score": -1.137,
  "referee_answer": "supported",
  "referee_overall": "consistent with a validated gene -> program -> disease chain re-derived from the tables"
}
```

## Acceptance checks (expected vs actual)

| check | expected | actual | pass |
|---|---|---|---|
| funnel.a_genes | `3935` | `3935` | ✅ |
| funnel.eligible_pairs | `22039` | `22039` | ✅ |
| funnel.disease_c_supported_total | `43` | `43` | ✅ |
| funnel.clean_supported | `30` | `30` | ✅ |
| funnel.pure_disjoint_clean | `1` | `1` | ✅ |
| funnel.chain_classes | `{'refuted_for_c': 21995, 'supported': 30, 'supported_weak': 10, 'supported_flagged': 3, 'refuted_effect': 1}` | `{'refuted_for_c': 21995, 'supported': 30, 'supported_weak': 10, 'supported_flagged': 3, 'refuted_effect': 1}` | ✅ |
| params.ab_gate_value | `26` | `26` | ✅ |
| pure_replay_cache_delta | `0` | `0` | ✅ |
| NAB2 rank (1-based) | `4` | `4` | ✅ |
| NAB2 ab | `66` | `66` | ✅ |
| NAB2 bc | `2184` | `2184` | ✅ |
| NAB2 ac_lit | `6` | `6` | ✅ |
| NAB2 ac_known | `0.0376` | `0.0376` | ✅ |
| NAB2 effect | `301` | `301` | ✅ |
| NAB2 referee_answer | `supported` | `supported` | ✅ |
| NAB2 score (3dp) | `-1.137` | `-1.137` | ✅ |


**ALL_PASS = True**