from autodoc.config.runtime_config import Config
from autodoc.datamodels.repo_config import (
    RepoConfig,
)


def get_repo(
    config: Config,
    github_repo: str,
) -> RepoConfig | None:

    for repo in config.repos:

        if repo.github_repo == github_repo:
            return repo

    return None
