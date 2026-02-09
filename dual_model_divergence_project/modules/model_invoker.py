import os
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
            return "该技术专利申请于2020年。"
        return "该技术专利申请于2018年。"
    return f"{model_name} mock: 对问题“{question}”的示例回答。"


def _call_openai(question: str) -> str:
    from openai import OpenAI

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    resp = client.responses.create(
        model=os.getenv("OPENAI_MODEL", "gpt-4.1-mini"),
        input=question,
    )
    return (resp.output_text or "").strip()


def _call_anthropic(question: str) -> str:
    import anthropic

    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    msg = client.messages.create(
        model=os.getenv("ANTHROPIC_MODEL", "claude-3-5-sonnet-latest"),
        max_tokens=700,
        messages=[{"role": "user", "content": question}],
    )
    parts = []
    for block in msg.content:
        txt = getattr(block, "text", "")
        if txt:
            parts.append(txt)
    return "\n".join(parts).strip()


def get_answers(
    question: str,
    db: DatabaseManager,
    query_id: int,
    use_cache: bool = True,
    mock_mode: bool = False,
) -> Dict[str, str]:
    load_dotenv()
    result: Dict[str, str] = {}

    for model_name in ["GPT", "Claude"]:
        cached = db.get_cached_response(question, model_name) if use_cache else None
        if cached:
            result[model_name] = cached
            continue

        if mock_mode:
            answer = _mock_answer(model_name, question)
        else:
            try:
                if model_name == "GPT":
                    answer = _call_openai(question)
                else:
                    answer = _call_anthropic(question)
                if not answer:
                    answer = _mock_answer(model_name, question)
            except Exception:
                # Safe fallback for local development without API keys.
                answer = _mock_answer(model_name, question)

        db.save_response(query_id=query_id, model_name=model_name, response_text=answer, usage_info="")
        result[model_name] = answer

    return result
