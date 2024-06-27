"""This module provides custom exceptions for `TaskStatusUpdateService`"""

from .base import ServiceException


class IncorrectCompletion(ServiceException):
    """Raised when trying to complete a task with uncompleted subtasks or incorrect current status"""
    def __str__(self):
        return "Current task status is incorrect or task has uncompleted subtasks"
