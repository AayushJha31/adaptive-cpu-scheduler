
from core.process import Process
from core.simulation import CPUSimulation
from schedulers.fcfs import FCFSScheduler
from schedulers.sjf import SJFScheduler
from schedulers.srtf import SRTFScheduler
from schedulers.round_robin import RoundRobinScheduler


def run(processes, scheduler):
    return CPUSimulation(processes, scheduler).run()


def test_fcfs_execution_order():
    result = run(
        [Process(1, 0, 1, [5]), Process(2, 0, 1, [2])],
        FCFSScheduler(),
    )

    assert [s.pid for s in result.execution_timeline] == [1, 2]
    assert result.end_time == 7


def test_sjf_selects_shortest_job():
    result = run(
        [Process(1, 0, 1, [5]), Process(2, 0, 1, [2])],
        SJFScheduler(),
    )

    assert result.execution_timeline[0].pid == 2
    assert result.execution_timeline[0].start_time == 0
    assert result.execution_timeline[0].end_time == 2


def test_srtf_preempts_when_shorter_process_arrives():
    result = run(
        [Process(1, 0, 1, [8]), Process(2, 2, 1, [2])],
        SRTFScheduler(),
    )

    assert [(s.pid, s.start_time, s.end_time) for s in result.execution_timeline] == [
        (1, 0, 2),
        (2, 2, 4),
        (1, 4, 10),
    ]


def test_round_robin_respects_time_quantum_without_arrivals():
    result = run(
        [Process(1, 0, 1, [5]), Process(2, 0, 1, [3])],
        RoundRobinScheduler(time_quantum=2),
    )

    assert [
        (s.pid, s.start_time, s.end_time)
        for s in result.execution_timeline
    ] == [
        (1, 0, 2),
        (2, 2, 4),
        (1, 4, 6),
        (2, 6, 7),
        (1, 7, 8),
    ]
    assert result.end_time == 8
