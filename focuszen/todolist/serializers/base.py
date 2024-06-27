"""This module provides `Task` model DRF serializer"""

from rest_framework import serializers

from ..models import Task


class BaseTaskSerializer(serializers.ModelSerializer):
    """
    This base serializer provides additional calculated fields
    """
    children_planned_effort = serializers.SerializerMethodField()
    """Sum of all subtasks planned efforts"""
    children_actual_effort = serializers.SerializerMethodField()
    """Sum of all subtasks actual efforts"""

    @staticmethod
    def get_children_planned_effort(obj: Task):
        """Counts subtasks planned effort"""
        return sum([child.planned_effort for child in obj.children])

    @staticmethod
    def get_children_actual_effort(obj: Task):
        """Counts subtasks actual effort"""
        return sum([child.actual_effort for child in obj.children if child.actual_effort])
