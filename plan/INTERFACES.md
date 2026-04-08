# INTERFACES.md

## Data Loader

### `load_dataset(dataset_name: str, split: str = "test", cache_dir: str = "data/") -> Dataset`
- **Description**: Load a benchmark dataset from HuggingFace or local cache
- **Parameters**: `dataset_name: str` — one of "math500", "gsm8k", "aime2024"; `split: str` — dataset split; `cache_dir: str` — local cache directory
- **Returns**: `Dataset` object with `problem`, `answer`, `solution` fields
- **Constraints**: dataset_name must be one of the three supported values; raises ValueError otherwise
- **Side effects**: Downloads dataset on first call, caches locally
- **Last modified**: iter-1

---

## Preprocessor

### `preprocess_math500(raw_data: Dataset) -> list[dict]`
- **Description**: Clean and normalize MATH-500 dataset entries
- **Parameters**: `raw_data: Dataset` — raw HuggingFace dataset
- **Returns**: list of dicts with keys `id`, `problem`, `answer`, `level`, `type`, `solution`
- **Side effects**: none
- **Last modified**: iter-1

### `preprocess_gsm8k(raw_data: Dataset) -> list[dict]`
- **Description**: Clean and normalize GSM8K dataset entries
- **Parameters**: `raw_data: Dataset` — raw HuggingFace dataset
- **Returns**: list of dicts with keys `id`, `problem`, `answer`
- **Side effects**: none
- **Last modified**: iter-1

### `preprocess_aime(raw_data: Dataset) -> list[dict]`
- **Description**: Clean and normalize AIME 2024 dataset entries
- **Parameters**: `raw_data: Dataset` — raw HuggingFace dataset
- **Returns**: list of dicts with keys `id`, `problem`, `answer`
- **Side effects**: none
- **Last modified**: iter-1

---

## Model Router

### `ModelRouter.__init__(config: dict)`
- **Description**: Initialize model router with model configurations
- **Parameters**: `config: dict` — model configs including type (local/api), name, path, api_key, etc.
- **Side effects**: Loads local models into memory, validates API connections
- **Last modified**: iter-1

### `ModelRouter.infer(prompt: str, model_name: str, temperature: float = 0.0, max_tokens: int = 2048) -> str`
- **Description**: Route inference request to the appropriate model backend
- **Parameters**: `prompt: str` — formatted prompt; `model_name: str` — model identifier; `temperature: float`; `max_tokens: int`
- **Returns**: `str` — model-generated response text
- **Constraints**: model_name must be registered; raises ModelNotFoundError if unknown
- **Side effects**: API calls consume tokens; local inference is CPU-bound
- **Last modified**: iter-1

---

## Prompt Methods (Base)

### `PromptMethod.__init__(config: dict = None)`
- **Description**: Base class constructor for all prompt methods
- **Last modified**: iter-1

### `PromptMethod.format(problem: str, **kwargs) -> str`
- **Description**: Format a math problem into the specific prompt template for this method
- **Parameters**: `problem: str` — the math problem text; `**kwargs` — method-specific params
- **Returns**: `str` — formatted prompt string
- **Side effects**: none
- **Last modified**: iter-1

### `PromptMethod.name -> str`
- **Description**: Return the method name identifier
- **Last modified**: iter-1

### `PromptMethod.is_multi_pass -> bool`
- **Description**: Whether this method requires multiple inference passes (e.g., Self-Consistency)
- **Last modified**: iter-1

---

## CoT

### `CoT.format(problem: str) -> str`
- **Description**: Format problem with Chain-of-Thought instructions
- **Returns**: prompt with "Let's think step by step" instruction appended
- **Last modified**: iter-1

---

## SelfConsistency

### `SelfConsistency.format(problem: str) -> str`
- **Description**: Format problem for Self-Consistency sampling
- **Parameters**: `n_samples: int = 5` — number of independent samples (default 5 per topic hint)
- **Returns**: Same as CoT format (sampling is controlled at inference level)
- **Side effects**: none; multi-sample logic is in the experiment runner
- **Last modified**: iter-1

### `SelfConsistency.aggregate(responses: list[str]) -> str`
- **Description**: Extract answers from multiple responses and return majority vote
- **Parameters**: `responses: list[str]` — list of model responses
- **Returns**: `str` — most common answer
- **Last modified**: iter-1

---

## SelfRefine

### `SelfRefine.format(problem: str) -> str`
- **Description**: Format initial problem with solve instruction
- **Last modified**: iter-1

### `SelfRefine.format_critique(problem: str, solution: str) -> str`
- **Description**: Format critique request given problem and initial solution
- **Last modified**: iter-1

### `SelfRefine.format_refine(problem: str, solution: str, critique: str) -> str`
- **Description**: Format refinement request given problem, solution, and critique
- **Last modified**: iter-1

---

## LeastToMost

### `LeastToMost.format(problem: str, sub_questions: list[str] = None) -> str`
- **Description**: Format problem for Least-to-Most decomposition
- **Parameters**: `sub_questions: list[str]` — optional pre-decomposed sub-questions
- **Last modified**: iter-1

### `LeastToMost.decompose(problem: str) -> list[str]`
- **Description**: Use model to decompose problem into sub-questions (requires model inference)
- **Last modified**: iter-1

---

## PVP (Progressive Verification Prompting)

### `PVP.format(problem: str) -> str`
- **Description**: Format problem with progressive verification instructions interspersed in the reasoning template
- **Returns**: prompt with step-by-step solving + verification checkpoints
- **Last modified**: iter-1

---

## Answer Extractor

### `extract_answer(response: str) -> str | None`
- **Description**: Extract the final numeric/mathematical answer from a model response
- **Parameters**: `response: str` — full model output
- **Returns**: `str | None` — extracted answer string, or None if not found
- **Supported formats**: `\boxed{answer}`, `The answer is X`, `#### X`, `$X$`, last number in response
- **Side effects**: none
- **Last modified**: iter-1

---

## Metrics

### `compute_accuracy(predictions: list[str], ground_truths: list[str]) -> float`
- **Description**: Compute exact-match accuracy between predictions and ground truths
- **Parameters**: `predictions: list[str]` — extracted answers; `ground_truths: list[str]` — correct answers
- **Returns**: `float` — accuracy between 0.0 and 1.0
- **Last modified**: iter-1

### `compute_response_lengths(responses: list[str]) -> dict`
- **Description**: Compute response length statistics
- **Returns**: `dict` with keys `mean`, `median`, `min`, `max`, `std`
- **Last modified**: iter-1

### `compute_step_correctness(response: str, ground_truth: str) -> float`
- **Description**: Evaluate what fraction of reasoning steps are correct (exploratory)
- **Returns**: `float` — step-level correctness ratio
- **Last modified**: iter-1

---

## Math Parser

### `normalize_answer(answer: str) -> str`
- **Description**: Normalize a math answer to canonical form for comparison
- **Parameters**: `answer: str` — raw answer string
- **Returns**: `str` — normalized form (e.g., "1/2" → "0.5", "3.0" → "3")
- **Last modified**: iter-1

### `answers_match(pred: str, truth: str) -> bool`
- **Description**: Check if two answers are mathematically equivalent
- **Last modified**: iter-1

---

## Experiment Runner

### `Runner.__init__(config: ExperimentConfig)`
- **Description**: Initialize runner with experiment configuration
- **Last modified**: iter-1

### `Runner.run() -> ExperimentResults`
- **Description**: Execute all experiment combinations defined in config with checkpoint support
- **Returns**: `ExperimentResults` — aggregated results
- **Side effects**: Saves checkpoints after each problem; writes results JSON
- **Last modified**: iter-1

---

## Results Store

### `ResultsStore.save(results: dict, path: str) -> None`
- **Description**: Persist experiment results to JSON file
- **Last modified**: iter-1

### `ResultsStore.load(path: str) -> dict`
- **Description**: Load experiment results from JSON file
- **Last modified**: iter-1

### `ResultsStore.load_checkpoints(run_id: str) -> list[str]`
- **Description**: Get list of completed problem IDs for a given run (for resume)
- **Last modified**: iter-1
