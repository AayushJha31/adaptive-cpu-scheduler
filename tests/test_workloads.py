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