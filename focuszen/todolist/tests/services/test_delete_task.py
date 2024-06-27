"""This module provides `DeleteTaskService` unit tests"""

import pytest

from unittest.mock import Mock

from django.test import TestCase

from ...services import DeleteTaskService
from ...services.exceptions import ServiceException, SubtasksExists


class TestDeleteTaskService:
    """Tests for `DeleteTaskService` service"""

    @pytest.fixture(scope="function")
    def single_task(self) -> Mock:
        """Provides `Task` mock without subtasks"""
        task = Mock()
        task.children = []
        return task

    @pytest.fixture(scope="function")
    def task_with_subtasks(self) -> Mock:
        """Provides `Task` mock with subtasks"""
        task = Mock()
        task.children = [Mock()]
        return task

    def test_delete_single_task(self, single_task):
        """Test successfully deletion"""
        assert DeleteTaskService.deletable(single_task)

        try:
            DeleteTaskService(task=single_task).execute()
        except Exception as exc:
            pytest.fail(exc.__class__.__name__)

    def test_delete_task_with_subtasks(self, task_with_subtasks):
        """
        Test deletion with subtasks.
        Task with existing subtasks should not be deleted.
        `DeleteTaskService` in this case should raise `ServiceException`
        """
        assert not DeleteTaskService.deletable(task_with_subtasks)

        with pytest.raises(ServiceException) as exc:
            DeleteTaskService(task=task_with_subtasks).execute()
            assert isinstance(exc, SubtasksExists)
