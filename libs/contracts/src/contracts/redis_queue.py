from typing import Protocol
from dataclasses import dataclass


@dataclass(frozen=True)
class Received[T]:
    body: T
    receipt: str
    delivery_count: str


class RedisQueue[T](Protocol):
    def send(self, body: T) -> None:
        pass

    def receive(
        self, max_messages: int = 10, wait_seconds: float = 5
    ) -> list[Received[T]]:
        a: list[Received[T]] = []
        return []

    def ack(self, msg: Received[T]) -> None:
        pass
