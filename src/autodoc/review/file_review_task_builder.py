from autodoc.config.runtime_config import Config

from autodoc.datamodels.file_review_task import (
    FileReviewTask,
)

from autodoc.git.worktree_manager import ensure_worktree_exists
from autodoc.review.review_branch import (
    create_review_branch_name,
)

from autodoc.review.file_loader import (
    load_file,
)

from autodoc.git.git_manager import (
    get_file_diff,
)


def build_file_review_task(
    config: Config,
    github_repo: str,
    repo_path: str,
    commit_hash: str,
    file_path: str,
) -> FileReviewTask:

    return FileReviewTask(
        github_repo=github_repo,
        commit_hash=commit_hash,
        file_path=file_path,
        review_branch=create_review_branch_name(file_path),
        diff=get_file_diff(
            repo_path,
            commit_hash,
            file_path,
        ),
        current_content=load_file(
            repo_path,
            file_path,
        ),
        worktree_path=ensure_worktree_exists(
            repo_path,
            create_review_branch_name(file_path),
            config.worktree_root,
        ),
    )
