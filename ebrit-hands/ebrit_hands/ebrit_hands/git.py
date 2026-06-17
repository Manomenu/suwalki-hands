import logging
import random
import shutil
from contextlib import contextmanager
from pathlib import Path

import gitlab
from git import Repo

from ebrit_hands_library.constants import ARTIFACTS
from ebrit_hands.settings import RepoConfig, settings

log = logging.getLogger(__name__)


@contextmanager
def repository(id: str, repo: RepoConfig, branch: str | None = None):
    actual_branch = branch or repo.default_branch
    project = ARTIFACTS / f"project-{id}"
    metadata = ARTIFACTS / f"metadata-{id}"

    if metadata.exists():
        shutil.rmtree(metadata)
    metadata.mkdir(parents=True)
    metadata.chmod(0o777)

    if project.exists():
        shutil.rmtree(project)
    project.mkdir(parents=True)
    project.chmod(0o777)

    repo_url = f"https://oauth2:{repo.token}@{settings.gitlab_host}/{repo.repo}.git"
    git_repo = Repo.clone_from(repo_url, project, branch=actual_branch, depth=1)
    git_repo.config_writer().set_value("user", "name", settings.gitlab_bot_name).release()
    git_repo.config_writer().set_value("user", "email", settings.gitlab_bot_email).release()
    log.info("Cloned %s (branch: %s) to %s", repo.repo, actual_branch, project)

    try:
        yield (project, metadata)
    finally:
        def _force_remove(path: Path) -> None:
            for p in path.rglob("*"):
                try:
                    p.chmod(0o777)
                except OSError:
                    pass
            shutil.rmtree(path, ignore_errors=True)

        _force_remove(metadata)
        _force_remove(project)
        log.info("Removed %s and %s", project, metadata)


def commit_leftovers(issue_id: str, repo_path: Path) -> None:
    repo = Repo(repo_path)
    repo.git.add(".")
    if repo.is_dirty(index=True):
        repo.index.commit(f"{issue_id}-leftover-changes-{random.randint(100,999)}-AI")
        log.info("Committed leftover changes in %s", repo_path)
    else:
        log.info("No leftover changes to commit in %s", repo_path)


def save_on_remote(repo_path: Path, branch: str) -> None:
    repo = Repo(repo_path)
    repo.remotes.origin.push(refspec=f"{branch}:{branch}", force=True)
    log.info("Pushed branch %s to remote", branch)


def create_merge_request(source_branch: str, target_branch: str, issue_id: str, title: str, mr_description: str, repo: RepoConfig) -> str:
    gl = gitlab.Gitlab(
        url=f"https://{settings.gitlab_host}",
        private_token=repo.token,
    )
    project = gl.projects.get(repo.repo)
    mr = project.mergerequests.create({
        "source_branch": source_branch,
        "target_branch": target_branch,
        "title": f"[{issue_id}] {title}",
        "description": mr_description,
        "remove_source_branch": True,
    })
    log.info("Created MR !%s: %s → %s", mr.iid, source_branch, target_branch)
    return mr.web_url


def get_mr_diff(project_id: int, mr_iid: int, repo: RepoConfig) -> str:
    gl = gitlab.Gitlab(
        url=f"https://{settings.gitlab_host}",
        private_token=repo.token,
    )
    mr = gl.projects.get(project_id).mergerequests.get(mr_iid)
    changes = mr.changes()
    return "\n\n".join(c["diff"] for c in changes.get("changes", []))


def switch_branch(repo_path: Path, issue_id: str, branch_name: str | None = None) -> str:
    repo = Repo(repo_path)
    if branch_name is None:
        branch_name = f"{issue_id}-{random.randint(100,999)}-AI"
    if branch_name in repo.heads:
        repo.heads[branch_name].checkout()
    else:
        repo.create_head(branch_name).checkout()
    return branch_name
