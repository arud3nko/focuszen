"""This module provides serializer for `Task` with sub-tasks"""

from rest_framework import serializers

from ..models import Task

from .base import BaseTaskSerializer


class NestedTaskSerializer(BaseTaskSerializer):
    """
    Serializer for `Task` model, including nested children tasks
    """

    class Meta:
        model = Task
        fields = "__all__"

    children = serializers.SerializerMethodField()

    @staticmethod
    def get_children(obj):
        """
        Serializes children tasks using the `children` property
        """
        return NestedTaskSerializer(obj.children, many=True).data

    # FIXME this is костыль
    def to_representation(self, instance):
        """Set `children` property to the bottom of the response"""
        ret = super().to_representation(instance)
        children = ret.pop("children")
        ret["children"] = children
        return ret
