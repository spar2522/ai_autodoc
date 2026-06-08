from pathlib import Path


def write_file(
    repo_path: str,
    relative_path: str,
    content: str,
):

    file_path = Path(repo_path) / relative_path

    file_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    file_path.write_text(
        content,
        encoding="utf-8",
    )
