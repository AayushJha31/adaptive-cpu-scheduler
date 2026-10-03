import json
import csv
from typing import List
from workloads.models import Workload, ProcessSpec

class WorkloadIO:
    @staticmethod
    def save_json(workload: Workload, filepath: str) -> None:
        data = {
            "name": workload.name,
            "seed": workload.seed,
            "description": workload.description,
            "processes": [
                {
                    "pid": p.pid,
                    "arrival_time": p.arrival_time,
                    "priority": p.priority,
                    "cpu_bursts": p.cpu_bursts,
                    "io_bursts": p.io_bursts
                } for p in workload.processes
            ]
        }
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    @staticmethod
    def load_json(filepath: str) -> Workload:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        processes = [
            ProcessSpec(
                pid=p["pid"],
                arrival_time=p["arrival_time"],
                priority=p["priority"],
                cpu_bursts=p["cpu_bursts"],
                io_bursts=p.get("io_bursts", [])
            ) for p in data["processes"]
        ]
        return Workload(
            name=data["name"],
            seed=data["seed"],
            description=data.get("description", ""),
            processes=processes
        )

    @staticmethod
    def save_csv(workload: Workload, filepath: str) -> None:
        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["pid", "arrival_time", "priority", "cpu_bursts", "io_bursts"])
            for p in workload.processes:
                cpu_s = ";".join(map(str, p.cpu_bursts))
                io_s = ";".join(map(str, p.io_bursts))
                writer.writerow([p.pid, p.arrival_time, p.priority, cpu_s, io_s])

    @staticmethod
    def load_csv(filepath: str, name: str = "loaded_csv", seed: int = 0) -> Workload:
        processes = []
        with open(filepath, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                cpu_bursts = [int(x) for x in row["cpu_bursts"].split(";") if x]
                io_bursts = [int(x) for x in row["io_bursts"].split(";")] if row["io_bursts"] else []
                processes.append(
                    ProcessSpec(
                        pid=row["pid"],
                        arrival_time=int(row["arrival_time"]),
                        priority=int(row["priority"]),
                        cpu_bursts=cpu_bursts,
                        io_bursts=io_bursts
                    )
                )
        return Workload(name=name, seed=seed, processes=processes)