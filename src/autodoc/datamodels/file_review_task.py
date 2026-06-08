from dataclasses import dataclass


@dataclass
class FileReviewTask:

    github_repo: str

    commit_hash: str

    file_path: str

    diff: str

    current_content: str

    review_branch: str

    worktree_path: str | None = None
