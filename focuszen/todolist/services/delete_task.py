from __future__ import annotations

from typing import Any, TYPE_CHECKING

from .base import BaseService
from .exceptions import SubtasksExists

if TYPE_CHECKING:
    from ..models import Task


class DeleteTaskService(BaseService):
    """This service is being used to check if `Task` can be deleted"""
    def __init__(self, task: Task):
        self._task = task

    def execute(self) -> Any:
        if not self.deletable(self._task):
            raise SubtasksExists("Task has children, please delete them first")

    @staticmethod
    def deletable(task: Task) -> bool:
        """Check if task can be deleted"""
        return not task.children
