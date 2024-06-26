from django.http import JsonResponse
from ..services.task import TasksHierarchyService
from ..models.task import Task


def task_to_dict(task: Task):
    """Helper function to convert a task and its children to a dictionary"""
    return {
        "id": task.pk,
        "name": task.name,
        "description": task.description,
        "status": task.status,
        "planned_effort": task.planned_effort,
        "performer": task.performer,
        "actual_effort": task.actual_effort,
        "created_at": task.created_at.isoformat(),
        "updated_at": task.updated_at.isoformat(),
        "children": [task_to_dict(child) for child in task.children]
    }


def get_tasks_hierarchy(request):
    """Returns tasks hierarchy"""
    root_tasks = Task.objects.filter(parent__isnull=True)
    tasks_dict = [task_to_dict(task) for task in root_tasks]
    return JsonResponse(tasks_dict, safe=False)
