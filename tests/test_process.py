from core.process import Process, ProcessState
from schedulers.demo_scheduler import DemoScheduler


def test_initialization():
    p = Process(1, 0, 2, [10, 5], [4])
    assert p.pid == 1
    assert p.arrival_time == 0
    assert p.priority == 2
    assert p.cpu_bursts == [10, 5]
    assert p.io_bursts == [4]
    assert p.remaining_burst == 10
    assert p.state == ProcessState.NEW


def test_first_start_sets_response_once():
    p = Process(1, 3, 1, [5])
    p.set_first_start_time(8)
    p.set_first_start_time(10)
    assert p.first_start_time == 8
    assert p.response_time == 5


def test_execute():
    p = Process(1, 0, 1, [5])
    p.set_state(ProcessState.RUNNING)
    p.execute(2)
    assert p.remaining_burst == 3
    p.execute(3)
    assert p.current_cpu_burst_completed()


def test_multiple_cpu_bursts():
    p = Process(1, 0, 1, [5, 3], [2])
    p.set_state(ProcessState.RUNNING)
    p.execute(5)
    assert p.move_to_next_cpu_burst() is True
    assert p.remaining_burst == 3
    p.execute(3)
    assert p.move_to_next_cpu_burst() is False
    assert p.is_completed()


def test_demo_scheduler():
    p = Process(7, 0, 1, [4])
    scheduler = DemoScheduler()
    scheduler.add_process(p)
    selected = scheduler.get_next_process()
    assert selected is p
    assert p.state == ProcessState.RUNNING
    assert scheduler.get_next_process() is None
