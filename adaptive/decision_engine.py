from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class DecisionResult:
    selected_policy: str
    scores: Dict[str, float]
    features: Dict[str, Any]
    explanation: str

class AdaptiveDecisionEngine:
    def select_policy(self, features: Dict[str, Any]) -> DecisionResult:
        mean_b = features.get("mean_burst", 0)
        std_b = features.get("std_burst", 0)
        p_std = features.get("priority_std", 0)

        scores = {
            "FCFS": 50.0,
            "SJF": 50.0 + (std_b * 2.0),
            "SRTF": 50.0 + (std_b * 2.5),
            "Round Robin": 50.0 + (features.get("short_ratio", 0) * 30),
            "Priority": 50.0 + (p_std * 10),
            "MLFQ": 60.0 + (std_b * 1.5)
        }

        selected_policy = max(scores, key=scores.get)

        explanation = (
            f"The selected policy is '{selected_policy}' based on the heuristic scoring model. "
            f"Workload features show a mean burst of {mean_b:.2f} and a burst variation (std) of {std_b:.2f}."
        )

        return DecisionResult(
            selected_policy=selected_policy,
            scores=scores,
            features=features,
            explanation=explanation
        )