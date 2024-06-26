"""This module describes base of `todolist` app models"""
from django.db import models
from django.utils import timezone


class BaseModel(models.Model):
    """Base app's model, consists of common attributes"""
    created_at = models.DateTimeField(db_index=True, default=timezone.now)
    """Creation time"""
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
