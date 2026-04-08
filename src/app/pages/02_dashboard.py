"""
Experiment Results Dashboard page.
Displays accuracy comparisons, response length stats, and charts.
"""

import sys
import os

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

st.set_page_config(page_title="Dashboard", page_icon="📊", layout="wide")
st.title("📊 Experiment Results Dashboard")

# Load results
results_dir = "results"
results_files = []
if os.path.exists(results_dir):
    for f in os.listdir(results_dir):
        if f.endswith("_results.json"):
            results_files.append(f)

if not results_files:
    st.info(
        "No experiment results found. Run experiments first using the experiment runner, "
        "or place results JSON files in the `results/` directory."
    )
    st.stop()

import json

selected_file = st.selectbox("Select experiment run", options=results_files)
if selected_file:
    with open(os.path.join(results_dir, selected_file), 'r') as f:
        results = json.load(f)

    # --- Summary Stats ---
    st.markdown("### Overall Summary")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Problems", results.get("total_problems", 0))
    col2.metric("Correct", results.get("total_correct", 0))
    col3.metric("Overall Accuracy", f"{results.get('overall_accuracy', 0):.2%}")
    col4.metric("Run ID", results.get("run_id", "N/A"))

    # --- Summary Table ---
    summary = results.get("summary", {})
    if summary:
        st.markdown("### Accuracy by Model × Method × Dataset")
        rows = []
        for key, val in summary.items():
            rows.append({
                "Model": val.get("model", ""),
                "Method": val.get("method", ""),
                "Dataset": val.get("dataset", ""),
                "Accuracy": f"{val.get('accuracy', 0):.2%}",
                "Correct": f"{val.get('correct', 0)}/{val.get('total', 0)}",
                "Extraction Rate": f"{val.get('extract_success_rate', 0):.2%}",
            })
        df = pd.DataFrame(rows)
        st.dataframe(df, use_container_width=True, hide_index=True)

        # --- Charts ---
        st.markdown("### Visualizations")

        # Bar chart: Accuracy by model and method
        if len(rows) > 0:
            chart_df = pd.DataFrame([
                {
                    "Model": val.get("model", ""),
                    "Method": val.get("method", ""),
                    "Dataset": val.get("dataset", ""),
                    "Accuracy": val.get("accuracy", 0) * 100,
                }
                for val in summary.values()
            ])

            tab1, tab2, tab3 = st.tabs(["By Model", "By Method", "By Dataset"])

            with tab1:
                fig1 = px.bar(
                    chart_df,
                    x="Model",
                    y="Accuracy",
                    color="Method",
                    barmode="group",
                    title="Accuracy by Model and Prompt Method",
                    labels={"Accuracy": "Accuracy (%)"},
                )
                st.plotly_chart(fig1, use_container_width=True)

            with tab2:
                fig2 = px.bar(
                    chart_df,
                    x="Method",
                    y="Accuracy",
                    color="Model",
                    barmode="group",
                    title="Accuracy by Prompt Method and Model",
                    labels={"Accuracy": "Accuracy (%)"},
                )
                st.plotly_chart(fig2, use_container_width=True)

            with tab3:
                fig3 = px.bar(
                    chart_df,
                    x="Dataset",
                    y="Accuracy",
                    color="Model",
                    barmode="group",
                    title="Accuracy by Dataset and Model",
                    labels={"Accuracy": "Accuracy (%)"},
                )
                st.plotly_chart(fig3, use_container_width=True)

    # --- Individual Responses ---
    st.markdown("### Individual Responses")
    responses = results.get("responses", [])
    if responses:
        # Filter
        filter_model = st.selectbox(
            "Filter by model",
            options=["All"] + list(set(r.get("model_name", "") for r in responses)),
        )
        filter_correct = st.selectbox(
            "Filter by result",
            options=["All", "Correct", "Incorrect"],
        )

        filtered = responses
        if filter_model != "All":
            filtered = [r for r in filtered if r.get("model_name") == filter_model]
        if filter_correct == "Correct":
            filtered = [r for r in filtered if r.get("is_correct")]
        elif filter_correct == "Incorrect":
            filtered = [r for r in filtered if not r.get("is_correct")]

        st.write(f"Showing {len(filtered)} of {len(responses)} responses")

        for i, resp in enumerate(filtered):
            with st.expander(
                f"{'✅' if resp.get('is_correct') else '❌'} "
                f"{resp.get('problem_id', '')} — "
                f"{resp.get('model_name', '')} / {resp.get('prompt_method', '')}"
            ):
                col_a, col_b = st.columns(2)
                with col_a:
                    st.markdown(f"**Extracted**: {resp.get('extracted_answer', 'N/A')}")
                    st.markdown(f"**Latency**: {resp.get('latency_ms', 0):.0f}ms")
                    st.markdown(f"**Response Length**: {resp.get('response_length', 0)} chars")
                with col_b:
                    st.markdown("**Response**")
                    st.text(resp.get("raw_response", "")[:2000])
