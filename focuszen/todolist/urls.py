from django.urls import path

from . import views

app_name = "todolist"
urlpatterns = [
    path("create/", views.create_task, name="create_task"),
    path("", views.get_tasks_hierarchy, name="task_list")
]
