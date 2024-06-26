"""This module provides `Task` Data Access Object"""
from __future__ import annotations

from typing import Iterable

from functools import cache

from todolist.models import TaskORMModel

from ..entities import TaskData, Task


class TaskDAO:
    """This class provides DAO"""

    @staticmethod
    @cache
    def __orm_to_entity(task_orm: TaskORMModel) -> Task:
        """
        Converts ORM model to `Task` instance. Uses `functools.cache` wrapper to avoid endless recursion.

        :param task_orm: `TaskORMModel` instance
        :return: `Task` instance
        """
        _ = TaskData(pk=task_orm.pk,
                     name=task_orm.name,
                     description=task_orm.description,
                     created_at=task_orm.created_at,
                     updated_at=task_orm.updated_at,
                     status=task_orm.status,
                     planned_effort=task_orm.planned_effort,
                     performer=task_orm.performer,
                     actual_effort=task_orm.actual_effort,
                     parent_pk=task_orm.parent.pk if task_orm.parent else None)
        return Task(data=_, parent=TaskDAO.__orm_to_entity(task_orm.parent) if task_orm.parent else None)

    @staticmethod
    def fetch_all() -> Iterable[Task]:
        """Returns `Task` iterator"""
        _ = map(TaskDAO.__orm_to_entity, TaskORMModel.objects.all())
        TaskDAO.__orm_to_entity.cache_clear()
        return _

    @staticmethod
    def get_by_pk(task_pk: int) -> Task:
        """
        Returns `TaskData` by Primary key

        :param task_pk: Task Primary key
        :return: `TaskData` instance
        """
        return TaskDAO.__orm_to_entity(TaskORMModel.objects.get(pk=task_pk))

    @staticmethod
    def create(task_data: TaskData) -> None:
        """
        Creates new `Task`

        :param task_data: `TaskData` instance
        """
        TaskORMModel.objects.create(name=task_data.name,
                                    description=task_data.description,
                                    status=task_data.status,
                                    planned_effort=task_data.planned_effort,
                                    performer=task_data.performer,
                                    actual_effort=task_data.actual_effort,
                                    parent=TaskORMModel.objects.get(
                                        pk=task_data.parent_pk) if task_data.parent_pk else None)

    @staticmethod
    def update(task_data: TaskData) -> None:
        """
        Updates `Task`

        :param task_data: `TaskData` instance
        """
        task = TaskORMModel.objects.get(pk=task_data.pk)
        task.name = task_data.name
        task.description = task_data.description
        task.status = task_data.status
        task.planned_effort = task_data.planned_effort
        task.performer = task_data.performer
        task.actual_effort = task_data.actual_effort
        task.parent = TaskORMModel.objects.get(pk=task_data.parent_pk) if task_data.parent_pk else None
        task.save()
