"""This module provides `Task` model DRF serializer"""

from rest_framework import serializers

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

    def validate_parent(self, value):
        if value and value == self.parent:
            raise serializers.ValidationError("Parent task cannot be set to itself.")
        return value
