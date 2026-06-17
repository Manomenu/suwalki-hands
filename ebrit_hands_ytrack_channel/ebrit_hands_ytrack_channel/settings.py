from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT = Path(__file__).parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=[ROOT / ".env.base", ROOT / ".env"],
        env_file_encoding="utf-8",
        extra="ignore",
    )

    youtrack_url: str = ""        # e.g. https://yourorg.youtrack.cloud
    youtrack_token: str = ""      # permanent token
    youtrack_bot_login: str = ""  # login of the bot user to watch for assignments
    webhook_secret: str = ""      # optional: verify YouTrack webhook signature

    ebrit_hands_url: str = "http://host.containers.internal:6009"

    mock_youtrack_issue_id: str = "TEST-001"
    mock_youtrack_title: str = "Test task"
    mock_youtrack_description: str = "Test description"
    mock_youtrack_source_branch: str = "master"
    mock_youtrack_assignee_login: str = ""  # defaults to youtrack_bot_login


settings = Settings()
