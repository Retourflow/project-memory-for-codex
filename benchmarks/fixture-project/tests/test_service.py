import sqlite3
import unittest

from studyflow.notifications import NotificationPort
from studyflow.repository import SqliteTaskRepository
from studyflow.service import TaskService


class RecordingNotification(NotificationPort):
    def __init__(self) -> None:
        self.completed_ids: list[int] = []

    def task_completed(self, task) -> None:
        self.completed_ids.append(task.id)


class TaskServiceTests(unittest.TestCase):
    def test_completion_persists_before_notification(self) -> None:
        connection = sqlite3.connect(":memory:")
        repository = SqliteTaskRepository(connection)
        notifications = RecordingNotification()
        service = TaskService(repository, notifications)
        task = service.create_task("Review chapter")

        completed = service.complete_task(task.id)

        self.assertTrue(completed.completed)
        self.assertEqual(repository.list_all()[0], completed)
        self.assertEqual(notifications.completed_ids, [task.id])


if __name__ == "__main__":
    unittest.main()
