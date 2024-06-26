"""This module provides base service class to realise `Command` pattern"""

from abc import ABC, abstractmethod

from typing import Any


class BaseService(ABC):
    """Abstract base class for services"""
    @abstractmethod
    def execute(self) -> Any:
        """Abstract method, follows `Command` pattern"""
        pass
