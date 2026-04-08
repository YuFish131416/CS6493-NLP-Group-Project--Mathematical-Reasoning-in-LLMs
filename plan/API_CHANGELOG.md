# API_CHANGELOG.md

## [iter-1] — 2026-04-08

### Changed Endpoints
No existing endpoints — initial API definitions.

### Defined Interfaces
All interfaces defined in this iteration are new. See `plan/INTERFACES.md` for the complete list.

### Key Interface Contracts
- All prompt methods implement `format(problem: str) -> str` via the `PromptMethod` base class
- `ModelRouter.infer()` returns `str` for all model types (local and API)
- `AnswerExtractor.extract_answer()` returns `str | None` (None indicates parse failure)
- All dataset preprocessors return `list[dict]` with normalized fields

### Migration Guide
N/A — initial iteration.
