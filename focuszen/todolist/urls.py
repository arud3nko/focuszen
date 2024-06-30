from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

crud = DefaultRouter()
crud.register(r'', views.TaskViewSet, basename="task")

hierarchy = DefaultRouter()
hierarchy.register(r'', views.TasksHierarchyViewSet, basename="tasks-hierarchy")
hierarchy.register(r'', views.SingleTaskHierarchyViewSet, basename="task-hierarchy")

app_name = "todolist"

urlpatterns = [
    path("hierarchy/", include(hierarchy.urls)),
    path("", include(crud.urls)),
]
