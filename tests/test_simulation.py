from core.process import Process, ProcessState
from core.simulation import CPUSimulation
from schedulers.demo_scheduler import DemoScheduler


def test_simulation_handles_arrivals_and_completion():
    processes = [
        Process(1, 0, 1, [5]),
        Process(2, 2, 1, [3]),
    ]

    result = CPUSimulation(processes, DemoScheduler()).run()

    assert result.end_time == 8
    assert result.completed_processes == 2
    assert result.cpu_busy_time == 8

    assert result.execution_timeline[0].pid == 1
    assert result.execution_timeline[0].start_time == 0
    assert result.execution_timeline[0].end_time == 5

    assert result.execution_timeline[1].pid == 2
    assert result.execution_timeline[1].start_time == 5
    assert result.execution_timeline[1].end_time == 8


def test_simulation_handles_cpu_idle_time():
    processes = [
        Process(1, 4, 1, [3]),
    ]

    result = CPUSimulation(processes, DemoScheduler()).run()

    assert result.end_time == 7
    assert result.cpu_busy_time == 3
    assert result.execution_timeline[0].start_time == 4
    assert result.execution_timeline[0].end_time == 7

    assert any(
        event.event_type == "CPU_IDLE"
        for event in result.events
    )


def test_arrival_event_is_recorded():
    process = Process(1, 2, 1, [4])

    result = CPUSimulation([process], DemoScheduler()).run()

    arrival_events = [
        event for event in result.events
        if event.event_type == "ARRIVAL"
    ]

    assert len(arrival_events) == 1
    assert arrival_events[0].time == 2
    assert arrival_events[0].pid == 1


def test_completion_time_is_stored_on_process():
    process = Process(1, 0, 1, [6])

    result = CPUSimulation([process], DemoScheduler()).run()

    assert process.completion_time == 6
    assert process.state == ProcessState.TERMINATED
    assert result.completed_processes == 1


def test_preemption_hook_can_be_supported():
    class PreemptOnceScheduler(DemoScheduler):
        def __init__(self):
            super().__init__()
            self.preempted = False

        def should_preempt(self, running_process, current_time):
            if not self.preempted and current_time == 2:
                self.preempted = True
                return True
            return False

    processes = [
        Process(1, 0, 1, [5]),
        Process(2, 2, 1, [2]),
    ]

    result = CPUSimulation(
        processes,
        PreemptOnceScheduler(),
    ).run()

    assert any(event.event_type == "PREEMPT" for event in result.events)
    assert result.completed_processes == 2
    assert result.end_time == 7
