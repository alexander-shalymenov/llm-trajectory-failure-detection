from __future__ import annotations

from pathlib import Path
import traceback

import numpy as np
import pandas as pd

from src.analysis import _dataframe_to_markdown
from src.trajectory_structure import STRUCTURE_METRIC_COLUMNS, _category_anova
from src.utils import ensure_dir


def compare_model_results(model_dirs: list[str | Path], output_path: str | Path) -> dict[str, pd.DataFrame]:
    if len(model_dirs) < 2:
        raise ValueError("Model comparison requires at least two model output folders.")

    output = Path(output_path)
    log_path = output.parent / "analysis.log"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    log_path.touch(exist_ok=True)

    try:
        model_frames = _load_model_frames(model_dirs)
        category_means = _category_means_by_model(model_frames)
        anova = _anova_by_model(model_frames)
        correlations = _correlations_by_model(model_frames)
        stability = _strong_metric_stability(anova)
        _write_comparison_report(output, category_means, anova, correlations, stability)
        return {
            "category_means": category_means,
            "anova": anova,
            "correlations": correlations,
            "stability": stability,
        }
    except Exception as exc:
        _log_error(log_path, "model_comparison", exc)
        raise


def _load_model_frames(model_dirs: list[str | Path]) -> dict[str, pd.DataFrame]:
    frames = {}
    for model_dir in model_dirs:
        path = Path(model_dir)
        csv_path = path / "results.csv"
        if not csv_path.exists():
            raise FileNotFoundError(f"Missing model results CSV: {csv_path}")

        frame = pd.read_csv(csv_path)
        missing = [column for column in STRUCTURE_METRIC_COLUMNS if column not in frame.columns]
        if missing:
            raise ValueError(f"{csv_path} is missing trajectory structure columns: {missing}")

        for column in STRUCTURE_METRIC_COLUMNS:
            frame[column] = pd.to_numeric(frame[column], errors="coerce")

        model_name = path.name
        if model_name in frames:
            raise ValueError(f"Duplicate model folder name in comparison: {model_name}")
        frames[model_name] = frame
    return frames


def _category_means_by_model(model_frames: dict[str, pd.DataFrame]) -> pd.DataFrame:
    rows = []
    for model_name, frame in model_frames.items():
        means = frame.groupby("category")[STRUCTURE_METRIC_COLUMNS].mean().reset_index()
        means.insert(0, "model", model_name)
        rows.append(means)
    return pd.concat(rows, ignore_index=True)


def _anova_by_model(model_frames: dict[str, pd.DataFrame]) -> pd.DataFrame:
    rows = []
    for model_name, frame in model_frames.items():
        anova = _category_anova(frame)
        anova.insert(0, "model", model_name)
        rows.append(anova)
    return pd.concat(rows, ignore_index=True)


def _correlations_by_model(model_frames: dict[str, pd.DataFrame]) -> pd.DataFrame:
    rows = []
    for model_name, frame in model_frames.items():
        correlations = frame[STRUCTURE_METRIC_COLUMNS].corr(method="pearson")
        for metric in correlations.index:
            row = {"model": model_name, "metric": metric}
            row.update(correlations.loc[metric].to_dict())
            rows.append(row)
    return pd.DataFrame(rows)


def _strong_metric_stability(anova: pd.DataFrame, top_n: int = 3) -> pd.DataFrame:
    model_top_metrics = {}
    for model_name, group in anova.groupby("model"):
        top_metrics = group.sort_values("eta_squared", ascending=False).head(top_n)["metric"].tolist()
        model_top_metrics[model_name] = top_metrics

    all_top_metrics = sorted({metric for metrics in model_top_metrics.values() for metric in metrics})
    rows = []
    for metric in all_top_metrics:
        present_in = [model for model, metrics in model_top_metrics.items() if metric in metrics]
        rows.append(
            {
                "metric": metric,
                "models_where_top_metric": ", ".join(present_in),
                "model_count": len(present_in),
                "stable_across_all_models": len(present_in) == len(model_top_metrics),
            }
        )
    return pd.DataFrame(rows)


def _write_comparison_report(
    output_path: Path,
    category_means: pd.DataFrame,
    anova: pd.DataFrame,
    correlations: pd.DataFrame,
    stability: pd.DataFrame,
) -> None:
    ensure_dir(output_path.parent)
    lines = [
        "# Model Comparison Report",
        "",
        "## Goal",
        "",
        "Test whether trajectory geometry signals are model-specific or behave similarly across Hugging Face causal language models. This report does not claim a universal constant.",
        "",
        "## Category Means by Model",
        "",
        _dataframe_to_markdown(category_means),
        "",
        "## ANOVA p-values and Eta Squared by Model",
        "",
        _dataframe_to_markdown(anova[["model", "metric", "p_value", "eta_squared", "anova_f"]]),
        "",
        "## Strongest Metric Stability",
        "",
        "A metric is considered stable here only if it appears in the top three eta-squared trajectory-structure metrics for every compared model.",
        "",
        _dataframe_to_markdown(stability),
        "",
        "## Correlation Matrices by Model",
        "",
        _dataframe_to_markdown(correlations),
        "",
        "## Interpretation Guardrail",
        "",
        "Similar rankings across models suggest a reusable geometry signal. Divergent rankings suggest the signal may be architecture, scale, or run dependent. Neither result proves a universal constant.",
    ]
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _log_error(log_path: Path, context: str, exc: Exception) -> None:
    with log_path.open("a", encoding="utf-8") as log_file:
        log_file.write(f"[{context}] {type(exc).__name__}: {exc}\n")
        log_file.write(traceback.format_exc())
        log_file.write("\n")
