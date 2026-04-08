# ARCHITECTURE.md

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Streamlit Web Demo                        │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────────────┐ │
│  │ Interactive   │ │  Dashboard   │ │  Comparison Analysis │ │
│  │  Solver       │ │  (Charts)    │ │  (Model x Method)    │ │
│  └──────┬───────┘ └──────┬───────┘ └──────────┬───────────┘ │
└─────────┼────────────────┼────────────────────┼─────────────┘
          │                │                    │
┌─────────▼────────────────▼────────────────────▼─────────────┐
│                   Experiment Runner                          │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────────────┐ │
│  │ Runner       │ │ Config       │ │ Results Store (JSON) │ │
│  │ (checkpoint) │ │ Manager      │ │                      │ │
│  └──────┬───────┘ └──────┬───────┘ └──────────▲───────────┘ │
└─────────┼────────────────┼────────────────────┼─────────────┘
          │                │                    │
┌─────────▼────────────────▼────────────────────┼─────────────┐
│                   Core Pipeline               │             │
│  ┌──────────┐ ┌──────────┐ ┌────────┐ ┌──────┴───────────┐ │
│  │  Data    │ │  Prompt  │ │ Model  │ │   Evaluation     │ │
│  │  Loader  │─│  Engine  │─│ Router │─│   (Accuracy,     │ │
│  │          │ │          │ │        │ │    Metrics)      │ │
│  └────▲─────┘ └──────────┘ └───┬────┘ └──────────────────┘ │
└─────┼──────────────────────────┼───────────────────────────┘
      │                          │
┌─────▼──────────┐    ┌──────────▼──────────┐
│   Datasets      │    │      Models         │
│ MATH-500        │    │ Local (GGUF/CPU)    │
│ GSM8K           │    │  - Qwen2.5-Math-1.5B│
│ AIME 2024       │    │  - DeepSeek-R1-1.5B │
│                  │    │ API                 │
│                  │    │  - GPT-4o-mini      │
│                  │    │  - DeepSeek Chat    │
└─────────────────┘    └─────────────────────┘
```

## Module Map

| Module | Path | Responsibility |
|--------|------|----------------|
| Data Loader | `src/data/loader.py` | Download and load datasets from HuggingFace |
| Preprocessor | `src/data/preprocessor.py` | Clean and normalize dataset format |
| Local Model | `src/models/local_model.py` | Load GGUF models and run CPU inference |
| API Model | `src/models/api_model.py` | Call OpenAI/DeepSeek API for inference |
| Model Router | `src/models/router.py` | Route inference requests to correct model backend |
| Prompt Base | `src/prompts/base.py` | Base class for all prompt methods |
| CoT | `src/prompts/cot.py` | Chain-of-Thought prompting |
| Self-Consistency | `src/prompts/self_consistency.py` | Multi-sample majority voting |
| Self-Refine | `src/prompts/self_refine.py` | Iterative self-critique and refinement |
| Least-to-Most | `src/prompts/least_to_most.py` | Problem decomposition prompting |
| PVP | `src/prompts/pvp.py` | Progressive Verification Prompting (novel) |
| Answer Extractor | `src/evaluation/answer_extractor.py` | Extract final answer from model response |
| Metrics | `src/evaluation/metrics.py` | Compute accuracy, response length, etc. |
| Math Parser | `src/evaluation/math_parser.py` | Parse and normalize math expressions |
| Runner | `src/experiment/runner.py` | Batch experiment execution with checkpoint |
| Config | `src/experiment/config.py` | Experiment configuration management |
| Results Store | `src/experiment/results_store.py` | JSON-based results persistence |
| Streamlit App | `src/app/main.py` | Web demo entry point |
| Interactive Page | `src/app/pages/01_interactive.py` | Interactive math problem solver |
| Dashboard Page | `src/app/pages/02_dashboard.py` | Experiment results dashboard |
| Comparison Page | `src/app/pages/03_comparison.py` | Model/method comparison analysis |

## Key Data Flows

### Flow 1: Single Problem Inference
```
User Input (problem text)
  → PromptEngine.format(problem, method="cot", model="qwen2.5-math")
  → ModelRouter.infer(prompt, model="qwen2.5-math")
  → ResponseParser.parse(response)
  → AnswerExtractor.extract(parsed_response)
  → Evaluator.evaluate(extracted_answer, ground_truth)
```

### Flow 2: Batch Experiment
```
ExperimentConfig.load("configs/exp_cot_qwen.yaml")
  → Runner.run(config)
    → for each dataset problem (with checkpoint):
        → PromptEngine.format() → ModelRouter.infer()
        → AnswerExtractor.extract() → Metrics.compute()
    → ResultsStore.save(results)
  → Dashboard.render(results)
```

### Flow 3: Streamlit Interactive
```
User enters problem + selects model + selects method
  → Backend: PromptEngine → ModelRouter → AnswerExtractor
  → Display: original problem, full response, extracted answer, confidence
```

## Affected Modules (iter-1)
All modules are new in this iteration — no existing modules to modify.
