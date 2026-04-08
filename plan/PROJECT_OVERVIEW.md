# PROJECT_OVERVIEW.md

## Goal
Systematically evaluate and compare mathematical reasoning performance across 4 LLMs and 5 prompting methods on 3 benchmark datasets, with a novel PVP prompting method as the main contribution.

## Feature List
### Existing
- [x] Course requirement analysis (Topic 1 specification)
- [x] SPEC.md project specification

### New (this iteration — iter-1)
- [ ] Dataset pipeline for MATH-500, GSM8K, AIME 2024
- [ ] Local CPU model inference (Qwen2.5-Math-1.5B, DeepSeek-R1-Qwen-1.5B via GGUF)
- [ ] API model inference (GPT-4o-mini, DeepSeek Chat)
- [ ] 5 prompt method implementations (CoT, Self-Consistency, Self-Refine, Least-to-Most, PVP)
- [ ] Answer extraction and evaluation metrics (Accuracy, Response Length, Step-level Correctness)
- [ ] Experiment runner with checkpoint/resume support
- [ ] Streamlit Web Demo (interactive solver, dashboard, comparison)
- [ ] Jupyter exploration notebooks
- [ ] Unit tests for core modules
- [ ] Progress report template
- [ ] Presentation outline

## Non-Goals
- No model training or fine-tuning
- No multi-modal math problem solving
- No production deployment or authentication
- No non-English language support
- No mobile app or complex frontend framework
- No custom neural network architecture

## Acceptance Criteria
- [ ] All 4 models produce valid outputs on sample math problems
- [ ] All 5 prompt methods generate correctly formatted prompts
- [ ] Evaluation pipeline extracts answers and computes accuracy on ≥95% of test cases
- [ ] Pilot experiments: ≥50 problems per dataset per model-method pair
- [ ] Streamlit demo supports interactive solving with ≥2 models and ≥3 methods
- [ ] Dashboard displays accuracy comparison charts
- [ ] All experiments reproducible from saved config
- [ ] Progress report generated from experimental data
- [ ] Source code runs end-to-end after `pip install -r requirements.txt`
