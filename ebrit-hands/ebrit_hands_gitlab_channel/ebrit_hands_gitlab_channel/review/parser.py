from ebrit_hands_library.contracts.review import ReviewRequest

from ebrit_hands_gitlab_channel.webhook.schemas import GitLabCommentPayload

TRIGGER = "@review"


def try_parse_review_request(payload: dict) -> ReviewRequest | None:
    if payload.get("object_kind") != "note":
        return None

    event = GitLabCommentPayload.model_validate(payload)

    if event.object_attributes.noteable_type != "MergeRequest":
        return None
    if event.merge_request is None:
        return None
    if TRIGGER not in event.object_attributes.note:
        return None

    note = event.object_attributes.note.replace(TRIGGER, "").strip()

    return ReviewRequest(
        project_id=event.project_id,
        mr_iid=event.merge_request.iid,
        note_id=event.object_attributes.id,
        discussion_id=event.object_attributes.discussion_id,
        note=note,
        mr_title=event.merge_request.title,
        source_branch=event.merge_request.source_branch,
    )
