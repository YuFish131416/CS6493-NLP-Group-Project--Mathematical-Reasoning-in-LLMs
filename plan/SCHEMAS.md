# SCHEMAS.md

## MathProblem

| Field | Type | Nullable | Default | Constraint | Notes |
|-------|------|----------|---------|------------|-------|
| id | str | NO | auto | UNIQUE | Problem identifier |
| problem | str | NO | — | NOT EMPTY | Original problem text |
| answer | str | NO | — | — | Canonical answer string |
| solution | str | YES | None | — | Full step-by-step solution (MATH-500 only) |
| level | int | YES | None | 1–5 | Difficulty level (MATH-500 only) |
| type | str | YES | None | — | Problem category: Algebra, Geometry, etc. |
| dataset | str | NO | — | enum | Source dataset: "math500", "gsm8k", "aime2024" |

## ModelResponse

| Field | Type | Nullable | Default | Constraint | Notes |
|-------|------|----------|---------|------------|-------|
| problem_id | str | NO | — | FK → MathProblem.id | Referenced problem |
| model_name | str | NO | — | — | Model identifier |
| prompt_method | str | NO | — | — | Prompt method name |
| raw_response | str | NO | — | — | Full model output |
| extracted_answer | str | YES | None | — | Extracted answer, None if parse failed |
| is_correct | bool | YES | None | — | Whether extracted_answer matches ground truth |
| response_length | int | NO | 0 | ≥ 0 | Character count of raw_response |
| token_count | int | YES | None | ≥ 0 | Token count if available |
| latency_ms | float | NO | 0 | ≥ 0 | Inference time in milliseconds |
| timestamp | str | NO | — | ISO 8601 | When the inference was run |

## ExperimentConfig

| Field | Type | Nullable | Default | Constraint | Notes |
|-------|------|----------|---------|------------|-------|
| run_id | str | NO | auto | UNIQUE | Unique experiment run identifier |
| models | list[str] | NO | — | len ≥ 1 | List of model names to evaluate |
| prompt_methods | list[str] | NO | — | len ≥ 1 | List of prompt methods to use |
| datasets | list[str] | NO | — | len ≥ 1 | List of dataset names |
| sample_size | int | NO | -1 | -1 = all, ≥ 1 | Number of problems per dataset (-1 = all) |
| temperature | float | NO | 0.0 | 0.0–2.0 | Generation temperature |
| max_tokens | int | NO | 2048 | ≥ 1 | Max generation tokens |
| seed | int | NO | 42 | — | Random seed for reproducibility |
| n_samples | int | NO | 5 | ≥ 1 | Samples for Self-Consistency |
| max_refine_rounds | int | NO | 2 | ≥ 1 | Refinement rounds for Self-Refine |
| checkpoint_dir | str | NO | "results/checkpoints" | — | Checkpoint save directory |
| output_dir | str | NO | "results" | — | Results output directory |
| created_at | str | NO | — | ISO 8601 | Config creation time |

## ExperimentResults

| Field | Type | Nullable | Default | Constraint | Notes |
|-------|------|----------|---------|------------|-------|
| run_id | str | NO | — | FK → ExperimentConfig.run_id | Experiment run reference |
| config | dict | NO | — | — | Full experiment config snapshot |
| responses | list[ModelResponse] | NO | [] | — | All individual model responses |
| summary | dict | NO | — | — | Aggregated accuracy/stats per model-method-dataset |
| total_problems | int | NO | 0 | ≥ 0 | Total problems attempted |
| total_correct | int | NO | 0 | ≥ 0 | Total correct answers |
| overall_accuracy | float | NO | 0.0 | 0.0–1.0 | Overall accuracy across all experiments |
| completed_at | str | YES | None | ISO 8601 | When experiment finished |

## SummaryEntry (nested in ExperimentResults.summary)

| Field | Type | Nullable | Default | Constraint | Notes |
|-------|------|----------|---------|------------|-------|
| model | str | NO | — | — | Model name |
| method | str | NO | — | — | Prompt method name |
| dataset | str | NO | — | — | Dataset name |
| accuracy | float | NO | 0.0 | 0.0–1.0 | Accuracy on this combination |
| avg_response_length | float | NO | 0.0 | ≥ 0 | Average response length |
| avg_latency_ms | float | NO | 0.0 | ≥ 0 | Average inference latency |
| total | int | NO | 0 | ≥ 0 | Total problems |
| correct | int | NO | 0 | ≥ 0 | Correct answers |
| extract_success_rate | float | NO | 1.0 | 0.0–1.0 | Rate of successful answer extraction |

## ModelConfig

| Field | Type | Nullable | Default | Constraint | Notes |
|-------|------|----------|---------|------------|-------|
| name | str | NO | — | UNIQUE | Model identifier (e.g., "qwen2.5-math-1.5b") |
| type | str | NO | — | enum | "local" or "api" |
| model_path | str | YES | None | — | Path to GGUF file (local models) |
| api_base | str | YES | None | — | API endpoint URL (API models) |
| api_key_env | str | YES | None | — | Environment variable name for API key |
| max_context | int | NO | 4096 | ≥ 1 | Maximum context window size |
| system_prompt | str | YES | None | — | Default system prompt override |

## ConfigYAML (config.example.yaml)

```yaml
models:
  qwen2.5-math:
    type: local
    model_path: "models/qwen2.5-math-1.5b-q4_k_m.gguf"
    max_context: 4096
  deepseek-r1:
    type: local
    model_path: "models/deepseek-r1-qwen-1.5b-q4_k_m.gguf"
    max_context: 4096
  gpt-4o-mini:
    type: api
    api_base: "https://api.openai.com/v1"
    api_key_env: "OPENAI_API_KEY"
    max_context: 128000
  deepseek-chat:
    type: api
    api_base: "https://api.deepseek.com/v1"
    api_key_env: "DEEPSEEK_API_KEY"
    max_context: 64000

datasets:
  math500:
    hf_id: "HuggingFaceH4/MATH-500"
    split: "test"
  gsm8k:
    hf_id: "openai/gsm8k"
    split: "test"
  aime2024:
    hf_id: "AI-MO/aimo-validation-aime24"
    split: "train"

experiments:
  temperature: 0.0
  max_tokens: 2048
  seed: 42
  n_samples: 5
  max_refine_rounds: 2
```

**Last modified**: iter-1
