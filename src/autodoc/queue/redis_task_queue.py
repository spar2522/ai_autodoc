import json

import redis.asyncio as redis

from autodoc.events.event import Event
from autodoc.queue.task_queue import TaskQueue


class RedisTaskQueue(TaskQueue):

    def __init__(
        self,
        queue_name: str,
    ):
        self.queue_name = queue_name
        self.redis_client = redis.Redis(
            host="localhost",
            port=6379,
            decode_responses=True,
            socket_timeout=None,
        )

    async def enqueue(
        self,
        event: Event,
    ):

        await self.redis_client.lpush(
            self.queue_name,
            json.dumps(event.to_dict()),
        )

    async def dequeue(self) -> dict:

        _, task_json = await self.redis_client.brpop(self.queue_name)

        return json.loads(task_json)
