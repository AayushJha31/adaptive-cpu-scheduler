from workloads.generator import WorkloadGenerator
from workloads.analyzer import WorkloadAnalyzer
from adaptive.decision_engine import AdaptiveDecisionEngine

def test_workload_reproducibility():
    g1 = WorkloadGenerator(seed=42).generate("mixed", count=10)
    g2 = WorkloadGenerator(seed=42).generate("mixed", count=10)
    assert g1 == g2

def test_adaptive_engine():
    generator = WorkloadGenerator(seed=42)
    workload = generator.generate("mixed", count=10)
    features = WorkloadAnalyzer.analyze(workload)
    
    engine = AdaptiveDecisionEngine()
    result = engine.select_policy(features)
    
    assert result.selected_policy in result.scores
    assert len(result.explanation) > 0

def test_experiment_runner_runs_each_policy_on_fresh_processes_and_adaptive():
    from experiments.runner import ExperimentRunner

    workload = WorkloadGenerator(seed=42).generate("mixed", count=6)
    results = ExperimentRunner.run_comparison(workload)

    assert len(results) == 7
    assert set(results["Policy"]) == {
        "FCFS", "SJF", "SRTF", "Round Robin", "Priority", "MLFQ", "Adaptive"
    }
    adaptive_row = results[results["Policy"] == "Adaptive"].iloc[0]
    assert adaptive_row["Adaptive Selection"] in {
        "FCFS", "SJF", "SRTF", "Round Robin", "Priority", "MLFQ"
    }
    assert (results["Avg Turnaround"] > 0).all()
