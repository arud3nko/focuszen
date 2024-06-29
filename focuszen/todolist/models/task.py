"""This module describes Task Django ORM model"""
from __future__ import annotations

from typing import Literal, Optional, List

from django.db import models

from .base import BaseModel
from ..enums import Status


class Task(BaseModel):
    """Task ORM model"""
    name = models.CharField(max_length=200)
    """Task name field"""
    description = models.TextField()
    """Task description field"""
    status: Literal["assigned", "running", "suspended", "completed"] = models.CharField(choices=Status,
                                                                                        default=Status.ASSIGNED)
    """Task's current status field, may be one of Status literals.
    I annotated the type here to avoid types conflict inside the DAO attributes."""
    planned_effort = models.PositiveIntegerField()
    """Planned time field"""
    performer = models.CharField(max_length=200)
    """Performer field"""
    actual_effort = models.PositiveIntegerField(blank=True, null=True)
    """Actual time field"""
    parent = models.ForeignKey('self', on_delete=models.PROTECT, blank=True, null=True)
    """Parent task field"""

    @property
    def is_root(self) -> bool:
        """If `Task`.parent is None, this `Task` is root"""
        return False if self.parent else True

    @property
    def children(self) -> Optional[List[Task]]:
        """Returns `Task` sub-tasks"""
        return Task.objects.filter(parent=self)
