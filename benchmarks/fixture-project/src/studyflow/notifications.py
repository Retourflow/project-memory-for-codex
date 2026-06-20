from typing import Protocol

from .models import Task


class NotificationPort(Protocol):
    def task_completed(self, task: Task) -> None: ...


class ConsoleNotification:
    def task_completed(self, task: Task) -> None:
        print(f"Completed: {task.title}")


class EmailNotification:
    def task_completed(self, task: Task) -> None:
        print(f"Email queued for task {task.id}")
