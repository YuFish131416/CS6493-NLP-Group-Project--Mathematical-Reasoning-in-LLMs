# REQUIREMENTS.md — User Requirements Agreement

> This document records all agreed-upon requirements and constraints from the initial consultation on 2026-04-08.

## Basic Info
- **Course**: CS6493 Natural Language Processing, City University of Hong Kong, Q2 2025-2026
- **Topic**: Topic 1 — Mathematical Reasoning Ability of Large Language Models
- **Deadline**: May 6, 2026 (Wednesday) 6:00 PM
- **Progress Report Deadline**: April 22, 2026

## Team Composition
- **Size**: 5 members
- **Background**: Mixed — some members have weaker NLP/ML foundations
- **Language**: Code with English comments, report in English, README bilingual

## Resource Constraints
- **Compute**: Only regular laptops, **no GPU available**
- **Model Inference Strategy**: Small models (1.5B) run locally on CPU; larger models via cloud API
- **Budget**: Minimal API spend; use free tiers and token limits

## Target & Effort
- **Target Grade**: B+ to A-
- **Effort Level**: Medium — balanced between quality and time investment

## Project Type
- **Type**: Mixed — both experimental research and demonstrable system
- **System**: Simple Web UI using Streamlit/Gradio for interactive demonstration

## Model Selection
1. **Qwen2.5-Math-1.5B** (Local, CPU) — **required by topic**
2. **DeepSeek-R1-Qwen-1.5B** (Local, CPU) — **required by topic**
3. **GPT-4o-mini** (API, OpenAI) — additional model for richer comparison
4. **DeepSeek Chat** (API) — additional model for richer comparison

## Prompt Methods (5 total)
1. **Chain-of-Thought (CoT)** — baseline
2. **Self-Consistency** — multi-sample majority voting
3. **Self-Refine** — iterative self-critique
4. **Least-to-Most** — problem decomposition
5. **PVP (Progressive Verification Prompting)** — **novel method, main innovation point**

## Datasets
- MATH-500 (500 problems, competition level)
- GSM8K Test Set (~1,319 problems, grade school level)
- AIME 2024 (30 problems, advanced competition)

## Evaluation Metrics
- **Accuracy** (primary) — exact match of extracted answer
- **Response Length** (secondary) — character/token count
- **Step-level Correctness** (exploratory/new) — fraction of correct reasoning steps
- **Token Efficiency** (exploratory/new) — accuracy per 1K tokens

## Deliverables
1. Source code (Python modules + Jupyter Notebooks)
2. Project report (≤6 pages main + unlimited refs/appendix with slides)
3. Progress report (≤5 pages, due April 22)
4. 15-minute in-class presentation
5. README.md with setup/usage instructions

## Workflow Agreement
- Follow `plan/AGENT_STARTUP.md` phases strictly
- Record all plan/ docs per the schemas defined
- Create `process/REQUIREMENTS.md` to persist agreements (this file)
- No code changes before Phase 2 (Planning) is complete
