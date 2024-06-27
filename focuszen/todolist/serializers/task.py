"""This module provides `Task` model DRF serializer"""

from ..models import Task

from .base import BaseTaskSerializer


class TaskSerializer(BaseTaskSerializer):
    """
    Serializer for `Task` model
    Currently serializes all fields
    """
    class Meta:
        model = Task
        fields = "__all__"
