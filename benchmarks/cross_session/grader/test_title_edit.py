"""Offline, independent behavioral checks for the three-session StudyFlow pilot.

Run OUTSIDE the agent workspace with the target workspace's src/ on PYTHONPATH.
Do not expose this file or grader outputs to the agent during the trial.
This checks code, not memory truth or real model token usage.
"""

from __future__ import annotations

import os
import sqlite3
import unittest

from studyflow import api
from studyflow.notifications import NotificationPort
from studyflow.repository import SqliteTaskRepository
from studyflow.service import TaskService


STAGE = os.environ.get("BENCHMARK_SESSION")
if STAGE not in {"session1", "session2", "session3"}:
    raise RuntimeError(
        "Set BENCHMARK_SESSION=session1, session2, or session3 explicitly"
    )


class SpyNotifications(NotificationPort):
    def __init__(self) -> None:
        self.completed: list[int] = []

    def task_completed(self, task) -> None:
        self.completed.append(task.id)


class TitleEditContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.connection = sqlite3.connect(":memory:")
        self.repo = SqliteTaskRepository(self.connection)
        self.spy = SpyNotifications()
        self.service = TaskService(self.repo, self.spy)

    def tearDown(self) -> None:
        self.connection.close()

    def test_repository_rename_persists_trimmed_title(self) -> None:
        task = self.service.create_task("First")
        renamed = self.repo.rename(task.id, "  Updated title  ")
        self.assertEqual(renamed.title, "Updated title")
        self.assertEqual(renamed.id, task.id)
        self.assertFalse(renamed.completed)
        self.assertEqual(self.repo.list_all()[0].title, "Updated title")

    def test_service_rejects_blank_title_without_mutating(self) -> None:
        task = self.service.create_task("Original")
        with self.assertRaises(ValueError):
            self.service.rename_task(task.id, " \t ")
        self.assertEqual(self.repo.list_all()[0].title, "Original")

    def test_missing_task_is_not_silently_created(self) -> None:
        with self.assertRaises(KeyError):
            self.service.rename_task(987654, "New title")
        self.assertEqual(self.repo.list_all(), [])

    def test_completed_state_and_notification_boundary(self) -> None:
        task = self.service.create_task("Finish it")
        self.service.complete_task(task.id)
        self.assertEqual(self.spy.completed, [task.id])
        renamed = self.service.rename_task(task.id, "Completed and renamed")
        self.assertTrue(renamed.completed)
        self.assertEqual(renamed.title, "Completed and renamed")
        self.assertEqual(self.spy.completed, [task.id])

    def test_existing_completion_api_contract_is_unchanged(self) -> None:
        task = self.service.create_task("Completion")
        response = api.complete_task(self.service, task.id)
        self.assertEqual(
            response, {"id": task.id, "title": "Completion", "completed": True}
        )
        self.assertEqual(self.spy.completed, [task.id])

    @unittest.skipUnless(
        STAGE in {"session2", "session3"}, "API work reserved for session 2"
    )
    def test_new_api_adapter_contract(self) -> None:
        task = self.service.create_task("Before")
        response = api.rename_task(self.service, task.id, " After ")
        self.assertEqual(
            response, {"id": task.id, "title": "After", "completed": False}
        )
        self.assertEqual(self.spy.completed, [])

    @unittest.skipUnless(
        STAGE in {"session2", "session3"}, "API work reserved for session 2"
    )
    def test_api_edit_of_completed_task_does_not_notify_again(self) -> None:
        task = self.service.create_task("Before")
        api.complete_task(self.service, task.id)
        response = api.rename_task(self.service, task.id, "After")
        self.assertTrue(response["completed"])
        self.assertEqual(set(response), {"id", "title", "completed"})
        self.assertEqual(self.spy.completed, [task.id])

    @unittest.skipUnless(
        STAGE in {"session2", "session3"}, "API work reserved for session 2"
    )
    def test_api_unknown_id_fails(self) -> None:
        with self.assertRaises(KeyError):
            api.rename_task(self.service, 987654, "Not found")

    @unittest.skipUnless(STAGE == "session1", "Only a session-1 scope check")
    def test_api_not_implemented_before_handoff(self) -> None:
        self.assertFalse(
            hasattr(api, "rename_task"),
            "Session 1 must leave the API adapter to the next agent session",
        )


if __name__ == "__main__":
    unittest.main()
