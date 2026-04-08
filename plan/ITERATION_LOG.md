# ITERATION_LOG.md

## [iter-1] Initial Project Setup — 2026-04-08
- ADD: SPEC.md — full project specification document
- ADD: plan/PROJECT_OVERVIEW.md — goals, features, non-goals, acceptance criteria
- ADD: plan/ARCHITECTURE.md — system architecture, module map, data flows
- ADD: plan/INTERFACES.md — all function signatures and API definitions
- ADD: plan/SCHEMAS.md — data structure definitions (MathProblem, ModelResponse, etc.)
- ADD: plan/CONSTRAINTS.md — tech stack, version locks, compatibility rules
- ADD: plan/DIR_MAP.md — directory and file index
- ADD: process/REQUIREMENTS.md — user requirements agreement record
- ADD: process/PROGRESS.md — milestone progress tracking
- ADD: process/CURRENT_TASK.md — current task breakpoint state
- ADD: src/__init__.py — package root
- ADD: src/data/__init__.py — data module init
- ADD: src/models/__init__.py — models module init
- ADD: src/prompts/__init__.py — prompts module init
- ADD: src/evaluation/__init__.py — evaluation module init
- ADD: src/experiment/__init__.py — experiment module init
- ADD: src/app/__init__.py — Streamlit app module init
- ADD: src/app/pages/__init__.py — Streamlit pages init
- ADD: src/app/components/__init__.py — Streamlit components init
- ADD: tests/__init__.py — test package root
- ADD: config/config.example.yaml — configuration template
- ADD: .env.example — environment variable template
- ADD: requirements.txt — Python dependencies
- ADD: .gitignore — Git ignore rules

## [iter-2] Bug Fixes & Config Setup — 2026-04-08
- MOD: src/prompts/cot.py — Fixed \\boxed{} → \\boxed{{}} for str.format() compatibility
- MOD: src/prompts/self_consistency.py — Fixed \\boxed{} → \\boxed{{}} for str.format() compatibility
- MOD: src/prompts/self_refine.py — Fixed \\boxed{} → \\boxed{{}} in all 3 templates (SOLVE, CRITIQUE, REFINE)
- MOD: src/prompts/least_to_most.py — Fixed \\boxed{} → \\boxed{{}} and typing import (list → List)
- MOD: src/prompts/pvp.py — Fixed \\boxed{} → \\boxed{{}} for str.format() compatibility
- MOD: src/evaluation/answer_extractor.py — Fixed _clean_extracted trailing period handling; fixed fallback number extraction
- MOD: src/evaluation/math_parser.py — Fixed normalize_answer: handle trailing period before sympy simplification
- MOD: src/data/__init__.py — Added missing preprocess_dataset and utility exports
- MOD: src/data/preprocessor.py — Fixed MATH-500 level parsing to handle "Level N" string format
- MOD: src/experiment/config.py — Added _raw_yaml storage; improved datasets parsing (dict/string/list)
- MOD: src/experiment/runner.py — Auto-create ModelRouter from config._raw_yaml; added multi-pass method handlers
- MOD: tests/test_answer_extractor.py — Fixed test assertions for improved extraction logic
- MOD: tests/test_metrics.py — Fixed test expectations for sympy-based normalization
- ADD: scripts/run_experiment.py — Main experiment runner CLI script
- ADD: config/config.local.yaml — Local-only configuration (2 GGUF models, 3 datasets, sample_size=20)
- ADD: tmp/verify_modules.py — Comprehensive module verification script (19 checks across all modules)

## [iter-2b] Module Verification & Dependency Fix — 2026-04-08
- MOD: requirements.txt — Added pyarrow compatibility note for datasets>=2.19.0
- FIX: datasets library upgraded from 2.11.0 to 4.8.4 (pyarrow 21.0.0 incompatibility with datasets 2.11.0)
- Verified: 63/63 unit tests pass, 19/19 module verification checks pass
- Verified modules: prompts (5 methods), evaluation (extraction, parsing, metrics), data (registry, preprocessors), experiment (config, runner, results_store), models (local_model, router)
- Verified cross-module: prompt->extraction->evaluation pipeline, config->Runner initialization

## [iter-2c] Dataset Download & Small-Sample Experiments — 2026-04-08
- FIX: datasets downgraded from 4.8.4 to 2.19.0, huggingface_hub from 0.35.0 to 0.23.5 (DatasetCard.load repo_id validation bug with cached paths)
- FIX: AIME 2024 dataset HF ID corrected from AI-MO/aimo-validation-aime24 to HuggingFaceH4/aime_2024
- MOD: src/data/loader.py — Made cache_dir optional (default=None uses HF cache), added trust_remote_code, added GSM8K "main" config name
- MOD: src/experiment/runner.py — Removed cache_dir="data/" from load_dataset call
- MOD: config/config.local.yaml — Updated aime2024 hf_id
- MOD: requirements.txt — Pinned datasets>=2.19.0,<4.0 and huggingface_hub>=0.23.0,<0.26
- MOD: scripts/run_experiment.py — Enhanced with --run-id, --n-samples, --max-refine-rounds args, per-model/method/dataset aggregation
- ADD: tmp/download_datasets.py — Dataset download and verification script
- ADD: tmp/test_single_problem.py — Single-problem integration test script
- ADD: tmp/run_all_methods.py — All 5 methods small-sample experiment script
- Downloaded: MATH-500 (500 problems), GSM8K (1319 problems), AIME2024 (30 problems)
- Integration test: qwen2.5-math + CoT + GSM8K → CORRECT (extracted 18, truth 18, 13.1s)
- Small experiment: qwen2.5-math x 5 methods x GSM8K x 3 samples → 14/15 correct (93.3%), 7.2min
  - CoT: 3/3 (100%), Self-Consistency: 3/3 (100%), Self-Refine: 3/3 (100%)
  - Least-to-Most: 3/3 (100%), PVP: 2/3 (66.7%)
- Results saved: results/test_all_methods_gsm8k_results.json, 51 checkpoints
