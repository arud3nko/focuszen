from django.http import JsonResponse

from ..services.task import TaskListService


def get_tasks(request):
    return JsonResponse([str(task) for task in TaskListService().execute()], safe=False)
