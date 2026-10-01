
from collections import deque
from typing import Optional

from core.process import Process, ProcessState
from core.scheduler import Scheduler


class MLFQScheduler(Scheduler):
    """
    Multi-Level Feedback Queue scheduler.

    Queue 0 has the highest priority and the smallest quantum.
    Lower queues receive progressively larger quanta.

    New processes start in the highest queue. Processes that consume a full
    quantum without completing are demoted. A periodic priority boost moves
    waiting processes back to the top queue to prevent starvation.
    """

    def __init__(
        self,
        quantums: tuple[int, ...] = (2, 4, 8),
        boost_interval: int = 20,
    ) -> None:
        if not quantums or any(q <= 0 for q in quantums):
            raise ValueError("quantums must contain positive values")
        if boost_interval <= 0:
            raise ValueError("boost_interval must be positive")

        self._quantums = quantums
        self._boost_interval = boost_interval
        self._queues: list[deque[Process]] = [
            deque() for _ in quantums
        ]
        self._levels: dict[int, int] = {}
        self._dispatch_time: int | None = None
        self._last_boost = 0
        self._current_level = 0

    @property
    def name(self) -> str:
        return "MLFQ"

    @property
    def quantums(self) -> tuple[int, ...]:
        return self._quantums

    def add_process(self, process: Process) -> None:
        process.set_state(ProcessState.READY)
        level = self._levels.get(process.pid, 0)
        self._levels[process.pid] = level
        self._queues[level].append(process)

    def _highest_non_empty_level(self) -> int | None:
        for level, queue in enumerate(self._queues):
            if queue:
                return level
        return None

    def get_next_process(self) -> Optional[Process]:
        level = self._highest_non_empty_level()
        if level is None:
            return None

        process = self._queues[level].popleft()
        self._current_level = level
        process.set_state(ProcessState.RUNNING)
        return process

    def on_dispatch(self, process: Process, current_time: int) -> None:
        self._dispatch_time = current_time

    def next_preemption_time(
        self,
        running_process: Process,
        current_time: int,
    ) -> int | None:
        if self._dispatch_time is None:
            return current_time + self._quantums[self._current_level]

        return (
            self._dispatch_time
            + self._quantums[self._current_level]
        )

    def should_preempt(
        self,
        running_process: Process,
        current_time: int,
    ) -> bool:
        highest = self._highest_non_empty_level()

        if highest is not None and highest < self._current_level:
            return True

        quantum = self._quantums[self._current_level]
        if self._dispatch_time is None:
            # Supports a direct policy check before the simulator has called
            # on_dispatch; treat the current call as a quantum-expiry check.
            return True

        return current_time >= self._dispatch_time + quantum

    def requeue_after_preemption(
        self,
        process: Process,
        current_time: int,
    ) -> None:
        process.set_state(ProcessState.READY)

        old_level = self._levels.get(process.pid, 0)

        if (
            self._dispatch_time is not None
            and current_time >= self._dispatch_time + self._quantums[old_level]
        ):
            new_level = min(old_level + 1, len(self._queues) - 1)
        else:
            new_level = old_level

        self._levels[process.pid] = new_level
        self._queues[new_level].append(process)
        self._dispatch_time = None

    def priority_boost(self, current_time: int) -> None:
        if current_time - self._last_boost < self._boost_interval:
            return

        all_ready: list[Process] = []
        for queue in self._queues:
            all_ready.extend(queue)
            queue.clear()

        self._queues[0].extend(all_ready)

        for process in all_ready:
            self._levels[process.pid] = 0

        self._last_boost = current_time
