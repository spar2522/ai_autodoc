from dataclasses import dataclass

from autodoc.datamodels.repo_config import (
    RepoConfig,
)


@dataclass
class Config:

    repos: list[RepoConfig]

    model: str

    worktree_root: str
