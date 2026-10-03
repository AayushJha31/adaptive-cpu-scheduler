from dataclasses import dataclass, field
from typing import List, Dict, Any

@dataclass
class ProcessSpec:
    pid: str
    arrival_time: int
    priority: int
    cpu_bursts: List[int]
    io_bursts: List[int] = field(default_factory=list)

@dataclass
class Workload:
    name: str
    seed: int
    processes: List[ProcessSpec]
    description: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)