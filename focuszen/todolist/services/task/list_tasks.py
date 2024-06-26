"""This module provides `Task` getter service"""
from typing import List

from ..base import BaseService
from ..entities import Task
from ..dao import TaskDAO


class ListTasksService(BaseService):
    """Provides all tasks list"""
    def execute(self) -> List[Task]:
        """Executes `ListTasksService` service"""
        return list(TaskDAO.fetch_all())
