"""This module provides `Task` creation service"""
from ..base import BaseService
from ..entities import TaskData
from ..dao import TaskDAO


class NewTaskService(BaseService):
    """Service to create a new task"""
    def __init__(self, task_data: TaskData):
        self.task_data = task_data

    def execute(self) -> None:
        """Executes `NewTaskService` service"""
        return TaskDAO.create(task_data=self.task_data)
