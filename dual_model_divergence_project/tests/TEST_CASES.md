# Stage-2 Test Cases

## Case 1: L1 evidence can auto-adjudicate

- Command:
```bash
python main.py "X技术专利申请年份是多少？" --mock --enable-evidence --no-cache
```
- Expected:
1. Output includes `year_conflict_X技术`.
2. Output includes `采用模型B结论`.
3. Database `evidence` row has `verdict=B`, `source_tier=L1`, `auto_applied=1`.

## Case 2: L3-only evidence must not auto-adjudicate

- Command:
```bash
python -m unittest tests.test_stage2_cases_unittest.Stage2SecurityAndEvidenceTests.test_l3_only_should_not_auto_apply -v
```
- Expected:
1. Test passes.
2. Verdict remains `unknown`.
3. `auto_applied=False`.

## Case 3: API failure must not silently fallback (strict mode)

- Command:
```bash
python -m unittest tests.test_stage2_cases_unittest.Stage2SecurityAndEvidenceTests.test_api_failure_without_fallback_raises -v
```
- Expected:
1. Test passes.
2. `RuntimeError` is raised when API call fails and fallback is not allowed.

## Case 4: Full stage-2 regression

- Command:
```bash
python -m unittest tests.test_stage2_cases_unittest -v
```
- Expected:
1. All tests pass.
2. No DB file lock errors on Windows cleanup.

