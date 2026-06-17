from pydantic import BaseModel


class MergeRequestChange(BaseModel):
    old_path: str
    new_path: str
    diff: str

    def to_string(self) -> str:
        import re
        out = [f"--- {self.old_path}", f"+++ {self.new_path}"]
        old_line = new_line = 0
        for raw in self.diff.splitlines():
            if raw.startswith("@@"):
                m = re.search(r"@@ -(\d+)(?:,\d+)? \+(\d+)(?:,\d+)? @@", raw)
                if m:
                    old_line = int(m.group(1)) - 1
                    new_line = int(m.group(2)) - 1
                out.append(raw)
            elif raw.startswith("-"):
                old_line += 1
                out.append(f"[old:{old_line}]-> {raw}")
            elif raw.startswith("+"):
                new_line += 1
                out.append(f"[new:{new_line}]-> {raw}")
            else:
                old_line += 1
                new_line += 1
                out.append(f"[old:{old_line},new:{new_line}]-> {raw}")
        return "\n".join(out)


class InlineComment(BaseModel):
    file_path: str
    new_line: int | None = None
    old_line: int | None = None
    new_line_start: int | None = None
    old_line_start: int | None = None
    comment: str


class ReviewRequest(BaseModel):
    project_id: int
    mr_iid: int
    note_id: int
    discussion_id: str
    note: str
    mr_title: str
    source_branch: str
    target_branch: str = ""
    changes: list[MergeRequestChange] = []
    callback_url: str | None = None


class ReviewResult(BaseModel):
    job_id: str
    project_id: int
    mr_iid: int
    discussion_id: str
    body: str
    status: str
    inline_comments: list[InlineComment] = []
