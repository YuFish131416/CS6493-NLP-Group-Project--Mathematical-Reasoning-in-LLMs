# CURRENT_TASK.md — Task Breakpoint State

## Task: iter-2 — Bug Fixes, Config, and Experiment Execution
**Status**: IN PROGRESS
**Last completed step**: S06
**Next step**: S07 (full-experiment)
**Blocked by**: none
**Started**: 2026-04-08

## Steps
- [x] S01 — Install all Python dependencies (llama-cpp-python, datasets, openai, etc.)
- [x] S02 — Download GGUF model files (Qwen2.5-Math-1.5B + DeepSeek-R1-Qwen-1.5B)
- [x] S03 — Fix critical bug: \\boxed{} in prompt templates conflicting with Python str.format() — escaped to \\boxed{{}} in all 5 prompt method templates
- [x] S04 — Fix bugs: answer_extractor fallback number extraction, math_parser normalize_answer trailing period handling, data/__init__.py missing preprocess_dataset export, MATH-500 level field parsing, ExperimentConfig._raw_yaml for auto ModelRouter creation
- [x] S05 — Fix and update unit tests: 14 failures → 0 failures (63/63 passed)
- [x] S06 — Download datasets, fix dependency issues, run small-sample experiments successfully
  - Fixed: datasets library (4.8.4→2.19.0) and huggingface_hub (0.35.0→0.23.5) compatibility
  - Fixed: AIME 2024 dataset HF ID (AI-MO/aimo-validation-aime24 → HuggingFaceH4/aime_2024)
  - Fixed: loader.py removed trust_remote_code issue, made cache_dir optional
  - Downloaded: MATH-500 (500), GSM8K (1319), AIME2024 (30) — all preprocessed successfully
  - Integration test: qwen2.5-math + CoT + GSM8K, 1 problem → CORRECT (18=18), 13.1s inference
  - Small experiment: qwen2.5-math x 5 methods x GSM8K x 3 samples → 14/15 correct (93.3%), 7.2min
- [ ] S07 — Run full experiment across all model-method-dataset combinations
- [ ] S08 — Generate results visualization and analysis

## Test Steps
- [x] T01 — All 63 unit tests pass (test_prompts, test_answer_extractor, test_metrics)
- [x] T02 — All module imports verified (prompts, evaluation, data, experiment, models)
- [x] T03 — Cross-module integration: prompt->extraction->evaluation pipeline verified
- [x] T04 — ExperimentConfig -> Runner initialization verified
- [x] T05 — ResultsStore save/load/checkpoint verified
- [x] T06 — Integration test: local model inference on 1 sample problem (qwen2.5-math, CoT, GSM8K) ✅
- [x] T07 — Integration test: full pipeline run with 5 methods x 3 samples (93.3% accuracy) ✅
- [ ] T08 — Full experiment: 2 models x 5 methods x 3 datasets x 20 samples
