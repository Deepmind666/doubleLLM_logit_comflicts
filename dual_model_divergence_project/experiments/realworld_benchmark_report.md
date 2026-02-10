# Realworld Benchmark Report

- Timestamp: `2026-02-10T10:50:55+08:00`
- Cases passed: `10/10` (100.0%)
- Checks passed: `48/48` (100.0%)

## Layer Metrics

- L1 pass: `10/10` (100.0%)
- L2 pass: `10/10` (100.0%)
- L3 pass: `10/10` (100.0%)

## Conflict Detection Error Analysis

- TP: `9`
- FP: `0`
- FN: `0`
- Precision: `100.0%`
- Recall: `100.0%`
- F1: `100.0%`

## Tier Breakdown

| tier_group | cases | case_pass_rate | L1_pass | L2_pass | L3_pass |
|---|---|---|---|---|---|
| L1 | 4 | 100.0% | 100.0% | 100.0% | 100.0% |
| L2 | 3 | 100.0% | 100.0% | 100.0% | 100.0% |
| L3 | 1 | 100.0% | 100.0% | 100.0% | 100.0% |
| NONE | 2 | 100.0% | 100.0% | 100.0% | 100.0% |

## Case Details

| case_id | source_ref | tier_group | result | failed_checks |
|---|---|---|---|---|
| rw_l1_autodesk_choose_a | US12353469B1 | L1 | PASS | - |
| rw_l1_bitvore_choose_b | US20250077777A1 | L1 | PASS | - |
| rw_l2_intuit_choose_a | WO2024254203A2 | L2 | PASS | - |
| rw_l2_single_source_remain_unknown | CN119493841A | L2 | PASS | - |
| rw_l3_keep_multi_solution | community_case | L3 | PASS | - |
| rw_cn_l1_huawei_natural_phrase | CN_sample_huawei | L1 | PASS | - |
| rw_cn_l1_zte_submission_phrase | CN_sample_zte | L1 | PASS | - |
| rw_cn_l2_baidu_publication_phrase | CN_sample_baidu | L2 | PASS | - |
| rw_none_no_conflict_control | US20250200392A1 | NONE | PASS | - |
| rw_none_generic_year_conflict | timeline_summary | NONE | PASS | - |

## Layered Findings

- Layer-1 (conflict detection) failures: `0` -> `[]`
- Layer-2 (evidence adjudication) failures: `0` -> `[]`
- Layer-3 (fusion output) failures: `0` -> `[]`
