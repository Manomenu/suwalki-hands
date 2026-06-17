from openhands.sdk import LLM

from ebrit_hands.settings import settings


def build_smart_llm() -> LLM:
    return LLM(
        model=f"openai/{settings.ollama_model}",
        base_url=settings.ollama_base_url.rstrip("/") + "/v1",
        api_key="ollama",
        timeout=3600,
    )


def build_quick_llm() -> LLM:
    return LLM(
        model=f"openai/{settings.vllm_quick_model}",
        base_url=settings.vllm_base_url.rstrip("/") + "/v1/",
        api_key="EMPTY",
        timeout=600,
    )
