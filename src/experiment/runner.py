"""
Experiment runner with checkpoint/resume support.
Orchestrates the full pipeline: data → prompt → model → extract → evaluate.
"""

import time
import logging
from datetime import datetime
from typing import Optional

from .config import ExperimentConfig
from .results_store import ResultsStore
from ..data.loader import load_dataset
from ..data.preprocessor import preprocess_dataset
from ..evaluation.answer_extractor import extract_answer
from ..evaluation.metrics import compute_accuracy, compute_response_lengths
from ..evaluation.math_parser import answers_match

logger = logging.getLogger(__name__)


class Runner:
    """
    Batch experiment runner with checkpoint/resume support.

    Executes experiments across all model x method x dataset combinations
    defined in the experiment configuration.
    """

    def __init__(self, config: ExperimentConfig, model_router=None):
        """
        Initialize runner.

        Args:
            config: Experiment configuration.
            model_router: ModelRouter instance for inference.
                         If None and config has _raw_yaml, auto-creates one.
        """
        self.config = config
        self.store = ResultsStore(output_dir=config.output_dir)

        if model_router is not None:
            self.router = model_router
        elif hasattr(config, '_raw_yaml') and config._raw_yaml:
            from ..models.router import ModelRouter
            self.router = ModelRouter(config._raw_yaml)
        else:
            self.router = None

        # Lazy-loaded prompt methods
        self._prompt_methods = {}

    def _get_prompt_method(self, method_name: str):
        """Lazy-load and cache prompt method instances."""
        if method_name in self._prompt_methods:
            return self._prompt_methods[method_name]

        from ..prompts import CoT, SelfConsistency, SelfRefine, LeastToMost, PVP

        method_map = {
            "cot": CoT,
            "self_consistency": SelfConsistency,
            "self_refine": SelfRefine,
            "least_to_most": LeastToMost,
            "pvp": PVP,
        }

        if method_name not in method_map:
            raise ValueError(f"Unknown prompt method: {method_name}")

        method_config = {
            "n_samples": self.config.n_samples,
            "max_refine_rounds": self.config.max_refine_rounds,
        }
        instance = method_map[method_name](config=method_config)
        self._prompt_methods[method_name] = instance
        return instance

    def run(self) -> dict:
        """
        Execute all experiment combinations defined in config.

        Supports checkpoint/resume: if a problem combination has already
        been evaluated (checkpoint exists), it is skipped.

        Returns:
            Full experiment results dict.
        """
        run_id = self.config.run_id
        logger.info(f"Starting experiment run: {run_id}")
        logger.info(
            f"Models: {self.config.models}, Methods: {self.config.prompt_methods}, "
            f"Datasets: {self.config.datasets}"
        )

        # Load existing checkpoints
        existing_ckpts = set(self.store.load_checkpoints(run_id))
        logger.info(f"Found {len(existing_ckpts)} existing checkpoints")

        all_responses = []
        summary = {}

        for dataset_name in self.config.datasets:
            # Load and preprocess dataset
            raw_data = load_dataset(dataset_name)
            problems = preprocess_dataset(raw_data, dataset_name)

            if self.config.sample_size > 0:
                problems = problems[: self.config.sample_size]

            for model_name in self.config.models:
                for method_name in self.config.prompt_methods:
                    combo_key = f"{model_name}__{method_name}__{dataset_name}"
                    logger.info(f"\n{'='*60}")
                    logger.info(f"Running: {model_name} x {method_name} x {dataset_name}")
                    logger.info(f"{'='*60}")

                    combo_responses = []
                    correct = 0
                    total = len(problems)
                    extract_success = 0

                    for i, problem in enumerate(problems):
                        ckpt_key = f"{model_name}__{method_name}__{dataset_name}__{problem['id']}"

                        if ckpt_key in existing_ckpts:
                            logger.info(
                                f"[{i+1}/{total}] SKIP (checkpoint exists): {problem['id']}"
                            )
                            continue

                        result = self._run_single(
                            problem=problem,
                            model_name=model_name,
                            method_name=method_name,
                            dataset_name=dataset_name,
                        )

                        all_responses.append(result)
                        combo_responses.append(result)

                        if result.get("is_correct"):
                            correct += 1
                        if result.get("extracted_answer"):
                            extract_success += 1

                        # Save checkpoint
                        self.store.save_checkpoint(
                            run_id=run_id,
                            model_name=model_name,
                            method_name=method_name,
                            dataset_name=dataset_name,
                            problem_id=problem["id"],
                            result=result,
                        )

                        logger.info(
                            f"[{i+1}/{total}] {'OK' if result.get('is_correct') else 'WRONG'} "
                            f"| Extracted: {result.get('extracted_answer', 'FAIL')} "
                            f"| Truth: {problem['answer']} "
                            f"| Time: {result.get('latency_ms', 0):.0f}ms"
                        )

                    accuracy = correct / total if total > 0 else 0
                    summary[combo_key] = {
                        "model": model_name,
                        "method": method_name,
                        "dataset": dataset_name,
                        "accuracy": accuracy,
                        "correct": correct,
                        "total": total,
                        "extract_success_rate": extract_success / total if total > 0 else 0,
                    }

        # Build final results
        total_correct = sum(1 for r in all_responses if r.get("is_correct"))
        results = {
            "run_id": run_id,
            "config": self.config.to_dict(),
            "responses": all_responses,
            "summary": summary,
            "total_problems": len(all_responses),
            "total_correct": total_correct,
            "overall_accuracy": total_correct / len(all_responses) if all_responses else 0,
            "completed_at": datetime.now().isoformat(),
        }

        # Save results
        self.store.save(results)
        logger.info(f"\nExperiment complete! Overall accuracy: {results['overall_accuracy']:.4f}")
        return results

    def _run_single(
        self,
        problem: dict,
        model_name: str,
        method_name: str,
        dataset_name: str,
    ) -> dict:
        """Run a single problem evaluation with method-specific logic."""
        prompt_method = self._get_prompt_method(method_name)
        start_time = time.time()

        try:
            if method_name == "self_consistency":
                response, extracted = self._run_self_consistency(
                    problem, model_name, prompt_method
                )
            elif method_name == "self_refine":
                response, extracted = self._run_self_refine(
                    problem, model_name, prompt_method
                )
            elif method_name == "least_to_most":
                response, extracted = self._run_least_to_most(
                    problem, model_name, prompt_method
                )
            else:
                # CoT, PVP — single pass
                prompt_text = prompt_method.format(problem=problem["problem"])
                response = self.router.infer(
                    prompt=prompt_text,
                    model_name=model_name,
                    temperature=self.config.temperature,
                    max_tokens=self.config.max_tokens,
                )
                extracted = extract_answer(response)
        except Exception as e:
            logger.error(f"Inference error for {problem['id']}: {e}")
            return {
                "problem_id": problem["id"],
                "model_name": model_name,
                "prompt_method": method_name,
                "dataset": dataset_name,
                "raw_response": "",
                "extracted_answer": None,
                "is_correct": False,
                "response_length": 0,
                "latency_ms": (time.time() - start_time) * 1000,
                "error": str(e),
            }

        latency_ms = (time.time() - start_time) * 1000
        is_correct = answers_match(extracted, problem["answer"]) if extracted else False

        return {
            "problem_id": problem["id"],
            "model_name": model_name,
            "prompt_method": method_name,
            "dataset": dataset_name,
            "raw_response": response,
            "extracted_answer": extracted,
            "is_correct": is_correct,
            "response_length": len(response),
            "latency_ms": latency_ms,
            "timestamp": datetime.now().isoformat(),
        }

    def _run_self_consistency(self, problem, model_name, prompt_method):
        """Self-Consistency: sample N responses, extract answers, majority vote."""
        prompt_text = prompt_method.format(problem=problem["problem"])
        answers = []
        all_responses = []

        for _ in range(prompt_method.n_samples):
            resp = self.router.infer(
                prompt=prompt_text,
                model_name=model_name,
                temperature=0.7,  # Need temperature > 0 for diversity
                max_tokens=self.config.max_tokens,
            )
            all_responses.append(resp)
            ans = extract_answer(resp)
            if ans:
                answers.append(ans)

        # Majority vote
        if answers:
            final_answer = prompt_method.aggregate(all_responses, answers)
        else:
            final_answer = extract_answer(all_responses[0]) if all_responses else None

        combined_response = "\n---SAMPLE---\n".join(all_responses)
        return combined_response, final_answer

    def _run_self_refine(self, problem, model_name, prompt_method):
        """Self-Refine: solve → critique → refine (iterative)."""
        # Phase 1: Initial solve
        solve_prompt = prompt_method.format(problem=problem["problem"])
        solution = self.router.infer(
            prompt=solve_prompt,
            model_name=model_name,
            temperature=self.config.temperature,
            max_tokens=self.config.max_tokens,
        )

        # Iterative critique-refine
        for _ in range(prompt_method.max_rounds):
            critique_prompt = prompt_method.format_critique(
                problem=problem["problem"], solution=solution
            )
            critique = self.router.infer(
                prompt=critique_prompt,
                model_name=model_name,
                temperature=self.config.temperature,
                max_tokens=self.config.max_tokens,
            )

            refine_prompt = prompt_method.format_refine(
                problem=problem["problem"], solution=solution, critique=critique
            )
            solution = self.router.infer(
                prompt=refine_prompt,
                model_name=model_name,
                temperature=self.config.temperature,
                max_tokens=self.config.max_tokens,
            )

        extracted = extract_answer(solution)
        return solution, extracted

    def _run_least_to_most(self, problem, model_name, prompt_method):
        """Least-to-Most: decompose → solve with sub-questions."""
        # Phase 1: Decompose
        decompose_prompt = prompt_method.format(problem=problem["problem"])
        decomposition = self.router.infer(
            prompt=decompose_prompt,
            model_name=model_name,
            temperature=self.config.temperature,
            max_tokens=self.config.max_tokens,
        )

        # Phase 2: Solve with sub-questions
        sub_questions = prompt_method.parse_subquestions(decomposition)
        sub_q_text = "\n".join(f"{i+1}. {q}" for i, q in enumerate(sub_questions))
        solve_prompt = prompt_method.format_with_subquestions(
            problem=problem["problem"], sub_questions=sub_q_text
        )
        solution = self.router.infer(
            prompt=solve_prompt,
            model_name=model_name,
            temperature=self.config.temperature,
            max_tokens=self.config.max_tokens,
        )

        extracted = extract_answer(solution)
        combined = f"[Decomposition]\n{decomposition}\n\n[Solution]\n{solution}"
        return combined, extracted
