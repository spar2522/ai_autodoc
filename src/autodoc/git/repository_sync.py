import subprocess


def sync_repository(
    repo_path: str,
):

    print(f"Fetching latest refs for {repo_path}")

    subprocess.run(
        [
            "git",
            "fetch",
            "origin",
        ],
        cwd=repo_path,
        check=True,
    )


def ensure_commit_exists(
    repo_path: str,
    commit_hash: str,
):

    result = subprocess.run(
        [
            "git",
            "cat-file",
            "-e",
            commit_hash,
        ],
        cwd=repo_path,
        capture_output=True,
    )

    if result.returncode == 0:
        return

    print("Commit missing locally. Refetching...")

    subprocess.run(
        [
            "git",
            "fetch",
            "--all",
        ],
        cwd=repo_path,
        check=True,
    )

    result = subprocess.run(
        [
            "git",
            "cat-file",
            "-e",
            commit_hash,
        ],
        cwd=repo_path,
        capture_output=True,
    )

    if result.returncode != 0:

        raise RuntimeError(f"Unable to locate commit {commit_hash}")
