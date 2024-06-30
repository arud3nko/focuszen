"""This module provides CRUD operations for `Task` model"""

from rest_framework import viewsets, mixins
from rest_framework.exceptions import APIException

from ..models import Task
from ..serializers import TaskSerializer
from ..services import TaskStatusUpdateService, DeleteTaskService
from ..services.exceptions import ServiceException


class UpdateTaskMixin(mixins.UpdateModelMixin):
    """
    Update `Task` mixin, handles specific fields update
    """

    def perform_update(self, serializer):
        """Overriding perform_update to handle status update"""
        instance = self.get_object()
        try:
            self._execute_update_services(task=instance, new=serializer.validated_data)
        except ServiceException as e:
            raise APIException(str(e))
        serializer.save()

    def _execute_update_services(self, task: Task, new: dict):
        """
        Here should be added any update rules.
        If I need to handle some fields updates, I execute the services-handlers.
        """
        if self._status_updated(task=task, new=new):
            TaskStatusUpdateService(task=task, new_status=new.get("status")).execute()

    @staticmethod
    def _status_updated(task: Task, new: dict) -> bool:
        """Checks if status is being updated"""
        return task.status != new.get("status")


class DeleteTaskMixin(mixins.DestroyModelMixin):
    """
    Delete `Task` view set mixin, handles deletion specific cases
    """

    def perform_destroy(self, instance):
        """Overriding perform_destroy to handle deletion"""
        try:
            self._execute_delete_services(task=instance)
        except ServiceException as e:
            raise APIException(str(e))
        instance.delete()

    @staticmethod
    def _execute_delete_services(task: Task):
        """
        Here should be added any deletion rules.
        """
        DeleteTaskService(task=task).execute()


class CreateTaskMixin(mixins.CreateModelMixin):
    """
    Create `Task` view set mixin, handles specific cases
    """

    def perform_create(self, serializer):
        """Overriding perform_create to handle creation"""
        serializer.validated_data.pop("status", None)  # FIXME this is костыль, provide proper status serialization
        serializer.save()
    pass


class CRUDTaskViewSet(UpdateTaskMixin,
                      DeleteTaskMixin,
                      CreateTaskMixin,
                      mixins.ListModelMixin,
                      mixins.RetrieveModelMixin,
                      viewsets.GenericViewSet):
    """Base CRUD view set class with required mixins"""
    pass


class TaskViewSet(CRUDTaskViewSet):
    """
    A view set for `Task` objects CRUD
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
