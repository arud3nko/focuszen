"""This module provides `DeleteTaskService` unit tests"""

import pytest
import copy

from unittest.mock import Mock

from ...services import TaskStatusUpdateService
from ...services.exceptions import ServiceException, StatusNotAllowed

from todolist.enums.status_choice import Status


class TestTaskStatusUpdateService:
    """
    Test if `Task` statuses updates correctly.
    `TaskStatusUpdateService` should raise `StatusNotAllowed` exception if status chain is incorrect.
    """

    @pytest.mark.django_db
    def test_update_status_incorrect_chain(self, task: Mock):
        """Test updating `Task` statuses to `Status.COMPLETED` & `Status.SUSPENDED` from incorrect source statuses"""
        for status, new_status in zip([Status.ASSIGNED, Status.SUSPENDED],
                                      [Status.COMPLETED, Status.SUSPENDED]):
            with pytest.raises(ServiceException) as exc:
                task.status = status
                TaskStatusUpdateService(task=task, new_status=new_status).execute()
                assert isinstance(exc, StatusNotAllowed)

    @pytest.mark.django_db
    @pytest.mark.parametrize("new_status", (Status.COMPLETED, Status.SUSPENDED))
    def test_update_status_correct(self, task, new_status):
        task.status = Status.RUNNING
        try:
            TaskStatusUpdateService(task=task, new_status=new_status).execute()
        except Exception as exc:
            pytest.fail(exc.__class__.__name__)

    @pytest.mark.django_db
    def test_recursive_task_completion(self, task: Mock):
        """
        Test updating `Task` with existing subtasks statuses to `Status.COMPLETED`.
        If there's any subtask, that can't be completed (not `Status.RUNNING`), no tasks should be changed.
        If `Task` can be completed, every subtask should be completed too.
        """
        subtask = copy.deepcopy(task)
        task.children = [subtask]

        task.status, subtask.status = Status.RUNNING, Status.RUNNING

        try:
            TaskStatusUpdateService(task=task, new_status=Status.COMPLETED).execute()
        except Exception as exc:
            pytest.fail(exc.__class__.__name__)

        assert task.status == Status.COMPLETED
        assert subtask.status == Status.COMPLETED

        task.status, task.children[0].status = Status.RUNNING, Status.SUSPENDED

        with pytest.raises(ServiceException) as exc:
            TaskStatusUpdateService(task=task, new_status=Status.COMPLETED).execute()
            assert isinstance(exc, StatusNotAllowed)

        assert task.status == Status.RUNNING
        assert subtask.status == Status.SUSPENDED
