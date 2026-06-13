from fastapi import APIRouter, Request
from autodoc.events.github_push_event import GithubPushEvent
from autodoc.queue.queue_names import REVIEW_QUEUE
from autodoc.queue.redis_task_queue import RedisTaskQueue

router = APIRouter()

task_queue = RedisTaskQueue(REVIEW_QUEUE)


@router.post("/webhook/github")
async def github_webhook(request: Request):
    """
    Receives GitHub webhook events and processes push events.

    Parses the request payload, extracts repository and commit information,
    and enqueues a GithubPushEvent for each relevant commit.

    Returns:
        dict: {"status": "accepted"} if successful
    """
    try:
        event_type = extract_event_type(request)
        print(f"Received GitHub event: {event_type}")

        webhook_payload = await parse_webhook_payload(request)
        repository_name = extract_repository_name(webhook_payload)

        if not repository_name:
            return {"error": "Missing repository information"}, 400

        commits = webhook_payload.get("commits", [])
        for commit in commits:
            if is_auto_doc_commit(commit):
                continue

            commit_hash = commit.get("id")
            if not commit_hash:
                continue

            event = GithubPushEvent(
                type="github_push",
                github_repo=repository_name,
                commit_hash=commit_hash,
            )
            await enqueue_event(event)

        return {"status": "accepted"}

    except Exception as e:
        print(f"Error processing webhook: {e}")
        return {"error": "Internal server error"}, 500

def extract_event_type(request: Request) -> str:
    """Extract the GitHub event type from the request headers."""
    return request.headers.get("X-GitHub-Event", "unknown")


async def parse_webhook_payload(request: Request) -> dict:
    """Parse the JSON payload from the request."""
    return await request.json()


def extract_repository_name(payload: dict) -> str:
    """Extract the full repository name from the payload."""
    repo_info = payload.get("repository", {})
    return repo_info.get("full_name")


def is_auto_doc_commit(commit: dict) -> bool:
    """Check if a commit is AutoDoc-generated."""
    message = commit.get("message", "")
    return message.startswith("AutoDoc improvements")


async def enqueue_event(event: GithubPushEvent):
    """Enqueue a GithubPushEvent into the task queue."""
    await task_queue.enqueue(event)
