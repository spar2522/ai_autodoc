from autodoc.events.github_push_event import (
    GithubPushEvent,
)

from autodoc.events.code_improvement_generated_event import (
    CodeImprovementGeneratedEvent,
)

from autodoc.events.event import Event


def create_event(
    payload: dict,
) -> Event:

    event_type = payload["type"]

    if event_type == "github_push":

        return GithubPushEvent(
            type=event_type,
            github_repo=payload["github_repo"],
            commit_hash=payload["commit_hash"],
        )

    if event_type == "code_improvement_generated":

        return CodeImprovementGeneratedEvent(
            type=event_type,
            github_repo=payload["github_repo"],
            review_branch=payload["review_branch"],
            worktree_path=payload["worktree_path"],
            file_path=payload["file_path"],
            commit_hash=payload["commit_hash"],
        )

    raise ValueError(f"Unknown event type: {event_type}")
