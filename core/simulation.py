from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from core.process import Process, ProcessState
from core.scheduler import Scheduler


@dataclass(frozen=True)
class ExecutionSegment:
    """A continuous interval during which one process owns the CPU."""

    pid: int
    start_time: int
    end_time: int

    @property
    def duration(self) -> int:
        return self.end_time - self.start_time


@dataclass(frozen=True)
class SimulationEvent:
    """Record of an important simulation event."""

    time: int
    event_type: str
    pid: int | None = None
    details: str = ""


class SimulationResult:
    """Results produced by a completed CPU simulation."""

    def __init__(
        self,
        execution_timeline: list[ExecutionSegment],
        events: list[SimulationEvent],
        processes: list[Process],
        end_time: int,
    ) -> None:
        self.execution_timeline = execution_timeline
        self.events = events
        self.processes = processes
        self.end_time = end_time

    @property
    def completed_processes(self) -> int:
        return sum(p.is_completed() for p in self.processes)

    @property
    def cpu_busy_time(self) -> int:
        return sum(segment.duration for segment in self.execution_timeline)

    def print_timeline(self) -> None:
        print("CPU Execution Timeline")
        print("-" * 48)

        if not self.execution_timeline:
            print("CPU remained idle.")
            return

        for segment in self.execution_timeline:
            print(
                f"t={segment.start_time:>3} -> "
                f"t={segment.end_time:>3} : P{segment.pid}"
            )

    def print_events(self) -> None:
        print("\nSimulation Events")
        print("-" * 48)

        for event in self.events:
            process_text = f" P{event.pid}" if event.pid is not None else ""
            detail_text = f" - {event.details}" if event.details else ""
            print(
                f"t={event.time:>3} {event.event_type}"
                f"{process_text}{detail_text}"
            )


class CPUSimulation:
    """
    Discrete-event CPU simulation engine.

    The engine is independent of the scheduling policy. It handles arrivals,
    CPU ownership, time progression, dispatch, preemption boundaries,
    completion, and the execution timeline.

    Each process currently contains exactly one CPU burst. Multi-burst/I/O
    behavior can be added later without changing the scheduler interface.
    """

    def __init__(
        self,
        processes: Iterable[Process],
        scheduler: Scheduler,
    ) -> None:
        self._processes = list(processes)
        self._scheduler = scheduler
        self._validate_processes()

        self._arrival_index = sorted(
            range(len(self._processes)),
            key=lambda i: (
                self._processes[i].arrival_time,
                self._processes[i].pid,
            ),
        )
        self._next_arrival_index = 0
        self._current_time = 0
        self._running_process: Process | None = None
        self._ready_since: dict[int, int] = {}

        self._timeline: list[ExecutionSegment] = []
        self._events: list[SimulationEvent] = []

    def _validate_processes(self) -> None:
        seen_pids: set[int] = set()

        for process in self._processes:
            if process.pid in seen_pids:
                raise ValueError(f"Duplicate process ID: {process.pid}")
            seen_pids.add(process.pid)

            if len(process.cpu_bursts) != 1:
                raise NotImplementedError(
                    "The current CPU simulation requires exactly one "
                    "CPU burst per process."
                )

    def _record_event(
        self,
        event_type: str,
        pid: int | None = None,
        details: str = "",
    ) -> None:
        self._events.append(
            SimulationEvent(
                time=self._current_time,
                event_type=event_type,
                pid=pid,
                details=details,
            )
        )

    def _add_arrivals(self) -> None:
        while self._next_arrival_index < len(self._arrival_index):
            process = self._processes[
                self._arrival_index[self._next_arrival_index]
            ]

            if process.arrival_time > self._current_time:
                break

            self._next_arrival_index += 1

            if process.state != ProcessState.NEW:
                continue

            self._scheduler.add_process(process)
            self._ready_since[process.pid] = self._current_time
            self._record_event(
                "ARRIVAL",
                process.pid,
                "Process entered the ready queue",
            )

    def _dispatch(self) -> bool:
        if self._running_process is not None:
            return True

        process = self._scheduler.get_next_process()
        if process is None:
            return False

        self._running_process = process
        process.set_state(ProcessState.RUNNING)

        ready_time = self._ready_since.pop(process.pid, None)
        if ready_time is not None:
            process.add_waiting_time(
                max(0, self._current_time - ready_time)
            )

        if process.first_start_time is None:
            process.set_first_start_time(self._current_time)

        self._scheduler.on_dispatch(process, self._current_time)

        self._record_event(
            "DISPATCH",
            process.pid,
            "Process assigned to the CPU",
        )
        return True

    def _next_arrival_time(self) -> int | None:
        if self._next_arrival_index >= len(self._arrival_index):
            return None

        process = self._processes[
            self._arrival_index[self._next_arrival_index]
        ]
        return process.arrival_time

    def _execute_until(self, end_time: int) -> None:
        if self._running_process is None:
            self._current_time = end_time
            return

        duration = end_time - self._current_time
        if duration <= 0:
            return

        process = self._running_process
        start_time = self._current_time
        process.execute(duration)
        self._current_time = end_time

        if self._timeline:
            last = self._timeline[-1]
            if last.pid == process.pid and last.end_time == start_time:
                self._timeline[-1] = ExecutionSegment(
                    pid=last.pid,
                    start_time=last.start_time,
                    end_time=end_time,
                )
                return

        self._timeline.append(
            ExecutionSegment(
                pid=process.pid,
                start_time=start_time,
                end_time=end_time,
            )
        )

    def _complete_running_process(self) -> None:
        if self._running_process is None:
            return

        process = self._running_process
        if not process.current_cpu_burst_completed():
            return

        process.set_completion_time(self._current_time)
        self._record_event(
            "COMPLETION",
            process.pid,
            "CPU burst completed and process terminated",
        )
        self._running_process = None

    def _preempt_running_process(self, reason: str) -> None:
        if self._running_process is None:
            return

        process = self._running_process

        requeue = getattr(self._scheduler, "requeue_after_preemption", None)
        if callable(requeue):
            requeue(process, self._current_time)
        else:
            process.set_state(ProcessState.READY)
            self._scheduler.add_process(process)

        self._ready_since[process.pid] = self._current_time

        self._record_event(
            "PREEMPT",
            process.pid,
            reason,
        )
        self._running_process = None

    def run(self) -> SimulationResult:
        if not self._processes:
            return SimulationResult([], [], [], 0)

        while True:
            self._add_arrivals()

            if self._running_process is None:
                if not self._dispatch():
                    next_arrival = self._next_arrival_time()
                    if next_arrival is None:
                        break

                    if next_arrival > self._current_time:
                        self._record_event(
                            "CPU_IDLE",
                            details=f"CPU idle until t={next_arrival}",
                        )
                        self._current_time = next_arrival
                    continue

            process = self._running_process
            assert process is not None

            completion_time = (
                self._current_time + process.remaining_burst
            )
            next_arrival = self._next_arrival_time()
            next_policy_boundary = self._scheduler.next_preemption_time(
                process,
                self._current_time,
            )

            candidates = [completion_time]

            if next_arrival is not None:
                candidates.append(next_arrival)

            if (
                next_policy_boundary is not None
                and next_policy_boundary > self._current_time
            ):
                candidates.append(next_policy_boundary)

            next_time = min(candidates)
            self._execute_until(next_time)

            # Completion has priority when the CPU burst ends now.
            if process.current_cpu_burst_completed():
                self._complete_running_process()
                continue

            # Arrivals at this time enter the ready queue before an
            # arrival-driven preemption decision is made.
            self._add_arrivals()

            should_preempt = self._scheduler.should_preempt(
                process,
                self._current_time,
            )

            if should_preempt:
                self._preempt_running_process(
                    "Scheduler requested CPU preemption"
                )

        return SimulationResult(
            execution_timeline=self._timeline,
            events=self._events,
            processes=self._processes,
            end_time=self._current_time,
        )
