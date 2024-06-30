"""This module provides `Task` model DRF serializer"""

from rest_framework.exceptions import APIException

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

    def validate(self, attrs):
        """Check if parent is not self"""
        parent = attrs.get('parent')
        if self.instance and parent:
            if parent.pk == self.instance.pk:
                raise APIException("A task cannot be its own parent.")
        if not self.instance and parent and parent.pk == attrs.get('id'):
            raise APIException("A task cannot be its own parent.")
        return attrs
