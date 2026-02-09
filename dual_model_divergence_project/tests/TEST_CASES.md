# Test Cases

## Case 1: Basic flow regression (unittest)

- Command:
```bash
python -m unittest tests.test_basic_flow -v
```
- Expected:
1. Year conflict detection works.
2. Mock pipeline writes query/response/fused records into SQLite.
3. Empty question is rejected with `ValueError`.

## Case 2: Stage-2 evidence gating regression

- Command:
```bash
python -m unittest tests.test_stage2_cases_unittest -v
```
- Expected:
1. L1 evidence can auto-adjudicate.
2. L3-only evidence remains unresolved (`unknown`).
3. API failure raises in strict mode (no silent fallback).
4. Integer year evidence (e.g. `2018`) is handled correctly.
5. Mock/live cache entries are isolated by response mode.

## Case 3: Benchmark experiment

- Command:
```bash
python experiments/run_benchmark.py
```
- Expected:
1. Benchmark cases pass.
2. Report generated at `experiments/benchmark_report.md`.
3. Report includes case-level pass/fail and aggregate metrics.

## Case 4: One-shot full validation

- Command:
```bash
python run_test_cases.py
```
- Expected:
1. Basic flow tests pass.
2. Stage-2 tests pass.
3. Benchmark experiment runs and writes report.
