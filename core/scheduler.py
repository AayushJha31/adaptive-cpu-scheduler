from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional

from core.process import Process


class Scheduler(ABC):
    """Common interface implemented by every CPU scheduling policy."""

    @abstractmethod
    def add_process(self, process: Process) -> None:
        """Place a newly available process into the ready queue."""

    @abstractmethod
    def get_next_process(self) -> Optional[Process]:
        """Select the next ready process for CPU execution."""

    @abstractmethod
    def should_preempt(
        self,
        running_process: Process,
        current_time: int,
    ) -> bool:
        """Return True when the running process should be preempted."""

    def on_dispatch(self, process: Process, current_time: int) -> None:
        """Notify a scheduler that a process has just been dispatched."""
        return None

    def next_preemption_time(
        self,
        running_process: Process,
        current_time: int,
    ) -> int | None:
        """
        Return the next scheduler-controlled preemption boundary.

        Policies such as Round Robin use this to request a quantum-expiry
        check even when no new process arrives.
        """
        return None

    @property
    @abstractmethod
    def name(self) -> str:
        """Human-readable scheduler name."""

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name={self.name!r})"
