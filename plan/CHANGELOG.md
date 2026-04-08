# CHANGELOG.md

## iter-1 — 2026-04-08

### What changed
Initialized the CS6493 NLP Group Project for Topic 1 (Mathematical Reasoning Ability of LLMs). Created the complete project specification, architecture design, interface definitions, data schemas, and all planning/process documents according to the AGENT_STARTUP.md workflow.

### Impact
All team members can now reference the project specification for scope and requirements. The architecture and interfaces serve as the blueprint for implementation.

### Breaking changes
None — this is the initial setup.

## iter-2 — 2026-04-08

### What changed
Fixed 14 critical bugs across the codebase. The most significant was that all 5 prompt method templates contained `\\boxed{}` which conflicted with Python's `str.format()` — the curly braces were interpreted as format placeholders, causing `IndexError` on every prompt generation. Also fixed answer extraction logic (trailing periods, fallback numbers), math parser normalization (sympy handling of "5."), data module exports, MATH-500 level field parsing, and experiment config auto-setup.

### Impact
All 63 unit tests now pass. The experiment pipeline is ready to run end-to-end with local GGUF models. The prompt templates correctly generate formatted prompts for all 5 methods.

### Breaking changes
None — all fixes maintain backward compatibility with existing interfaces.
