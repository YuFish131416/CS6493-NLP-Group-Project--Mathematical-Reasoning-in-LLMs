# CONSTRAINTS.md

## Stack
- **Language**: Python 3.10+
- **Package Manager**: pip (requirements.txt)
- **Model Inference (Local)**: llama-cpp-python ≥ 0.2.90 (GGUF/CPU), transformers ≥ 4.40.0
- **Model Inference (API)**: openai ≥ 1.30.0 (compatible with OpenAI and DeepSeek endpoints)
- **Datasets**: datasets (HuggingFace) ≥ 2.19.0
- **Data Processing**: pandas ≥ 2.2.0
- **Prompt Templates**: Jinja2 ≥ 3.1.0
- **Math Parsing**: sympy ≥ 1.12
- **Visualization**: Streamlit ≥ 1.35.0, Plotly ≥ 5.22.0, Matplotlib ≥ 3.9.0
- **Experiment Utils**: tqdm ≥ 4.66.0, PyYAML ≥ 6.0
- **Testing**: pytest ≥ 8.2.0
- **Notebooks**: jupyter ≥ 1.0.0, ipykernel

## Compatibility Rules
- GGUF model files must use Q4_K_M quantization (balance of quality vs. CPU speed)
- API models must use the OpenAI SDK interface (both OpenAI and DeepSeek support this)
- All prompt methods must produce a single `str` prompt output (multi-pass methods managed at runner level)
- Answer extraction must handle all common answer formats: `\boxed{}`, `#### X`, `The answer is X`, `$X$`, bare number
- Temperature must be 0.0 for deterministic evaluation (except Self-Consistency which uses sampling)
- Results JSON files must be valid JSON and human-readable (indent=2)
- All relative paths in code must be relative to project root

## Known Risks (do-not-touch)
- GGUF model download URLs and file hashes — verify before first use, do not modify without testing
- HuggingFace dataset identifiers — changing may break loading pipeline
- API endpoint URLs — must match provider documentation exactly
- Answer extraction regex patterns — carefully tested, changes may affect accuracy measurements

## Environment Variables
| Variable | Purpose | Required |
|----------|---------|----------|
| `OPENAI_API_KEY` | GPT-4o-mini API access | Yes (if using API models) |
| `DEEPSEEK_API_KEY` | DeepSeek Chat API access | Yes (if using API models) |
| `PYTHONPATH` | Project root in Python path | No (handled by setup) |

## File Size Limits
- GGUF model files: ~1 GB each (Q4_K_M quantized)
- Dataset cache: ~500 MB total
- Results JSON per run: < 100 MB
- Checkpoint files: < 1 KB each

## Performance Targets
- Local model inference: < 60s per problem on modern CPU
- API model inference: < 15s per problem (network dependent)
- Streamlit page load: < 5s
- Dashboard chart render: < 3s
