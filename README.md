# Workload-Aware Adaptive CPU Scheduler and Performance Analyzer

## Subtask 1: Python foundation + process model + scheduler interface

### Structure
```text
adaptive-cpu-scheduler/
├── core/
│   ├── __init__.py
│   ├── process.py
│   └── scheduler.py
├── schedulers/
│   ├── __init__.py
│   └── demo_scheduler.py
├── tests/
│   ├── __init__.py
│   └── test_process.py
├── main.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Windows setup with venv

Open CMD in this folder:

```cmd
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Run the foundation:

```cmd
python main.py
```

Run tests:

```cmd
python -m pytest
```

Deactivate:

```cmd
deactivate
```

Do NOT commit `.venv`.

## Expected main output

```text
Workload-Aware Adaptive CPU Scheduler
Subtask 1: project foundation initialized successfully.

Process ID       : 1
Arrival Time     : 0
Priority         : 2
CPU Bursts       : [10, 5]
I/O Bursts       : [4]
Initial State    : NEW
Current CPU Burst: 10

Scheduler        : Demo Scheduler
Next Process     : PID 1
```

## Commit

```text
feat(core): initialize Python scheduler architecture and process model
```

## CPU execution timeline behavior

The timeline records continuous CPU ownership. If another process arrives while the current process continues running, the arrival is recorded as an event but does not split the current execution segment. A segment is split only when CPU ownership actually changes, such as completion or preemption.
