import subprocess


def push_branch(
    worktree_path: str,
    review_branch: str,
):

    subprocess.run(
        [
            "git",
            "push",
            "-u",
            "origin",
            review_branch,
        ],
        cwd=worktree_path,
        check=True,
    )
