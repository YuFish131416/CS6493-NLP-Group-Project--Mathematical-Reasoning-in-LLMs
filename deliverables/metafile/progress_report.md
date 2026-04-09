# Progress Report — 中期进度报告

**CS6493 NLP Group Project — Topic 1: Mathematical Reasoning Ability of Large Language Models**

**Group Members**: 余沛翰, 翁梓严, 胡薛林, 赵海超, 邓乐盈
**Date**: April 22, 2026

---

## 1. Introduction

Large Language Models (LLMs) have demonstrated remarkable capabilities across a wide range of natural language tasks, yet mathematical reasoning remains a significant challenge. While models can generate fluent text, they frequently make errors in multi-step logical deductions, arithmetic calculations, and mathematical formalization. This limitation is critical as mathematical reasoning underpins applications in education, scientific computing, and financial analysis.

In this project, we systematically evaluate how different prompting strategies affect the mathematical reasoning performance of LLMs. We investigate five prompting methods — Chain-of-Thought (CoT), Self-Consistency, Self-Refine, Least-to-Most, and our novel Progressive Verification Prompting (PVP) — across multiple model scales and problem difficulties. Our primary research questions are:

- **RQ1**: How do different prompt methods compare across model scales?
- **RQ2**: Can a verification-based prompt method (PVP) outperform standard CoT?
- **RQ3**: How does problem difficulty affect method effectiveness?

Our main contribution is **PVP (Progressive Verification Prompting)**, a novel prompting strategy that intersperses self-verification checkpoints within the reasoning process, forcing the model to verify each intermediate step before proceeding.

---

## 2. Related Work

**Chain-of-Thought (CoT) Prompting.** Wei et al. (2022) demonstrated that instructing LLMs to "think step by step" significantly improves reasoning performance. CoT has become the standard baseline for mathematical reasoning evaluation.

**Self-Consistency.** Wang et al. (2022) proposed sampling multiple reasoning paths and selecting the most common answer via majority vote. This approach leverages the diversity of model outputs to improve robustness.

**Self-Refine.** Madaan et al. (2024) introduced an iterative refinement framework where the model generates an initial solution, critiques it, and produces an improved version. This self-feedback loop can correct errors without external supervision.

**Least-to-Most Prompting.** Zhou et al. (2023) showed that decomposing complex problems into simpler sub-problems and solving them sequentially helps LLMs handle multi-step reasoning tasks more effectively.

**Mathematical Reasoning Benchmarks.** We evaluate on three standard benchmarks: MATH-500 (Hendrycks et al., 2021), a 500-problem subset of competition mathematics; GSM8K (Cobbe et al., 2021), containing 1,319 grade-school math word problems; and AIME 2024, comprising 30 advanced competition problems.

**Self-Verification Approaches.** Recent work has explored using LLMs as their own verifiers (Weng et al., 2023). Our PVP method extends this idea by integrating verification directly into the reasoning prompt rather than as a separate post-hoc step.

---

## 3. Methodology

### 3.1 Problem Formulation

We formalize the evaluation task as: given a math problem $p$, a prompt method $m$, and a model $\mathcal{M}$, the pipeline produces:

$$p \xrightarrow{m} \text{prompt} \xrightarrow{\mathcal{M}} \text{response} \xrightarrow{\text{extract}} \text{answer} \xrightarrow{\text{evaluate}} \text{correct/incorrect}$$

### 3.2 Prompt Methods

We implement five prompting methods:

1. **CoT (Baseline)**: Instructs the model to solve step-by-step with the answer in `\boxed{}` format.
2. **Self-Consistency**: Same prompt as CoT but samples 5 responses (temperature > 0) and takes majority vote.
3. **Self-Refine**: Three-phase process — Solve → Critique → Refine (max 2 refinement rounds).
4. **Least-to-Most**: Two-phase — Decompose the problem into sub-questions → Solve sequentially.
5. **PVP (Ours)**: Instructs the model to verify each step immediately after completing it, checking for logical correctness, consistency with previous steps, and arithmetic errors.

### 3.3 Evaluation Metrics

- **Accuracy** (primary): Exact match between extracted answer and ground truth, with mathematical equivalence checking via SymPy.
- **Response Length** (secondary): Character count of the model's full response.
- **Inference Latency**: Wall-clock time per problem.
- **Answer Extraction Success Rate**: Fraction of responses from which an answer was successfully extracted.

### 3.4 Experimental Setup

| Component | Details |
|-----------|---------|
| **Models** | Qwen2.5-Math-1.5B (local, GGUF Q4_K_M), DeepSeek-R1-Qwen-1.5B (local, GGUF Q4_K_M) |
| **Datasets** | MATH-500 (competition), GSM8K (grade school), AIME 2024 (advanced) |
| **Infrastructure** | CPU-only inference via llama-cpp-python |
| **Temperature** | 0.0 (deterministic), except Self-Consistency (sampling) |
| **Max tokens** | 2,048 per response |
| **Random seed** | 42 |

---

## 4. Preliminary Results

We have completed experiments across 2 models × 5 methods × 2 datasets with 164 total problem evaluations.

### 4.1 Overall Results

| Metric | Value |
|--------|-------|
| Total problems evaluated | 164 |
| Overall accuracy | **57.93%** (95/164) |
| Answer extraction success | **100%** across all combinations |

### 4.2 Model Comparison

| Model | Correct | Total | Accuracy |
|-------|---------|-------|----------|
| Qwen2.5-Math-1.5B | 79 | 120 | **65.83%** |
| DeepSeek-R1-Qwen-1.5B | 16 | 44 | **36.36%** |

Qwen2.5-Math-1.5B outperforms DeepSeek-R1 by +29.5 percentage points, confirming that task-specific fine-tuning is crucial for mathematical reasoning.

### 4.3 Method Comparison

| Rank | Method | Accuracy |
|------|--------|----------|
| 1 | Least-to-Most | **69.57%** |
| 2 | Self-Refine | **66.67%** |
| 3 | **PVP (Ours)** | **64.00%** |
| 4 | CoT (Baseline) | 57.45% |
| 5 | Self-Consistency | 44.44% |

### 4.4 PVP vs Baselines

PVP achieves **64.00%** accuracy, outperforming the CoT baseline (**57.45%**) by **+6.55 percentage points**. Notably, PVP achieves this improvement with comparable latency to CoT (24–31s vs 22–73s), making it the most efficient verification-based method.

### 4.5 Dataset Comparison

| Dataset | Accuracy |
|---------|----------|
| GSM8K (grade school) | **75.00%** |
| MATH-500 (competition) | **55.00%** |

---

## 5. Current Progress & Plan

### Completed ✅

- [x] Complete data pipeline (MATH-500: 500, GSM8K: 1,319, AIME 2024: 30 problems)
- [x] Model inference engine (local CPU via GGUF + API support)
- [x] All 5 prompt method implementations (CoT, Self-Consistency, Self-Refine, Least-to-Most, PVP)
- [x] Evaluation framework (answer extraction, math parsing, metrics)
- [x] Experiment runner with checkpoint/resume support
- [x] 63/63 unit tests passing
- [x] Pilot experiments (164 problems across 14 model×method×dataset combinations)
- [x] 7 visualization charts generated
- [x] Streamlit Web Demo (interactive solver, dashboard, comparison)

### Remaining

- [ ] Full-scale experiments (increase sample size to 50+ per combination)
- [ ] API model experiments (GPT-4o-mini, DeepSeek Chat) for cross-scale comparison
- [ ] AIME 2024 experiments
- [ ] Detailed error analysis and ablation studies
- [ ] Final report writing
- [ ] Presentation slides preparation

### Timeline

| Task | Target Date |
|------|------------|
| Full-scale experiments | April 25, 2026 |
| API model experiments | April 27, 2026 |
| Analysis and report draft | April 30, 2026 |
| Final report | May 4, 2026 |
| Presentation slides | May 5, 2026 |

---

## 6. Challenges & Solutions

| Challenge | Solution | Status |
|-----------|----------|--------|
| No GPU available | GGUF Q4_K_M quantization for CPU inference | ✅ Resolved |
| CPU inference slow (~10–70s/problem) | Checkpoint/resume system for fault tolerance | ✅ Resolved |
| Answer extraction across formats | Multi-pattern regex + SymPy normalization | ✅ Resolved |
| `\boxed{}` conflicts with Python `str.format()` | Escaped to `\boxed{{}}` in all templates | ✅ Resolved |
| Dataset library compatibility | Pinned datasets==2.19.0, huggingface_hub<0.26 | ✅ Resolved |
| API cost control | Token budgets + pilot testing before full runs | 🔄 In progress |

---

## References

1. Wei J, et al. *Chain-of-thought prompting elicits reasoning in large language models.* NeurIPS 2022.
2. Wang X, et al. *Self-consistency improves chain of thought reasoning.* NeurIPS 2022.
3. Madaan A, et al. *Self-refine: Iterative refinement with self-feedback.* NeurIPS 2024.
4. Zhou D, et al. *Least-to-Most Prompting Enables Complex Reasoning.* NeurIPS 2023.
5. Cobbe K, et al. *Training verifiers to solve math word problems.* 2021.
6. Hendrycks D, et al. *Measuring Mathematical Problem Solving With the MATH Dataset.* NeurIPS 2021.

---

## Appendix A: Prompt Templates

### A.1 Chain-of-Thought (CoT)
```
Solve the following math problem step by step. Show your reasoning clearly
and put your final answer in \boxed{}.

Problem: {problem}

Please reason step by step:
```

### A.2 PVP (Progressive Verification Prompting) — Our Method
```
Solve the following math problem. Follow these instructions carefully:

1. Break the problem into clear reasoning steps.
2. After EACH step, pause and verify:
   - Is this step logically correct?
   - Does it follow from the previous step?
   - Are there any arithmetic errors?
   If you find an error, correct it immediately before proceeding.
3. After all steps, perform a final review to verify the overall solution
   is consistent.
4. Put your final answer in \boxed{}.

Problem: {problem}

Begin solving with progressive verification:
```

### A.3 Self-Refine (3-phase)
- **Phase 1 (Solve)**: Same as CoT
- **Phase 2 (Critique)**: "Review the following solution... Identify any errors..."
- **Phase 3 (Refine)**: "Based on the critique, improve the solution..."

### A.4 Least-to-Most (2-phase)
- **Phase 1 (Decompose)**: "Break down the following math problem into simpler sub-questions..."
- **Phase 2 (Solve)**: "Solve each sub-question in order..."

## Appendix B: System Architecture

```
┌──────────────────────────────────────────────────────────┐
│                   Streamlit Web Demo                      │
│  ┌──────────────┐ ┌──────────┐ ┌──────────────────────┐  │
│  │ Interactive   │ │Dashboard │ │ Comparison Analysis  │  │
│  │   Solver      │ │ (Charts) │ │  (Model × Method)    │  │
│  └──────┬───────┘ └────┬─────┘ └──────────┬───────────┘  │
└─────────┼──────────────┼──────────────────┼──────────────┘
          │              │                  │
┌─────────▼──────────────▼──────────────────▼──────────────┐
│                  Experiment Runner                         │
│  ┌──────────┐ ┌──────────┐ ┌──────────────────────────┐  │
│  │ Runner   │ │  Config  │ │  Results Store (JSON)    │  │
│  │(ckpt)    │ │  Manager │ │                          │  │
│  └──────┬───┘ └────┬─────┘ └──────────▲───────────────┘  │
└─────────┼──────────┼──────────────────┼──────────────────┘
          │          │                  │
┌─────────▼──────────▼──────────────────┼──────────────────┐
│                 Core Pipeline         │                   │
│  ┌────────┐ ┌────────┐ ┌──────┐ ┌────┴────────────────┐  │
│  │  Data  │→│ Prompt │→│Model │→│   Evaluation        │  │
│  │ Loader │ │ Engine │ │Router│ │ (Accuracy, Metrics) │  │
│  └────────┘ └────────┘ └──────┘ └─────────────────────┘  │
└──────────────────────────────────────────────────────────┘
```
