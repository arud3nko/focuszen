from __future__ import annotations

from typing import Optional, List

from .task_data import TaskData


class Task(object):
    def __init__(self, data: TaskData = None, parent: Optional[Task] = None):
        self.data:              TaskData = data
        self._parent_task:      Optional[Task] = None
        self._sub_tasks:        List[Task] = []

        if parent:
            self._set_parent(parent)

    def __repr__(self):
        return f"<{self.__class__.__name__} id {self.data.pk} amount of children {len(self.children)}>"

    def __str__(self):
        return self.__repr__()

    @property
    def is_root(self):
        return False if self.parent else True

    @property
    def parent(self) -> Optional[Task]:
        return self._parent_task

    @property
    def children(self) -> Optional[List[Task]]:
        return self._sub_tasks

    @parent.setter
    def parent(self, v: Task):
        self._set_parent(v)

    def _add_children(self, v: Task):
        self._sub_tasks.append(v)

    def _set_parent(self, v: Task):
        self._parent_task = v
        v._add_children(self)


    