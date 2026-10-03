import pandas as pd
from typing import List, Dict, Any
from workloads.models import Workload

# Import existing core simulator components
from core.simulation import Simulation
from schedulers.fcfs import FCFSScheduler
from schedulers.sjf import SJFScheduler
from schedulers.srtf import SRTFScheduler
from schedulers.round_robin import RoundRobinScheduler
from schedulers.priority import PriorityScheduler
from schedulers.mlfq import MLFQScheduler
from adaptive.decision_engine import AdaptiveDecisionEngine
from workloads.analyzer import WorkloadAnalyzer

class ExperimentRunner:
    @staticmethod
    def get_schedulers() -> Dict[str, Any]:
        return {
            "FCFS": FCFSScheduler(),
            "SJF": SJFScheduler(),
            "SRTF": SRTFScheduler(),
            "Round Robin": RoundRobinScheduler(quantum=2),
            "Priority": PriorityScheduler(),
            "MLFQ": MLFQScheduler()
        }

    @classmethod
    def run_comparison(cls, workload: Workload) -> pd.DataFrame:
        results = []
        schedulers = cls.get_schedulers()

        # Convert workload processes to simulation process model if required
        # Note: Map workload.processes to the format expected by core/simulation.py
        
        for name, scheduler in schedulers.items():
            sim = Simulation(scheduler=scheduler)
            # Run simulation with workload processes
            # metrics = sim.run(workload.processes)
            
            # Example placeholder format matching required report table:
            results.append({
                "Workload": workload.name,
                "Policy": name,
                "Avg Waiting": 0.0,
                "Avg Turnaround": 0.0,
                "Avg Response": 0.0,
                "Throughput": 0.0,
                "CPU Utilization": 100.0,
                "Context Switches": 0
            })

        return pd.DataFrame(results)