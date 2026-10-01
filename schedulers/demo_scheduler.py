from collections import deque
from typing import Optional

from core.process import Process, ProcessState
from core.scheduler import Scheduler


class DemoScheduler(Scheduler):
    """Minimal FIFO implementation used only to verify the foundation."""

    def __init__(self) -> None:
        self._ready_queue: deque[Process] = deque()

    @property
    def name(self) -> str:
        return "Demo Scheduler"

    def add_process(self, process: Process) -> None:
        process.set_state(ProcessState.READY)
        self._ready_queue.append(process)

    def get_next_process(self) -> Optional[Process]:
        if not self._ready_queue:
            return None
        process = self._ready_queue.popleft()
        process.set_state(ProcessState.RUNNING)
        return process

    def should_preempt(self, running_process: Process, current_time: int) -> bool:
        return False
