"""This module provides `CountSubTasksEffort` unit tests"""

import copy
import random

from unittest.mock import Mock

from ...services import CountSubTasksEffort


class TestCountSubTasksEffort:
    """Tests for `CountSubTasksEffort` service"""

    def test_count_without_subtasks(self, task: Mock):
        """Test `Task` without subtasks effort counting"""
        task.actual_effort = 0
        task.planned_effort = 0

        assert CountSubTasksEffort.count_actual_effort(task) == 0
        assert CountSubTasksEffort.count_planned_effort(task) == 0

    def test_count_subtasks_effort(self, task: Mock):
        """Test `Task` effort counting"""
        task.children = [copy.deepcopy(task), copy.deepcopy(task)]

        task.planned_effort, task.actual_effort = 0, 0

        a, b, c, d = [random.randint(1, 100) for _ in range(4)]

        task.children[0].planned_effort, task.children[-1].planned_effort = a, b
        task.children[0].actual_effort, task.children[-1].actual_effort = c, d

        task.children[-1].children = []

        assert CountSubTasksEffort.count_planned_effort(task) == a + b
        assert CountSubTasksEffort.count_actual_effort(task) == c + d
