import yaml

from autodoc.datamodels.repo_config import RepoConfig
from autodoc.config.runtime_config import Config


# testing
def load_config(path: str) -> Config:

    with open(path) as f:
        data = yaml.safe_load(f)

    repos = [RepoConfig(**repo) for repo in data["repos"]]

    return Config(
        repos=repos,
        model=data["model"],
        worktree_root=data["worktree_root"],
    )
