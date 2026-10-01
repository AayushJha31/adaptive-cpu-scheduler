from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional

from core.process import Process


class Scheduler(ABC):
    """Common interface that all scheduling policies will implement."""

    @abstractmethod
    def add_process(self, process: Process) -> None:
        pass

    @abstractmethod
    def get_next_process(self) -> Optional[Process]:
        pass

    @abstractmethod
    def should_preempt(
        self, running_process: Process, current_time: int
    ) -> bool:
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name={self.name!r})"
