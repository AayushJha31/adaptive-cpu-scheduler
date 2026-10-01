
from __future__ import annotations

from core.analysis import SimulationAnalysis


def format_analysis(analysis: SimulationAnalysis) -> str:
    metrics = analysis.metrics

    lines = [
        f"Scheduler: {analysis.scheduler_name}",
        f"Average waiting time : {metrics.average_waiting_time:.2f}",
        f"Average turnaround   : {metrics.average_turnaround_time:.2f}",
        f"Average response     : {metrics.average_response_time:.2f}",
        f"Throughput           : {metrics.throughput:.4f}",
        f"CPU utilization      : {metrics.cpu_utilization:.2f}%",
        f"Context switches     : {metrics.context_switches}",
        f"Fairness index       : {metrics.fairness_index:.4f}",
        f"Starvation count     : {metrics.starvation_count}",
    ]

    return "\n".join(lines)
