from pydantic import BaseModel

from lmnr import observe
from openhands.sdk.llm import Message, TextContent

from ebrit_hands.ai.llm import build_quick_llm, build_smart_llm


class _BranchName(BaseModel):
    branch_name: str


@observe(name="generate_branch_name", tags=["llm", "branch-name"])
def generate_branch_name(issue_id: str, title: str, description: str) -> str:
    llm = build_quick_llm()
    response = llm.completion(
        messages=[Message(role="user", content=[TextContent(
            text=(
                f"""
                Create a git branch name for given task title and description.

                Title: {title}

                Description: {description}

                "Branch Name Format: kebab-case, 1-5 words, no special characters, no whitespace. Examples: add-login-endpoint, fix-typo-in-readme
                """
            )
        )])],
        response_format=_BranchName,
    )
    return f"{issue_id}-{_BranchName.model_validate_json(response.message.content[0].text).branch_name}-AI"


@observe(name="generate_review", tags=["llm", "review"])
def generate_review(instructions: str, diff: str, mr_title: str) -> str:
    llm = build_smart_llm()
    response = llm.completion(
        messages=[Message(role="user", content=[TextContent(
            text=(
                f"You are a code reviewer. Review the following merge request diff and respond with your findings.\n\n"
                f"MR Title: {mr_title}\n\n"
                f"Reviewer instructions: {instructions}\n\n"
                f"Diff:\n{diff}"
            )
        )])],
    )
    return response.message.content[0].text
