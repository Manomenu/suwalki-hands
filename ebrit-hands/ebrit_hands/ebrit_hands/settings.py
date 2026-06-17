import os
from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

from ebrit_hands_library.constants import SOLUTION_ROOT

ROOT = Path(__file__).parent.parent


class RepoConfig(BaseModel):
    repo: str
    token: str
    project_id: int | None = None
    default_branch: str = "master"
    image: str = "default"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=[SOLUTION_ROOT / ".env.base", SOLUTION_ROOT / ".env", ROOT / ".env.base", ROOT / ".env"],
        env_file_encoding="utf-8",
        extra="allow",
    )

    gitlab_host: str = "git.adrentech.com"
    gitlab_bot_name: str = "ebrit-bot"
    gitlab_bot_email: str = "ebrit-bot@adrentech.com"

    ollama_base_url: str = ""
    ollama_model: str = "qwen3.6:27b"

    vllm_base_url: str = ""
    vllm_quick_model: str = "gpt-oss:20b"

    image_registry: str = ""

    lmnr_project_api_key: str = ""
    lmnr_base_url: str = "http://localhost"
    lmnr_http_port: int = 18000
    lmnr_grpc_port: int = 18001

    @property
    def repositories(self) -> dict[str, RepoConfig]:
        repos = {}
        i = 1
        while True:
            repo = getattr(self, f"gitlab_repo_{i}", None) or os.environ.get(f"GITLAB_REPO_{i}")
            token = getattr(self, f"gitlab_token_{i}", None) or os.environ.get(f"GITLAB_TOKEN_{i}")
            if not repo:
                break
            raw_pid = getattr(self, f"gitlab_project_id_{i}", None) or os.environ.get(f"GITLAB_PROJECT_ID_{i}")
            repos[repo] = RepoConfig(
                repo=repo,
                token=token or "",
                project_id=int(raw_pid) if raw_pid else None,
                default_branch=getattr(self, f"gitlab_default_branch_{i}", None) or os.environ.get(f"GITLAB_DEFAULT_BRANCH_{i}", "master"),
                image=getattr(self, f"project_image_{i}", None) or os.environ.get(f"PROJECT_IMAGE_{i}", "default"),
            )
            i += 1
        return repos

    def get_repo(self, gitlab_project_id: int) -> RepoConfig:
        for repo in self.repositories.values():
            if repo.project_id == gitlab_project_id:
                return repo
        raise KeyError(f"No repo configured for project_id={gitlab_project_id}")


settings = Settings()
