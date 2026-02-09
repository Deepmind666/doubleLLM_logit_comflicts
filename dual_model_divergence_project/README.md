# Dual Model Divergence Project (Scaffold)

This is a stage-1 runnable scaffold for:

1. Calling two models (or mock providers)
2. Detecting divergence between answers
3. Structuring divergence data
4. Optional evidence hook
5. Generating fused output
6. Persisting all steps to SQLite

## Quick Start

```bash
cd dual_model_divergence_project
python -m venv .venv
.venv\\Scripts\\activate
pip install -r requirements.txt
python main.py "太阳系中最大的行星是哪一颗？" --mock --enable-evidence
```

## Run Tests

```bash
cd dual_model_divergence_project
pytest -q
```

## Environment Variables (for real API mode)

- `OPENAI_API_KEY`
- `ANTHROPIC_API_KEY`
- Optional:
  - `OPENAI_MODEL`
  - `ANTHROPIC_MODEL`

If API calls fail, the scaffold safely falls back to mock responses.

