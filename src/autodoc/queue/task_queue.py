from abc import ABC, abstractmethod
from autodoc.events.event import Event


class TaskQueue(ABC):

    @abstractmethod
    async def enqueue(
        self,
        event: Event,
    ):
        pass

    async def dequeue(
        self,
    ) -> Event:
        pass
