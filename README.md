
# Workload-Aware Adaptive CPU Scheduler and Performance Analyzer

## Advanced CPU Scheduling Policies

The simulator now includes:

- FCFS
- SJF
- SRTF
- Round Robin
- Priority Scheduling with aging
- Multi-Level Feedback Queue (MLFQ)

### Priority Scheduling

Lower numeric priority means higher priority.

A waiting process receives an effective priority improvement after each configured aging interval. This provides an explicit mechanism for reducing starvation.

Example:

```python
PriorityScheduler(aging_interval=5)
```

### MLFQ

New processes start in the highest-priority queue. Each queue has a different time quantum.

Default configuration:

```text
Queue 0 -> quantum 2
Queue 1 -> quantum 4
Queue 2 -> quantum 8
```

Processes that consume their full quantum without completing are demoted. Higher-priority queues can preempt lower-priority running processes.

The design also includes a priority-boost operation that can move waiting processes back to the highest queue.

## Run

```cmd
.venv\Scripts\activate
pip install -r requirements.txt
python main.py
python -m pytest
```

## Git commit

```text
feat(schedulers): add priority scheduling with aging and MLFQ
```
