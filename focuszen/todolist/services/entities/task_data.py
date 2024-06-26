"""This is a Task entity, independent of Django ORM model"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Literal
from datetime import datetime


@dataclass
class TaskData:
    """Task Value Object"""
    pk:             int
    """Primary key (aka ID)"""
    name:           str
    """Task name"""
    description:    str
    """Task description"""
    status:         Literal["assigned", "running", "suspended", "completed"]
    """Task's current status"""
    planned_effort: int
    """Planned time - should be counted with self and sub-tasks"""
    performer:     str
    """Performer"""
    created_at:     datetime
    """Creation time"""
    updated_at:     datetime
    """Update time"""
    actual_effort:  Optional[int] = None
    """Actual time"""
    parent_pk:      Optional[int] = None
    """Parent task. If there's no parent, this task is root"""
