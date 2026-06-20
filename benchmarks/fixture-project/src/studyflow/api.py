from .service import TaskService


def complete_task(service: TaskService, task_id: int) -> dict[str, object]:
    task = service.complete_task(task_id)
    return {"id": task.id, "title": task.title, "completed": task.completed}
