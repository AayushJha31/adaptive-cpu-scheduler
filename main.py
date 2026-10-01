
from core.process import Process
from core.simulation import CPUSimulation
from schedulers.fcfs import FCFSScheduler
from schedulers.sjf import SJFScheduler
from schedulers.srtf import SRTFScheduler
from schedulers.round_robin import RoundRobinScheduler


def main() -> None:
    print("Workload-Aware Adaptive CPU Scheduler")
    print("CPU scheduling policies initialized.")
    print()

    policies = [
        FCFSScheduler(),
        SJFScheduler(),
        SRTFScheduler(),
        RoundRobinScheduler(time_quantum=2),
    ]

    workload = [
        (1, 0, 2, [8]),
        (2, 1, 1, [3]),
        (3, 2, 3, [5]),
    ]

    for scheduler in policies:
        processes = [
            Process(pid, arrival, priority, bursts)
            for pid, arrival, priority, bursts in workload
        ]

        result = CPUSimulation(processes, scheduler).run()

        print(f"{scheduler.name}")
        result.print_timeline()
        print(f"Completion time: {result.end_time}")
        print()


if __name__ == "__main__":
    main()
