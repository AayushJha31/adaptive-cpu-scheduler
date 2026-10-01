
from dataclasses import dataclass
from typing import Optional

from core.process import Process, ProcessState
from core.scheduler import Scheduler


@dataclass
class _ReadyEntry:
    process: Process
    ready_since: int = 0


class PriorityScheduler(Scheduler):
    """
    Preemptive priority scheduler with aging.

    Lower numeric priority values represent higher priority.
    Aging improves a waiting process's effective priority over time.
    """

    def __init__(self, aging_interval: int = 5) -> None:
        if aging_interval <= 0:
            raise ValueError("aging_interval must be positive")

        self._aging_interval = aging_interval
        self._ready_queue: list[_ReadyEntry] = []
        self._current_time = 0

    @property
    def name(self) -> str:
        return f"Priority (aging={self._aging_interval})"

    def add_process(self, process: Process) -> None:
        process.set_state(ProcessState.READY)
        self._ready_queue.append(
            _ReadyEntry(process=process, ready_since=self._current_time)
        )

    def _effective_priority(self, entry: _ReadyEntry, current_time: int) -> int:
        waiting_time = max(0, current_time - entry.ready_since)
        aging_steps = waiting_time // self._aging_interval
        return max(0, entry.process.priority - aging_steps)

    def get_next_process(self) -> Optional[Process]:
        if not self._ready_queue:
            return None

        best_index = min(
            range(len(self._ready_queue)),
            key=lambda i: (
                self._ready_queue[i].process.priority,
                self._ready_queue[i].process.arrival_time,
                self._ready_queue[i].process.pid,
            ),
        )

        entry = self._ready_queue.pop(best_index)
        entry.process.set_state(ProcessState.RUNNING)
        return entry.process

    def on_dispatch(self, process: Process, current_time: int) -> None:
        self._current_time = current_time

    def should_preempt(
        self,
        running_process: Process,
        current_time: int,
    ) -> bool:
        self._current_time = current_time

        if not self._ready_queue:
            return False

        best = min(
            self._ready_queue,
            key=lambda entry: (
                self._effective_priority(entry, current_time),
                entry.process.arrival_time,
                entry.process.pid,
            ),
        )

        return (
            self._effective_priority(best, current_time)
            < running_process.priority
        )
