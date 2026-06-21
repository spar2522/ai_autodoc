from autodoc.events.code_improvement_generated_event import (
    CodeImprovementGeneratedEvent,
)
from autodoc.git.git_push import push_branch
from autodoc.github.pr_manager import PRManager
from autodoc.queue.redis_task_queue import RedisTaskQueue
from autodoc.config.runtime_config import Config
from autodoc.repositories.repository_registry import get_repo
from autodoc.git.repository_sync import (
    sync_repository,
)

from autodoc.events.event_factory import (
    create_event,
)

task_queue = RedisTaskQueue(PR_QUEUE)

async def worker(
    config: Config,
):
    print("PR Worker started")
    while True:

        try:

            event_data = await task_queue.dequeue()
            event = create_event(event_data)
            print(
                f"================ Received event for PR Worker: "
                f"{event} ================="
            )
            if isinstance(
                event,
                CodeImprovementGeneratedEvent,
            ):
                print(f"Pushing branch : {event.review_branch}")
                push_branch(
                    worktree_path=event.worktree_path,
                    review_branch=event.review_branch,
                )

                pr_manager = PRManager()

                existing_pr = await pr_manager.find_open_pr_for_file(
                    github_repo=event.github_repo,
                    file_path=event.file_path,
                )

                if existing_pr:
                    print(f"Closing stale PR: {existing_pr['html_url']}")
                    await pr_manager.close_pr(
                        github_repo=event.github_repo,
                        pr_number=existing_pr["number"],
                    )

                pr = await pr_manager.create_pr(
                    github_repo=event.github_repo,
                    review_branch=event.review_branch,
                    file_path=event.file_path,
                )

                print(f"Created PR: {pr['html_url']}")

        except Exception as ex:
            print(f"PR Worker failed: {ex}")