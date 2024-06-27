"""This configuration provides common fixtures for `pytest` tests"""

import pytest

from unittest.mock import Mock


@pytest.fixture(scope="function")
def task() -> Mock:
    """Provides `Task` mock without subtasks"""
    task = Mock()
    task.children = []
    return task
