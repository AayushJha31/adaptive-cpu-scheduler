from __future__ import annotations

from enum import Enum
from typing import Sequence


class ProcessState(Enum):
    NEW = "NEW"
    READY = "READY"
    RUNNING = "RUNNING"
    BLOCKED = "BLOCKED"
    TERMINATED = "TERMINATED"


class Process:
    """Process model for the CPU scheduling simulator."""

    def __init__(
        self,
        pid: int,
        arrival_time: int,
        priority: int,
        cpu_bursts: Sequence[int],
        io_bursts: Sequence[int] | None = None,
    ) -> None:
        if pid < 0:
            raise ValueError("pid must be non-negative")
        if arrival_time < 0:
            raise ValueError("arrival_time must be non-negative")
        if not cpu_bursts:
            raise ValueError("A process needs at least one CPU burst")
        if any(x <= 0 for x in cpu_bursts):
            raise ValueError("CPU bursts must be positive")

        self._pid = pid
        self._arrival_time = arrival_time
        self._priority = priority
        self._cpu_bursts = list(cpu_bursts)
        self._io_bursts = list(io_bursts or [])

        if any(x <= 0 for x in self._io_bursts):
            raise ValueError("I/O bursts must be positive")
        if len(self._io_bursts) > len(self._cpu_bursts) - 1:
            raise ValueError("Too many I/O bursts for the CPU bursts")

        self._current_cpu_burst = 0
        self._remaining_burst = self._cpu_bursts[0]
        self._state = ProcessState.NEW
        self._first_start_time: int | None = None
        self._completion_time: int | None = None
        self._total_waiting_time = 0
        self._response_time: int | None = None

    @property
    def pid(self) -> int:
        return self._pid

    @property
    def arrival_time(self) -> int:
        return self._arrival_time

    @property
    def priority(self) -> int:
        return self._priority

    @property
    def cpu_bursts(self) -> list[int]:
        return self._cpu_bursts.copy()

    @property
    def io_bursts(self) -> list[int]:
        return self._io_bursts.copy()

    @property
    def current_cpu_burst_index(self) -> int:
        return self._current_cpu_burst

    @property
    def remaining_burst(self) -> int:
        return self._remaining_burst

    @property
    def state(self) -> ProcessState:
        return self._state

    @property
    def first_start_time(self) -> int | None:
        return self._first_start_time

    @property
    def completion_time(self) -> int | None:
        return self._completion_time

    @property
    def total_waiting_time(self) -> int:
        return self._total_waiting_time

    @property
    def response_time(self) -> int | None:
        return self._response_time

    def set_state(self, state: ProcessState) -> None:
        self._state = state

    def set_first_start_time(self, time: int) -> None:
        if time < 0:
            raise ValueError("time must be non-negative")
        if self._first_start_time is None:
            self._first_start_time = time
            self._response_time = time - self._arrival_time

    def set_completion_time(self, time: int) -> None:
        if time < 0:
            raise ValueError("time must be non-negative")
        self._completion_time = time
        self._state = ProcessState.TERMINATED

    def add_waiting_time(self, duration: int) -> None:
        if duration < 0:
            raise ValueError("duration must be non-negative")
        self._total_waiting_time += duration

    def execute(self, duration: int = 1) -> None:
        if duration <= 0:
            raise ValueError("duration must be positive")
        if self._state != ProcessState.RUNNING:
            raise RuntimeError("Only a RUNNING process can execute")
        if duration > self._remaining_burst:
            raise ValueError("Execution exceeds remaining CPU burst")
        self._remaining_burst -= duration

    def current_cpu_burst_completed(self) -> bool:
        return self._remaining_burst == 0

    def move_to_next_cpu_burst(self) -> bool:
        if not self.current_cpu_burst_completed():
            raise RuntimeError("Current CPU burst is not completed")

        self._current_cpu_burst += 1
        if self._current_cpu_burst >= len(self._cpu_bursts):
            self._state = ProcessState.TERMINATED
            return False

        self._remaining_burst = self._cpu_bursts[self._current_cpu_burst]
        return True

    def is_completed(self) -> bool:
        return self._state == ProcessState.TERMINATED

    def __repr__(self) -> str:
        return (
            f"Process(pid={self._pid}, arrival={self._arrival_time}, "
            f"priority={self._priority}, state={self._state.value}, "
            f"remaining={self._remaining_burst})"
        )
