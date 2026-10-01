from collections import deque
from typing import Optional

from core.process import Process, ProcessState
from core.scheduler import Scheduler


class RoundRobinScheduler(Scheduler):
    """Preemptive Round Robin scheduling with a configurable time quantum."""

    def __init__(self, time_quantum: int = 2) -> None:
        if time_quantum <= 0:
            raise ValueError("time_quantum must be positive")

        self._time_quantum = time_quantum
        self._ready_queue: deque[Process] = deque()
        self._quantum_start: int | None = 0

    @property
    def name(self) -> str:
        return f"Round Robin (q={self._time_quantum})"

    @property
    def time_quantum(self) -> int:
        return self._time_quantum

    def add_process(self, process: Process) -> None:
        process.set_state(ProcessState.READY)
        self._ready_queue.append(process)

    def get_next_process(self) -> Optional[Process]:
        if not self._ready_queue:
            return None

        process = self._ready_queue.popleft()
        process.set_state(ProcessState.RUNNING)
        return process

    def on_dispatch(self, process: Process, current_time: int) -> None:
        self._quantum_start = current_time

    def next_preemption_time(
        self,
        running_process: Process,
        current_time: int,
    ) -> int | None:
        if self._quantum_start is None:
            return current_time + self._time_quantum

        return self._quantum_start + self._time_quantum

    def requeue_after_preemption(self, process: Process) -> None:
        process.set_state(ProcessState.READY)
        self._ready_queue.append(process)
        self._quantum_start = None

    def should_preempt(
        self,
        running_process: Process,
        current_time: int,
    ) -> bool:
        if self._quantum_start is None:
            return False

        return current_time >= self._quantum_start + self._time_quantum
