from openhands.sdk import Agent

from ebrit_hands.ai.llm import build_smart_llm


def create_basic_agent() -> Agent:
    return Agent(llm=build_smart_llm())
