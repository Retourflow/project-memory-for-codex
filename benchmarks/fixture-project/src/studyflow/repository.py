import sqlite3
from typing import Protocol

from .models import Task


class TaskRepository(Protocol):
    def add(self, title: str) -> Task: ...

    def list_all(self) -> list[Task]: ...

    def complete(self, task_id: int) -> Task: ...


class SqliteTaskRepository:
    def __init__(self, connection: sqlite3.Connection) -> None:
        self.connection = connection
        self.connection.execute(
            "CREATE TABLE IF NOT EXISTS tasks "
            "(id INTEGER PRIMARY KEY, title TEXT NOT NULL, completed INTEGER NOT NULL)"
        )

    def add(self, title: str) -> Task:
        cursor = self.connection.execute(
            "INSERT INTO tasks(title, completed) VALUES (?, 0)", (title,)
        )
        self.connection.commit()
        return Task(id=cursor.lastrowid, title=title)

    def list_all(self) -> list[Task]:
        rows = self.connection.execute(
            "SELECT id, title, completed FROM tasks ORDER BY id"
        ).fetchall()
        return [Task(id=row[0], title=row[1], completed=bool(row[2])) for row in rows]

    def complete(self, task_id: int) -> Task:
        self.connection.execute(
            "UPDATE tasks SET completed = 1 WHERE id = ?", (task_id,)
        )
        self.connection.commit()
        row = self.connection.execute(
            "SELECT id, title, completed FROM tasks WHERE id = ?", (task_id,)
        ).fetchone()
        if row is None:
            raise KeyError(task_id)
        return Task(id=row[0], title=row[1], completed=bool(row[2]))
