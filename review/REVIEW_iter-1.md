# REVIEW_iter-1.md — Code Review

## Code Review: iter-1 — Initial Project Setup & Core Implementation — 2026-04-08

## Changed Files
| File | Change Type | Quality | Notes |
|------|-------------|---------|-------|
| SPEC.md | Added | Good | Comprehensive specification |
| plan/PROJECT_OVERVIEW.md | Added | Good | Clear goals and acceptance criteria |
| plan/ARCHITECTURE.md | Added | Good | Well-structured module map and data flows |
| plan/INTERFACES.md | Added | Good | Complete function signatures |
| plan/SCHEMAS.md | Added | Good | Detailed data structure definitions |
| plan/CONSTRAINTS.md | Added | Good | Clear version and compatibility rules |
| plan/DIR_MAP.md | Added | Good | Complete file index |
| plan/ITERATION_LOG.md | Added | Good | Structured log |
| plan/CHANGELOG.md | Added | Good | Narrative log |
| plan/API_CHANGELOG.md | Added | Good | API contract log |
| plan/TECH_DEBT.md | Added | Good | 6 items documented |
| process/REQUIREMENTS.md | Added | Good | All user agreements recorded |
| process/PROGRESS.md | Added | Good | Milestone tracking |
| process/CURRENT_TASK.md | Added | Good | Breakpoint state |
| src/data/loader.py | Added | Good | Clean HuggingFace integration |
| src/data/preprocessor.py | Added | Good | Robust normalization with regex + fallbacks |
| src/models/local_model.py | Added | Good | Proper error handling, lazy loading |
| src/models/api_model.py | Added | Good | OpenAI-compatible client, env var handling |
| src/models/router.py | Added | Good | Clean dispatch pattern |
| src/prompts/base.py | Added | Good | Clean ABC design |
| src/prompts/cot.py | Added | Good | Simple template |
| src/prompts/self_consistency.py | Added | Good | Aggregate with Counter |
| src/prompts/self_refine.py | Added | Good | Three-phase template design |
| src/prompts/least_to_most.py | Added | Good | Decompose + parse sub-questions |
| src/prompts/pvp.py | Added | Good | Novel method, clear documentation |
| src/evaluation/answer_extractor.py | Added | Good | Multi-pattern with fallback |
| src/evaluation/math_parser.py | Added | Good | sympy + numeric comparison |
| src/evaluation/metrics.py | Added | Good | Comprehensive metrics suite |
| src/experiment/config.py | Added | Good | YAML loading + dict serialization |
| src/experiment/results_store.py | Added | Good | Checkpoint/resume support |
| src/experiment/runner.py | Added | Good | Full pipeline orchestration |
| src/app/main.py | Added | Good | Clean Streamlit landing page |
| src/app/pages/01_interactive.py | Added | Good | Interactive solver with error handling |
| src/app/pages/02_dashboard.py | Added | Good | Plotly charts + data tables |
| src/app/pages/03_comparison.py | Added | Good | Heatmap + ranking |
| tests/test_answer_extractor.py | Added | Good | 10 test cases |
| tests/test_metrics.py | Added | Good | 14 test cases |
| tests/test_prompts.py | Added | Good | 20 test cases |
| notebooks/01_data_exploration.ipynb | Added | Good | Data loading exploration |
| notebooks/02_prompt_testing.ipynb | Added | Good | Prompt + extraction testing |
| notebooks/03_results_analysis.ipynb | Added | Good | Results visualization |
| docs/PROGRESS_REPORT.md | Added | Good | Complete template with TODO markers |
| docs/PRESENTATION.md | Added | Good | 15-slide outline with timing |
| README.md | Added | Good | Bilingual, complete setup guide |

## Architecture Assessment
The architecture follows a clean modular design with clear separation of concerns:
- **data/** handles only loading/preprocessing
- **models/** abstracts inference behind a router
- **prompts/** uses an ABC base class for extensibility
- **evaluation/** is independent of inference
- **experiment/** orchestrates the pipeline
- **app/** is a presentation layer that depends on all above

No architectural violations detected. Data flows are unidirectional and well-documented.

## New Tech Debt Introduced
| ID | File | Description | Severity |
|----|------|-------------|----------|
| TD-007 | src/prompts/self_refine.py | Self-Refine multi-round logic not yet implemented in Runner | Medium |
| TD-008 | src/prompts/self_consistency.py | Self-Consistency temperature/sampling not yet handled in Runner | Medium |
| TD-009 | src/prompts/least_to_most.py | Least-to-Most decomposition requires model call, not yet wired | Medium |
| TD-010 | src/evaluation/metrics.py | Step-level correctness is approximate, needs improvement | Low |

## Risks
- **CPU inference speed**: 1.5B models on CPU may be very slow for full-scale experiments (1800+ problems). Mitigation: checkpoint/resume + prioritize pilot runs first.
- **API cost**: Full-scale Self-Consistency (5 samples) across all datasets could be expensive. Mitigation: run pilot (50 per dataset) first to validate pipeline.
- **AIME 2024 dataset**: May have different format than expected; field names may vary. Mitigation: preprocessor has flexible field name handling.

## Recommendations
1. Prioritize running pilot experiments (50 problems per dataset) before full-scale runs
2. Wire up multi-pass methods (Self-Refine, Self-Consistency, Least-to-Most) in the Runner
3. Add proper typing to all public functions (use `from __future__ import annotations`)
4. Consider adding a `run_experiment.py` CLI script for easy experiment launching
