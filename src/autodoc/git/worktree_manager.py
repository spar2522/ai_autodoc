from pathlib import Path
import subprocess


def ensure_worktree_exists(
    repo_path: str,
    review_branch: str,
    worktree_root: str,
) -> str:

    worktree_name = review_branch.replace("/", "-")

    worktree_path = Path(worktree_root) / worktree_name

    #
    # Worktree already exists
    #
    if worktree_path.exists():
        return str(worktree_path)

    #
    # Check if branch already exists
    #
    result = subprocess.run(
        [
            "git",
            "branch",
            "--list",
            review_branch,
        ],
        cwd=repo_path,
        capture_output=True,
        text=True,
        check=True,
    )

    branch_exists = bool(result.stdout.strip())

    #
    # Existing branch
    #
    if branch_exists:

        print(f"Attaching existing branch {review_branch}")

        subprocess.run(
            [
                "git",
                "worktree",
                "add",
                str(worktree_path),
                review_branch,
            ],
            cwd=repo_path,
            check=True,
        )

    #
    # New branch
    #
    else:

        print(f"Creating worktree {worktree_path}")

        subprocess.run(
            [
                "git",
                "worktree",
                "add",
                "-b",
                review_branch,
                str(worktree_path),
            ],
            cwd=repo_path,
            check=True,
        )

    return str(worktree_path)


def get_worktree_diff(
    worktree_path: str,
) -> str:

    result = subprocess.run(
        [
            "git",
            "diff",
        ],
        cwd=worktree_path,
        capture_output=True,
        text=True,
        check=True,
    )

    return result.stdout
