
# Workload-Aware Adaptive CPU Scheduler and Performance Analyzer

## Performance Analysis

The simulator now records and calculates:

- Average waiting time
- Average turnaround time
- Average response time
- Throughput
- CPU utilization
- Context switches
- Jain's fairness index
- Starvation count

Waiting time is measured from the time a process enters the READY state until it is dispatched. This includes additional waiting caused by preemption.

### Metric definitions

```text
Turnaround = completion time - arrival time

Response = first CPU start time - arrival time

Throughput = completed processes / simulation end time

CPU utilization = CPU busy time / simulation end time × 100

Jain fairness = (sum(x))² / (n × sum(x²))
```

The current fairness calculation uses process turnaround times as the comparison values. This definition is kept explicit so that experiments can use the same metric consistently.

Starvation is counted using a configurable waiting-time threshold.

## Run

```cmd
.venv\Scripts\activate
pip install -r requirements.txt
python main.py
python -m pytest
```

## Git commit

```text
feat(metrics): add performance analysis and simulation reporting
```
