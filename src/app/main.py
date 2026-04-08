"""
Streamlit Web Demo — Main Entry Point.
CS6493 NLP Group Project: Mathematical Reasoning Evaluation.
"""

import streamlit as st

st.set_page_config(
    page_title="Math Reasoning Evaluator",
    page_icon="🧮",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("🧮 Mathematical Reasoning Evaluator")
st.caption(
    "CS6493 NLP Group Project — Topic 1: Evaluating Mathematical Reasoning in LLMs"
)

st.markdown("""
### Welcome
This application evaluates and compares how different prompting strategies
affect the mathematical reasoning performance of various large language models.

### Pages
- **Interactive Solver**: Try solving math problems with different models and methods
- **Dashboard**: View experiment results and accuracy comparisons
- **Comparison**: Deep-dive comparison across models and methods

### Models
| Model | Scale | Backend |
|-------|-------|---------|
| Qwen2.5-Math-1.5B | 1.5B | Local CPU |
| DeepSeek-R1-Qwen-1.5B | 1.5B | Local CPU |
| GPT-4o-mini | ~8B eq. | API |
| DeepSeek Chat | V3 | API |

### Prompt Methods
| Method | Type |
|--------|------|
| Chain-of-Thought (CoT) | Baseline |
| Self-Consistency | Multi-sample voting |
| Self-Refine | Iterative critique |
| Least-to-Most | Problem decomposition |
| PVP | Progressive Verification (Ours) |
""")
