
from core.process import Process
from core.simulation import CPUSimulation
from schedulers.priority import PriorityScheduler
from schedulers.mlfq import MLFQScheduler


def test_priority_selects_higher_priority_process():
    processes = [
        Process(1, 0, 5, [4]),
        Process(2, 0, 1, [2]),
    ]

    result = CPUSimulation(processes, PriorityScheduler()).run()

    assert result.execution_timeline[0].pid == 2


def test_priority_preempts_when_higher_priority_arrives():
    processes = [
        Process(1, 0, 5, [8]),
        Process(2, 2, 1, [2]),
    ]

    result = CPUSimulation(processes, PriorityScheduler()).run()

    assert [
        (s.pid, s.start_time, s.end_time)
        for s in result.execution_timeline
    ] == [
        (1, 0, 2),
        (2, 2, 4),
        (1, 4, 10),
    ]


def test_priority_aging_improves_effective_priority():
    scheduler = PriorityScheduler(aging_interval=2)
    waiting = Process(1, 0, 5, [3])
    running = Process(2, 0, 3, [10])

    scheduler.add_process(waiting)
    scheduler.on_dispatch(running, 0)

    # A priority-5 process becomes effective priority 2 after 6 time units
    # of waiting; the running process has priority 1, so it has not yet
    # overtaken it. At time 9 it reaches effective priority 1.
    assert scheduler.should_preempt(running, 7) is True


def test_mlfq_starts_new_processes_in_top_queue():
    scheduler = MLFQScheduler(quantums=(2, 4, 8))
    p1 = Process(1, 0, 1, [5])

    scheduler.add_process(p1)
    selected = scheduler.get_next_process()

    assert selected is p1
    assert scheduler.name == "MLFQ"


def test_mlfq_demotes_after_quantum():
    scheduler = MLFQScheduler(quantums=(2, 4, 8))
    p1 = Process(1, 0, 1, [8])
    p2 = Process(2, 0, 1, [2])

    scheduler.add_process(p1)
    scheduler.add_process(p2)

    first = scheduler.get_next_process()
    assert first is p1

    assert scheduler.should_preempt(p1, 2) is True
    scheduler.requeue_after_preemption(p1, 2)

    second = scheduler.get_next_process()
    assert second is p2
