"""This module provides `DeleteTaskService` unit tests"""

import pytest
import copy

from unittest.mock import Mock

from ...services import DeleteTaskService
from ...services.exceptions import ServiceException, SubtasksExists


class TestDeleteTaskService:
    """Tests for `DeleteTaskService` service"""

    def test_delete_single_task(self, task: Mock):
        """Test successfully deletion"""
        assert DeleteTaskService.deletable(task)

        try:
            DeleteTaskService(task=task).execute()
        except Exception as exc:
            pytest.fail(exc.__class__.__name__)

    def test_delete_task_with_subtasks(self, task: Mock):
        """
        Test deletion with subtasks.
        Task with existing subtasks should not be deleted.
        `DeleteTaskService` in this case should raise `ServiceException`
        """
        task.children = copy.deepcopy(task)
        assert not DeleteTaskService.deletable(task)

        with pytest.raises(ServiceException) as exc:
            DeleteTaskService(task=task).execute()
            assert isinstance(exc, SubtasksExists)
