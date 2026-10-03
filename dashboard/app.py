import streamlit as st
import pandas as pd
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

from workloads.generator import WorkloadGenerator
from workloads.analyzer import WorkloadAnalyzer
from adaptive.decision_engine import AdaptiveDecisionEngine

st.set_page_config(page_title="CPU Scheduler Analyzer", layout="wide")
st.title("Workload-Aware Adaptive CPU Scheduler")

# Sidebar Controls
st.sidebar.header("Workload Configuration")
workload_type = st.sidebar.selectbox("Workload Type", ["short_burst", "long_cpu", "mixed"])
process_count = st.sidebar.slider("Number of Processes", 5, 50, 10)
seed = st.sidebar.number_input("Random Seed", value=42, step=1)

# Generate & Analyze
generator = WorkloadGenerator(seed=seed)
workload = generator.generate(workload_type, count=process_count)
features = WorkloadAnalyzer.analyze(workload)

st.subheader("Workload Analysis")
col1, col2, col3 = st.columns(3)
col1.metric("Process Count", features.get("process_count", 0))
col2.metric("Mean Burst", f"{features.get('mean_burst', 0):.2f}")
col3.metric("Burst Std Dev", f"{features.get('std_burst', 0):.2f}")

# Decision Engine
engine = AdaptiveDecisionEngine()
decision = engine.select_policy(features)

st.subheader("Adaptive Policy Decision")
st.success(f"**Selected Policy:** {decision.selected_policy}")
st.write(decision.explanation)

st.subheader("Policy Suitability Scores")
scores_df = pd.DataFrame(list(decision.scores.items()), columns=["Policy", "Score"])
st.bar_chart(scores_df.set_index("Policy"))