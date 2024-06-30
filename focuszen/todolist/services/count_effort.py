"""This module provides helper-class `CountSubTasksEffort`"""
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..models import Task


class CountSubTasksEffort:
    """This class provides methods to count subtasks effort"""

    @staticmethod
    def count_planned_effort(obj: Task) -> int:
        """Counts subtasks planned effort"""

        def recursive_sum(task: Task) -> int:
            total = task.planned_effort
            for child in task.children:
                total += recursive_sum(child)
            return total

        return recursive_sum(obj) - obj.planned_effort

    @staticmethod
    def count_actual_effort(obj: Task) -> int:
        """Counts subtasks actual effort"""

        def recursive_sum(task: Task) -> int:
            total = task.actual_effort if task.actual_effort else 0
            for child in task.children:
                total += recursive_sum(child)
            return total

        return recursive_sum(obj) - (obj.actual_effort if obj.actual_effort else 0)
