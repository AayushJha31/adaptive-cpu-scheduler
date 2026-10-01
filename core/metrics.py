
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from core.process import Process


@dataclass(frozen=True)
class ProcessMetrics:
    pid: int
    arrival_time: int
    completion_time: int
    waiting_time: int
    turnaround_time: int
    response_time: int


@dataclass(frozen=True)
class PerformanceMetrics:
    average_waiting_time: float
    average_turnaround_time: float
    average_response_time: float
    throughput: float
    cpu_utilization: float
    context_switches: int
    fairness_index: float
    starvation_count: int


class MetricsCalculator:
    """Calculates performance statistics from a completed simulation."""

    def __init__(
        self,
        processes: Iterable[Process],
        end_time: int,
        cpu_busy_time: int,
        context_switches: int = 0,
        starvation_threshold: int = 50,
    ) -> None:
        self._processes = list(processes)
        self._end_time = end_time
        self._cpu_busy_time = cpu_busy_time
        self._context_switches = context_switches
        self._starvation_threshold = starvation_threshold

        if end_time < 0:
            raise ValueError("end_time must be non-negative")
        if cpu_busy_time < 0:
            raise ValueError("cpu_busy_time must be non-negative")
        if context_switches < 0:
            raise ValueError("context_switches must be non-negative")
        if starvation_threshold < 0:
            raise ValueError("starvation_threshold must be non-negative")

    def process_metrics(self) -> list[ProcessMetrics]:
        result: list[ProcessMetrics] = []

        for process in self._processes:
            if process.completion_time is None:
                raise ValueError(
                    f"Process {process.pid} has not completed."
                )
            if process.response_time is None:
                raise ValueError(
                    f"Process {process.pid} has no response time."
                )

            turnaround = process.completion_time - process.arrival_time

            result.append(
                ProcessMetrics(
                    pid=process.pid,
                    arrival_time=process.arrival_time,
                    completion_time=process.completion_time,
                    waiting_time=process.total_waiting_time,
                    turnaround_time=turnaround,
                    response_time=process.response_time,
                )
            )

        return result

    def calculate(self) -> PerformanceMetrics:
        process_data = self.process_metrics()

        if not process_data:
            return PerformanceMetrics(
                average_waiting_time=0.0,
                average_turnaround_time=0.0,
                average_response_time=0.0,
                throughput=0.0,
                cpu_utilization=0.0,
                context_switches=self._context_switches,
                fairness_index=1.0,
                starvation_count=0,
            )

        count = len(process_data)

        average_waiting = (
            sum(x.waiting_time for x in process_data) / count
        )
        average_turnaround = (
            sum(x.turnaround_time for x in process_data) / count
        )
        average_response = (
            sum(x.response_time for x in process_data) / count
        )

        throughput = (
            count / self._end_time if self._end_time > 0 else 0.0
        )

        cpu_utilization = (
            (self._cpu_busy_time / self._end_time) * 100
            if self._end_time > 0
            else 0.0
        )

        # Jain's fairness index is calculated from completed-process
        # turnaround values. Higher values indicate a more even distribution.
        values = [float(x.turnaround_time) for x in process_data]
        denominator = count * sum(value * value for value in values)
        fairness = (
            (sum(values) ** 2) / denominator
            if denominator > 0
            else 1.0
        )

        starvation_count = sum(
            x.waiting_time >= self._starvation_threshold
            for x in process_data
        )

        return PerformanceMetrics(
            average_waiting_time=average_waiting,
            average_turnaround_time=average_turnaround,
            average_response_time=average_response,
            throughput=throughput,
            cpu_utilization=cpu_utilization,
            context_switches=self._context_switches,
            fairness_index=fairness,
            starvation_count=starvation_count,
        )
