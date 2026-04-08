# 交付物清单 / Deliverables Index

> **CS6493 NLP 小组项目** — 大语言模型的数学推理能力
> **截止日期**：2026 年 5 月 6 日（周三）18:00

---

## 📋 交付物总览

| # | 交付物 | 文件位置 | 状态 | 截止日期 |
|---|--------|----------|------|----------|
| 1 | **源代码** | `src/`, `scripts/`, `tests/`, `notebooks/` | ✅ 已完成 | 5 月 6 日 |
| 2 | **项目终期报告** | [`deliverables/project_report.md`](project_report.md) | ✅ 已完成 | 5 月 6 日 |
| 3 | **中期进度报告** | [`deliverables/progress_report.md`](progress_report.md) | ✅ 已完成 | 4 月 22 日 |
| 4 | **课堂演示大纲** | [`deliverables/presentation.md`](presentation.md) | ✅ 已完成 | 5 月 6 日 |
| 5 | **README 文档** | [`README.md`](../README.md) | ✅ 已完成 | 5 月 6 日 |
| 6 | **实验结果与可视化** | [`results/`](../results/) | ✅ 已完成 | — |

---

## 1. 源代码 (Source Code)

完整的 Python 实验框架，包含数据管道、模型推理、提示方法、评估指标和实验编排。

### 1.1 核心模块 (`src/`)

| 模块 | 路径 | 文件数 | 功能描述 |
|------|------|--------|----------|
| **数据管道** | `src/data/` | 3 | HuggingFace 数据集加载（`loader.py`）、统一预处理（`preprocessor.py`），支持 MATH-500、GSM8K、AIME 2024 |
| **模型推理** | `src/models/` | 4 | 本地 GGUF/CPU 推理（`local_model.py`）、API 推理（`api_model.py`）、多模型路由（`router.py`） |
| **提示方法** | `src/prompts/` | 6 | 5 种方法实现：CoT、Self-Consistency、Self-Refine、Least-to-Most、**PVP（创新方法）** |
| **评估框架** | `src/evaluation/` | 4 | 答案提取（`answer_extractor.py`）、数学解析（`math_parser.py`）、指标计算（`metrics.py`） |
| **实验引擎** | `src/experiment/` | 4 | 批量运行（`runner.py`）、配置管理（`config.py`）、断点续传（`results_store.py`） |
| **Web 演示** | `src/app/` | 5 | Streamlit 交互求解器、结果仪表盘、对比分析 |

### 1.2 脚本 (`scripts/`)

| 脚本 | 功能 |
|------|------|
| `download_models.py` | 从 HuggingFace 下载 Q4_K_M 量化 GGUF 模型（约 2.5 GB） |
| `download_datasets.py` | 下载并缓存 MATH-500、GSM8K、AIME 2024 数据集 |
| `run_experiment.py` | 主实验运行器（支持 CLI 参数自定义模型/方法/数据集/样本数） |
| `aggregate_results.py` | 聚合检查点结果为最终 JSON 汇总 |
| `generate_figures.py` | 生成 7 张可视化图表（PNG） |

### 1.3 Jupyter Notebooks (`notebooks/`)

| Notebook | 功能 |
|----------|------|
| `01_data_exploration.ipynb` | 数据集加载与探索（分布统计、样例展示） |
| `02_prompt_testing.ipynb` | 提示模板测试、答案提取验证、数学等价性检测 |
| `03_results_analysis.ipynb` | 实验结果可视化分析（热力图、分组柱状图） |

### 1.4 单元测试 (`tests/`)

| 测试文件 | 测试数 | 覆盖内容 |
|----------|--------|----------|
| `test_prompts.py` | 20 | 5 种提示方法的格式化输出验证 |
| `test_answer_extractor.py` | 10 | 多格式答案提取（`\boxed{}`、`####`、纯数字等） |
| `test_metrics.py` | 14 | 准确率计算、数学表达式归一化、等价性匹配 |
| **合计** | **63** | 全部通过 ✅ |

---

## 2. 项目终期报告 (Final Report)

- **文件**: [`deliverables/project_report.md`](project_report.md)
- **格式**: ≤ 6 页正文 + 不限页数参考文献与附录
- **章节**: Introduction → Related Work → Methodology → Experiments → Discussion → Conclusion → References → Appendix

---

## 3. 中期进度报告 (Progress Report)

- **文件**: [`deliverables/progress_report.md`](progress_report.md)
- **格式**: ≤ 5 页
- **截止**: 2026 年 4 月 22 日
- **内容**: 项目目标、方法论、初步实验结果（58.97% 准确率）、后续计划

---

## 4. 课堂演示 (Presentation)

- **文件**: [`deliverables/presentation.md`](presentation.md)
- **时长**: 15 分钟
- **幻灯片数**: 15 页主要内容 + 备用幻灯片
- **演示**: 包含 Streamlit 现场 Demo

---

## 5. 实验结果 (Experiment Results)

| 资源 | 路径 | 说明 |
|------|------|------|
| 结果分析文档 | `results/RESULTS.md` | 完整实验结果报告（含 5 大发现） |
| 聚合统计 | `results/json/final_summary.json` | 14 组模型×方法×数据集组合的准确率 |
| 完整结果 | `results/json/final_results.json` | 156 道题的完整推理响应 |
| 可视化图表 | `results/figures/` | 7 张图表（见下表） |

### 可视化图表

| 文件 | 内容 |
|------|------|
| `fig1_accuracy_by_model.png` | 按模型分组的准确率对比 |
| `fig2_accuracy_by_method.png` | 按提示方法分组的准确率排名 |
| `fig3_accuracy_by_dataset.png` | 按数据集分组的准确率对比 |
| `fig4_model_x_method.png` | 模型 × 方法交叉分组柱状图 |
| `fig5_heatmap_model_method.png` | 模型 × 方法准确率热力图 |
| `fig6_length_vs_accuracy.png` | 响应长度 vs 准确率散点图 |
| `fig7_latency_by_method.png` | 各方法推理延迟对比 |

---

## 核心实验结果速览

| 指标 | 数值 |
|------|------|
| 总体准确率 | **58.97%**（92/156） |
| 最佳模型 | Qwen2.5-Math-1.5B（**65.83%**） |
| 最佳方法 | Least-to-Most（**69.57%**） |
| PVP（我们的创新） | **64.00%**（优于 CoT 基线 57.45%） |
| 最易数据集 | GSM8K（**75.00%**） |
| 最难数据集 | MATH-500（**56.06%**） |
