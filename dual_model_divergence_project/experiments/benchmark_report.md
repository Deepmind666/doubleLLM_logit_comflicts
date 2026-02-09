# Benchmark Report

- Timestamp: `2026-02-10T00:38:21+08:00`
- Cases passed: `6/6` (100.0%)
- Checks passed: `17/17` (100.0%)
- Conflict detection checks: `3/3` (100.0%)
- Verdict checks: `4/4` (100.0%)
- Auto-apply checks: `4/4` (100.0%)

## Case Summary

| case_id | kind | pass | failed_checks |
|---|---|---|---|
| pipeline_planet_no_conflict | pipeline | PASS | - |
| pipeline_patent_l1_adjudication | pipeline | PASS | - |
| pipeline_patent_without_evidence | pipeline | PASS | - |
| evidence_l2_dual_source_auto_apply_a | evidence_only | PASS | - |
| evidence_l3_should_remain_unknown | evidence_only | PASS | - |
| evidence_unsupported_type_unknown | evidence_only | PASS | - |

## Check Details

### pipeline_planet_no_conflict
- Kind: `pipeline`
- Result: `PASS`
- [x] `conflict_count` conflict_count expected=0, actual=0
- [x] `final_contains` final contains '融合答案'
- [x] `final_contains` final contains '木星'

### pipeline_patent_l1_adjudication
- Kind: `pipeline`
- Result: `PASS`
- [x] `conflict_count` conflict_count expected=1, actual=1
- [x] `verdict` year_conflict_X技术 verdict expected=B, actual=B
- [x] `auto_applied` year_conflict_X技术 auto_applied expected=True, actual=True
- [x] `final_contains` final contains 'year_conflict_X技术'
- [x] `final_contains` final contains '采用模型B结论'

### pipeline_patent_without_evidence
- Kind: `pipeline`
- Result: `PASS`
- [x] `conflict_count` conflict_count expected=1, actual=1
- [x] `final_contains` final contains 'year_conflict_X技术'
- [x] `final_contains` final contains '暂无充分证据'

### evidence_l2_dual_source_auto_apply_a
- Kind: `evidence_only`
- Result: `PASS`
- [x] `verdict` year_conflict_ExampleTech verdict expected=A, actual=A
- [x] `auto_applied` year_conflict_ExampleTech auto_applied expected=True, actual=True

### evidence_l3_should_remain_unknown
- Kind: `evidence_only`
- Result: `PASS`
- [x] `verdict` year_conflict_CommunityCase verdict expected=unknown, actual=unknown
- [x] `auto_applied` year_conflict_CommunityCase auto_applied expected=False, actual=False

### evidence_unsupported_type_unknown
- Kind: `evidence_only`
- Result: `PASS`
- [x] `verdict` logic_conflict_X verdict expected=unknown, actual=unknown
- [x] `auto_applied` logic_conflict_X auto_applied expected=False, actual=False
