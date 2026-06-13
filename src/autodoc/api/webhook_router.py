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
        # Extract event type from headers
        event_type = request.headers.get("X-GitHub-Event")
        print(f"Received GitHub event: {event_type}")

        # Parse JSON payload
        webhook_payload = await request.json()

        # Extract repository name
        repo_info = webhook_payload.get("repository", {})
        repo_name = repo_info.get("full_name")

        if not repo_name:
            return {"error": "Missing repository information"}, 400

        # Process commits
        commits = webhook_payload.get("commits", [])
        for commit in commits:
            # Skip AutoDoc-generated commits
            message = commit.get("message", "")
            if message.startswith("AutoDoc improvements"):
                continue

            # Extract commit hash
            commit_hash = commit.get("id")
            if not commit_hash:
                continue  # Skip commits without an ID

            # Create and enqueue event
            event = GithubPushEvent(
                type="github_push",
                github_repo=repo_name,
                commit_hash=commit_hash,
            )
            await task_queue.enqueue(event)

        return {"status": "accepted"}

    except Exception as e:
        print(f"Error processing webhook: {e}")
        return {"error": "Internal server error"}, 500
