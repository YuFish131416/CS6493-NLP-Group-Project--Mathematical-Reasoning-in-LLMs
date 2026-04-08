# TECH_DEBT.md

| ID | File | Description | Severity | Added | Resolution |
|----|------|-------------|----------|-------|------------|
| TD-001 | src/evaluation/answer_extractor.py | Regex-based answer extraction may miss uncommon formats; should add fallback heuristics | Medium | iter-1 | Partially resolved in iter-2 (improved trailing period handling and fallback) |
| TD-002 | src/evaluation/math_parser.py | sympy-based normalization may fail on complex expressions (e.g., sets, intervals) | Medium | iter-1 | Partially resolved in iter-2 (fixed trailing period before sympy) |
| TD-003 | src/prompts/self_consistency.py | Self-Consistency with n_samples=5 consumes 5x tokens; hard limit for cost control | Low | iter-1 | — |
| TD-004 | src/prompts/least_to_most.py | Least-to-Most decomposition requires extra model call per problem; increases latency | Low | iter-1 | — |
| TD-005 | src/app/ | Streamlit does not support real-time inference progress display; long-running local inference may timeout | Low | iter-1 | — |
| TD-006 | src/models/local_model.py | No model response caching; repeated identical queries will re-run inference | Low | iter-1 | — |
| TD-007 | src/experiment/runner.py | Checkpoint resume only skips recomputation but summary stats don't include skipped results | Medium | iter-2 | — |
| TD-008 | src/prompts/*.py | Prompt templates were fixed with {{}} escaping; any future template changes must maintain double-brace escaping for \\boxed | Low | iter-2 | Documented |

Severity: Critical / High / Medium / Low
