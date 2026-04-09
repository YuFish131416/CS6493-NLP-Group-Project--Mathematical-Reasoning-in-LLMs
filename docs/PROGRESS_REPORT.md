# Progress Report / 中期报告

**CS6493 NLP Group Project — Topic 1: Mathematical Reasoning Ability of Large Language Models**

**Group Members**: 余沛翰, 翁梓严, 胡薛林, 赵海超, 邓乐盈
**Date**: April 22, 2026

---

## 1. Introduction (0.5 page)

- Brief overview of LLMs and their mathematical reasoning challenges
- Motivation: why evaluating and improving math reasoning matters
- Research question: How do different prompting strategies affect mathematical reasoning across model scales?
- Our contribution: novel PVP (Progressive Verification Prompting) method

## 2. Related Work (1 page)

- Chain-of-Thought prompting (Wei et al., 2022)
- Self-Consistency (Wang et al., 2022)
- Self-Refine (Madaan et al., 2024)
- Least-to-Most prompting (Zhou et al., 2023)
- Mathematical reasoning benchmarks: MATH, GSM8K, AIME
- Self-verification and critique-based approaches

## 3. Methodology (1.5 pages)

### 3.1 Problem Formulation
- Formal definition of the evaluation task
- Input: math problem → Prompt → Model → Response → Extract answer → Evaluate

### 3.2 Prompt Methods
- **CoT**: Baseline step-by-step reasoning
- **Self-Consistency**: Multi-sample majority vote (n=5)
- **Self-Refine**: Generate → Critique → Refine (2 rounds)
- **Least-to-Most**: Decompose → Solve sequentially
- **PVP (Ours)**: CoT + interspersed verification checkpoints

### 3.3 Evaluation Metrics
- Accuracy (exact match with mathematical equivalence)
- Response Length (character count)
- Step-level Correctness (exploratory)
- Answer Extraction Success Rate

### 3.4 Experimental Setup
- Models: Qwen2.5-Math-1.5B, DeepSeek-R1-Qwen-1.5B, GPT-4o-mini, DeepSeek Chat
- Datasets: MATH-500, GSM8K (Test), AIME 2024
- Infrastructure: CPU-only (GGUF Q4_K_M quantization for local models)
- Temperature: 0.0 (deterministic, except Self-Consistency)

## 4. Preliminary Results (1 page)

> **TODO**: Fill in after running pilot experiments (50 problems per dataset).

### 4.1 Answer Extraction Performance
- Extraction success rates across methods

### 4.2 Model Comparison
- Accuracy comparison table

### 4.3 Method Comparison
- Prompt method effectiveness ranking

### 4.4 PVP vs Baselines
- Preliminary evidence of PVP improvement

## 5. Current Progress & Plan (0.5 page)

### Completed
- [x] Dataset pipeline (MATH-500, GSM8K, AIME 2024)
- [x] Model inference engine (local CPU + API)
- [x] 5 prompt method implementations
- [x] Evaluation framework
- [x] Experiment runner with checkpoint support
- [x] Streamlit Web Demo
- [x] Pilot experiments (if completed)

### Remaining
- [ ] Full-scale experiments (all problems × all combinations)
- [ ] Detailed analysis and ablation studies
- [ ] Final report writing
- [ ] Presentation preparation

### Timeline
| Task | Target Date |
|------|------------|
| Full experiments complete | April 25 |
| Analysis and report draft | April 30 |
| Final report | May 4 |
| Presentation slides | May 5 |

## 6. Challenges & Solutions (0.5 page)

- **Challenge**: No GPU → Solution: GGUF quantization + API models
- **Challenge**: CPU inference slow → Solution: Checkpoint/resume support
- **Challenge**: Answer extraction accuracy → Solution: Multi-pattern extraction + sympy normalization
- **Challenge**: API cost → Solution: Token budgets, pilot testing before full runs

---

## Appendices

- A: Prompt templates for all 5 methods
- B: Sample model outputs (1 correct, 1 incorrect per method)
- C: System architecture diagram
