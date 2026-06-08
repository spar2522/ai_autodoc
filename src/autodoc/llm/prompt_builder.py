from autodoc.datamodels.file_review_task import (
    FileReviewTask,
)

from autodoc.skills.skill_loader import (
    load_skill,
)


def build_prompt(
    task: FileReviewTask,
) -> str:

    skill = load_skill("file_review")

    return f"""
{skill}

FILE PATH:
{task.file_path}

GIT DIFF:
{task.diff}

CURRENT FILE:
{task.current_content}
"""
