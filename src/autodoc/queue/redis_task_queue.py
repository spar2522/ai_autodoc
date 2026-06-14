import json
from typing import Optional, Dict, Any

import redis.asyncio as redis

from autodoc.events.event import Event
from autodoc.queue.task_queue import TaskQueue


class RedisTaskQueue(TaskQueue):
    """A task queue implementation using Redis for message storage and retrieval."""

    def __init__(
        self,
        queue_name: str,
        host: str = "localhost",
        port: int = 6380,
        decode_responses: bool = True,
        socket_timeout: Optional[int] = None,
    ):
        """
        Initialize RedisTaskQueue with Redis connection parameters.

        Args:
            queue_name: Name of the Redis list to use as the task queue.
            host: Redis server host (default: localhost).
            port: Redis server port (default: 6380).
            decode_responses: Whether to decode Redis responses as strings (default: True).
            socket_timeout: Socket timeout in seconds (default: None).
        """
        self.queue_name = queue_name
        self.redis_client = redis.Redis(
            host=host,
            port=port,
            decode_responses=decode_responses,
            socket_timeout=socket_timeout,
        )

    async def enqueue(
        self,
        event: Event,
    ) -> None:
        """
        Add an event to the task queue.

        Args:
            event: Event object to be enqueued.
        """
        await self.redis_client.lpush(
            self.queue_name,
            json.dumps(event.to_dict()),
        )

    async def dequeue(self) -> Dict[str, Any]:
        """
        Dequeue and return the oldest task from the queue.

        Returns:
            A dictionary representation of the dequeued event.
        """
        _, task_json = await self.redis_client.brpop(self.queue_name)
        return json.loads(task_json)