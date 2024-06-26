from django.http import JsonResponse

from ..services.task import ListTasksService


def get_tasks(request):
    return JsonResponse([str(task) for task in ListTasksService().execute()], safe=False)
