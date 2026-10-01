from typing import Optional

from core.process import Process, ProcessState
from core.scheduler import Scheduler


class SJFScheduler(Scheduler):
    """Non-preemptive Shortest Job First scheduling."""

    def __init__(self) -> None:
        self._ready_queue: list[Process] = []

    @property
    def name(self) -> str:
        return "SJF"

    def add_process(self, process: Process) -> None:
        process.set_state(ProcessState.READY)
        self._ready_queue.append(process)

    def get_next_process(self) -> Optional[Process]:
        if not self._ready_queue:
            return None

        # Tie-breaking is deterministic:
        # shorter burst -> earlier arrival -> lower PID.
        process = min(
            self._ready_queue,
            key=lambda p: (
                p.remaining_burst,
                p.arrival_time,
                p.pid,
            ),
        )
        self._ready_queue.remove(process)
        process.set_state(ProcessState.RUNNING)
        return process

    def should_preempt(
        self, running_process: Process, current_time: int
    ) -> bool:
        return False
