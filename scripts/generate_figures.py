"""
Generate visualization charts for experiment results.
Produces publication-quality PNG figures saved to results/figures/.
"""

import json
import os
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

# ─── Configuration ───────────────────────────────────────────
RESULTS_DIR = "results"
FIGURES_DIR = os.path.join(RESULTS_DIR, "figures")
os.makedirs(FIGURES_DIR, exist_ok=True)

# Load summary data
with open(os.path.join(RESULTS_DIR, "json", "final_summary.json"), "r", encoding="utf-8") as f:
    data = json.load(f)

summary = data["summary"]
aggregated = data["aggregated"]

# Color palettes
MODEL_COLORS = {
    "qwen2.5-math": "#4C72B0",
    "deepseek-r1": "#DD8452",
}

METHOD_COLORS = {
    "cot": "#4C72B0",
    "self_consistency": "#DD8452",
    "self_refine": "#55A868",
    "least_to_most": "#C44E52",
    "pvp": "#8172B3",
}

METHOD_LABELS = {
    "cot": "CoT",
    "self_consistency": "Self-Consistency",
    "self_refine": "Self-Refine",
    "least_to_most": "Least-to-Most",
    "pvp": "PVP (Ours)",
}

DATASET_LABELS = {
    "gsm8k": "GSM8K",
    "math500": "MATH-500",
    "aime2024": "AIME 2024",
}

MODEL_LABELS = {
    "qwen2.5-math": "Qwen2.5-Math-1.5B",
    "deepseek-r1": "DeepSeek-R1-Qwen-1.5B",
}

# ─── Helper functions ────────────────────────────────────────
def get_label(name, label_map):
    return label_map.get(name, name)

def save_fig(fig, name, dpi=150):
    path = os.path.join(FIGURES_DIR, name)
    fig.savefig(path, dpi=dpi, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f"  Saved: {path}")


# ═══════════════════════════════════════════════════════════════
# Figure 1: Overall Accuracy by Model (Bar Chart)
# ═══════════════════════════════════════════════════════════════
print("\n[1/7] Generating: Overall Accuracy by Model...")
fig, ax = plt.subplots(figsize=(8, 5))
by_model = aggregated["by_model"]
models = sorted(by_model.keys())
accs = [by_model[m]["accuracy"] * 100 for m in models]
colors = [MODEL_COLORS.get(m, "#888888") for m in models]

bars = ax.bar([get_label(m, MODEL_LABELS) for m in models], accs, color=colors, width=0.5, edgecolor='white', linewidth=1.5)
for bar, acc, m in zip(bars, accs, models):
    info = by_model[m]
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1.5,
            f'{acc:.1f}%\n({info["correct"]}/{info["total"]})',
            ha='center', va='bottom', fontsize=11, fontweight='bold')

ax.set_ylabel("Accuracy (%)", fontsize=12)
ax.set_title("Overall Accuracy by Model", fontsize=14, fontweight='bold')
ax.set_ylim(0, 100)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.grid(axis='y', alpha=0.3)
save_fig(fig, "fig1_accuracy_by_model.png")


# ═══════════════════════════════════════════════════════════════
# Figure 2: Accuracy by Prompt Method (Bar Chart)
# ═══════════════════════════════════════════════════════════════
print("[2/7] Generating: Accuracy by Prompt Method...")
fig, ax = plt.subplots(figsize=(10, 5))
by_method = aggregated["by_method"]
methods_sorted = sorted(by_method.keys(), key=lambda m: by_method[m]["accuracy"], reverse=True)
accs = [by_method[m]["accuracy"] * 100 for m in methods_sorted]
colors = [METHOD_COLORS.get(m, "#888888") for m in methods_sorted]
labels = [get_label(m, METHOD_LABELS) for m in methods_sorted]

bars = ax.bar(labels, accs, color=colors, width=0.6, edgecolor='white', linewidth=1.5)
for bar, acc, m in zip(bars, accs, methods_sorted):
    info = by_method[m]
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1.5,
            f'{acc:.1f}%\n({info["correct"]}/{info["total"]})',
            ha='center', va='bottom', fontsize=10, fontweight='bold')

ax.set_ylabel("Accuracy (%)", fontsize=12)
ax.set_title("Accuracy by Prompt Method (Averaged Across Models & Datasets)", fontsize=13, fontweight='bold')
ax.set_ylim(0, 100)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.grid(axis='y', alpha=0.3)
save_fig(fig, "fig2_accuracy_by_method.png")


# ═══════════════════════════════════════════════════════════════
# Figure 3: Accuracy by Dataset (Bar Chart)
# ═══════════════════════════════════════════════════════════════
print("[3/7] Generating: Accuracy by Dataset...")
fig, ax = plt.subplots(figsize=(8, 5))
by_dataset = aggregated["by_dataset"]
datasets = sorted(by_dataset.keys())
accs = [by_dataset[d]["accuracy"] * 100 for d in datasets]
colors_ds = ["#4C72B0", "#DD8452", "#55A868"]

bars = ax.bar([get_label(d, DATASET_LABELS) for d in datasets], accs, 
              color=colors_ds[:len(datasets)], width=0.5, edgecolor='white', linewidth=1.5)
for bar, acc, d in zip(bars, accs, datasets):
    info = by_dataset[d]
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1.5,
            f'{acc:.1f}%\n({info["correct"]}/{info["total"]})',
            ha='center', va='bottom', fontsize=11, fontweight='bold')

ax.set_ylabel("Accuracy (%)", fontsize=12)
ax.set_title("Accuracy by Dataset", fontsize=14, fontweight='bold')
ax.set_ylim(0, 100)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.grid(axis='y', alpha=0.3)
save_fig(fig, "fig3_accuracy_by_dataset.png")


# ═══════════════════════════════════════════════════════════════
# Figure 4: Grouped Bar Chart — Model × Method
# ═══════════════════════════════════════════════════════════════
print("[4/7] Generating: Grouped Bar Chart (Model × Method)...")

# Get all methods and models present
all_models = sorted(set(v["model"] for v in summary.values()))
all_methods = sorted(set(v["method"] for v in summary.values()))

fig, ax = plt.subplots(figsize=(12, 6))
x = np.arange(len(all_methods))
width = 0.35
offsets = [-width/2, width/2]

for i, model in enumerate(all_models):
    accs = []
    for method in all_methods:
        # Average across datasets for this model+method
        matching = [v for v in summary.values() if v["model"] == model and v["method"] == method]
        if matching:
            total_correct = sum(m["correct"] for m in matching)
            total_problems = sum(m["total"] for m in matching)
            acc = (total_correct / total_problems * 100) if total_problems > 0 else 0
        else:
            acc = 0
        accs.append(acc)
    
    bars = ax.bar(x + offsets[i], accs, width, 
                  label=get_label(model, MODEL_LABELS),
                  color=MODEL_COLORS.get(model, "#888"),
                  edgecolor='white', linewidth=1)
    
    for j, (bar, acc) in enumerate(zip(bars, accs)):
        if acc > 0:
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                    f'{acc:.1f}%', ha='center', va='bottom', fontsize=9, fontweight='bold')

ax.set_ylabel("Accuracy (%)", fontsize=12)
ax.set_title("Accuracy by Model × Prompt Method", fontsize=14, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels([get_label(m, METHOD_LABELS) for m in all_methods], fontsize=10)
ax.set_ylim(0, 100)
ax.legend(fontsize=10, framealpha=0.9)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.grid(axis='y', alpha=0.3)
save_fig(fig, "fig4_model_x_method.png")


# ═══════════════════════════════════════════════════════════════
# Figure 5: Heatmap — Accuracy (Model × Method)
# ═══════════════════════════════════════════════════════════════
print("[5/7] Generating: Accuracy Heatmap (Model × Method)...")

# Build pivot table
heatmap_data = np.zeros((len(all_models), len(all_methods)))
for i, model in enumerate(all_models):
    for j, method in enumerate(all_methods):
        matching = [v for v in summary.values() if v["model"] == model and v["method"] == method]
        if matching:
            total_correct = sum(m["correct"] for m in matching)
            total_problems = sum(m["total"] for m in matching)
            heatmap_data[i, j] = (total_correct / total_problems * 100) if total_problems > 0 else 0
        else:
            heatmap_data[i, j] = np.nan

fig, ax = plt.subplots(figsize=(10, 4))
import copy as _copy
cmap = _copy.copy(plt.cm.get_cmap("RdYlGn"))
cmap.set_bad(color='#f0f0f0')

im = ax.imshow(heatmap_data, cmap=cmap, vmin=0, vmax=100, aspect='auto')

# Add text annotations
for i in range(len(all_models)):
    for j in range(len(all_methods)):
        val = heatmap_data[i, j]
        if not np.isnan(val):
            text_color = 'white' if val < 40 or val > 80 else 'black'
            ax.text(j, i, f'{val:.1f}%', ha='center', va='center', 
                    fontsize=12, fontweight='bold', color=text_color)
        else:
            ax.text(j, i, 'N/A', ha='center', va='center', 
                    fontsize=10, color='#999999')

ax.set_xticks(np.arange(len(all_methods)))
ax.set_xticklabels([get_label(m, METHOD_LABELS) for m in all_methods], fontsize=10)
ax.set_yticks(np.arange(len(all_models)))
ax.set_yticklabels([get_label(m, MODEL_LABELS) for m in all_models], fontsize=10)
ax.set_title("Accuracy Heatmap (Model × Prompt Method)", fontsize=14, fontweight='bold', pad=15)

cbar = fig.colorbar(im, ax=ax, shrink=0.8)
cbar.set_label("Accuracy (%)", fontsize=10)

save_fig(fig, "fig5_heatmap_model_method.png")


# ═══════════════════════════════════════════════════════════════
# Figure 6: Response Length vs Accuracy (Scatter Plot)
# ═══════════════════════════════════════════════════════════════
print("[6/7] Generating: Response Length vs Accuracy...")

fig, ax = plt.subplots(figsize=(10, 6))

for key, val in summary.items():
    model = val["model"]
    method = val["method"]
    dataset = val["dataset"]
    acc = val["accuracy"] * 100
    avg_len = val["avg_response_length"]
    total = val["total"]
    
    marker = 'o' if dataset == 'math500' else 's' if dataset == 'gsm8k' else '^'
    color = MODEL_COLORS.get(model, "#888")
    
    ax.scatter(avg_len, acc, c=color, marker=marker, s=total * 15 + 50, 
              alpha=0.8, edgecolors='white', linewidth=1,
              label=f'{get_label(model, MODEL_LABELS)} / {get_label(dataset, DATASET_LABELS)}')
    
    ax.annotate(get_label(method, METHOD_LABELS),
                (avg_len, acc), textcoords="offset points",
                xytext=(8, 4), fontsize=7, alpha=0.8)

# Remove duplicate labels
handles, labels = ax.get_legend_handles_labels()
unique = dict(zip(labels, handles))
ax.legend(unique.values(), unique.keys(), fontsize=8, loc='upper right', framealpha=0.9)

ax.set_xlabel("Avg. Response Length (chars)", fontsize=12)
ax.set_ylabel("Accuracy (%)", fontsize=12)
ax.set_title("Response Length vs. Accuracy\n(bubble size = number of problems)", fontsize=13, fontweight='bold')
ax.set_ylim(0, 105)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.grid(alpha=0.3)
save_fig(fig, "fig6_length_vs_accuracy.png")


# ═══════════════════════════════════════════════════════════════
# Figure 7: Average Latency by Method (Bar Chart)
# ═══════════════════════════════════════════════════════════════
print("[7/7] Generating: Average Latency by Method...")

fig, ax = plt.subplots(figsize=(10, 5))

# Compute average latency per method
method_latencies = {}
for val in summary.values():
    method = val["method"]
    if method not in method_latencies:
        method_latencies[method] = []
    method_latencies[method].append(val["avg_latency_ms"])

methods_sorted = sorted(method_latencies.keys(), 
                       key=lambda m: np.mean(method_latencies[m]))
avg_lats = [np.mean(method_latencies[m]) / 1000 for m in methods_sorted]  # Convert to seconds
colors = [METHOD_COLORS.get(m, "#888") for m in methods_sorted]
labels = [get_label(m, METHOD_LABELS) for m in methods_sorted]

bars = ax.barh(labels, avg_lats, color=colors, height=0.5, edgecolor='white', linewidth=1.5)
for bar, lat in zip(bars, avg_lats):
    ax.text(bar.get_width() + 1, bar.get_y() + bar.get_height()/2,
            f'{lat:.1f}s', ha='left', va='center', fontsize=10, fontweight='bold')

ax.set_xlabel("Average Latency (seconds)", fontsize=12)
ax.set_title("Average Inference Latency by Prompt Method", fontsize=14, fontweight='bold')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.grid(axis='x', alpha=0.3)
save_fig(fig, "fig7_latency_by_method.png")


# ─── Done ────────────────────────────────────────────────────
print(f"\nAll 7 figures saved to {FIGURES_DIR}/")
print("Files:")
for f in sorted(os.listdir(FIGURES_DIR)):
    size = os.path.getsize(os.path.join(FIGURES_DIR, f))
    print(f"  {f}  ({size/1024:.1f} KB)")
