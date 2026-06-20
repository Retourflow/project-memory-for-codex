from .models import Task
from .notifications import NotificationPort
from .repository import TaskRepository


class TaskService:
    def __init__(
        self, repository: TaskRepository, notifications: NotificationPort
    ) -> None:
        self.repository = repository
        self.notifications = notifications

    def create_task(self, title: str) -> Task:
        normalized = title.strip()
        if not normalized:
            raise ValueError("title is required")
        return self.repository.add(normalized)

    def list_tasks(self) -> list[Task]:
        return self.repository.list_all()

    def complete_task(self, task_id: int) -> Task:
        task = self.repository.complete(task_id)
        self.notifications.task_completed(task)
        return task
