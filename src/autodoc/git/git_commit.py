import subprocess


def commit_changes(
    worktree_path: str,
    file_path: str,
):

    subprocess.run(
        [
            "git",
            "add",
            file_path,
        ],
        cwd=worktree_path,
        check=True,
    )

    subprocess.run(
        [
            "git",
            "commit",
            "-m",
            f"AutoDoc improvements for {file_path}",
        ],
        cwd=worktree_path,
        check=True,
    )
