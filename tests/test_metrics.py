
from core.analysis import analyze_simulation, count_context_switches
from core.metrics import MetricsCalculator
from core.process import Process
from core.simulation import CPUSimulation
from schedulers.fcfs import FCFSScheduler
from schedulers.round_robin import RoundRobinScheduler


def test_waiting_time_is_recorded_from_ready_queue():
    processes = [
        Process(1, 0, 1, [5]),
        Process(2, 0, 1, [3]),
    ]

    result = CPUSimulation(processes, FCFSScheduler()).run()

    assert processes[0].total_waiting_time == 0
    assert processes[1].total_waiting_time == 5


def test_turnaround_response_and_utilization():
    processes = [
        Process(1, 0, 1, [5]),
        Process(2, 0, 1, [3]),
    ]

    result = CPUSimulation(processes, FCFSScheduler()).run()
    analysis = analyze_simulation(result, "FCFS")

    metrics = analysis.metrics

    assert metrics.average_waiting_time == 2.5
    assert metrics.average_turnaround_time == 6.5
    assert metrics.average_response_time == 2.5
    assert metrics.throughput == 2 / 8
    assert metrics.cpu_utilization == 100.0
    assert metrics.context_switches == 1


def test_round_robin_context_switches():
    processes = [
        Process(1, 0, 1, [5]),
        Process(2, 0, 1, [3]),
    ]

    result = CPUSimulation(
        processes,
        RoundRobinScheduler(time_quantum=2),
    ).run()

    assert count_context_switches(result) == 4


def test_starvation_threshold():
    process = Process(1, 0, 1, [2])
    process.add_waiting_time(10)
    process.set_first_start_time(10)
    process.set_completion_time(12)

    metrics = MetricsCalculator(
        processes=[process],
        end_time=12,
        cpu_busy_time=2,
        starvation_threshold=10,
    ).calculate()

    assert metrics.starvation_count == 1


def test_fairness_is_between_zero_and_one():
    processes = [
        Process(1, 0, 1, [2]),
        Process(2, 0, 1, [2]),
    ]

    result = CPUSimulation(processes, FCFSScheduler()).run()
    metrics = MetricsCalculator(
        processes=result.processes,
        end_time=result.end_time,
        cpu_busy_time=result.cpu_busy_time,
    ).calculate()

    assert 0.0 < metrics.fairness_index <= 1.0
