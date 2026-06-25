from __future__ import annotations

from pathlib import Path
import traceback

import numpy as np
import pandas as pd

from src.analysis import _dataframe_to_markdown
from src.utils import ensure_dir


EPSILON = 1e-12
RATIO_DEFINITIONS = {
    "dispersion_over_expansion": ("hidden_state_dispersion", "trajectory_expansion"),
    "radius_over_dispersion": ("hidden_state_radius", "hidden_state_dispersion"),
    "loop_score_over_expansion": ("trajectory_loop_score", "trajectory_expansion"),
    "entropy_step_over_curvature_density": ("entropy_per_step", "curvature_density"),
    "dispersion_over_radius": ("hidden_state_dispersion", "hidden_state_radius"),
    "expansion_over_radius": ("trajectory_expansion", "hidden_state_radius"),
}


def run_invariant_search(model_dirs: list[str | Path], output_path: str | Path) -> dict[str, pd.DataFrame]:
    if len(model_dirs) < 2:
        raise ValueError("Invariant search requires at least two model output folders.")

    output = Path(output_path)
    log_path = output.parent / "analysis.log"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    log_path.touch(exist_ok=True)

    try:
        data = _load_ratio_data(model_dirs)
        global_summary = _summary_by_group(data, [], "global")
        model_summary = _summary_by_group(data, ["model"], "per_model")
        category_summary = _summary_by_group(data, ["category"], "per_category")
        model_category_summary = _summary_by_group(data, ["model", "category"], "per_model_category")
        stability = _rank_ratio_stability(data, model_summary, category_summary)

        _write_invariant_report(
            output,
            data,
            global_summary,
            model_summary,
            category_summary,
            model_category_summary,
            stability,
        )

        return {
            "ratios": data,
            "global_summary": global_summary,
            "model_summary": model_summary,
            "category_summary": category_summary,
            "model_category_summary": model_category_summary,
            "stability": stability,
        }
    except Exception as exc:
        _log_error(log_path, "invariant_search", exc)
        raise


def _load_ratio_data(model_dirs: list[str | Path]) -> pd.DataFrame:
    frames = []
    for model_dir in model_dirs:
        path = Path(model_dir)
        csv_path = path / "results.csv"
        if not csv_path.exists():
            raise FileNotFoundError(f"Missing model results CSV: {csv_path}")

        frame = pd.read_csv(csv_path)
        required = sorted({column for pair in RATIO_DEFINITIONS.values() for column in pair})
        missing = [column for column in required if column not in frame.columns]
        if missing:
            raise ValueError(f"{csv_path} is missing required existing metric columns: {missing}")

        ratio_frame = frame[["id", "category", *required]].copy()
        ratio_frame.insert(0, "model", path.name)
        for column in required:
            ratio_frame[column] = pd.to_numeric(ratio_frame[column], errors="coerce")
        for ratio_name, (numerator, denominator) in RATIO_DEFINITIONS.items():
            denominator_values = ratio_frame[denominator]
            ratio_frame[ratio_name] = np.where(
                denominator_values.abs() > EPSILON,
                ratio_frame[numerator] / denominator_values,
                np.nan,
            )
        frames.append(ratio_frame[["model", "id", "category", *RATIO_DEFINITIONS.keys()]])

    return pd.concat(frames, ignore_index=True)


def _summary_by_group(data: pd.DataFrame, group_columns: list[str], scope: str) -> pd.DataFrame:
    rows = []
    if group_columns:
        grouped = data.groupby(group_columns, dropna=False)
        for group_key, group in grouped:
            if not isinstance(group_key, tuple):
                group_key = (group_key,)
            base = {"scope": scope}
            base.update(dict(zip(group_columns, group_key)))
            rows.extend(_ratio_summary_rows(group, base))
    else:
        rows.extend(_ratio_summary_rows(data, {"scope": scope}))
    return pd.DataFrame(rows)


def _ratio_summary_rows(frame: pd.DataFrame, base: dict[str, object]) -> list[dict[str, object]]:
    rows = []
    for ratio in RATIO_DEFINITIONS:
        values = pd.to_numeric(frame[ratio], errors="coerce").replace([np.inf, -np.inf], np.nan).dropna()
        mean = float(values.mean()) if len(values) else np.nan
        std = float(values.std(ddof=1)) if len(values) > 1 else 0.0
        rows.append(
            {
                **base,
                "ratio": ratio,
                "mean": mean,
                "std": std,
                "coefficient_of_variation": _coefficient_of_variation(mean, std),
                "count": int(len(values)),
            }
        )
    return rows


def _rank_ratio_stability(
    data: pd.DataFrame,
    model_summary: pd.DataFrame,
    category_summary: pd.DataFrame,
) -> pd.DataFrame:
    global_summary = _summary_by_group(data, [], "global").set_index("ratio")
    rows = []
    for ratio in RATIO_DEFINITIONS:
        model_means = model_summary.loc[model_summary["ratio"] == ratio, "mean"]
        category_means = category_summary.loc[category_summary["ratio"] == ratio, "mean"]
        model_mean = float(model_means.mean())
        category_mean = float(category_means.mean())
        model_cv = _coefficient_of_variation(model_mean, float(model_means.std(ddof=1)))
        category_cv = _coefficient_of_variation(category_mean, float(category_means.std(ddof=1)))
        global_cv = float(global_summary.loc[ratio, "coefficient_of_variation"])
        stability_score = float(np.nanmean([global_cv, model_cv, category_cv]))
        rows.append(
            {
                "ratio": ratio,
                "global_cv": global_cv,
                "model_mean_cv": model_cv,
                "category_mean_cv": category_cv,
                "stability_score": stability_score,
                "global_mean": float(global_summary.loc[ratio, "mean"]),
                "model_mean_range": float(model_means.max() - model_means.min()),
                "category_mean_range": float(category_means.max() - category_means.min()),
            }
        )
    return pd.DataFrame(rows).sort_values("stability_score", ascending=True).reset_index(drop=True)


def _write_invariant_report(
    output_path: Path,
    data: pd.DataFrame,
    global_summary: pd.DataFrame,
    model_summary: pd.DataFrame,
    category_summary: pd.DataFrame,
    model_category_summary: pd.DataFrame,
    stability: pd.DataFrame,
) -> None:
    ensure_dir(output_path.parent)
    models = ", ".join(sorted(data["model"].unique()))
    lines = [
        "# Invariant Ratio Search Report",
        "",
        "## Goal",
        "",
        "Search for approximately stable ratios across GPT-2-family model outputs using only existing trajectory structure metrics. These ratios are not prediction targets and do not establish a universal constant.",
        "",
        "## Models",
        "",
        f"- {models}",
        "",
        "## Ratio Definitions",
        "",
        *[f"- `{name}` = `{num}` / `{den}`" for name, (num, den) in RATIO_DEFINITIONS.items()],
        "",
        "## Stability Ranking",
        "",
        "Ratios are ranked by the average of global coefficient of variation, model-mean coefficient of variation, and category-mean coefficient of variation. Lower is more stable.",
        "",
        _dataframe_to_markdown(stability),
        "",
        "## Global Summary",
        "",
        _dataframe_to_markdown(global_summary),
        "",
        "## Per-Model Summary",
        "",
        _dataframe_to_markdown(model_summary),
        "",
        "## Per-Category Summary",
        "",
        _dataframe_to_markdown(category_summary),
        "",
        "## Per-Model Per-Category Summary",
        "",
        _dataframe_to_markdown(model_category_summary),
        "",
        "## Interpretation Guardrail",
        "",
        "A ratio is interesting when it has low coefficient of variation and similar means across both models and categories. This report only identifies candidates for follow-up validation.",
    ]
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _coefficient_of_variation(mean: float, std: float) -> float:
    if not np.isfinite(mean) or abs(mean) <= EPSILON:
        return np.nan
    return float(abs(std / mean))


def _log_error(log_path: Path, context: str, exc: Exception) -> None:
    with log_path.open("a", encoding="utf-8") as log_file:
        log_file.write(f"[{context}] {type(exc).__name__}: {exc}\n")
        log_file.write(traceback.format_exc())
        log_file.write("\n")
