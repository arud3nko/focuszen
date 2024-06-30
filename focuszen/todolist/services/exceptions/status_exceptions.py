"""This module provides custom exceptions for `TaskStatusUpdateService`"""

from .base import ServiceException


class StatusNotAllowed(ServiceException):
    """Raised when trying to complete a task with uncompleted subtasks or incorrect current status"""
    def __init__(self, msg: str):
        self.msg = msg

    def __str__(self):
        return self.msg
