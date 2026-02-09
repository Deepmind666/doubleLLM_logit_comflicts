import os
import time
from typing import Dict

try:
    from dotenv import load_dotenv
except Exception:  # pragma: no cover - optional dependency fallback
    def load_dotenv():
        return None

from .database import DatabaseManager


def _mock_answer(model_name: str, question: str) -> str:
    ql = question.lower()
    if ("太阳系" in question and "最大" in question) or ("planet" in ql and "largest" in ql):
        if model_name == "GPT":
            return "太阳系中最大的行星是木星。"
        return "太阳系最大的行星是木星，土星的体积也很大。"
    if ("专利" in question and "年份" in question) or ("patent" in ql and "year" in ql):
        if model_name == "GPT":
            return "X技术专利申请于2020年。"
        return "X技术专利申请于2018年。"
    return f"{model_name} mock: 示例回答。"


def _call_openai(question: str) -> str:
    from openai import OpenAI

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    resp = client.responses.create(
        model=os.getenv("OPENAI_MODEL", "gpt-4.1-mini"),
        input=question,
        timeout=30,
    )
    return (resp.output_text or "").strip()


def _call_anthropic(question: str) -> str:
    import anthropic

    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    msg = client.messages.create(
        model=os.getenv("ANTHROPIC_MODEL", "claude-3-5-sonnet-latest"),
        max_tokens=700,
        messages=[{"role": "user", "content": question}],
        timeout=30,
    )
    parts = []
    for block in msg.content:
        txt = getattr(block, "text", "")
        if txt:
            parts.append(txt)
    return "\n".join(parts).strip()


def _retry_call(call_fn, retries: int = 2):
    last_error = None
    for attempt in range(retries + 1):
        try:
            return call_fn()
        except Exception as e:
            last_error = e
            if attempt < retries:
                time.sleep(0.5 * (2**attempt))
    raise last_error  # type: ignore[misc]


def get_answers(
    question: str,
    db: DatabaseManager,
    query_id: int,
    use_cache: bool = True,
    mock_mode: bool = False,
    allow_mock_fallback: bool = False,
) -> Dict[str, str]:
    load_dotenv()
    result: Dict[str, str] = {}
    cache_mode = "mock" if mock_mode else "live"

    for model_name in ["GPT", "Claude"]:
        cached = (
            db.get_cached_response(question, model_name, response_mode=cache_mode)
            if use_cache
            else None
        )
        if cached:
            result[model_name] = cached
            continue

        answer_mode = cache_mode
        if mock_mode:
            answer = _mock_answer(model_name, question)
        else:
            try:
                if model_name == "GPT":
                    answer = _retry_call(lambda: _call_openai(question))
                else:
                    answer = _retry_call(lambda: _call_anthropic(question))
                if not answer:
                    raise RuntimeError(f"{model_name} returned empty response.")
            except Exception as e:
                if allow_mock_fallback:
                    answer = _mock_answer(model_name, question)
                    answer_mode = "fallback_mock"
                else:
                    raise RuntimeError(
                        f"{model_name} API call failed; set --allow-mock-fallback to continue in degraded mode."
                    ) from e

        db.save_response(
            query_id=query_id,
            model_name=model_name,
            response_text=answer,
            usage_info=f"mode={answer_mode}",
        )
        result[model_name] = answer

    return result
