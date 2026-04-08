# CS6493 NLP 小组项目：大语言模型的数学推理能力

> 通过系统化的提示工程（Prompt Engineering），评估和提升大语言模型的数学推理能力。

**课程**：CS6493 自然语言处理，香港城市大学，2025-2026 学年第二学期
**选题**：课题 1 — 大语言模型的数学推理能力
**截止日期**：2026 年 5 月 6 日

---

## 项目概述

本项目系统性地评估了不同提示策略对大语言模型数学推理性能的影响，涵盖不同规模的模型和不同难度的数学问题。我们提出了一种新颖的提示方法 — **渐进验证提示法（Progressive Verification Prompting, PVP）** — 通过在推理过程中穿插自我验证检查点来提高准确率。

### 核心实验结果

| 指标 | 数值 |
|------|------|
| 总体准确率 | **58.97%**（92/156） |
| 最佳模型 | Qwen2.5-Math-1.5B（**65.8%**） |
| 最佳方法 | Least-to-Most（**69.6%**） |
| PVP（我们的方法） | **64.0%**（优于 CoT 基线） |

完整实验结果与分析请参见 [`results/RESULTS.md`](results/RESULTS.md)。

---

## 快速开始 — 复现我们的实验结果

### 前置要求

- **Python**: 3.10+
- **磁盘空间**: 约 2.5 GB（模型文件）+ 约 200 MB（数据集）
- **内存**: 建议 8 GB 以上（模型通过 llama.cpp 在 CPU 上运行）

### 第 1 步：克隆仓库并搭建环境

```bash
git clone <repo-url>
cd "Group Project"

# 创建虚拟环境（推荐）
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

> **提示**：如果 `datasets` 或 `huggingface_hub` 出现兼容性问题，`requirements.txt` 中已锁定经过测试的版本组合。

### 第 2 步：创建配置文件

```bash
# 复制配置模板
cp config/config.example.yaml config/config.local.yaml
```

默认的 `config.local.yaml` 已预配置为仅使用本地 GGUF 模型，无需 API 密钥即可运行核心实验。

如需使用 API 模型（GPT-4o-mini、DeepSeek Chat）：
```bash
cp .env.example .env
# 编辑 .env 文件并添加 API 密钥：
#   OPENAI_API_KEY=sk-...
#   DEEPSEEK_API_KEY=sk-...
```

### 第 3 步：下载 GGUF 模型（共约 2.5 GB）

```bash
python scripts/download_models.py
```

此命令将下载两个 Q4_K_M 量化模型到 `models/` 目录：
- `qwen2.5-math-1.5b-q4_k_m.gguf`（约 1.1 GB）— 数学专用模型
- `deepseek-r1-qwen-1.5b-q4_k_m.gguf`（约 1.1 GB）— 通用推理模型

> **故障排除**：如果下载因网络问题失败，可以手动从 HuggingFace 下载：
> - [Qwen2.5-Math-1.5B GGUF](https://huggingface.co/QuantFactory/Qwen2.5-Math-1.5B-Instruct-GGUF) — 文件名: `Qwen2.5-Math-1.5B-Instruct.Q4_K_M.gguf`
> - [DeepSeek-R1-Qwen-1.5B GGUF](https://huggingface.co/bartowski/DeepSeek-R1-Distill-Qwen-1.5B-GGUF) — 文件名: `DeepSeek-R1-Distill-Qwen-1.5B-Q4_K_M.gguf`
>
> 将文件放入 `models/` 目录并重命名为上述预期文件名。

### 第 4 步：下载数据集

```bash
python scripts/download_datasets.py
```

从 HuggingFace 下载并预处理 3 个基准数据集：

| 数据集 | HuggingFace ID | 数据划分 | 规模 |
|--------|---------------|----------|------|
| MATH-500 | `HuggingFaceH4/MATH-500` | test | 500 道题 |
| GSM8K | `openai/gsm8k` | test | 1,319 道题 |
| AIME 2024 | `HuggingFaceH4/aime_2024` | train | 30 道题 |

数据集缓存在 HuggingFace 默认缓存目录（`~/.cache/huggingface/`）。

### 第 5 步：运行实验

```bash
# 使用默认配置运行（2 模型 × 5 方法 × 2 数据集 × 每组 20 题）
python scripts/run_experiment.py

# 自定义运行：
python scripts/run_experiment.py --sample-size 5                    # 快速测试
python scripts/run_experiment.py --models qwen2.5-math              # 单模型
python scripts/run_experiment.py --methods cot,pvp --datasets gsm8k # 指定子集
python scripts/run_experiment.py --sample-size 50 --verbose         # 大规模运行
```

**预估运行时间**（CPU 推理）：
- 快速测试（`--sample-size 3`）：约 5–10 分钟
- 默认配置（`--sample-size 20`）：约 1–3 小时
- 每道题约需 10–70 秒，取决于模型和提示方法

实验运行器支持**断点续传** — 如果中途中断，重新运行相同命令即可跳过已完成的问题。

### 第 6 步：聚合结果并生成可视化

```bash
# 将所有检查点结果聚合为最终 JSON
python scripts/aggregate_results.py

# 生成可视化图表
python scripts/generate_figures.py
```

结果将保存到：
- `results/json/final_summary.json` — 聚合统计数据
- `results/json/final_results.json` — 包含所有响应的完整结果
- `results/figures/` — 7 张可视化图表（PNG 格式）

### 第 7 步：运行测试

```bash
# 运行所有单元测试
pytest tests/ -v

# 运行指定测试文件
pytest tests/test_prompts.py -v
```

---

## 模型

| 模型 | 参数规模 | 类型 | 说明 |
|------|---------|------|------|
| Qwen2.5-Math-1.5B | 1.5B | 本地 (GGUF) | 数学专用模型，在数学数据上微调 |
| DeepSeek-R1-Qwen-1.5B | 1.5B | 本地 (GGUF) | 通用推理模型，从 DeepSeek-R1 蒸馏 |
| GPT-4o-mini | 约 8B 等效 | API (OpenAI) | 附加模型 — 需要 API 密钥 |
| DeepSeek Chat | V3 | API (DeepSeek) | 附加模型 — 需要 API 密钥 |

## 提示方法

| 方法 | 类型 | 说明 |
|------|------|------|
| **链式思维（CoT）** | 基线 | 逐步推理 |
| **自一致性（Self-Consistency）** | 采样 | 多次采样 + 多数投票（n=5） |
| **自我优化（Self-Refine）** | 迭代 | 自我批评 + 优化（最多 2 轮） |
| **从少到多（Least-to-Most）** | 分解 | 拆解子问题，逐步求解 |
| **渐进验证提示（PVP，我们的方法）** | 验证 | 渐进式逐步自检 |

---

## 项目结构

```
project-root/
├── config/                 # 配置文件
│   ├── config.example.yaml # 配置模板（复制为 config.local.yaml 使用）
│   └── config.local.yaml   # 本地配置（git-ignored）
│
├── src/                    # 源代码
│   ├── data/               # 数据集加载与预处理
│   │   ├── loader.py       # HuggingFace 数据集加载器
│   │   └── preprocessor.py # 统一预处理
│   ├── models/             # 模型推理
│   │   ├── local_model.py  # 通过 llama-cpp-python 运行 GGUF 模型
│   │   └── router.py       # 多模型路由器
│   ├── prompts/            # 5 种提示方法实现
│   │   ├── cot.py          # 链式思维（Chain-of-Thought）
│   │   ├── self_consistency.py  # 自一致性
│   │   ├── self_refine.py       # 自我优化
│   │   ├── least_to_most.py     # 从少到多
│   │   └── pvp.py               # 渐进验证提示（我们的方法）
│   ├── evaluation/         # 答案提取与指标计算
│   │   ├── answer_extractor.py  # 答案提取器
│   │   ├── math_parser.py       # 数学表达式解析器
│   │   └── metrics.py           # 评估指标
│   ├── experiment/         # 实验编排
│   │   ├── config.py       # 实验配置加载器
│   │   ├── runner.py       # 主实验运行器
│   │   └── results_store.py # 断点保存与加载
│   └── app/                # Streamlit Web 演示（可选）
│
├── scripts/                # 可运行脚本
│   ├── download_models.py  # 下载 GGUF 模型文件
│   ├── download_datasets.py # 下载 HuggingFace 数据集
│   ├── run_experiment.py   # 通过 CLI 参数运行实验
│   ├── aggregate_results.py # 将检查点聚合为最终结果
│   └── generate_figures.py # 生成可视化图表
│
├── tests/                  # 单元测试（63 个测试）
│   ├── test_prompts.py
│   ├── test_answer_extractor.py
│   └── test_metrics.py
│
├── results/                # 实验结果
│   ├── RESULTS.md          # 最终结果文档（含分析）
│   ├── figures/            # 可视化图表（PNG）
│   ├── json/               # 机器可读的结果数据（JSON）
│   └── checkpoints/        # 逐题检查点文件
│
├── notebooks/              # Jupyter 探索性笔记本
├── docs/                   # 文档
├── plan/                   # 项目规划文档
├── process/                # 任务进度追踪
│
├── models/                 # GGUF 模型文件（git-ignored，约 2.5 GB）
├── data/                   # 数据集缓存（git-ignored）
│
├── requirements.txt        # Python 依赖
├── SPEC.md                 # 项目技术规格书
├── .env.example            # API 密钥模板
└── README.md               # 本文件
```

---

## 配置说明

### `config/config.local.yaml`

关键配置项：

```yaml
models:
  qwen2.5-math:
    type: local
    model_path: "models/qwen2.5-math-1.5b-q4_k_m.gguf"
    max_context: 4096

experiments:
  temperature: 0.0        # 确定性采样
  max_tokens: 2048        # 最大生成 token 数
  seed: 42                # 随机种子
  n_samples: 5            # Self-Consistency 采样次数
  max_refine_rounds: 2    # Self-Refine 最大迭代轮数
  sample_size: 20         # 每个数据集的题目数
```

### `run_experiment.py` CLI 参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--config` | 配置 YAML 文件路径 | `config/config.local.yaml` |
| `--sample-size` | 每个数据集的题目数 | 配置文件中的值 |
| `--models` | 逗号分隔的模型名称 | 配置文件中的值 |
| `--methods` | 逗号分隔的提示方法 | 配置文件中的值 |
| `--datasets` | 逗号分隔的数据集名称 | 配置文件中的值 |
| `--run-id` | 自定义运行 ID（用于断点续传） | 自动生成 |
| `--n-samples` | Self-Consistency 采样次数 | 配置文件中的值 |
| `--max-refine-rounds` | Self-Refine 最大迭代轮数 | 配置文件中的值 |
| `--verbose` | 启用调试日志 | `False` |

---

## 已测试的依赖版本

以下版本组合已通过测试并确认可正常运行：

| 包名 | 版本 |
|------|------|
| Python | 3.10+ |
| llama-cpp-python | 0.2.90+ |
| datasets | 2.19.0 |
| huggingface_hub | 0.23.5 |
| matplotlib | 3.5.3+ |
| transformers | 4.40.0+ |
| sympy | 1.12+ |

> **已知问题**：`datasets >= 4.0` 配合 `huggingface_hub >= 0.26` 可能在加载缓存数据集时出现 `validate_repo_id` 错误。请使用 `requirements.txt` 中锁定的版本以避免此问题。

---

## 团队

5 名成员 — 任务分工详见 `process/REQUIREMENTS.md`。

## 参考文献

1. Wei J, et al. *Chain-of-thought prompting elicits reasoning in large language models.* NeurIPS 2022.
2. Wang X, et al. *Self-consistency improves chain of thought reasoning.* NeurIPS 2022.
3. Madaan A, et al. *Self-refine: Iterative refinement with self-feedback.* NeurIPS 2024.
4. Zhou D, et al. *Least-to-Most Prompting Enables Complex Reasoning.* NeurIPS 2023.
5. Cobbe K, et al. *Training verifiers to solve math word problems.* 2021.
6. Zhang Z, et al. *Automatic Chain of Thought Prompting.* 2022.

---

## 交付物清单

所有交付物整合在 [`deliverables/`](deliverables/) 文件夹下，详见 [`deliverables/DELIVERABLES_INDEX.md`](deliverables/DELIVERABLES_INDEX.md)。

### 交付物总览

| # | 交付物 | 文件位置 | 说明 |
|---|--------|----------|------|
| 1 | **源代码** | `src/`、`scripts/`、`tests/`、`notebooks/` | 30 个 Python 模块 + 5 个脚本 + 63 个单元测试 + 3 个 Jupyter Notebook |
| 2 | **项目终期报告** | [`deliverables/project_report.md`](deliverables/project_report.md) | ≤ 6 页正文：Introduction → Related Work → Methodology → Experiments → Discussion → Conclusion + 附录（提示模板、架构图、可视化图表） |
| 3 | **中期进度报告** | [`deliverables/progress_report.md`](deliverables/progress_report.md) | ≤ 5 页：项目目标、方法论、初步实验结果（58.97% 准确率）、后续计划，截止 4 月 22 日 |
| 4 | **课堂演示大纲** | [`deliverables/presentation.md`](deliverables/presentation.md) | 15 分钟 / 15 页幻灯片 + 备用幻灯片，含 Streamlit 现场 Demo |
| 5 | **README 文档** | [`README.md`](README.md)（本文件） | 中文，含环境搭建、实验复现、配置说明 |

### 详细内容索引

#### 📦 1. 源代码

| 模块 | 路径 | 文件数 | 功能 |
|------|------|--------|------|
| 数据管道 | `src/data/` | 3 | HuggingFace 数据集加载与预处理（MATH-500、GSM8K、AIME 2024） |
| 模型推理 | `src/models/` | 4 | 本地 GGUF/CPU 推理 + API 推理 + 多模型路由 |
| 提示方法 | `src/prompts/` | 6 | 5 种方法：CoT、Self-Consistency、Self-Refine、Least-to-Most、**PVP（创新方法）** |
| 评估框架 | `src/evaluation/` | 4 | 答案提取、数学表达式解析（SymPy）、指标计算 |
| 实验引擎 | `src/experiment/` | 4 | 批量运行、配置管理、断点续传 |
| Web 演示 | `src/app/` | 5 | Streamlit 交互求解器 + 结果仪表盘 + 对比分析 |
| 脚本 | `scripts/` | 5 | 模型下载、数据下载、实验运行、结果聚合、图表生成 |
| Notebook | `notebooks/` | 3 | 数据探索、提示测试、结果分析 |
| 单元测试 | `tests/` | 4 | 63 个测试用例（全部通过 ✅） |

#### 📝 2. 项目终期报告 (`deliverables/project_report.md`)

- **格式**：≤ 6 页正文 + 不限页数附录
- **章节**：
  - §1 Introduction — 研究背景、三个研究问题、主要贡献
  - §2 Related Work — CoT、Self-Consistency、Self-Refine、Least-to-Most、Self-Verification 文献综述
  - §3 Methodology — 5 种提示方法详细设计（含 PVP 理论基础）、模型、数据集、评估方法
  - §4 Experiments — 14 组实验结果表格、模型×方法交叉分析、效率分析
  - §5 Discussion — 5 大关键发现
  - §6 Limitations — 样本量、模型规模、缺失数据集等局限
  - §7 Conclusion — 总结与未来工作
  - Appendix A-E — PVP 模板、全部提示模板、系统架构、可视化图表、演示大纲

#### 📋 3. 中期进度报告 (`deliverables/progress_report.md`)

- **格式**：≤ 5 页
- **章节**：
  - §1 Introduction — 项目目标与研究问题
  - §2 Related Work — 6 篇核心文献综述
  - §3 Methodology — 问题形式化、5 种方法设计、实验配置
  - §4 Preliminary Results — 156 题实验数据（模型/方法/数据集对比表格）
  - §5 Progress & Plan — 已完成 9 项里程碑 + 6 项后续计划 + 时间表
  - §6 Challenges — 6 个技术挑战及解决方案
  - Appendix A-C — 提示模板、系统架构

#### 🎤 4. 课堂演示 (`deliverables/presentation.md`)

- **时长**：15 分钟（含 Q&A）
- **内容**：
  - Slide 1 — 标题与团队
  - Slide 2 — 研究动机与背景
  - Slide 3 — 三个研究问题
  - Slide 4 — 4 种基线方法介绍
  - Slide 5 — **PVP 创新方法** 详细设计
  - Slide 6 — 实验设置（模型、数据集、配置）
  - Slide 7 — 系统架构
  - Slide 8-9 — 实验结果（准确率对比、热力图）
  - Slide 10 — PVP 深入分析
  - Slide 11 — 效率分析
  - Slide 12 — 讨论与洞察（5 大发现）
  - Slide 13 — **Streamlit 现场 Demo**
  - Slide 14 — 结论与未来工作
  - Slide 15 — Q&A
  - Backup — 详细数据、错误分析示例、技术栈

#### 📊 5. 实验结果 (`results/`)

| 资源 | 路径 | 说明 |
|------|------|------|
| 结果分析文档 | `results/RESULTS.md` | 230 行完整实验报告（含 5 大发现、6 项局限） |
| 聚合统计 | `results/json/final_summary.json` | 14 组模型×方法×数据集准确率数据 |
| 完整结果 | `results/json/final_results.json` | 156 道题的完整推理响应 |
| 检查点 | `results/checkpoints/` | 135+ 个逐题检查点文件 |
| **可视化图表** | `results/figures/` | **7 张 PNG 图表**（见下） |

**7 张可视化图表**：

| 图表 | 文件 | 内容 |
|------|------|------|
| 图 1 | `fig1_accuracy_by_model.png` | 按模型分组的准确率柱状图 |
| 图 2 | `fig2_accuracy_by_method.png` | 按提示方法的准确率排名 |
| 图 3 | `fig3_accuracy_by_dataset.png` | 按数据集的准确率对比 |
| 图 4 | `fig4_model_x_method.png` | 模型 × 方法交叉分组柱状图 |
| 图 5 | `fig5_heatmap_model_method.png` | 模型 × 方法准确率热力图 |
| 图 6 | `fig6_length_vs_accuracy.png` | 响应长度 vs 准确率散点图 |
| 图 7 | `fig7_latency_by_method.png` | 各方法推理延迟对比 |

---

## 许可证

本项目仅用于教育目的（CS6493 课程作业）。
