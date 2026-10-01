
from core.analysis import analyze_simulation
from core.process import Process
from core.reporting import format_analysis
from core.simulation import CPUSimulation
from schedulers.fcfs import FCFSScheduler
from schedulers.round_robin import RoundRobinScheduler


def main() -> None:
    print("Workload-Aware Adaptive CPU Scheduler")
    print("Performance analysis initialized.")
    print()

    workload = [
        (1, 0, 2, [8]),
        (2, 1, 1, [3]),
        (3, 2, 3, [5]),
    ]

    schedulers = [
        FCFSScheduler(),
        RoundRobinScheduler(time_quantum=2),
    ]

    for scheduler in schedulers:
        processes = [
            Process(pid, arrival, priority, bursts)
            for pid, arrival, priority, bursts in workload
        ]

        result = CPUSimulation(processes, scheduler).run()
        analysis = analyze_simulation(result, scheduler.name)

        print("=" * 52)
        print(scheduler.name)
        result.print_timeline()
        print()
        print(format_analysis(analysis))
        print()


if __name__ == "__main__":
    main()
