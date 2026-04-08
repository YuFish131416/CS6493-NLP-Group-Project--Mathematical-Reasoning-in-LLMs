# PROGRESS.md — Milestone Progress Tracker

## iter-1: Initial Project Setup & Core Implementation
- [x] M01 — Create SPEC.md and all plan/ documentation files
- [x] M02 — Create process/ documentation (REQUIREMENTS, PROGRESS, CURRENT_TASK)
- [x] M03 — Create project skeleton (src/, tests/, notebooks/, docs/, config/, etc.)
- [x] M04 — Implement data loading and preprocessing modules
- [x] M05 — Implement model inference and 5 prompt methods
- [x] M06 — Implement evaluation metrics and experiment runner
- [ ] M07 — Implement Streamlit Web Demo
- [ ] M08 — Create Jupyter notebooks and unit tests
- [ ] M09 — Generate progress report template, presentation outline, and code review

## iter-2: Bug Fixes, Dependency Setup, and Experiment Execution
- [x] M10 — Install all Python dependencies
- [x] M11 — Download GGUF model files
- [x] M12 — Fix critical bugs (prompt template escaping, answer extraction, config parsing)
- [x] M13 — All 63 unit tests passing
- [x] M14 — Comprehensive module verification: 19/19 checks passed
- [x] M14b — Fix datasets library compatibility (datasets 2.19.0 + huggingface_hub 0.23.5)
- [x] M14c — Fix AIME 2024 dataset HF ID and loader.py cache_dir/trust_remote_code issues
- [x] M15 — Download all 3 datasets: MATH-500 (500), GSM8K (1319), AIME2024 (30)
- [x] M16 — Single-problem integration test: qwen2.5-math + CoT + GSM8K → CORRECT
- [x] M17 — Small-sample experiment: 1 model x 5 methods x GSM8K x 3 samples → 93.3% accuracy
- [ ] M18 — Run full experiments (2 models x 5 methods x 3 datasets x 20 samples)
- [ ] M19 — Generate experiment results and visualizations
