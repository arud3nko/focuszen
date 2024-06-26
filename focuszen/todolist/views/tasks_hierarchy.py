from django.http import JsonResponse
from ..services.task import TasksHierarchyService
from ..services.entities import Task


def task_to_dict(task: Task) -> dict:
    """Helper function to convert a task and its children to a dictionary"""
    return {
        "id": task.data.pk,
        "name": task.data.name,
        "description": task.data.description,
        "status": task.data.status,
        "planned_effort": task.data.planned_effort,
        "performer": task.data.performer,
        "actual_effort": task.data.actual_effort,
        "created_at": task.data.created_at.isoformat(),
        "updated_at": task.data.updated_at.isoformat(),
        "children": [task_to_dict(child) for child in task.children]
    }


def get_tasks_hierarchy(request):
    """Returns tasks hierarchy"""
    root_tasks = TasksHierarchyService().execute()
    tasks_dict = {task.data.pk: task_to_dict(task) for task in root_tasks}
    return JsonResponse(tasks_dict, safe=False)
