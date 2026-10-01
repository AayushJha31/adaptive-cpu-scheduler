
from core.process import Process
from core.simulation import CPUSimulation
from schedulers.mlfq import MLFQScheduler
from schedulers.priority import PriorityScheduler


def main() -> None:
    print("Workload-Aware Adaptive CPU Scheduler")
    print("Advanced scheduling policies initialized.")
    print()

    workload = [
        Process(1, 0, 5, [8]),
        Process(2, 1, 2, [3]),
        Process(3, 2, 4, [5]),
    ]

    for scheduler_class in (PriorityScheduler, MLFQScheduler):
        processes = [
            Process(
                p.pid,
                p.arrival_time,
                p.priority,
                p.cpu_bursts,
                p.io_bursts,
            )
            for p in workload
        ]

        scheduler = scheduler_class()
        result = CPUSimulation(processes, scheduler).run()

        print(scheduler.name)
        result.print_timeline()
        print(f"Completion time: {result.end_time}")
        print()


if __name__ == "__main__":
    main()
