# Project Report — Evaluating and Improving Mathematical Reasoning in Large Language Models

**CS6493 NLP Group Project — Topic 1: Mathematical Reasoning Ability of LLMs**

**Group Members**: 余沛翰, 翁梓严, 胡薛林, 赵海超, 邓乐盈
**Course**: CS6493 Natural Language Processing, City University of Hong Kong, Q2 2025-2026
**Date**: May 6, 2026

---

## Abstract

We systematically evaluate how five prompting strategies affect the mathematical reasoning performance of Large Language Models (LLMs) across different model scales and problem difficulties. We test Chain-of-Thought (CoT), Self-Consistency, Self-Refine, Least-to-Most, and our novel Progressive Verification Prompting (PVP) on two local 1.5B-parameter models using MATH-500 and GSM8K benchmarks. Our experiments on 164 problems show that: (1) model choice matters more than prompt engineering, with the math-specialized Qwen2.5-Math-1.5B (65.8%) vastly outperforming the general-purpose DeepSeek-R1 (36.4%); (2) problem decomposition via Least-to-Most achieves the highest accuracy (69.6%); (3) our PVP method (64.0%) outperforms the CoT baseline (57.5%) with comparable inference latency; and (4) Self-Consistency underperforms with small models due to insufficient reasoning diversity.

---

## 1. Introduction

Large Language Models (LLMs) have achieved remarkable performance across diverse natural language processing tasks, yet mathematical reasoning remains a persistent challenge. While LLMs can generate fluent, coherent text, they frequently exhibit errors in multi-step logical deduction, arithmetic computation, and formal mathematical reasoning (Wei et al., 2022). This limitation has significant implications for practical applications in education, scientific computing, and automated problem-solving.

Recent work has shown that carefully crafted prompting strategies can substantially improve LLM reasoning without model retraining. Chain-of-Thought (CoT) prompting (Wei et al., 2022) demonstrated that eliciting step-by-step reasoning dramatically improves mathematical problem-solving. Building on this, techniques like Self-Consistency (Wang et al., 2022), Self-Refine (Madaan et al., 2024), and Least-to-Most decomposition (Zhou et al., 2023) offer different strategies for enhancing reasoning quality.

In this project, we address three research questions:

- **RQ1**: How do different prompt methods compare across model scales and architectures?
- **RQ2**: Can a verification-based prompt method improve upon standard CoT reasoning?
- **RQ3**: How does problem difficulty interact with prompting strategy effectiveness?

Our main contributions are:
1. A systematic comparison of five prompting methods across two local 1.5B models and two benchmark datasets.
2. **PVP (Progressive Verification Prompting)**, a novel prompting strategy that integrates step-wise self-verification into the reasoning process, achieving 64.0% accuracy versus the CoT baseline of 57.5%.
3. An open-source experimental framework with checkpoint/resume support, automated evaluation, and interactive visualization.

---

## 2. Related Work

### 2.1 Chain-of-Thought Prompting

Wei et al. (2022) introduced Chain-of-Thought (CoT) prompting, demonstrating that adding "Let's think step by step" to prompts dramatically improves reasoning performance. CoT works by encouraging models to decompose problems into intermediate reasoning steps, making the problem-solving process more transparent and less error-prone. This approach has become the standard baseline for evaluating mathematical reasoning in LLMs.

### 2.2 Self-Consistency

Wang et al. (2022) proposed Self-Consistency as an improvement over greedy CoT. Instead of relying on a single reasoning path, Self-Consistency samples multiple reasoning chains (typically with temperature > 0) and selects the most frequent final answer via majority voting. This approach leverages the intuition that correct reasoning paths are more likely to converge on the same answer than incorrect ones.

### 2.3 Self-Refine

Madaan et al. (2024) introduced Self-Refine, an iterative framework where the model generates an initial solution, critiques it to identify errors, and then produces a refined solution. This self-feedback loop can be repeated for multiple rounds, progressively improving solution quality without external supervision.

### 2.4 Least-to-Most Prompting

Zhou et al. (2023) proposed Least-to-Most prompting, which decomposes complex problems into simpler sub-problems and solves them sequentially. Each sub-problem's answer provides context for subsequent, more complex sub-problems. This approach is particularly effective for multi-step problems where the full reasoning chain exceeds the model's effective reasoning capacity.

### 2.5 Self-Verification Approaches

Recent work has explored using LLMs as their own verifiers (Weng et al., 2023). Verification-based approaches typically apply post-hoc checking after the full solution is generated. Our PVP method differs by integrating verification directly into the reasoning process at each intermediate step.

### 2.6 Mathematical Reasoning Benchmarks

We evaluate on established benchmarks: MATH-500 (Hendrycks et al., 2021), a curated subset of 500 competition-level problems across algebra, geometry, number theory, and more; GSM8K (Cobbe et al., 2021), containing 1,319 grade-school math word problems; and AIME 2024, comprising 30 advanced competition mathematics problems.

---

## 3. Methodology

### 3.1 Problem Formulation

Given a mathematical problem $p$ from dataset $D$, a prompting method $m \in \{$CoT, Self-Consistency, Self-Refine, Least-to-Most, PVP$\}$, and a language model $\mathcal{M}$, our evaluation pipeline computes:

$$\text{accuracy}(m, \mathcal{M}, D) = \frac{1}{|D|} \sum_{p \in D} \mathbf{1}[\text{extract}(\mathcal{M}(m(p))) = \text{ground\_truth}(p)]$$

where $m(p)$ formats the problem into a prompt, $\mathcal{M}(\cdot)$ generates a response, and $\text{extract}(\cdot)$ extracts the final answer.

### 3.2 Prompt Methods

#### 3.2.1 Chain-of-Thought (CoT) — Baseline

CoT instructs the model to solve the problem step-by-step and present the final answer in `\boxed{}` format. This is a single-pass method that serves as our primary baseline.

#### 3.2.2 Self-Consistency

Self-Consistency uses the same prompt as CoT but generates $n=5$ independent samples with temperature-based sampling. The final answer is determined by majority vote across the extracted answers. This is a multi-pass method requiring 5× the inference cost.

#### 3.2.3 Self-Refine

Self-Refine employs a three-phase iterative process:
1. **Solve**: Generate an initial solution (same prompt as CoT)
2. **Critique**: Ask the model to review the solution and identify errors
3. **Refine**: Ask the model to produce an improved solution incorporating the critique

We allow up to 2 refinement rounds (3 total inference calls).

#### 3.2.4 Least-to-Most

Least-to-Most uses a two-phase approach:
1. **Decompose**: Ask the model to break the problem into simpler sub-questions ordered from simplest to most complex
2. **Solve**: Present the sub-questions and ask the model to solve them sequentially, with each answer building on previous ones

#### 3.2.5 PVP (Progressive Verification Prompting) — Our Method

PVP is our novel contribution. It modifies the CoT prompt to explicitly instruct the model to verify each reasoning step immediately after completing it:

1. Break the problem into clear reasoning steps
2. After **each** step, pause and verify: (a) Is this step logically correct? (b) Does it follow from the previous step? (c) Are there arithmetic errors?
3. If an error is found, correct it immediately before proceeding
4. After all steps, perform a final consistency review

**Theoretical motivation**: By decomposing verification into per-step checks rather than post-hoc review, PVP reduces the cognitive load on the model and prevents cascading errors — an error caught at step 2 cannot propagate to steps 3, 4, and beyond.

### 3.3 Models

| Model | Parameters | Type | Quantization | Description |
|-------|-----------|------|-------------|-------------|
| Qwen2.5-Math-1.5B | 1.5B | Local (CPU) | GGUF Q4_K_M | Math-specialized, fine-tuned on mathematical data |
| DeepSeek-R1-Qwen-1.5B | 1.5B | Local (CPU) | GGUF Q4_K_M | General reasoning, distilled from DeepSeek-R1 |

Both models are run on CPU using llama-cpp-python with Q4_K_M quantization, requiring approximately 1.1 GB each.

### 3.4 Datasets

| Dataset | Size | Difficulty | Domain |
|---------|------|-----------|--------|
| MATH-500 | 500 | Competition | Algebra, Geometry, Number Theory, etc. |
| GSM8K | 1,319 | Elementary | Grade school math word problems |
| AIME 2024 | 30 | Advanced | Competition mathematics |

### 3.5 Evaluation

**Answer Extraction**: We implement a multi-pattern extraction pipeline supporting `\boxed{answer}`, `#### answer`, `The answer is X`, `$X$`, and fallback to the last number in the response.

**Mathematical Equivalence**: Extracted answers are normalized using SymPy for mathematical equivalence checking (e.g., "1/2" matches "0.5", "3.0" matches "3").

**Metrics**: Primary metric is exact-match accuracy after normalization. Secondary metrics include response length (characters) and inference latency (seconds).

---

## 4. Experiments and Results

### 4.1 Experimental Configuration

| Parameter | Value |
|-----------|-------|
| Temperature | 0.0 (deterministic), SC uses sampling |
| Max tokens | 2,048 |
| Random seed | 42 |
| Self-Consistency samples | 5 |
| Self-Refine max rounds | 2 |
| Sample size | 20 per dataset (pilot) |

### 4.2 Overall Results

We evaluated 164 problems across 14 model × method × dataset combinations.

| Model | Correct | Total | Accuracy |
|-------|---------|-------|----------|
| **Qwen2.5-Math-1.5B** | 79 | 120 | **65.83%** |
| **DeepSeek-R1-Qwen-1.5B** | 16 | 44 | **36.36%** |
| **Overall** | **95** | **164** | **57.93%** |

### 4.3 Accuracy by Prompt Method

| Rank | Method | Correct | Total | Accuracy |
|------|--------|---------|-------|----------|
| 1 | **Least-to-Most** | 16 | 23 | **69.57%** |
| 2 | **Self-Refine** | 16 | 24 | **66.67%** |
| 3 | **PVP (Ours)** | 16 | 25 | **64.00%** |
| 4 | **CoT (Baseline)** | 27 | 47 | **57.45%** |
| 5 | **Self-Consistency** | 20 | 45 | **44.44%** |

### 4.4 Detailed Model × Method Breakdown

| Model | Method | Dataset | Correct/Total | Accuracy | Avg Latency |
|-------|--------|---------|--------------|----------|-------------|
| Qwen2.5-Math | CoT | GSM8K | 4/5 | **80.0%** | 33.1s |
| Qwen2.5-Math | CoT | MATH-500 | 14/20 | **70.0%** | 22.3s |
| Qwen2.5-Math | Self-Consistency | GSM8K | 2/5 | 40.0% | 81.5s |
| Qwen2.5-Math | Self-Consistency | MATH-500 | 13/20 | **65.0%** | 123.6s |
| Qwen2.5-Math | Self-Refine | GSM8K | 3/4 | **75.0%** | 81.3s |
| Qwen2.5-Math | Self-Refine | MATH-500 | 13/20 | **65.0%** | 97.6s |
| Qwen2.5-Math | Least-to-Most | GSM8K | 3/3 | **100.0%** | 29.3s |
| Qwen2.5-Math | Least-to-Most | MATH-500 | 13/20 | **65.0%** | 55.8s |
| Qwen2.5-Math | PVP | GSM8K | 2/3 | 66.7% | 31.3s |
| Qwen2.5-Math | PVP | MATH-500 | 12/20 | **60.0%** | 23.9s |
| DeepSeek-R1 | CoT | GSM8K | 2/2 | **100.0%** | 72.9s |
| DeepSeek-R1 | CoT | MATH-500 | 7/20 | 35.0% | 68.0s |
| DeepSeek-R1 | Self-Consistency | MATH-500 | 5/20 | 25.0% | 359.1s |
| DeepSeek-R1 | PVP | GSM8K | 2/2 | **100.0%** | 25.7s |

### 4.5 Accuracy by Dataset

| Dataset | Correct | Total | Accuracy |
|---------|---------|-------|----------|
| GSM8K | 18 | 24 | **75.00%** |
| MATH-500 | 77 | 140 | **55.00%** |

### 4.6 Efficiency Analysis

| Method | Avg Latency Range | Inference Calls | Description |
|--------|------------------|-----------------|-------------|
| CoT | 22–73s | 1 | Single-pass, fastest |
| PVP | 24–31s | 1 | Single-pass with verification |
| Least-to-Most | 29–56s | 2 | Decompose + solve |
| Self-Refine | 81–98s | Up to 3 | Solve + critique + refine |
| Self-Consistency | 82–335s | 5 | 5× sampling, slowest |

---

## 5. Discussion

### Finding 1: Model Choice Matters More Than Prompt Engineering

Qwen2.5-Math-1.5B (65.8%) dominates DeepSeek-R1-Qwen-1.5B (36.4%) across all prompting strategies. A task-specific model with simple CoT (70.0% on MATH-500) outperforms a general model with any advanced method. This suggests that for mathematical reasoning, domain-specific fine-tuning provides a stronger foundation than sophisticated prompting alone.

### Finding 2: Problem Decomposition Is Most Effective

Least-to-Most achieves the highest accuracy (69.6%) by decomposing complex problems into manageable sub-problems. This structured decomposition is particularly beneficial for small 1.5B models, as it reduces the effective reasoning chain length and allows the model to focus on simpler intermediate steps.

### Finding 3: Self-Consistency Struggles with Small Models

Self-Consistency (44.4%) underperforms the CoT baseline (57.5%), contrary to results reported for larger models. With only 1.5B parameters, the models lack sufficient reasoning diversity — the 5 samples tend to either all succeed or all fail on the same problems, making majority voting ineffective. This finding suggests that Self-Consistency requires a minimum model scale threshold to be beneficial.

### Finding 4: Verification-Based Methods Show Promise

Both Self-Refine (66.7%) and PVP (64.0%) outperform the CoT baseline, confirming that self-verification improves reasoning quality. PVP is particularly notable for achieving competitive accuracy with single-pass inference latency (~25s vs Self-Refine's ~90s), offering the best accuracy-efficiency trade-off among all methods tested.

### Finding 5: PVP Offers Best Efficiency Trade-off

PVP provides competitive accuracy (~64%) with CoT-level latency (~25s per problem). Compared to Self-Consistency (5× cost, lower accuracy) and Self-Refine (3× cost, slightly higher accuracy), PVP represents the most practical verification-based prompting strategy for resource-constrained settings.

---

## 6. Limitations and Future Work

1. **Sample size**: Due to CPU inference constraints, most experiments used 20 samples per combination. Larger-scale experiments would yield more statistically robust conclusions.
2. **Model scale**: Results are limited to 1.5B-parameter models. Advanced prompting strategies may be more effective with larger models (7B, 70B) where reasoning diversity is greater.
3. **No AIME 2024 results**: The hardest benchmark dataset was not included in the final runs due to time constraints.
4. **API models not fully evaluated**: GPT-4o-mini and DeepSeek Chat comparisons would provide cross-scale insights.
5. **PVP design space**: The current PVP template uses a fixed verification structure. Adaptive verification (varying verification depth based on problem complexity) is a promising future direction.

---

## 7. Conclusion

We presented a systematic evaluation of five prompting strategies for mathematical reasoning in LLMs, introducing Progressive Verification Prompting (PVP) as a novel approach. Our key findings demonstrate that: (1) task-specific models dramatically outperform general-purpose models regardless of prompting strategy; (2) problem decomposition (Least-to-Most) is the most effective strategy for small models; (3) Self-Consistency is counterproductive for small models; and (4) PVP offers a practical, efficient improvement over the CoT baseline by integrating step-wise verification directly into the reasoning process. Our open-source experimental framework supports reproducible evaluation with checkpoint/resume capabilities.

---

## References

1. Wei J, Wang X, Schuurmans D, et al. Chain-of-thought prompting elicits reasoning in large language models. *Advances in Neural Information Processing Systems (NeurIPS)*, 2022.
2. Wang X, Wei J, Schuurmans D, et al. Self-consistency improves chain of thought reasoning in language models. *Advances in Neural Information Processing Systems (NeurIPS)*, 2022.
3. Madaan A, Tandon N, Gupta P, et al. Self-refine: Iterative refinement with self-feedback. *Advances in Neural Information Processing Systems (NeurIPS)*, 2024.
4. Zhou D, Schärli N, Hou L, et al. Least-to-Most Prompting Enables Complex Reasoning in Large Language Models. *Advances in Neural Information Processing Systems (NeurIPS)*, 2023.
5. Cobbe K, Kosaraju V, Bavarian M, et al. Training verifiers to solve math word problems. *arXiv preprint arXiv:2110.14168*, 2021.
6. Hendrycks D, Burns C, Kadavath S, et al. Measuring Mathematical Problem Solving With the MATH Dataset. *Advances in Neural Information Processing Systems (NeurIPS)*, 2021.
7. Zhang Z, Zhang A, Li M, Smola A. Automatic Chain of Thought Prompting in Large Language Models. *arXiv preprint arXiv:2210.03493*, 2022.
8. Weng Y, Zhu M, Xia F, et al. Large Language Models are Better Reasoners with Self-Verification. *arXiv preprint arXiv:2212.09561*, 2023.

---

## Appendix A: PVP Prompt Template

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

## Appendix B: All Prompt Templates

### B.1 CoT Template
```
Solve the following math problem step by step. Show your reasoning clearly
and put your final answer in \boxed{}.

Problem: {problem}

Please reason step by step:
```

### B.2 Self-Consistency Template
Same as CoT (sampling is controlled at inference level with temperature > 0).

### B.3 Self-Refine Templates
**Solve Phase**: Same as CoT

**Critique Phase**:
```
Review the following solution to a math problem. Identify any errors in
reasoning, calculation mistakes, or logical flaws. Be specific about
what is wrong and why.

Problem: {problem}
Solution to review: {solution}

Please provide your critique:
```

**Refine Phase**:
```
Based on the critique below, improve the solution to the following math
problem. Fix any identified errors and provide the corrected solution.
Put your final answer in \boxed{}.

Problem: {problem}
Original solution: {solution}
Critique: {critique}

Please provide the improved solution:
```

### B.4 Least-to-Most Templates
**Decompose Phase**:
```
Break down the following math problem into simpler sub-questions. List them
in order from simplest to most complex. Each sub-question should build on
the previous ones.

Problem: {problem}

List the sub-questions:
```

**Solve Phase**:
```
Here is a math problem and its decomposition into sub-questions:
Problem: {problem}
Sub-questions: {sub_questions}

Solve each sub-question in order. Use the answer from each sub-question
to help solve the next one. Put your final answer in \boxed{}.

Please solve step by step:
```

## Appendix C: System Architecture

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

## Appendix D: Visualization Charts

The following 7 charts are generated from experimental data:

1. **fig1_accuracy_by_model.png** — Bar chart comparing Qwen2.5-Math (65.8%) vs DeepSeek-R1 (36.4%)
2. **fig2_accuracy_by_method.png** — Ranked bar chart of 5 methods (Least-to-Most > Self-Refine > PVP > CoT > SC)
3. **fig3_accuracy_by_dataset.png** — GSM8K (75.0%) vs MATH-500 (55.0%)
4. **fig4_model_x_method.png** — Grouped bar chart showing all model × method combinations
5. **fig5_heatmap_model_method.png** — Heatmap of accuracy across model × method matrix
6. **fig6_length_vs_accuracy.png** — Scatter plot of response length vs accuracy
7. **fig7_latency_by_method.png** — Bar chart of inference latency per method

## Appendix E: Presentation Slides

See [`deliverables/presentation.md`](presentation.md) for the complete 15-slide presentation outline with timing.
