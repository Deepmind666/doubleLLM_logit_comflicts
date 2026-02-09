# Dual Model Divergence Project (Scaffold)

This is a runnable scaffold for:

1. Calling two models (or mock providers)
2. Detecting divergence between answers
3. Structuring divergence data
4. Tiered evidence adjudication
5. Generating fused output
6. Persisting all steps to SQLite

## Quick Start

```bash
cd dual_model_divergence_project
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python main.py "Which is the largest planet in the solar system?" --mock --enable-evidence
```

Strict mode (default) raises an error on API failure.  
Use degraded fallback explicitly:

```bash
python main.py "your question" --allow-mock-fallback
```

## Run Tests

```bash
cd dual_model_divergence_project
python -m unittest tests.test_basic_flow -v
python -m unittest tests.test_stage2_cases_unittest -v
python -m unittest tests.test_stage3_realworld_benchmark_unittest -v
```

Or run bundled test runner:

```bash
cd dual_model_divergence_project
python run_test_cases.py
```

Run benchmark experiment (generates metrics report):

```bash
cd dual_model_divergence_project
python experiments/run_benchmark.py
python experiments/run_realworld_benchmark.py
```

Output report: `dual_model_divergence_project/experiments/benchmark_report.md`
Output report: `dual_model_divergence_project/experiments/realworld_benchmark_report.md`

## Environment Variables (for real API mode)

- `OPENAI_API_KEY`
- `ANTHROPIC_API_KEY`
- Optional:
  - `OPENAI_MODEL`
  - `ANTHROPIC_MODEL`
  - `EVIDENCE_CATALOG_PATH` (override evidence catalog path)

Fallback to mock responses is disabled by default unless `--allow-mock-fallback` is set.

## Notes on cache behavior

- Cache is mode-aware:
  - `mode=mock` only reused in mock mode
  - `mode=live` only reused in live mode
- Fallback responses are stored as `mode=fallback_mock` for audit and are not reused as live cache.
