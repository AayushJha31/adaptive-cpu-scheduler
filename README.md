
# Workload-Aware Adaptive CPU Scheduler and Performance Analyzer

## CPU Scheduling Policies

The simulator now supports four conventional scheduling policies:

- **FCFS** — First-Come, First-Served
- **SJF** — Shortest Job First
- **SRTF** — Shortest Remaining Time First
- **Round Robin** — configurable time quantum

All policies implement the same scheduler interface and plug into the same discrete-event CPU simulation engine.

### FCFS
Non-preemptive. Processes are selected in ready-queue order.

### SJF
Non-preemptive. Selects the ready process with the smallest current CPU burst.

### SRTF
Preemptive. If a newly ready process has a smaller remaining burst than the running process, the CPU is reassigned.

### Round Robin
Preemptive. Each process receives a configurable time quantum. Quantum expiry is treated as a simulation event, so Round Robin also works when no new process arrives.

## Run

```cmd
.venv\Scripts\activate
pip install -r requirements.txt
python main.py
python -m pytest
```

## Commit

```text
feat(schedulers): implement FCFS SJF SRTF and Round Robin policies
```
