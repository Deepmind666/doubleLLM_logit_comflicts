# Realworld Benchmark Report

- Timestamp: `2026-02-10T00:55:55+08:00`
- Cases passed: `7/7` (100.0%)
- Checks passed: `33/33` (100.0%)

## Layer Metrics

- L1 pass: `7/7` (100.0%)
- L2 pass: `7/7` (100.0%)
- L3 pass: `7/7` (100.0%)

## Conflict Detection Error Analysis

- TP: `6`
- FP: `0`
- FN: `0`
- Precision: `100.0%`
- Recall: `100.0%`
- F1: `100.0%`

## Tier Breakdown

| tier_group | cases | case_pass_rate | L1_pass | L2_pass | L3_pass |
|---|---|---|---|---|---|
| L1 | 2 | 100.0% | 100.0% | 100.0% | 100.0% |
| L2 | 2 | 100.0% | 100.0% | 100.0% | 100.0% |
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
| rw_none_no_conflict_control | US20250200392A1 | NONE | PASS | - |
| rw_none_generic_year_conflict | timeline_summary | NONE | PASS | - |

## Layered Findings

- Layer-1 (conflict detection) failures: `0` -> `[]`
- Layer-2 (evidence adjudication) failures: `0` -> `[]`
- Layer-3 (fusion output) failures: `0` -> `[]`
