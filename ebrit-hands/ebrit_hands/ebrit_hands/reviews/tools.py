import json
import uuid
from collections.abc import Sequence
from pathlib import Path

from pydantic import Field

from openhands.sdk import Action, Observation, ToolDefinition, register_tool
from openhands.sdk.tool import ToolAnnotations, ToolExecutor


class CreateGitInlineCommentAction(Action):
    file_path: str = Field(description="Relative file path in the repo, e.g. 'src/foo.py'")
    new_line: int | None = Field(None, description="End line (or single line) in the new file version")
    old_line: int | None = Field(None, description="End line (or single line) in the old file version (deleted lines)")
    new_line_start: int | None = Field(None, description="Start of range on new side (omit for single-line comment)")
    old_line_start: int | None = Field(None, description="Start of range on old side (omit for single-line comment)")
    comment: str = Field(description="Review comment body (markdown supported)")


class CreateGitInlineCommentObservation(Observation):
    pass


class CreateGitInlineCommentExecutor(ToolExecutor):
    def __init__(self, metadata_dir: str):
        self._comments_dir = Path(metadata_dir) / "inline_comments"

    def __call__(self, action: CreateGitInlineCommentAction, conversation=None) -> CreateGitInlineCommentObservation:
        self._comments_dir.mkdir(parents=True, exist_ok=True)
        data = {
            "file_path": action.file_path,
            "new_line": action.new_line,
            "old_line": action.old_line,
            "new_line_start": action.new_line_start,
            "old_line_start": action.old_line_start,
            "comment": action.comment,
        }
        path = self._comments_dir / f"{uuid.uuid4()}.json"
        path.write_text(json.dumps(data))
        line_ref = action.new_line or action.old_line
        return CreateGitInlineCommentObservation.from_text(
            f"Queued inline comment on {action.file_path}:{line_ref}"
        )


class CreateGitInlineCommentTool(ToolDefinition[CreateGitInlineCommentAction, CreateGitInlineCommentObservation]):
    @classmethod
    def create(cls, conv_state=None, **params) -> Sequence["CreateGitInlineCommentTool"]:
        return [
            cls(
                action_type=CreateGitInlineCommentAction,
                observation_type=CreateGitInlineCommentObservation,
                description=(
                    "Queue an inline code review comment on a specific line or range of lines in the merge request diff.\n"
                    "Line number rules — read the diff @@ headers to get correct numbers:\n"
                    "- Added or unchanged lines (+ or context): use new_line with the line number from the +++ side.\n"
                    "- Deleted lines (- prefix): use old_line with the line number from the --- side. NEVER use new_line for deleted lines.\n"
                    "- Deleted file (all lines are -): always use old_line. new_line must be null.\n"
                    "- Added file (all lines are +): always use new_line. old_line must be null.\n"
                    "For a range comment, also set new_line_start (or old_line_start) to the first line of the range; "
                    "new_line/old_line is then the last line. Omit *_start for a single-line comment.\n"
                    "The comment text must refer only to the code contained within the specified line range — do not reference or summarise lines outside that range."
                ),
                annotations=ToolAnnotations(
                    title="create_git_inline_comment",
                    readOnlyHint=False,
                    destructiveHint=False,
                    idempotentHint=False,
                    openWorldHint=False,
                ),
                executor=CreateGitInlineCommentExecutor(**params),
            )
        ]


register_tool(CreateGitInlineCommentTool.name, CreateGitInlineCommentTool)
