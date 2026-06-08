from pathlib import Path

from autodoc.constants import PROJECT_ROOT


def load_skill(
    skill_name: str,
) -> str:

    skill_file = PROJECT_ROOT / "skills" / skill_name / "SKILL.md"

    return skill_file.read_text()
