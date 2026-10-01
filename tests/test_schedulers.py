from core.process import Process, ProcessState
from schedulers.fcfs import FCFSScheduler
from schedulers.sjf import SJFScheduler
from schedulers.srtf import SRTFScheduler
from schedulers.round_robin import RoundRobinScheduler


def test_fcfs_uses_arrival_order():
    p1 = Process(1, 0, 1, [5])
    p2 = Process(2, 1, 1, [2])

    scheduler = FCFSScheduler()
    scheduler.add_process(p1)
    scheduler.add_process(p2)

    assert scheduler.get_next_process() is p1
    assert scheduler.get_next_process() is p2


def test_sjf_selects_shortest_ready_burst():
    long_job = Process(1, 0, 1, [10])
    short_job = Process(2, 0, 1, [3])

    scheduler = SJFScheduler()
    scheduler.add_process(long_job)
    scheduler.add_process(short_job)

    assert scheduler.get_next_process() is short_job
    assert scheduler.get_next_process() is long_job


def test_srtf_preempts_for_shorter_remaining_time():
    running = Process(1, 0, 1, [8])
    short_job = Process(2, 3, 1, [2])

    running.set_state(ProcessState.RUNNING)

    scheduler = SRTFScheduler()
    scheduler.add_process(short_job)

    assert scheduler.should_preempt(running, 3) is True


def test_srtf_does_not_preempt_for_longer_job():
    running = Process(1, 0, 1, [4])
    long_job = Process(2, 3, 1, [8])

    running.set_state(ProcessState.RUNNING)

    scheduler = SRTFScheduler()
    scheduler.add_process(long_job)

    assert scheduler.should_preempt(running, 3) is False


def test_round_robin_quantum():
    process = Process(1, 0, 1, [10])
    scheduler = RoundRobinScheduler(time_quantum=3)

    scheduler.add_process(process)
    selected = scheduler.get_next_process()

    assert selected is process
    assert scheduler.should_preempt(process, 0) is False
    assert scheduler.should_preempt(process, 2) is False
    assert scheduler.should_preempt(process, 3) is True


def test_round_robin_requeues_preempted_process():
    p1 = Process(1, 0, 1, [8])
    p2 = Process(2, 0, 1, [3])

    scheduler = RoundRobinScheduler(time_quantum=2)
    scheduler.add_process(p1)
    scheduler.add_process(p2)

    first = scheduler.get_next_process()
    assert first is p1

    assert scheduler.should_preempt(p1, 2) is True
    scheduler.requeue_after_preemption(p1)

    second = scheduler.get_next_process()
    assert second is p2
