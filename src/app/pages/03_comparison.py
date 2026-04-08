"""
Comparison Analysis page.
Side-by-side comparison of models and prompt methods.
"""

import sys
import os

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

st.set_page_config(page_title="Comparison", page_icon="⚖️", layout="wide")
st.title("⚖️ Model & Method Comparison")

# Load results
results_dir = "results"
if not os.path.exists(results_dir):
    st.info("No results found. Run experiments first.")
    st.stop()

results_files = [f for f in os.listdir(results_dir) if f.endswith("_results.json")]
if not results_files:
    st.info("No results found. Run experiments first.")
    st.stop()

selected_file = st.selectbox("Select experiment run", options=results_files)
with open(os.path.join(results_dir, selected_file), 'r') as f:
    results = json.load(f)

summary = results.get("summary", {})
if not summary:
    st.warning("No summary data available in this results file.")
    st.stop()

# Build comparison dataframe
rows = []
for key, val in summary.items():
    rows.append({
        "Combo": key,
        "Model": val.get("model", ""),
        "Method": val.get("method", ""),
        "Dataset": val.get("dataset", ""),
        "Accuracy": val.get("accuracy", 0),
        "Correct": val.get("correct", 0),
        "Total": val.get("total", 0),
        "Extraction Rate": val.get("extract_success_rate", 0),
    })
df = pd.DataFrame(rows)

# --- Comparison Tabs ---
tab1, tab2, tab3 = st.tabs(["Heatmap", "Ranking", "Details"])

with tab1:
    st.markdown("### Accuracy Heatmap")

    # Pivot for heatmap
    dataset_filter = st.selectbox(
        "Filter dataset",
        options=["All"] + list(df["Dataset"].unique()),
        key="heatmap_dataset",
    )
    filtered_df = df if dataset_filter == "All" else df[df["Dataset"] == dataset_filter]

    if len(filtered_df) > 0:
        pivot = filtered_df.pivot_table(
            index="Model",
            columns="Method",
            values="Accuracy",
            aggfunc="mean",
        )
        pivot = pivot * 100  # Convert to percentage

        fig = go.Figure(
            data=go.Heatmap(
                z=pivot.values,
                x=list(pivot.columns),
                y=list(pivot.index),
                colorscale="RdYlGn",
                text=pivot.values.round(1),
                texttemplate="%{text}%",
                hovertemplate="%{y} × %{x}: %{text}%",
                zmin=0,
                zmax=100,
            )
        )
        fig.update_layout(
            title="Accuracy Heatmap (Model × Method)",
            xaxis_title="Prompt Method",
            yaxis_title="Model",
            height=400,
        )
        st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.markdown("### Method Ranking")

    # Rank by average accuracy across all datasets
    method_ranking = (
        df.groupby("Method")["Accuracy"]
        .mean()
        .sort_values(ascending=False)
        .reset_index()
    )
    method_ranking["Accuracy"] = method_ranking["Accuracy"] * 100

    st.dataframe(method_ranking, use_container_width=True, hide_index=True)

    # Bar chart
    fig = px.bar(
        method_ranking,
        x="Method",
        y="Accuracy",
        title="Average Accuracy by Prompt Method",
        labels={"Accuracy": "Accuracy (%)"},
        color="Accuracy",
        color_continuous_scale="RdYlGn",
    )
    st.plotly_chart(fig, use_container_width=True)

    # Model ranking
    st.markdown("### Model Ranking")
    model_ranking = (
        df.groupby("Model")["Accuracy"]
        .mean()
        .sort_values(ascending=False)
        .reset_index()
    )
    model_ranking["Accuracy"] = model_ranking["Accuracy"] * 100

    st.dataframe(model_ranking, use_container_width=True, hide_index=True)

    fig2 = px.bar(
        model_ranking,
        x="Model",
        y="Accuracy",
        title="Average Accuracy by Model",
        labels={"Accuracy": "Accuracy (%)"},
        color="Accuracy",
        color_continuous_scale="RdYlGn",
    )
    st.plotly_chart(fig2, use_container_width=True)

with tab3:
    st.markdown("### Detailed Comparison Table")
    st.dataframe(
        df.sort_values("Accuracy", ascending=False),
        use_container_width=True,
        hide_index=True,
    )
