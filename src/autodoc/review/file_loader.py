from pathlib import Path


def load_file(
    repo_path: str,
    relative_path: str,
) -> str:

    file_path = Path(repo_path) / relative_path

    return file_path.read_text()
