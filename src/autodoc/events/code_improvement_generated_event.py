from dataclasses import dataclass

from autodoc.events.event import Event


@dataclass
class CodeImprovementGeneratedEvent(Event):

    github_repo: str

    review_branch: str

    worktree_path: str

    file_path: str

    commit_hash: str
