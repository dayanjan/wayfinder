# Provenance — full-pipeline-in-CS run (2026-07-09), pulled from operon-cli.db

Read-only extract from Claude Science's own audit store. OPERON = the scientist (Opus 4.8); REVIEWER = the critic (Sonnet 5).


## Stage 0 — feasibility probe
`proj_9bbb495de66b`

| frame | agent | model | effort | status | in/out tok | cost |
|---|---|---|---|---|---|---|
| ed86b7f7 | UPLOADS | - | - | completed | None/None | $0.0000 |
| 0c391ac5 | OPERON | claude-opus-4-8 | high | completed | 1007345/13017 | $1.5449 |
| debb79a1 | REVIEWER | claude-sonnet-5 | - | completed | 235837/5191 | $0.3855 |
| 51d12beb | REVIEWER | claude-sonnet-5 | - | completed | 64167/3477 | $0.1229 |

**Run cost: $2.0533**

execution_log: 15 cells, 7 with file writes.

_verification_checks: none captured for this run (reviewer async / not surfaced by root_frame_id)._

## Stage 1 — LBD proposer (full sweep)
`proj_4f40ad0d829b`

| frame | agent | model | effort | status | in/out tok | cost |
|---|---|---|---|---|---|---|
| 2d828d11 | UPLOADS | - | - | completed | None/None | $0.0000 |
| ea4d8563 | OPERON | claude-opus-4-8 | high | completed | 1125733/13566 | $1.2274 |
| 24d6f1cc | REVIEWER | claude-sonnet-5 | - | completed | 38702/4428 | $0.1474 |
| e66823db | REVIEWER | claude-sonnet-5 | - | completed | 220502/13854 | $0.4115 |

**Run cost: $1.7863**

execution_log: 13 cells, 5 with file writes.

_verification_checks: none captured for this run (reviewer async / not surfaced by root_frame_id)._

## Stage 3 — STAT6 cis-check (native S3)
`proj_ea76f1a08006`

| frame | agent | model | effort | status | in/out tok | cost |
|---|---|---|---|---|---|---|
| 3289b3f3 | UPLOADS | - | - | completed | None/None | $0.0000 |
| fb886080 | OPERON | claude-opus-4-8 | high | completed | 690522/8651 | $0.6954 |
| 30b16948 | REVIEWER | claude-sonnet-5 | - | completed | 28813/2291 | $0.0783 |
| da1605bf | REVIEWER | claude-sonnet-5 | - | completed | 30096/2097 | $0.0802 |

**Run cost: $0.8539**

execution_log: 9 cells, 4 with file writes.

_verification_checks: none captured for this run (reviewer async / not surfaced by root_frame_id)._

## Stage 5 — receipt chain + review
`proj_99ccc044f003`

| frame | agent | model | effort | status | in/out tok | cost |
|---|---|---|---|---|---|---|
| d278ccb1 | UPLOADS | - | - | completed | None/None | $0.0000 |
| 4473ddef | OPERON | claude-opus-4-8 | high | completed | 964446/10928 | $0.9360 |
| a04f86db | REVIEWER | claude-sonnet-5 | - | completed | 88011/10480 | $0.2311 |
| f26287dc | REVIEWER | claude-sonnet-5 | - | completed | 344951/12154 | $0.4138 |
| ef3f9200 | REVIEWER | claude-sonnet-5 | - | completed | 183984/2789 | $0.1373 |

**Run cost: $1.7182**

execution_log: 23 cells, 6 with file writes.

**Reviewer verification_checks:**
- [WARN/low] resolved: review.json summary field contains a literal '\u2014' escape-sequence artifact instead of an em dash
- [PASS/None] open: Final overall verdict and 'what ran where' table printed to stdout match chain.json source-of-truth
- [PASS/None] open: All numeric receipts cited in final chat message (funnel counts 3,935→22,039→43→30; NAB2 row ab=66,bc=2184,ac_lit=6,ac_known=0.0376,effect=301; cis-ch
- [PASS/None] open: Reviewer's calibrated-language notes (flagging 'validated' in title and 'definitive' in Stage-3 heading) were both applied via the two edit_file calls
