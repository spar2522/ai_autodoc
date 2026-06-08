from dataclasses import dataclass


@dataclass
class RepoConfig:

    github_repo: str

    local_path: str

    default_branch: str
