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
    """Immutable-style result container returned by the simulator."""

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
        return sum(process.is_completed() for process in self.processes)

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
                f"t={segment.end_time:>3} : "
                f"P{segment.pid}"
            )

    def print_events(self) -> None:
        print("\nSimulation Events")
        print("-" * 48)

        for event in self.events:
            process_text = f" P{event.pid}" if event.pid is not None else ""
            detail_text = f" - {event.details}" if event.details else ""
            print(f"t={event.time:>3} {event.event_type}{process_text}{detail_text}")


class CPUSimulation:
    """
    Discrete-event CPU simulation engine.

    The scheduler owns ready-queue selection. The simulation engine owns
    time progression, arrivals, CPU execution, dispatching, preemption
    boundaries, and completion.

    The engine currently models one CPU burst per process. The Process model
    already supports multiple CPU bursts; I/O event handling will be added
    when the workload and scheduling layers are expanded.
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
            key=lambda index: (
                self._processes[index].arrival_time,
                self._processes[index].pid,
            ),
        )

        self._next_arrival_index = 0
        self._current_time = 0
        self._running_process: Process | None = None

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
                    "The CPU simulation engine currently requires exactly "
                    "one CPU burst per process."
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
        """Move every process arriving now into the scheduler."""
        while self._next_arrival_index < len(self._arrival_index):
            process = self._processes[self._arrival_index[self._next_arrival_index]]

            if process.arrival_time > self._current_time:
                break

            self._next_arrival_index += 1

            if process.state != ProcessState.NEW:
                continue

            self._scheduler.add_process(process)
            self._record_event(
                "ARRIVAL",
                process.pid,
                "Process entered the ready queue",
            )

    def _dispatch(self) -> bool:
        """Select the next ready process and dispatch it to the CPU."""
        if self._running_process is not None:
            return True

        process = self._scheduler.get_next_process()

        if process is None:
            return False

        self._running_process = process
        process.set_state(ProcessState.RUNNING)

        if process.first_start_time is None:
            process.set_first_start_time(self._current_time)

        self._record_event(
            "DISPATCH",
            process.pid,
            "Process assigned to the CPU",
        )
        return True

    def _next_arrival_time(self) -> int | None:
        if self._next_arrival_index >= len(self._arrival_index):
            return None

        index = self._arrival_index[self._next_arrival_index]
        return self._processes[index].arrival_time

    def _execute_until(self, end_time: int) -> None:
        """Execute the current process until the requested event boundary."""
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

        # An arrival event does not necessarily mean the running process
        # stopped using the CPU. Keep the execution timeline continuous
        # unless the CPU actually changes ownership.
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

    def _preempt_running_process(self) -> None:
        if self._running_process is None:
            return

        process = self._running_process
        process.set_state(ProcessState.READY)
        self._scheduler.add_process(process)

        self._record_event(
            "PREEMPT",
            process.pid,
            "Running process returned to the ready queue",
        )

        self._running_process = None

    def run(self) -> SimulationResult:
        """Run the complete simulation and return its execution history."""
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
                            details=(
                                f"CPU idle until t={next_arrival}"
                            ),
                        )
                        self._current_time = next_arrival

                    continue

            process = self._running_process
            assert process is not None

            completion_time = (
                self._current_time + process.remaining_burst
            )
            next_arrival = self._next_arrival_time()

            if next_arrival is None or completion_time <= next_arrival:
                self._execute_until(completion_time)
                self._complete_running_process()
                continue

            # An arrival happens before the running process completes.
            self._execute_until(next_arrival)
            self._add_arrivals()

            if self._scheduler.should_preempt(
                process,
                self._current_time,
            ):
                self._preempt_running_process()

        return SimulationResult(
            execution_timeline=self._timeline,
            events=self._events,
            processes=self._processes,
            end_time=self._current_time,
        )
