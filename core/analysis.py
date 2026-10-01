
from __future__ import annotations

from dataclasses import dataclass

from core.metrics import MetricsCalculator, PerformanceMetrics
from core.simulation import SimulationResult


@dataclass(frozen=True)
class SimulationAnalysis:
    scheduler_name: str
    metrics: PerformanceMetrics


def count_context_switches(result: SimulationResult) -> int:
    """Count CPU ownership changes in the execution timeline."""
    segments = result.execution_timeline

    if len(segments) <= 1:
        return 0

    return sum(
        segments[index].pid != segments[index - 1].pid
        for index in range(1, len(segments))
    )


def analyze_simulation(
    result: SimulationResult,
    scheduler_name: str,
    starvation_threshold: int = 50,
) -> SimulationAnalysis:
    switches = count_context_switches(result)

    metrics = MetricsCalculator(
        processes=result.processes,
        end_time=result.end_time,
        cpu_busy_time=result.cpu_busy_time,
        context_switches=switches,
        starvation_threshold=starvation_threshold,
    ).calculate()

    return SimulationAnalysis(
        scheduler_name=scheduler_name,
        metrics=metrics,
    )
