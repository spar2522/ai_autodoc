def create_review_branch_name(
    file_path: str,
) -> str:

    sanitized = file_path.replace("/", "-").replace(".", "-").lower()

    return f"autodoc/{sanitized}"
