"""This module provides hierarchical view of tasks list"""

from rest_framework import mixins, viewsets

from ..models import Task
from ..serializers import NestedTaskSerializer


class TasksHierarchyViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    A simple ListAPIView for viewing tasks hierarchy
    """
    queryset = Task.objects.filter(parent=None)  # I filter here only root tasks to make tasks hierarchy
    serializer_class = NestedTaskSerializer


class SingleTaskHierarchyViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    A single `Task` hierarchy view
    """
    queryset = Task.objects.all()
    serializer_class = NestedTaskSerializer
