import sys
from pathlib import Path

# Ensure project root is in sys.path
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

from typing import Any, Dict

import pandas as pd

from adaptive.decision_engine import AdaptiveDecisionEngine
from core.analysis import analyze_simulation
from core.process import Process
from core.simulation import CPUSimulation
from schedulers.fcfs import FCFSScheduler
from schedulers.mlfq import MLFQScheduler
from schedulers.priority import PriorityScheduler
from schedulers.round_robin import RoundRobinScheduler
from schedulers.sjf import SJFScheduler
from schedulers.srtf import SRTFScheduler
from workloads.analyzer import WorkloadAnalyzer
from workloads.models import Workload


class ExperimentRunner:
    @staticmethod
    def _coerce_process(spec: Any) -> Process:
        pid_value = spec.pid
        if isinstance(pid_value, str):
            digits = "".join(ch for ch in pid_value if ch.isdigit())
            if digits:
                pid_value = int(digits)
            else:
                pid_value = int(pid_value)

        return Process(
            pid=int(pid_value),
            arrival_time=int(spec.arrival_time),
            priority=int(spec.priority),
            cpu_bursts=list(spec.cpu_bursts),
            io_bursts=list(spec.io_bursts or []),
        )

    @staticmethod
    def get_schedulers() -> Dict[str, Any]:
        return {
            "FCFS": FCFSScheduler(),
            "SJF": SJFScheduler(),
            "SRTF": SRTFScheduler(),
            "Round Robin": RoundRobinScheduler(time_quantum=2),
            "Priority": PriorityScheduler(),
            "MLFQ": MLFQScheduler(),
        }

    @classmethod
    def run_comparison(cls, workload: Workload) -> pd.DataFrame:
        if workload is None or not workload.processes:
            return pd.DataFrame(
                columns=[
                    "Workload",
                    "Policy",
                    "Avg Waiting",
                    "Avg Turnaround",
                    "Avg Response",
                    "Throughput",
                    "CPU Utilization",
                    "Context Switches",
                ]
            )

        processes = [cls._coerce_process(spec) for spec in workload.processes]
        results = []

        for name, scheduler in cls.get_schedulers().items():
            result = CPUSimulation(processes, scheduler).run()
            analysis = analyze_simulation(result, scheduler.name)
            metrics = analysis.metrics

            results.append(
                {
                    "Workload": workload.name,
                    "Policy": name,
                    "Avg Waiting": float(metrics.average_waiting_time),
                    "Avg Turnaround": float(metrics.average_turnaround_time),
                    "Avg Response": float(metrics.average_response_time),
                    "Throughput": float(metrics.throughput),
                    "CPU Utilization": float(metrics.cpu_utilization),
                    "Context Switches": int(metrics.context_switches),
                }
            )

        return pd.DataFrame(results)