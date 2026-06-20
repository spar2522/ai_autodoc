from autodoc.agents.code_improvement_agent import CodeImprovementAgent
from autodoc.events.code_improvement_generated_event import (
    CodeImprovementGeneratedEvent,
)
from autodoc.git.git_commit import commit_changes
from autodoc.git.worktree_manager import get_worktree_diff
from autodoc.queue.queue_names import PR_QUEUE, REVIEW_QUEUE
from autodoc.queue.redis_task_queue import RedisTaskQueue
from autodoc.config.runtime_config import Config
from autodoc.repositories.repository_registry import get_repo
from autodoc.git.repository_sync import (
    sync_repository,
    ensure_commit_exists,
)

from autodoc.git.git_manager import (
    get_changed_files,
)
from autodoc.events.event_factory import (
    create_event,
)
from autodoc.review.change_validator import has_meaningful_change
from autodoc.review.file_review_task_builder import build_file_review_task
from autodoc.git.file_writer import (
    write_file,
)

review_task_queue = RedisTaskQueue(REVIEW_QUEUE)
pr_task_queue = RedisTaskQueue(PR_QUEUE)


async def worker(
    config: Config,
):
    """Main worker function for processing code review tasks."""
    print("Review Worker started")
    while True:
        try:
            event_data = await review_task_queue.dequeue()
            event = create_event(event_data)
            print(event)
            repo = get_repo(
                config,
                event.github_repo,
            )

            if repo is None:
                print(f"Unknown repository: {event.github_repo}")
                continue

            print(f"Resolved repo: {repo.local_path}")

            # Sync repository and ensure commit exists
            sync_repository(repo.local_path)
            ensure_commit_exists(repo.local_path, event.commit_hash)

            # Get changed files for the commit
            files = get_changed_files(repo.local_path, event.commit_hash)
            print("Changed files:")

            for file in files:
                try:
                    task = build_file_review_task(
                        config=config,
                        github_repo=event.github_repo,
                        repo_path=repo.local_path,
                        commit_hash=event.commit_hash,
                        file_path=file,
                    )

                    if task is None:
                        continue

                    print(task)

                    agent = CodeImprovementAgent()
                    updated_file = await agent.run(task, config.model)

                    write_file(
                        repo_path=task.worktree_path,
                        relative_path=task.file_path,
                        content=updated_file,
                    )

                    print(f"Updated {task.file_path}")

                    diff = get_worktree_diff(worktree_path=task.worktree_path)
                    print("=== GENERATED DIFF ===")
                    print(diff)

                    if not has_meaningful_change(diff):
                        print("No meaningful changes.")
                        continue

                    commit_changes(
                        worktree_path=task.worktree_path,
                        file_path=task.file_path,
                    )

                    code_improvement_event = CodeImprovementGeneratedEvent(
                        type="code_improvement_generated",
                        github_repo=task.github_repo,
                        review_branch=task.review_branch,
                        worktree_path=task.worktree_path,
                        file_path=task.file_path,
                        commit_hash=event.commit_hash,
                    )

                    await pr_task_queue.enqueue(code_improvement_event)
                except Exception as e:
                    print(f"Failed review for file {task.file_path}: {e}")
                    print(f"Trying other files if any...")
                    continue

        except Exception as e:
            print(f"Failed review: {e}")