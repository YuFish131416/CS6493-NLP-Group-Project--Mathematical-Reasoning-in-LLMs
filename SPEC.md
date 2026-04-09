# SPEC.md — CS6493 NLP Group Project Specification

> **Project**: Evaluating and Improving Mathematical Reasoning in Large Language Models
> **Course**: CS6493 Natural Language Processing, City University of Hong Kong, Q2 2025-2026
> **Topic**: Topic 1 — Mathematical Reasoning Ability of Large Language Models

---

## 1. Project Goals

Systematically evaluate how different prompting strategies affect the mathematical reasoning performance of LLMs across varying model scales and problem difficulties, and propose a novel prompting method (PVP) that improves reasoning accuracy through progressive step-wise verification.

## 2. Feature List

### Core Features
- **Dataset Pipeline**: Download, preprocess, and unify format for MATH-500, GSM8K (Test Set), and AIME 2024
- **Model Inference Engine**: Local CPU inference for 1.5B models (Qwen2.5-Math-1.5B, DeepSeek-R1-Qwen-1.5B) via GGUF quantization; API-based inference for larger models (GPT-4o-mini, DeepSeek Chat)
- **Prompt Method Library**: Implementation of 5 prompting methods — CoT, Self-Consistency, Self-Refine, Least-to-Most, and the novel PVP (Progressive Verification Prompting)
- **Evaluation Framework**: Automated answer extraction, accuracy computation, response length measurement, and step-level correctness analysis
- **Experiment Runner**: Batch experiment execution with checkpoint/resume support, configuration management, and results persistence (JSON)
- **Streamlit Web Demo**: Interactive math problem solver, experiment results dashboard, and comparative analysis visualization

### Innovation Feature
- **PVP (Progressive Verification Prompting)**: A novel prompting strategy that intersperses verification instructions between reasoning steps, forcing the model to self-check each intermediate result before proceeding

## 3. Non-Goals (Out of Scope)

- No training or fine-tuning of any model
- No multi-modal or vision-based math problem solving
- No real-time production deployment or user authentication
- No support for languages other than English math problems
- No mobile application or complex frontend framework
- No custom model architecture design
- No neural network training from scratch

## 4. Technical Constraints

### Hard Constraints
- **No GPU available**: All local inference must run on CPU; use GGUF Q4_K_M quantization for 1.5B models
- **Python 3.10+**: Project language
- **Models required by topic**: Qwen2.5-Math-1.5B and DeepSeek-R1-Qwen-1.5B must be included
- **At least 3 prompt methods**: Course requirement
- **Datasets**: MATH-500, GSM8K (Test Set), AIME 2024
- **API cost control**: Set daily token budget limits for API-based models

### Soft Constraints
- Target response time per query on CPU: < 60 seconds for 1.5B models
- Experiment results should be reproducible with the same random seed and configuration
- Streamlit app should be runnable via `streamlit run` with minimal setup

## 5. Acceptance Criteria

- [ ] All 4 models load and produce valid outputs on sample math problems
- [ ] All 5 prompt methods generate correctly formatted prompts and responses
- [ ] Evaluation pipeline correctly extracts answers and computes accuracy on at least 95% of test cases
- [ ] At least 50 problems per dataset are evaluated per model-method combination for pilot experiments
- [ ] Streamlit demo allows interactive problem solving with at least 2 models and 3 prompt methods
- [ ] Dashboard displays accuracy comparison charts across models and methods
- [ ] All experiments are reproducible from saved configuration files
- [ ] Progress report (due April 22) is generated from experimental results
- [ ] Final report sections (introduction, related work, methodology, experiments, discussion) are supported by experiment data
- [ ] Presentation slides are included in the final report appendix
- [ ] Source code runs end-to-end with `pip install -r requirements.txt` followed by documented commands

## 6. Models

| Model | Type | Scale | Inference | Notes |
|-------|------|-------|-----------|-------|
| Qwen2.5-Math-1.5B | Open | 1.5B | Local (CPU, GGUF) | Required by topic |
| DeepSeek-R1-Qwen-1.5B | Open | 1.5B | Local (CPU, GGUF) | Required by topic |
| GPT-4o-mini | Closed (API) | ~8B equivalent | API (OpenAI) | Additional comparison |
| DeepSeek Chat | Closed (API) | V3 | API (DeepSeek) | Additional comparison |

## 7. Prompt Methods

| Method | Type | Key Idea | Expected Complexity |
|--------|------|----------|-------------------|
| Chain-of-Thought (CoT) | Baseline | Step-by-step reasoning instructions | Low (single-pass) |
| Self-Consistency | Sampling | Multiple samples, majority vote | Medium (N passes) |
| Self-Refine | Iterative | Generate → self-critique → refine | Medium (2-3 rounds) |
| Least-to-Most | Decomposition | Break problem into sub-problems | Medium (multi-step) |
| PVP (Ours) | Verification | CoT + interspersed self-check | Medium (single-pass, longer prompt) |

## 8. Datasets

| Dataset | Problems | Difficulty | Domain | Source |
|---------|----------|------------|--------|--------|
| MATH-500 | 500 | Competition | Algebra, Geometry, Number Theory, etc. | HuggingFace |
| GSM8K (Test) | 1,319 | Elementary | Grade school math word problems | HuggingFace |
| AIME 2024 | 30 | Advanced | Competition mathematics | Manual/Auto |

## 9. Evaluation Metrics

| Metric | Type | Description |
|--------|------|-------------|
| Accuracy | Primary | Exact match of extracted answer with ground truth |
| Response Length | Secondary | Character count / token count of model response |
| Step-level Correctness (New) | Exploratory | Percentage of reasoning steps that are logically correct |
| Token Efficiency | Exploratory | Accuracy per 1K tokens consumed |

## 10. Deliverables

### 10.1 Source Code

| Component | Location | Description |
|-----------|----------|-------------|
| Data Pipeline | `src/data/` | 数据加载 (`loader.py`) 与预处理 (`preprocessor.py`)，支持 MATH-500、GSM8K、AIME 2024 三个 HuggingFace 数据集 |
| Model Inference | `src/models/` | 本地 GGUF 推理 (`local_model.py`)、API 推理 (`api_model.py`)、多模型路由 (`router.py`) |
| Prompt Methods | `src/prompts/` | 5 种提示方法实现：CoT (`cot.py`)、Self-Consistency (`self_consistency.py`)、Self-Refine (`self_refine.py`)、Least-to-Most (`least_to_most.py`)、PVP (`pvp.py`) |
| Evaluation | `src/evaluation/` | 答案提取 (`answer_extractor.py`)、数学表达式解析 (`math_parser.py`)、指标计算 (`metrics.py`) |
| Experiment Runner | `src/experiment/` | 实验编排 (`runner.py`)、配置管理 (`config.py`)、断点续传与结果持久化 (`results_store.py`) |
| Streamlit Web Demo | `src/app/` | 交互式数学求解器、实验结果仪表盘、模型/方法对比分析 |
| Scripts | `scripts/` | 模型下载 (`download_models.py`)、数据下载 (`download_datasets.py`)、实验运行 (`run_experiment.py`)、结果聚合 (`aggregate_results.py`)、可视化图表生成 (`generate_figures.py`) |
| Jupyter Notebooks | `notebooks/` | 数据探索 (`01_data_exploration.ipynb`)、提示方法测试 (`02_prompt_testing.ipynb`)、结果分析 (`03_results_analysis.ipynb`) |
| Unit Tests | `tests/` | 63 个单元测试，覆盖提示方法、答案提取、指标计算三大模块 |

**技术栈**: Python 3.10+, llama-cpp-python (GGUF/CPU), OpenAI SDK, HuggingFace datasets, Streamlit, Plotly, SymPy, pytest

### 10.2 Project Report (Final Report)

- **格式要求**: ≤ 6 页正文 + 不限页数的参考文献和附录
- **截止日期**: 2026 年 5 月 6 日（周三）18:00
- **章节结构**:

| Section | Content | Data Source |
|---------|---------|-------------|
| Introduction | 研究背景、研究问题、主要贡献 | — |
| Related Work | CoT、Self-Consistency、Self-Refine、Least-to-Most 等文献综述 | References [1]–[6] |
| Methodology | 5 种提示方法的详细设计（含 PVP 创新方法）、实验设置 | `src/prompts/`, `SPEC.md §7` |
| Experiments | 2 模型 × 5 方法 × 2+ 数据集的完整实验结果和分析 | `results/RESULTS.md`, `results/figures/` |
| Discussion | 关键发现、局限性、未来工作 | `results/RESULTS.md §5–6` |
| Appendix | 演示幻灯片、补充实验数据、代码片段 | `docs/PRESENTATION.md`, `notebooks/` |

### 10.3 Progress Report

- **格式要求**: ≤ 5 页
- **截止日期**: 2026 年 4 月 22 日（周二）
- **要求内容**:
  - 项目目标与研究问题
  - 已完成工作（数据管道、模型推理、提示方法实现、初步实验结果）
  - 初步实验数据（已有 57.93% 总体准确率，7 张可视化图表）
  - 接下来的计划与时间表
- **模板位置**: `docs/PROGRESS_REPORT.md`

### 10.4 Presentation

- **时长**: 15 分钟课堂报告
- **形式**: 幻灯片 + 现场演示
- **幻灯片大纲** (参见 `docs/PRESENTATION.md`):

| Slide | Topic | Time |
|-------|-------|------|
| 1 | Title & Team Introduction | 1 min |
| 2–3 | Background & Motivation | 2 min |
| 4–5 | Methodology — 5 Prompt Methods + PVP Design | 3 min |
| 6–7 | Experimental Setup (Models, Datasets, Config) | 2 min |
| 8–10 | Results & Analysis (Accuracy, Heatmap, Efficiency) | 3 min |
| 11–12 | Key Findings & Discussion | 2 min |
| 13 | Demo (Streamlit interactive solver) | 1 min |
| 14–15 | Conclusion & Q&A | 1 min |

### 10.5 README.md

- **语言**: 中文
- **内容要求**:
  - 项目概述与核心结果摘要
  - 完整的环境搭建指南（依赖安装、模型下载、数据下载）
  - 实验复现步骤（端到端命令行流程）
  - 模型与提示方法说明
  - 项目目录结构说明
  - 配置文件与 CLI 参数说明
  - 团队信息与参考文献
- **位置**: 项目根目录 `README.md`
