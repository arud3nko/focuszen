"""This module provides helper-class `CountSubTasksEffort`"""
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..models import Task


class CountSubTasksEffort:
    """This class provides methods to count subtasks effort"""

    @staticmethod
    def count_planned_effort(obj: Task):
        """Counts subtasks planned effort"""
        return sum([child.planned_effort for child in obj.children])

    @staticmethod
    def count_actual_effort(obj: Task):
        """Counts subtasks actual effort"""
        return sum([child.actual_effort for child in obj.children if child.actual_effort])
