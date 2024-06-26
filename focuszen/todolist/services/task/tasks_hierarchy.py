"""This module provides `Task` hierarchy"""
from typing import List

from ..base import BaseService
from ..entities import Task
from ..dao import TaskDAO


class TasksHierarchyService(BaseService):
    """Provides tasks hierarchy - list of root tasks"""
    def execute(self) -> List[Task]:
        """Executes `TaskHierarchyService` service"""
        _tasks = list(TaskDAO.fetch_all())
        return [task for task in _tasks if task.is_root]
