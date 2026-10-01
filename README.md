# Workload-Aware Adaptive CPU Scheduler and Performance Analyzer

A Python-based Operating Systems project that simulates CPU scheduling algorithms, measures their performance, and provides the foundation for a workload-aware adaptive scheduling system.

The project uses a **discrete-event CPU simulation** rather than creating real operating-system processes. This makes the behavior reproducible, observable, and suitable for comparing scheduling policies under controlled workloads.

---

## 1. Project Objective

Traditional CPU scheduling algorithms behave differently depending on the workload.

For example:

- FCFS is simple and has low scheduling complexity.
- SJF/SRTF can favor short jobs.
- Round Robin is useful when responsiveness and time-sharing are important.
- Priority Scheduling can prioritize important processes but may require aging to reduce starvation.
- MLFQ dynamically moves processes between priority queues.

The purpose of this project is to build a framework that can:

1. Represent processes and their CPU requirements.
2. Simulate CPU scheduling using discrete events.
3. Implement multiple scheduling algorithms.
4. Measure scheduling performance.
5. Analyze workload characteristics.
6. Select a scheduling policy using a workload-aware decision mechanism.
7. Compare the adaptive policy with conventional scheduling algorithms.
8. Visualize scheduling behavior and performance.

The adaptive component is intended as a **heuristic decision system for experimentation**. It does not claim to mathematically guarantee the globally optimal scheduling policy.

---

# 2. Current Implementation Status

The following core/backend components have been implemented:

- Process model
- Process states
- Scheduler interface
- Discrete-event CPU simulator
- FCFS
- SJF
- SRTF
- Round Robin
- Priority Scheduling
- Priority aging
- MLFQ
- Actual READY-state waiting-time tracking
- Performance metrics
- Context-switch analysis
- Fairness analysis
- Starvation analysis
- Simulation reporting
- Automated tests

The remaining project layer is:

- Workload generation
- Workload input/output
- Workload feature analysis
- Adaptive decision engine
- Experiment runner
- Comparative experiment framework
- Visualization
- Streamlit dashboard
- Final integration

These components can be added without rewriting the existing scheduling backend.

---

# 3. Technology Stack

| Technology | Purpose |
| --- | --- |
| Python | Main programming language |
| NumPy | Numerical calculations |
| Pandas | Result tables and experiment analysis |
| Matplotlib | Gantt charts and performance plots |
| Streamlit | Interactive dashboard |
| pytest | Automated testing |
| Git/GitHub | Version control |

---

# 4. Project Architecture

The intended architecture is:

```text
                    ┌──────────────────────┐
                    │ Workload Generator   │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Workload Analyzer    │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Adaptive Decision     │
                    │ Engine                │
                    └──────────┬───────────┘
                               │
                         Selected Policy
                               │
                               ▼
                    ┌──────────────────────┐
                    │ CPU Simulation Engine │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Metrics & Event Log  │
                    └──────────┬───────────┘
                               │
                  ┌────────────┴────────────┐
                  ▼                         ▼
        ┌──────────────────┐      ┌──────────────────┐
        │ Experiment Runner│      │ Visualization    │
        └────────┬─────────┘      └────────┬─────────┘
                 │                         │
                 └────────────┬────────────┘
                              ▼
                    ┌──────────────────────┐
                    │ Streamlit Dashboard  │
                    └──────────────────────┘
```

---

# 5. Directory Structure

The current/target repository should follow this organization:

```text
adaptive-cpu-scheduler/
│
├── core/
│   ├── __init__.py
│   ├── process.py
│   ├── scheduler.py
│   ├── simulation.py
│   ├── metrics.py
│   ├── analysis.py
│   └── reporting.py
│
├── schedulers/
│   ├── __init__.py
│   ├── fcfs.py
│   ├── sjf.py
│   ├── srtf.py
│   ├── round_robin.py
│   ├── priority.py
│   └── mlfq.py
│
├── workloads/
│   ├── __init__.py
│   ├── models.py
│   ├── generator.py
│   ├── presets.py
│   ├── analyzer.py
│   └── io.py
│
├── adaptive/
│   ├── __init__.py
│   ├── decision_engine.py
│   ├── scoring.py
│   └── explanation.py
│
├── experiments/
│   ├── __init__.py
│   ├── runner.py
│   └── comparison.py
│
├── visualization/
│   ├── __init__.py
│   ├── gantt.py
│   └── charts.py
│
├── dashboard/
│   └── app.py
│
├── tests/
│   ├── test_process.py
│   ├── test_simulation.py
│   ├── test_scheduling_policies.py
│   ├── test_advanced_scheduling.py
│   ├── test_metrics.py
│   ├── test_workloads.py
│   ├── test_workload_io.py
│   ├── test_workload_analyzer.py
│   ├── test_adaptive_engine.py
│   └── test_experiments.py
│
├── data/
│   ├── workloads/
│   └── results/
│
├── main.py
├── requirements.txt
├── .gitignore
└── README.md
```

Some folders such as `workloads/`, `adaptive/`, `experiments/`, `visualization/`, and `dashboard/` may be added by the second project member during final integration.

---

# 6. Process Model

The process model represents a simulated process.

A process contains information such as:

```text
PID
Arrival Time
Priority
CPU Burst(s)
I/O Burst(s)
Current State
First CPU Start
Completion Time
Waiting Time
Response Time
```

Supported process states include:

```text
NEW
READY
RUNNING
BLOCKED
TERMINATED
```

The current CPU simulation primarily operates with single CPU bursts. Multi-burst CPU/I/O simulation can be introduced later without changing the conceptual process model.

---

# 7. Scheduler Interface

All scheduling algorithms follow a common scheduler interface.

The simulator can therefore work with different policies without changing its core simulation logic.

The interface supports operations such as:

```text
add_process()
get_next_process()
should_preempt()
on_dispatch()
next_preemption_time()
```

This separation is important because scheduling policy logic should remain independent from the simulation engine.

---

# 8. Implemented Scheduling Algorithms

## FCFS

First Come First Served.

Characteristics:

- Non-preemptive
- Processes are handled in arrival order
- Simple scheduling policy

---

## SJF

Shortest Job First.

Characteristics:

- Non-preemptive
- Chooses the ready process with the shortest CPU burst
- Useful for studying average waiting behavior

---

## SRTF

Shortest Remaining Time First.

Characteristics:

- Preemptive version of shortest-job scheduling
- Can preempt the running process when a shorter job arrives

---

## Round Robin

Characteristics:

- Preemptive
- Uses a configurable time quantum
- Suitable for studying time-sharing behavior

Example:

```python
RoundRobinScheduler(quantum=4)
```

---

## Priority Scheduling

Characteristics:

- Lower numeric priority value means higher priority
- Supports aging
- Can preempt when a sufficiently high-priority process becomes ready

Example:

```python
PriorityScheduler(aging_interval=5)
```

Aging reduces the possibility of indefinite starvation by improving the effective priority of processes that have waited for a long time.

---

## MLFQ

Multilevel Feedback Queue.

Characteristics:

- Multiple priority queues
- Processes can move between queues
- Higher-priority queues can preempt lower-priority work
- Processes using their complete quantum can be demoted
- Priority boosting can be used to reduce starvation

Default queue quantums are configurable.

Example:

```python
MLFQScheduler(quantums=(2, 4, 8))
```

---

# 9. Discrete-Event Simulation

The project uses a simulation engine rather than real CPU processes.

The simulation maintains:

```text
Process arrivals
Ready queue
Running process
CPU execution
Preemption
Completion
CPU idle periods
```

The simulator records an execution timeline containing segments such as:

```text
P1: 0 → 5
P2: 5 → 8
P3: 8 → 12
```

Adjacent execution segments belonging to the same process are merged when there is no actual ownership change.

This makes the generated Gantt timeline easier to interpret.

---

# 10. Performance Metrics

The performance-analysis layer calculates:

## Waiting Time

Total time a process spends waiting in the READY state.

```text
Waiting Time =
actual accumulated READY-state waiting
```

This includes additional waiting caused by preemption.

---

## Turnaround Time

```text
Turnaround Time =
Completion Time - Arrival Time
```

---

## Response Time

```text
Response Time =
First CPU Start Time - Arrival Time
```

---

## Throughput

```text
Throughput =
Completed Processes / Simulation End Time
```

---

## CPU Utilization

```text
CPU Utilization =
CPU Busy Time / Total Simulation Time × 100
```

---

## Context Switches

Context switches are estimated from changes between adjacent execution segments.

For example:

```text
P1 → P2
```

is a process switch.

---

## Fairness

The project uses Jain's fairness index:

```text
J = (Σx)² / (n × Σx²)
```

The exact quantity represented by `x` must remain documented when interpreting results.

---

## Starvation

Starvation is detected using a configurable waiting-time threshold.

Example:

```text
starvation_threshold = 50
```

A process whose waiting time reaches or exceeds that threshold is counted as a starvation occurrence for the analysis.

The threshold is an experimental parameter, not a universal OS definition.

---

# 11. Running the Current Backend

## Step 1 — Clone the Repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd adaptive-cpu-scheduler
```

---

## Step 2 — Create Virtual Environment

Windows:

```bash
python -m venv .venv
```

Activate:

```bash
.venv\Scripts\activate
```

If PowerShell blocks activation, use:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then activate again:

```powershell
.venv\Scripts\Activate.ps1
```

---

## Step 3 — Install Dependencies

```bash
pip install -r requirements.txt
```

Expected core dependencies include:

```text
numpy
pandas
matplotlib
streamlit
pytest
```

---

# 12. Verify the Installation

Run:

```bash
python -m pytest -q
```

The current completed backend should pass its existing test suite.

The exact number of tests may increase as the workload/adaptive/dashboard components are added.

A successful run should look similar to:

```text
30 passed
```

for the current completed backend version.

---

# 13. Run the Current Demonstration

The project includes `main.py` for backend demonstration/testing.

Run:

```bash
python main.py
```

This can be used to verify that the process model, scheduler implementations, simulator, and reporting layer are functioning.

---

# 14. Running the Final Dashboard

After the remaining dashboard work is integrated:

```bash
streamlit run dashboard/app.py
```

Streamlit will display a local URL, normally similar to:

```text
http://localhost:8501
```

Open the displayed address in your browser.

---

# 15. Expected Dashboard Flow

The final dashboard should follow this workflow:

```text
Select Workload
       ↓
Generate / Load Workload
       ↓
Analyze Workload
       ↓
Display Workload Features
       ↓
Adaptive Decision Engine
       ↓
Select Policy
       ↓
Run Simulation
       ↓
Display Gantt Chart
       ↓
Display Performance Metrics
       ↓
Run Baseline Policies
       ↓
Compare Results
```

---

# 16. Workload Types

The final system should support at least:

### Short-Burst

Mostly short CPU bursts.

Suggested range:

```text
1–5
```

### Long CPU-Bound

Long CPU bursts.

Suggested range:

```text
21–80
```

### I/O-Heavy

Processes with frequent short CPU bursts and I/O activity.

The current simulator's single-CPU-burst limitation must be respected. If actual multi-burst simulation has not yet been implemented, the workload specification can still preserve CPU/I/O burst structure for future integration.

### Mixed

A mixture of short, medium, and long bursts.

### High-Concurrency

Many overlapping processes.

### Priority-Heavy

Large variation in process priorities.

### Changing

Workload characteristics change between phases.

---

# 17. Reproducibility

Experiments should always support explicit random seeds.

Example:

```python
seed = 42
```

The same:

```text
workload type
process count
seed
configuration
```

should produce the same workload.

This is essential for fair comparisons.

For example, all scheduling policies should receive the exact same generated workload when comparing their performance.

---

# 18. Adaptive Decision Engine

The adaptive system should analyze workload characteristics and assign suitability scores to policies.

Conceptually:

```text
Score(policy)
    =
Σ weight(policy, feature) × feature_value
```

Potential features include:

```text
process count
mean CPU burst
burst variation
coefficient of variation
short-burst ratio
long-burst ratio
CPU-bound ratio
I/O-related features
priority dispersion
arrival/concurrency characteristics
```

The system should consider:

```text
FCFS
SJF
SRTF
Round Robin
Priority
MLFQ
```

The selected policy should be accompanied by an explanation.

Example:

```text
Selected Policy: SRTF

Reason:
The workload has substantial CPU-burst variation and a
large proportion of short processes. The workload scoring
model therefore assigns high suitability to a
shortest-remaining-time policy.
```

The explanation should describe the decision without claiming that the selected policy is universally optimal.

---

# 19. Experiment Framework

The final system should automatically run:

```text
FCFS
SJF
SRTF
Round Robin
Priority
MLFQ
Adaptive
```

on the same workload.

Results should be stored in a Pandas DataFrame containing fields such as:

```text
Workload
Seed
Policy
Average Waiting Time
Average Turnaround Time
Average Response Time
Throughput
CPU Utilization
Context Switches
Fairness
Starvation Count
```

---

# 20. Multiple Seeds

For development:

```text
5 seeds
```

is sufficient.

For final experiments:

```text
30 seeds
```

can be used.

For example:

```text
7 workload classes
×
7 policies
×
30 seeds
=
1470 simulation runs
```

This provides a much more meaningful experimental comparison than a single random workload.

---

# 21. Visualization

The final system should provide:

### Gantt Chart

Display CPU execution over time.

### Metric Comparison

Compare policies using charts for:

- waiting time
- turnaround time
- response time
- throughput
- CPU utilization
- context switches
- fairness
- starvation

### Adaptive Scores

Display the decision engine's policy scores.

This helps demonstrate that the adaptive selection is based on measurable workload characteristics.

---

# 22. Data and Result Storage

Recommended structure:

```text
data/
├── workloads/
└── results/
```

Generated workloads can be stored as:

```text
.json
.csv
```

Experiment results can be stored as:

```text
experiment_results.csv
```

Large generated datasets should generally not be committed unless the team explicitly decides that they are required for reproducibility.

---

# 23. Testing

Run the complete test suite with:

```bash
python -m pytest -q
```

Tests should cover:

```text
Process model
Simulation engine
FCFS
SJF
SRTF
Round Robin
Priority
MLFQ
Metrics
Workload generation
Workload I/O
Workload analysis
Adaptive decision engine
Experiment runner
```

Before every major merge:

```bash
python -m pytest -q
```

must pass.

---

# 24. Git Workflow

Create a branch for a feature:

```bash
git checkout -b feature/workload-adaptive-analysis
```

After implementation:

```bash
git add .
git commit -m "feat: add workload adaptive experiment pipeline"
git push origin feature/workload-adaptive-analysis
```

Use small, meaningful commits where practical.

Recommended examples:

```text
feat(workloads): add reproducible workload generator
```

```text
feat(workloads): add workload json and csv io
```

```text
feat(analysis): add workload feature extraction
```

```text
feat(adaptive): add policy suitability scoring
```

```text
feat(adaptive): add workload-based decision engine
```

```text
feat(experiments): add multi-policy experiment runner
```

```text
feat(visualization): add gantt and comparison charts
```

```text
feat(dashboard): add streamlit scheduling dashboard
```

```text
test: add workload and adaptive engine coverage
```

---

# 25. .gitignore

The repository should not commit:

```text
.venv/
__pycache__/
.pytest_cache/
*.pyc
```

A typical `.gitignore` contains:

```gitignore
.venv/
__pycache__/
*.py[cod]
.pytest_cache/
.coverage
htmlcov/
.DS_Store
```

---

# 26. Important Design Rules

## Do not hard-code results

Incorrect:

```python
adaptive_result = 12.4
```

Correct:

```python
adaptive_result = metrics.average_waiting_time
```

---

## Do not hard-code the final winner

The adaptive engine should calculate scores from workload features.

---

## Do not claim universal optimality

Use:

```text
selected by the workload-scoring model
```

instead of:

```text
best scheduler
```

---

## Do not put all logic in Streamlit

The dashboard should call reusable modules.

---

## Do not use machine learning just for decoration

A deterministic feature-based scoring model is sufficient for the initial project.

Machine learning is optional and should only be introduced if there is a meaningful dataset and evaluation methodology.

---

# 27. Academic Positioning

This project is best described as:

> A workload-aware CPU scheduling simulation and performance analysis framework that evaluates conventional scheduling algorithms and investigates adaptive policy selection based on workload characteristics.

It is not:

- a replacement for the Linux scheduler
- a kernel modification
- a real-time production scheduler
- a machine-learning operating system
- a claim of globally optimal scheduling

The project is an experimental and educational scheduling framework.

---

# 28. Recommended Demonstration

For the final presentation:

### Demonstration 1 — Mixed Workload

Generate a seeded mixed workload.

Show:

```text
Workload features
       ↓
Policy scores
       ↓
Selected policy
       ↓
Gantt chart
       ↓
Metrics
```

Then run all baseline algorithms on exactly the same workload.

---

### Demonstration 2 — Different Workload

Change from:

```text
Mixed
```

to:

```text
Long CPU-bound
```

or:

```text
High concurrency
```

Show that the workload characteristics change and the adaptive scoring process responds accordingly.

Do not claim that a policy must always be selected for a workload class. The actual score and selection should come from the implemented decision model.

---

# 29. Research Question

The project can be presented around this research question:

> Can a workload-aware scheduling policy dynamically select or adjust scheduling behavior to improve performance compared with conventional fixed scheduling policies under different workload characteristics?

The experiments should investigate this question using measurable metrics rather than simply assuming that adaptation is better.

---

# 30. Limitations

Current/possible limitations include:

- Single-CPU simulation
- Simplified process model
- Discrete-event abstraction
- Heuristic adaptive scoring
- Configurable starvation threshold rather than a universal starvation definition
- Limited or future multi-burst I/O simulation
- No real kernel modification
- No hardware-level CPU effects
- Context-switch cost may be represented as a metric rather than a full execution delay unless explicitly modeled

These limitations should be documented rather than hidden.

---

# 31. Final Definition of Done

The complete project is ready for final submission when:

- [x] Process model implemented
- [x] Scheduler interface implemented
- [x] Discrete-event simulator implemented
- [x] FCFS implemented
- [x] SJF implemented
- [x] SRTF implemented
- [x] Round Robin implemented
- [x] Priority implemented
- [x] Priority aging implemented
- [x] MLFQ implemented
- [x] Performance metrics implemented
- [x] Context-switch analysis implemented
- [x] Fairness analysis implemented
- [x] Starvation analysis implemented
- [x] Reporting implemented
- [x] Automated backend tests implemented
- [ ] Workload generator integrated
- [ ] Workload I/O integrated
- [ ] Workload analyzer integrated
- [ ] Adaptive decision engine integrated
- [ ] Experiment runner integrated
- [ ] Visualization integrated
- [ ] Streamlit dashboard integrated
- [ ] Final integration tests passing
- [ ] Final README updated
- [ ] Final demo verified

The checked items represent the completed backend work.

---

# 32. Quick Start

Once the repository is complete:

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd adaptive-cpu-scheduler

python -m venv .venv
.venv\Scripts\activate

pip install -r requirements.txt

python -m pytest -q

python main.py

streamlit run dashboard/app.py
```

---

# 33. Team Development Principle

Keep the project modular.

The most important dependency flow is:

```text
Workload
   ↓
Analysis
   ↓
Adaptive Decision
   ↓
Existing Scheduler
   ↓
Existing Simulation Engine
   ↓
Existing Metrics
   ↓
Experiment
   ↓
Visualization
   ↓
Dashboard
```

The existing scheduling backend should remain reusable and independent of the UI.

That separation makes the project easier to test, demonstrate, explain in the viva, and extend in the future.
