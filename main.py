from core.process import Process
from core.simulation import CPUSimulation
from schedulers.demo_scheduler import DemoScheduler


def main() -> None:
    print("Workload-Aware Adaptive CPU Scheduler")
    print("CPU simulation engine initialized successfully.")
    print()

    processes = [
        Process(1, 0, 1, [5]),
        Process(2, 2, 1, [3]),
    ]

    result = CPUSimulation(processes, DemoScheduler()).run()
    result.print_timeline()
    print()
    print(f"Completed Processes : {result.completed_processes}")
    print(f"CPU Busy Time       : {result.cpu_busy_time}")
    print(f"Simulation End Time : {result.end_time}")


if __name__ == "__main__":
    main()
