from __future__ import annotations

from dataclasses import asdict
from pathlib import Path

import numpy as np
import pandas as pd
from tqdm import tqdm

from src.analysis import run_statistical_analysis
from src.evaluation import evaluate_response
from src.metrics import compute_trajectory_metrics, token_entropy_from_logits
from src.model_runner import GPT2Runner
from src.trajectory_structure import compute_structure_features, run_trajectory_structure_analysis
from src.utils import ensure_dir, load_json, write_json


class TrajectoryExperiment:
    def __init__(
        self,
        prompts_path: str | Path,
        results_dir: str | Path,
        model_name: str = "gpt2",
        max_new_tokens: int = 48,
        temperature: float = 0.7,
        top_k: int | None = 50,
        do_sample: bool = True,
        angle_threshold_degrees: float = 90.0,
    ) -> None:
        self.prompts_path = Path(prompts_path)
        self.results_dir = ensure_dir(results_dir)
        self.charts_dir = ensure_dir(self.results_dir / "charts")
        self.model_name = model_name
        self.max_new_tokens = max_new_tokens
        self.temperature = temperature
        self.top_k = top_k
        self.do_sample = do_sample
        self.angle_threshold_degrees = angle_threshold_degrees

    def run(self) -> pd.DataFrame:
        prompts = load_json(self.prompts_path)
        runner = GPT2Runner(model_name=self.model_name)

        records: list[dict] = []
        raw_data: dict[str, np.ndarray] = {}

        for item in tqdm(prompts, desc="Running prompts"):
            result = runner.generate(
                item["prompt"],
                max_new_tokens=self.max_new_tokens,
                temperature=self.temperature,
                top_k=self.top_k,
                do_sample=self.do_sample,
            )
            entropy = token_entropy_from_logits(result.logits)
            metrics = compute_trajectory_metrics(
                result.hidden_states,
                entropy,
                angle_threshold_degrees=self.angle_threshold_degrees,
            )
            structure_features = compute_structure_features(
                hidden_states=result.hidden_states,
                L=metrics.L,
                D=metrics.D,
                E=metrics.E,
                V=metrics.V,
                output_token_count=result.output_token_count,
            )
            evaluation = evaluate_response(
                result.generated_response,
                item.get("expected_answer"),
                item.get("evaluation_type"),
            )

            prompt_id = item["id"]
            raw_data[f"{prompt_id}__logits"] = result.logits
            raw_data[f"{prompt_id}__hidden_states"] = result.hidden_states

            record = {
                "id": prompt_id,
                "category": item["category"],
                "prompt": result.prompt,
                "expected_answer": item.get("expected_answer"),
                "evaluation_type": item.get("evaluation_type"),
                "generated_response": result.generated_response,
                "generated_tokens": result.generated_tokens,
                "generated_token_ids": result.generated_token_ids,
                "output_token_count": result.output_token_count,
                "generation_time_seconds": result.generation_time_seconds,
                "is_evaluable": evaluation.is_evaluable,
                "is_correct": evaluation.is_correct,
                "evaluation_notes": evaluation.evaluation_notes,
                "token_entropy": entropy.tolist(),
                "mean_token_entropy": float(np.mean(entropy)) if entropy.size else 0.0,
                "logits_shape": list(result.logits.shape),
                "hidden_states_shape": list(result.hidden_states.shape),
                **asdict(metrics),
                **asdict(structure_features),
            }
            records.append(record)

        frame = pd.DataFrame(records)
        self._save_results(frame, records, raw_data)
        run_statistical_analysis(frame, self.results_dir)
        run_trajectory_structure_analysis(self.results_dir)
        return frame

    def _save_results(
        self,
        frame: pd.DataFrame,
        records: list[dict],
        raw_data: dict[str, np.ndarray],
    ) -> None:
        csv_frame = frame.copy()
        for column in ["generated_tokens", "generated_token_ids", "token_entropy", "logits_shape", "hidden_states_shape"]:
            csv_frame[column] = csv_frame[column].apply(lambda value: repr(value))

        csv_frame.to_csv(self.results_dir / "results.csv", index=False)
        write_json(self.results_dir / "results.json", records)
        np.savez_compressed(self.results_dir / "raw_internal_data.npz", **raw_data)
