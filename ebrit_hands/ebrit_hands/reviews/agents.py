from openhands.sdk import Agent, Tool
from openhands.tools.file_editor.definition import FileEditorTool
from openhands.tools.glob.definition import GlobTool
from openhands.tools.grep.definition import GrepTool

from ebrit_hands.ai.llm import build_smart_llm
from ebrit_hands.reviews.tools import CreateGitInlineCommentTool


def create_review_agent(metadata_dir: str) -> Agent:
    return Agent(
        llm=build_smart_llm(),
        tools=[
            Tool(name=FileEditorTool.name),
            Tool(name=GlobTool.name),
            Tool(name=GrepTool.name),
            Tool(
                name=CreateGitInlineCommentTool.name,
                params={"metadata_dir": metadata_dir},
            ),
        ],
    )
