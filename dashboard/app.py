import os
import sys
from pathlib import Path

# Get project root (parent directory of 'dashboard')
ROOT_DIR = Path(__file__).resolve().parent.parent

# Force root directory to the top of Python's import paths
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

os.chdir(ROOT_DIR)

import json
import streamlit as st
import pandas as pd
from workloads.generator import WorkloadGenerator
from workloads.analyzer import WorkloadAnalyzer
from workloads.io import WorkloadIO
from adaptive.decision_engine import AdaptiveDecisionEngine
from experiments.runner import ExperimentRunner

st.set_page_config(page_title="CPU Scheduler Analyzer", layout="wide")
st.title("Workload-Aware Adaptive CPU Scheduler")

# Sidebar Controls
st.sidebar.header("1. Workload Configuration")
workload_type = st.sidebar.selectbox("Workload Type", ["short_burst", "long_cpu", "mixed"])
process_count = st.sidebar.slider("Number of Processes", 5, 50, 10)
seed = st.sidebar.number_input("Random Seed", value=42, step=1)

# Generate & Analyze Workload
generator = WorkloadGenerator(seed=seed)
workload = generator.generate(workload_type, count=process_count)
features = WorkloadAnalyzer.analyze(workload)

# Display Workload Analysis
st.subheader("2. Workload Characteristics")
col1, col2, col3 = st.columns(3)
col1.metric("Process Count", features.get("process_count", 0))
col2.metric("Mean Burst", f"{features.get('mean_burst', 0):.2f}")
col3.metric("Burst Std Dev", f"{features.get('std_burst', 0):.2f}")

# Workload Export Options
st.subheader("3. Workload Export")
col_json, col_csv = st.columns(2)

json_data = json.dumps({
    "name": workload.name,
    "seed": workload.seed,
    "processes": [{"pid": p.pid, "arrival_time": p.arrival_time, "priority": p.priority, "cpu_bursts": p.cpu_bursts} for p in workload.processes]
}, indent=2)

col_json.download_button(
    label="Export Workload as JSON",
    data=json_data,
    file_name=f"{workload_type}_seed{seed}.json",
    mime="application/json"
)

# Adaptive Decision Engine
engine = AdaptiveDecisionEngine()
decision = engine.select_policy(features)

st.subheader("4. Adaptive Policy Decision")
st.success(f"**Selected Policy:** {decision.selected_policy}")
st.info(decision.explanation)

st.write("**Policy Suitability Scores:**")
scores_df = pd.DataFrame(list(decision.scores.items()), columns=["Policy", "Score"])
st.bar_chart(scores_df.set_index("Policy"))

# Policy Comparison Runner
st.subheader("5. Performance Comparison")
if st.button("Run All Baseline Policies vs Adaptive"):
    comparison_df = ExperimentRunner.run_comparison(workload)
    st.dataframe(comparison_df, use_container_width=True)