tasks: list[str] = []


def add_task(title: str) -> None:
    tasks.append(title)


def list_tasks() -> list[str]:
    return list(tasks)
