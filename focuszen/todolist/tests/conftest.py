"""This configuration provides common fixtures for `pytest` tests"""

import pytest

from typing import Tuple

from unittest.mock import Mock

from todolist.models import Task


@pytest.fixture(scope="function")
def task() -> Mock:
    """Provides `Task` mock without subtasks"""
    task = Mock()
    task.children = []
    return task


@pytest.fixture
def api_client():
    """Provides DRF test API client"""
    from rest_framework.test import APIClient
    return APIClient


@pytest.fixture
def make_task_bakery() -> Tuple[Task, dict]:
    """Provides `Task` instance, saved to DB & it's expected JSON representation"""
    from model_bakery import baker
    _ = baker.make(Task)

    return _, task_to_json(_)


@pytest.fixture
def prepare_task_bakery() -> Tuple[Task, dict]:
    """Provides `Task` instance & it's expected JSON representation"""
    from model_bakery import baker
    _ = baker.prepare(Task)

    return _, task_to_json(_)


@pytest.fixture
def hierarchy() -> Task:
    """Prepare hierarchy for testing"""
    from model_bakery import baker
    _1 = baker.make(Task)
    _2 = baker.make(Task, parent=_1)
    _3 = baker.make(Task, parent=_1)
    _4 = baker.make(Task)
    _5 = baker.make(Task, parent=_2)

    return _1


def task_to_json(task: Task) -> dict:
    """Provides expected JSON dict for testing API endpoints"""
    return {
        'name': task.name,
        'description': task.description,
        'status': task.status,
        'planned_effort': task.planned_effort,
        'actual_effort': task.actual_effort,
        'performer': task.performer,
        'parent': task.parent.id if task.parent else None
    }
