from core.process import Process
from schedulers.demo_scheduler import DemoScheduler


def main() -> None:
    print("Workload-Aware Adaptive CPU Scheduler")
    print("Subtask 1: project foundation initialized successfully.")
    print()

    process = Process(1, 0, 2, [10, 5], [4])

    print(f"Process ID       : {process.pid}")
    print(f"Arrival Time     : {process.arrival_time}")
    print(f"Priority         : {process.priority}")
    print(f"CPU Bursts       : {process.cpu_bursts}")
    print(f"I/O Bursts       : {process.io_bursts}")
    print(f"Initial State    : {process.state.value}")
    print(f"Current CPU Burst: {process.remaining_burst}")
    print()

    scheduler = DemoScheduler()
    scheduler.add_process(process)
    selected = scheduler.get_next_process()

    print(f"Scheduler        : {scheduler.name}")
    print(
        "Next Process     : PID "
        + (str(selected.pid) if selected else "None")
    )


if __name__ == "__main__":
    main()
