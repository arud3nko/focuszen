from __future__ import annotations

from typing import Literal, Any, TYPE_CHECKING

from django.db import transaction

from .base import BaseService
from .exceptions import StatusNotAllowed
from ..enums import Status

if TYPE_CHECKING:
    from ..models import Task


class TaskStatusUpdateService(BaseService):
    """
    Service for updating task status
    This service is Facade for group of status update services
    """
    def __init__(self,
                 task: Task,
                 new_status: Literal[Status.RUNNING, Status.COMPLETED, Status.SUSPENDED, Status.ASSIGNED]):
        self._task = task
        self._new_status = new_status

    def execute(self) -> None:
        """Executes `TaskStatusUpdateService` service - handle status and execute special service"""
        if self._new_status == Status.COMPLETED:
            return CompleteTaskService(task=self._task).execute()
        elif self._new_status == Status.SUSPENDED:
            return SuspendTaskService(task=self._task).execute()


class CompleteTaskService(BaseService):
    """This service can be used separately or inside the `TaskStatusUpdateService` to set `Task` status to completed"""
    def __init__(self,
                 task: Task):
        self._task = task

    def execute(self) -> Any:  # FIXME this is business-logic and it should be independent from Django transactions
        """Executes `CompleteTaskService` service - checks completable & recursively completes subtasks"""
        if self.completable(self._task):
            self._complete(self._task)
        else:
            raise StatusNotAllowed("Task is not completable due to current status or subtasks statuses")

    @staticmethod
    def completable(task: Task) -> bool:
        """Check if task can be marked as completed"""
        if task.status not in [Status.RUNNING, Status.COMPLETED]:
            return False
        for child in task.children:
            if not CompleteTaskService.completable(child):
                return False
        return True

    @staticmethod
    def _complete(task: Task) -> None:
        """Complete `Task`"""
        task.status = Status.COMPLETED
        task.save()

        with transaction.atomic():
            for child in task.children:
                CompleteTaskService._complete(child)


class SuspendTaskService(BaseService):
    """This service can be used separately or inside the `TaskStatusUpdateService` to set `Task` status to suspended"""
    def __init__(self,
                 task: Task):
        self._task = task

    def execute(self) -> Any:
        """Executes `SuspendTaskService` service"""
        if not self.suspendable(self._task):
            raise StatusNotAllowed("Task cannot be suspended due to its current status")

    @staticmethod
    def suspendable(task: Task) -> bool:
        """Check if task can be marked as suspended"""
        if task.status != Status.RUNNING:
            return False
        return True
