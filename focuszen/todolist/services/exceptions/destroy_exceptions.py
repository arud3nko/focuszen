"""This module provides custom exceptions for `DeleteTaskService`"""

from .base import ServiceException


class SubtasksExists(ServiceException):
    """Raised when trying to delete a task with existing subtasks"""
    def __str__(self):
        return "Current task cannot be deleted due to existing subtasks"
