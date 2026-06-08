import subprocess


def get_changed_files(
    repo_path: str,
    commit_hash: str,
) -> list[str]:

    result = subprocess.run(
        [
            "git",
            "show",
            "--name-only",
            "--pretty=",
            commit_hash,
        ],
        cwd=repo_path,
        capture_output=True,
        text=True,
        check=True,
    )

    files = [line.strip() for line in result.stdout.splitlines() if line.strip()]

    return files


def get_file_diff(
    repo_path: str,
    commit_hash: str,
    file_path: str,
) -> str:

    result = subprocess.run(
        [
            "git",
            "show",
            commit_hash,
            "--",
            file_path,
        ],
        cwd=repo_path,
        capture_output=True,
        text=True,
        check=True,
    )

    return result.stdout
