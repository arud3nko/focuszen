from django.shortcuts import render, redirect

from django.http import HttpResponse

from ..forms import NewTaskForm
from ..services.task import NewTaskService
from ..services.dao import TaskDAO


def create_task(request):
    if request.method == 'POST':
        form = NewTaskForm(request.POST)
        if form.is_valid():
            task_instance = form.save(commit=False)
            task_data = TaskDAO.__orm_to_entity(task_orm=task_instance)
            service = NewTaskService(task_data=task_data)
            service.execute()
            return HttpResponse(task_instance)
    else:
        form = NewTaskForm()

    return render(request, 'create_task.html', {'form': form})
