import os
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

from ebrit_hands_library.constants import SOLUTION_ROOT

ROOT = Path(__file__).parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=[SOLUTION_ROOT / ".env.base", SOLUTION_ROOT / ".env", ROOT / ".env.base", ROOT / ".env"],
        env_file_encoding="utf-8",
        extra="allow",
    )

    gitlab_webhook_secret: str = ""
    ebrit_hands_url: str = "http://host.containers.internal:6009"

    gitlab_host: str = "git.adrentech.com"
    gitlab_channel_url: str = "http://host.containers.internal:5085"

    @property
    def gitlab_token(self) -> str:
        token = getattr(self, "gitlab_token_1", None) or os.environ.get("GITLAB_TOKEN_1", "")
        return token


settings = Settings()
