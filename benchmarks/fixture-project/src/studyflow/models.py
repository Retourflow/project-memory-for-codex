from dataclasses import dataclass


@dataclass(frozen=True)
class Task:
    id: int
    title: str
    completed: bool = False
