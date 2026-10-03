import numpy as np
from typing import Dict, Any
from workloads.models import Workload

class WorkloadAnalyzer:
    @staticmethod
    def analyze(workload: Workload) -> Dict[str, Any]:
        bursts = [p.cpu_bursts[0] for p in workload.processes if p.cpu_bursts]
        priorities = [p.priority for p in workload.processes]

        if not bursts:
            return {}

        q1, q3 = np.percentile(bursts, [25, 75])
        
        return {
            "process_count": len(workload.processes),
            "mean_burst": float(np.mean(bursts)),
            "std_burst": float(np.std(bursts)),
            "min_burst": int(np.min(bursts)),
            "max_burst": int(np.max(bursts)),
            "q1_burst": float(q1),
            "q3_burst": float(q3),
            "priority_std": float(np.std(priorities)),
            "short_ratio": float(np.mean([1 if b <= q1 else 0 for b in bursts])),
            "long_ratio": float(np.mean([1 if b >= q3 else 0 for b in bursts]))
        }