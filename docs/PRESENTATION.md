# Presentation Outline / 演讲稿大纲

**Duration**: 15 minutes
**Topic**: Evaluating and Improving Mathematical Reasoning in LLMs

---

## Slide 1: Title (30s)
- Title: Evaluating and Improving Mathematical Reasoning in Large Language Models
- Team members
- Course info

## Slide 2: Motivation (1 min)
- LLMs excel at language tasks but struggle with mathematical reasoning
- Real-world impact: education, scientific computing, financial analysis
- Key question: Can we improve math reasoning through better prompting?

## Slide 3: Research Questions (30s)
- RQ1: How do different prompt methods compare across model scales?
- RQ2: Can a verification-based prompt method (PVP) outperform standard CoT?
- RQ3: How does problem difficulty affect method effectiveness?

## Slide 4: Background — Prompt Methods (1.5 min)
- CoT (Wei et al., 2022): step-by-step reasoning
- Self-Consistency (Wang et al., 2022): majority vote over samples
- Self-Refine (Madaan et al., 2024): iterative critique
- Least-to-Most (Zhou et al., 2023): problem decomposition

## Slide 5: Our Contribution — PVP (1.5 min)
- Progressive Verification Prompting
- Key idea: Insert verification checkpoints between reasoning steps
- Forces model to self-check each step before proceeding
- Theoretical basis: decomposed verification reduces cognitive load

## Slide 6: Experimental Setup (1 min)
- 4 models (2 local 1.5B + 2 API)
- 5 prompt methods (4 baselines + PVP)
- 3 datasets (MATH-500, GSM8K, AIME 2024)
- Metrics: Accuracy, Response Length, Step Correctness

## Slide 7: System Architecture (1 min)
- Data pipeline diagram
- Model inference flow (local vs API)
- Evaluation pipeline

## Slide 8-9: Results — Accuracy Comparison (2 min)
- Heatmap: Model × Method accuracy
- Bar charts per dataset
- Key finding 1: Larger models significantly outperform 1.5B models
- Key finding 2: PVP consistently improves over CoT baseline

## Slide 10: Results — PVP Analysis (1.5 min)
- PVP vs CoT improvement breakdown
- Per-dataset analysis
- Where PVP helps most (harder problems)

## Slide 11: Results — Response Efficiency (1 min)
- Accuracy vs Response Length tradeoff
- Token efficiency comparison

## Slide 12: Discussion (1 min)
- Why verification helps: error detection at intermediate steps
- Limitations: increased prompt length, single-pass only
- Scaling effects: PVP benefits are more pronounced on smaller models

## Slide 13: Demo (1.5 min)
- Live demo with Streamlit: solve a problem using different methods
- Show side-by-side comparison

## Slide 14: Conclusion (30s)
- PVP is a simple yet effective prompting strategy
- Verification-based prompting improves math reasoning
- Works best on challenging problems and smaller models

## Slide 15: Q&A (1 min)
- Open for questions

---

## Backup Slides
- Detailed per-dataset results
- Prompt templates for all methods
- Error analysis examples
- Ablation study details
