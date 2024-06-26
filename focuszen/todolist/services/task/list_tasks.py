"""This module provides `Task` getter service"""
from typing import List

from ..base import BaseService
from ...models.task import Task


class TaskListService(BaseService):
    """Provides all tasks as a simple list"""
    def execute(self) -> List[Task]:
        """Executes `ListTasksService` service"""
        return list(Task.objects.all())
