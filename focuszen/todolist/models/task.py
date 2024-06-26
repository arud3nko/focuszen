"""This module describes Task Django ORM model"""
from __future__ import annotations

from typing import Literal, Optional, List

from django.db import models

from .base import BaseModel


class Status(models.TextChoices):
    """Task status literals, same as enum"""
    ASSIGNED:   str = "assigned"
    RUNNING:    str = "running"
    SUSPENDED:  str = "suspended"
    COMPLETED:  str = "completed"


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
    planned_effort = models.IntegerField()
    """Planned time field"""
    performer = models.CharField(max_length=200)
    """Performer field"""
    actual_effort = models.IntegerField(blank=True, null=True)
    """Actual time field"""
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True)
    """Parent task field"""

    @property
    def is_root(self):
        return False if self.parent else True

    @property
    def children(self) -> Optional[List[Task]]:
        return Task.objects.filter(parent=self)

