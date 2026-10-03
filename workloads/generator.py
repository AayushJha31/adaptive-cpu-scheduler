import random
from typing import List
from workloads.models import Workload, ProcessSpec

class WorkloadGenerator:
    def __init__(self, seed: int = 42):
        self.seed = seed

    def generate(self, workload_type: str, count: int = 10) -> Workload:
        rng = random.Random(self.seed)
        processes: List[ProcessSpec] = []

        for i in range(count):
            pid = f"P{i+1}"
            arrival = rng.randint(0, 10)
            priority = rng.randint(0, 10)

            if workload_type == "short_burst":
                bursts = [rng.randint(1, 5)]
            elif workload_type == "long_cpu":
                bursts = [rng.randint(21, 80)]
            elif workload_type == "mixed":
                bursts = [rng.randint(1, 40)]
            else:
                bursts = [rng.randint(1, 20)]

            processes.append(
                ProcessSpec(
                    pid=pid,
                    arrival_time=arrival,
                    priority=priority,
                    cpu_bursts=bursts,
                    io_bursts=[]
                )
            )

        return Workload(name=workload_type, seed=self.seed, processes=processes)