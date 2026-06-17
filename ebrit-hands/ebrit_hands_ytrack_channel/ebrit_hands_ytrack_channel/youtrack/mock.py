def build_payload(
    issue_id: str,
    title: str,
    description: str,
    source_branch: str,
    assignee_login: str,
) -> dict:
    return {
        "issue": {
            "id": issue_id,
            "summary": title,
            "description": description,
            "customFields": [{"name": "Branch", "value": source_branch}],
            "comments": [],
        },
        "change": {
            "fields": [{"name": "Assignee", "added": [{"login": assignee_login}]}]
        },
    }
