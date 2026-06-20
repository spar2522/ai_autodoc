def create_review_branch_name(
    file_path: str,
    commit_hash: str,
) -> str:

    sanitized = file_path.replace("/", "-").replace(".", "-").lower()

    return f"autodoc/" f"{sanitized}-" f"{commit_hash[:7]}"
