def has_meaningful_change(
    git_diff: str,
) -> bool:

    return bool(git_diff.strip())
