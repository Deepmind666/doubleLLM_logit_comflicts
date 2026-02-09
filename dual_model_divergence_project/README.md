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
python -m unittest tests.test_stage2_cases_unittest -v
```

Or run bundled test runner:

```bash
cd dual_model_divergence_project
python run_test_cases.py
```

If `pytest` is installed, you can also run:

```bash
pytest -q
```

## Environment Variables (for real API mode)

- `OPENAI_API_KEY`
- `ANTHROPIC_API_KEY`
- Optional:
  - `OPENAI_MODEL`
  - `ANTHROPIC_MODEL`
  - `EVIDENCE_CATALOG_PATH` (override evidence catalog path)

Fallback to mock responses is disabled by default unless `--allow-mock-fallback` is set.
