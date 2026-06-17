from openhands.sdk import Agent, Tool, AgentContext
from openhands.tools.file_editor import FileEditorTool
from openhands.tools.task_tracker import TaskTrackerTool
from openhands.tools.terminal import TerminalTool
from openhands.sdk.skills import Skill

from ebrit_hands.ai.constants import SKILLS_DIR
from ebrit_hands.ai.llm import build_smart_llm

context = AgentContext(
    skills=[
        Skill.load(SKILLS_DIR / "dotnet" / "SKILL.md", SKILLS_DIR),
        Skill.load(SKILLS_DIR / "mr-description" / "SKILL.md", SKILLS_DIR),
        Skill.load(SKILLS_DIR / "complete-task" / "SKILL.md", SKILLS_DIR),
    ]
)

tools = [
    Tool(name=TerminalTool.name),
    Tool(name=FileEditorTool.name),
    Tool(name=TaskTrackerTool.name),
]

def create_task_agent() -> Agent:
    return Agent(
        llm=build_smart_llm(),
        tools=tools,
        agent_context=context
    )
