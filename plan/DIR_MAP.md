# DIR_MAP.md

| Path | Purpose |
|------|---------|
| `plan/` | Compressed knowledge base — project planning and architecture docs |
| `plan/AGENT_STARTUP.md` | Agent startup guide — read first every session |
| `plan/PROJECT_OVERVIEW.md` | Project goals, features, non-goals, acceptance criteria |
| `plan/ARCHITECTURE.md` | System architecture, module map, data flows |
| `plan/INTERFACES.md` | All function signatures, API endpoints, and constraints |
| `plan/SCHEMAS.md` | Data structures: MathProblem, ModelResponse, ExperimentConfig, etc. |
| `plan/CONSTRAINTS.md` | Tech stack, version locks, compatibility rules, env vars |
| `plan/DIR_MAP.md` | This file — one-line purpose for every folder and key file |
| `plan/ITERATION_LOG.md` | Structured iteration log for Agent (machine-readable) |
| `plan/CHANGELOG.md` | Narrative changelog for humans |
| `plan/API_CHANGELOG.md` | Contract diff for interface changes |
| `plan/TECH_DEBT.md` | Known issues, shortcuts, and optimization candidates |
| `process/` | Task progress and checkpoint state |
| `process/PROGRESS.md` | Milestone-level progress checkboxes |
| `process/CURRENT_TASK.md` | Breakpoint-resume state — updated after every step |
| `process/REQUIREMENTS.md` | User requirements and agreements record |
| `src/` | Main source code |
| `src/data/` | Dataset loading and preprocessing |
| `src/models/` | Model loading, inference, and routing |
| `src/prompts/` | Prompt method implementations |
| `src/evaluation/` | Answer extraction, metrics, math parsing |
| `src/experiment/` | Experiment runner, config, results storage |
| `src/app/` | Streamlit Web Demo application |
| `src/app/pages/` | Streamlit multi-page components |
| `src/app/components/` | Reusable Streamlit UI components |
| `tests/` | Unit tests mirroring src/ structure |
| `notebooks/` | Jupyter notebooks for exploratory analysis |
| `docs/` | External-facing documentation (progress report, presentation) |
| `review/` | Per-iteration self code review outputs |
| `config/` | Configuration files |
| `config/config.example.yaml` | Committed config template — no secrets |
| `config/config.local.yaml` | Local secrets — gitignored |
| `data/` | Dataset cache directory — gitignored |
| `results/` | Experiment results output |
| `results/checkpoints/` | Experiment checkpoints for resume |
| `tmp/` | Temporary files — gitignored |
| `models/` | Local GGUF model files — gitignored |
| `scripts/` | Utility scripts |
| `scripts/run_experiment.py` | Main CLI script to run experiments |
| `scripts/download_models.py` | Script to download GGUF model files from HuggingFace |
| `SPEC.md` | Full project specification |
| `README.md` | Project overview and setup instructions |
| `requirements.txt` | Python dependencies |
| `.env.example` | Environment variable template |
| `.env` | Local environment variables — gitignored |
| `.gitignore` | Git ignore rules |
