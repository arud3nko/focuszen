"""This module provides Status enum"""

from django.db import models


class Status(models.TextChoices):
    """Task status literals, same as enum"""
    ASSIGNED:   str = "assigned"
    RUNNING:    str = "running"
    SUSPENDED:  str = "suspended"
    COMPLETED:  str = "completed"
