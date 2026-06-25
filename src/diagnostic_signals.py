from __future__ import annotations

from itertools import combinations
from pathlib import Path
import traceback

import numpy as np
import pandas as pd
from sklearn.feature_selection import f_classif

from src.analysis import METRIC_COLUMNS, _dataframe_to_markdown
from src.trajectory_structure import STRUCTURE_METRIC_COLUMNS


DIAGNOSTIC_METRICS = METRIC_COLUMNS + STRUCTURE_METRIC_COLUMNS
STRONG_ETA = 0.06
WEAK_ETA = 0.03


def run_diagnostic_signal_report(model_dirs: list[str | Path], output_path: str | Path) -> dict[str, pd.DataFrame]:
    if len(model_dirs) < 2:
        raise ValueError("Diagnostic signal report requires at least two model output folders.")

    output = Path(output_path)
    log_path = output.parent / "analysis.log"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    log_path.touch(exist_ok=True)

    try:
        model_frames = _load_model_frames(model_dirs)
        separation = _category_separation_by_model(model_frames)
        category_rankings = _category_mean_rankings(model_frames)
        correlation_similarity = _correlation_similarity(model_frames)
        correctness_similarity = _correctness_similarity(model_frames)
        portable_scores = _portable_signal_scores(separation, category_rankings, correlation_similarity, correctness_similarity)
        model_specific = _model_specific_signals(separation)
        conclusion = _plain_english_conclusion(portable_scores, model_specific)
        _write_report(
            output,
            model_frames,
            separation,
            category_rankings,
            correlation_similarity,
            correctness_similarity,
            portable_scores,
            model_specific,
            conclusion,
        )
        return {
            "separation": separation,
            "category_rankings": category_rankings,
            "correlation_similarity": correlation_similarity,
            "correctness_similarity": correctness_similarity,
            "portable_scores": portable_scores,
            "model_specific": model_specific,
        }
    except Exception as exc:
        _log_error(log_path, "diagnostic_signals", exc)
        raise


def _load_model_frames(model_dirs: list[str | Path]) -> dict[str, pd.DataFrame]:
    frames = {}
    for model_dir in model_dirs:
        path = Path(model_dir)
        csv_path = path / "results.csv"
        if not csv_path.exists():
            raise FileNotFoundError(f"Missing results CSV: {csv_path}")

        frame = pd.read_csv(csv_path)
        missing = [metric for metric in DIAGNOSTIC_METRICS if metric not in frame.columns]
        if missing:
            raise ValueError(f"{csv_path} is missing diagnostic metric columns: {missing}")

        for metric in DIAGNOSTIC_METRICS:
            frame[metric] = pd.to_numeric(frame[metric], errors="coerce")
        if "is_evaluable" in frame.columns:
            frame["is_evaluable"] = frame["is_evaluable"].astype(str).str.lower().eq("true")
        if "is_correct" in frame.columns:
            frame["is_correct_numeric"] = frame["is_correct"].astype(str).str.lower().map({"true": 1.0, "false": 0.0})

        model_name = path.name
        if model_name in frames:
            raise ValueError(f"Duplicate model folder name: {model_name}")
        frames[model_name] = frame
    return frames


def _category_separation_by_model(model_frames: dict[str, pd.DataFrame]) -> pd.DataFrame:
    rows = []
    for model, frame in model_frames.items():
        category_codes = frame["category"].astype("category").cat.codes.to_numpy()
        for metric in DIAGNOSTIC_METRICS:
            values = frame[[metric]].replace([np.inf, -np.inf], np.nan).fillna(0.0)
            f_values, p_values = f_classif(values, category_codes)
            rows.append(
                {
                    "model": model,
                    "metric": metric,
                    "p_value": float(p_values[0]),
                    "eta_squared": _eta_squared(frame, metric, "category"),
                    "anova_f": float(f_values[0]),
                    "category_mean_ranking": _category_ranking_string(frame, metric),
                }
            )
    return pd.DataFrame(rows)


def _category_mean_rankings(model_frames: dict[str, pd.DataFrame]) -> pd.DataFrame:
    model_names = list(model_frames)
    rows = []
    for metric in DIAGNOSTIC_METRICS:
        means_by_model = {
            model: model_frames[model].groupby("category")[metric].mean()
            for model in model_names
        }
        pairwise_similarities = []
        for first, second in combinations(model_names, 2):
            aligned = pd.concat([means_by_model[first], means_by_model[second]], axis=1, keys=[first, second]).dropna()
            similarity = aligned[first].corr(aligned[second], method="spearman") if len(aligned) > 1 else np.nan
            if pd.notna(similarity):
                pairwise_similarities.append(float(similarity))

        row = {
            "metric": metric,
            "category_ranking_similarity": float(np.mean(pairwise_similarities)) if pairwise_similarities else np.nan,
            "pairwise_category_ranking_similarity": "; ".join(
                _pairwise_ranking_similarity_string(means_by_model, first, second)
                for first, second in combinations(model_names, 2)
            ),
        }
        for model, means in means_by_model.items():
            row[f"{model}_ranking"] = _ranking_from_series(means)
        rows.append(row)
    return pd.DataFrame(rows)


def _correlation_similarity(model_frames: dict[str, pd.DataFrame]) -> pd.DataFrame:
    model_names = list(model_frames)
    correlations_by_model = {
        model: frame[DIAGNOSTIC_METRICS].corr(method="pearson")
        for model, frame in model_frames.items()
    }
    rows = []
    for metric in DIAGNOSTIC_METRICS:
        pairwise_similarities = []
        pairwise_notes = []
        for first, second in combinations(model_names, 2):
            first_vector = correlations_by_model[first].loc[metric].drop(index=metric)
            second_vector = correlations_by_model[second].loc[metric].drop(index=metric)
            aligned = pd.concat([first_vector, second_vector], axis=1, keys=[first, second]).dropna()
            similarity = aligned[first].corr(aligned[second], method="pearson") if len(aligned) > 1 else np.nan
            if pd.notna(similarity):
                pairwise_similarities.append(float(similarity))
                pairwise_notes.append(f"{first} vs {second}: {similarity:.4f}")
        rows.append(
            {
                "metric": metric,
                "correlation_pattern_similarity": float(np.mean(pairwise_similarities)) if pairwise_similarities else np.nan,
                "pairwise_correlation_pattern_similarity": "; ".join(pairwise_notes),
            }
        )
    return pd.DataFrame(rows)


def _correctness_similarity(model_frames: dict[str, pd.DataFrame]) -> pd.DataFrame:
    rows = []
    per_model = []
    for model, frame in model_frames.items():
        if "is_correct_numeric" not in frame.columns or "is_evaluable" not in frame.columns:
            continue
        evaluable = frame[frame["is_evaluable"] & frame["is_correct_numeric"].notna()]
        for metric in DIAGNOSTIC_METRICS:
            correlation = evaluable["is_correct_numeric"].corr(evaluable[metric]) if len(evaluable) > 1 else np.nan
            per_model.append({"model": model, "metric": metric, "correctness_correlation": correlation})

    per_model_frame = pd.DataFrame(per_model)
    if per_model_frame.empty:
        return pd.DataFrame(columns=["metric", "correctness_relationship_similarity", "correctness_correlation_by_model"])

    for metric, group in per_model_frame.groupby("metric"):
        correlations = group.set_index("model")["correctness_correlation"].dropna()
        if len(correlations) < 2:
            similarity = np.nan
        else:
            difference = float(correlations.max() - correlations.min())
            similarity = max(0.0, 1.0 - min(1.0, difference))
        rows.append(
            {
                "metric": metric,
                "correctness_relationship_similarity": similarity,
                "correctness_correlation_by_model": "; ".join(f"{model}: {value:.4f}" for model, value in correlations.items()),
            }
        )
    return pd.DataFrame(rows)


def _portable_signal_scores(
    separation: pd.DataFrame,
    category_rankings: pd.DataFrame,
    correlation_similarity: pd.DataFrame,
    correctness_similarity: pd.DataFrame,
) -> pd.DataFrame:
    rows = []
    for metric in DIAGNOSTIC_METRICS:
        metric_sep = separation[separation["metric"] == metric]
        eta_min = float(metric_sep["eta_squared"].min())
        eta_max = float(metric_sep["eta_squared"].max())
        eta_mean = float(metric_sep["eta_squared"].mean())
        separation_score = min(1.0, eta_min / STRONG_ETA)

        ranking_similarity = _value_for_metric(category_rankings, metric, "category_ranking_similarity")
        ranking_score = _similarity_to_score(ranking_similarity)
        corr_similarity = _value_for_metric(correlation_similarity, metric, "correlation_pattern_similarity")
        corr_score = _similarity_to_score(corr_similarity)
        correctness_score = _value_for_metric(correctness_similarity, metric, "correctness_relationship_similarity")
        if np.isnan(correctness_score):
            correctness_score = 0.5

        portable_score = float(
            0.40 * separation_score
            + 0.25 * corr_score
            + 0.20 * ranking_score
            + 0.15 * correctness_score
        )
        rows.append(
            {
                "metric": metric,
                "portable_signal_score": portable_score,
                "classification": _classify_metric(portable_score, eta_min, eta_max),
                "min_eta_squared": eta_min,
                "mean_eta_squared": eta_mean,
                "max_eta_squared": eta_max,
                "category_ranking_similarity": ranking_similarity,
                "correlation_pattern_similarity": corr_similarity,
                "correctness_relationship_similarity": correctness_score,
            }
        )
    return pd.DataFrame(rows).sort_values("portable_signal_score", ascending=False).reset_index(drop=True)


def _model_specific_signals(separation: pd.DataFrame) -> pd.DataFrame:
    rows = []
    models = list(separation["model"].unique())
    for metric in DIAGNOSTIC_METRICS:
        values = separation[separation["metric"] == metric].set_index("model")["eta_squared"]
        strong_models = [model for model in models if values.get(model, 0.0) >= STRONG_ETA]
        weak_models = [model for model in models if values.get(model, 0.0) < WEAK_ETA]
        if strong_models and len(strong_models) + len(weak_models) == len(models):
            rows.append(
                {
                    "metric": metric,
                    "model_specific_pattern": f"strong in {', '.join(strong_models)}, weak in {', '.join(weak_models)}",
                }
            )
    return pd.DataFrame(rows)


def _classify_metric(score: float, eta_min: float, eta_max: float) -> str:
    if eta_max >= STRONG_ETA and eta_min < WEAK_ETA:
        return "model-specific signal"
    if score >= 0.70 and eta_min >= WEAK_ETA:
        return "strong reusable diagnostic signal"
    if score >= 0.50 and eta_min >= 0.015:
        return "weak reusable diagnostic signal"
    return "not useful"


def _plain_english_conclusion(scores: pd.DataFrame, model_specific: pd.DataFrame) -> list[str]:
    strong = scores[scores["classification"] == "strong reusable diagnostic signal"]["metric"].tolist()
    weak = scores[scores["classification"] == "weak reusable diagnostic signal"]["metric"].tolist()
    not_useful = scores[scores["classification"] == "not useful"]["metric"].tolist()
    lines = []
    if strong:
        lines.append(f"What worked: {', '.join(strong)} showed the best cross-model diagnostic behavior.")
    elif weak:
        lines.append(f"What worked: no metric reached the strong threshold, but {', '.join(weak[:5])} showed weak reusable signal.")
    else:
        lines.append("What worked: no metric reached the reusable diagnostic threshold in this model comparison.")

    if not_useful:
        lines.append(f"What failed: {', '.join(not_useful[:6])} had too little portable separation or inconsistent relationships.")
    if not model_specific.empty:
        patterns = "; ".join(f"{row.metric} ({row.model_specific_pattern})" for row in model_specific.itertuples(index=False))
        lines.append(f"Model-specific behavior: {patterns}.")
    lines.append("What to test next: run the same prompt set on additional causal language models and check whether the top-ranked diagnostics preserve category ranking, correlation fingerprints, and correctness relationships.")
    return lines


def _write_report(
    output_path: Path,
    model_frames: dict[str, pd.DataFrame],
    separation: pd.DataFrame,
    category_rankings: pd.DataFrame,
    correlation_similarity: pd.DataFrame,
    correctness_similarity: pd.DataFrame,
    scores: pd.DataFrame,
    model_specific: pd.DataFrame,
    conclusion: list[str],
) -> None:
    lines = [
        "# Diagnostic Signal Report",
        "",
        "## Goal",
        "",
        "Compare completed model runs to identify trajectory metrics that are diagnostically useful across models. The goal is diagnostic usefulness, not proving a new constant.",
        "",
        "## Models",
        "",
        f"- {', '.join(model_frames.keys())}",
        "",
        "## Portable Signal Ranking",
        "",
        _dataframe_to_markdown(scores),
        "",
        "## Category Separation Within Each Model",
        "",
        _dataframe_to_markdown(separation[["model", "metric", "p_value", "eta_squared", "category_mean_ranking"]]),
        "",
        "## Category Ranking Similarity",
        "",
        _dataframe_to_markdown(category_rankings),
        "",
        "## Correlation Pattern Similarity",
        "",
        _dataframe_to_markdown(correlation_similarity),
        "",
        "## Correctness Relationship Similarity",
        "",
        _dataframe_to_markdown(correctness_similarity),
        "",
        "## Model-Specific Signals",
        "",
        _dataframe_to_markdown(model_specific) if not model_specific.empty else "No strong/weak split matched the model-specific threshold.",
        "",
        "## Plain-English Conclusion",
        "",
        *[f"- {line}" for line in conclusion],
    ]
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _eta_squared(frame: pd.DataFrame, metric: str, group_column: str) -> float:
    values = frame[metric].to_numpy(dtype=float)
    grand_mean = float(np.nanmean(values))
    ss_total = float(np.nansum((values - grand_mean) ** 2))
    if ss_total <= 0.0:
        return 0.0
    ss_between = 0.0
    for _, group in frame.groupby(group_column):
        group_values = group[metric].to_numpy(dtype=float)
        ss_between += len(group_values) * float((np.nanmean(group_values) - grand_mean) ** 2)
    return float(ss_between / ss_total)


def _category_ranking_string(frame: pd.DataFrame, metric: str) -> str:
    means = frame.groupby("category")[metric].mean()
    return _ranking_from_series(means)


def _ranking_from_series(series: pd.Series) -> str:
    ordered = series.sort_values(ascending=False)
    return " > ".join(f"{category} ({value:.4f})" for category, value in ordered.items())


def _pairwise_ranking_similarity_string(
    means_by_model: dict[str, pd.Series],
    first: str,
    second: str,
) -> str:
    aligned = pd.concat([means_by_model[first], means_by_model[second]], axis=1, keys=[first, second]).dropna()
    similarity = aligned[first].corr(aligned[second], method="spearman") if len(aligned) > 1 else np.nan
    if pd.isna(similarity):
        return f"{first} vs {second}: n/a"
    return f"{first} vs {second}: {similarity:.4f}"


def _value_for_metric(frame: pd.DataFrame, metric: str, column: str) -> float:
    values = frame.loc[frame["metric"] == metric, column]
    if values.empty:
        return np.nan
    return float(values.iloc[0])


def _similarity_to_score(value: float) -> float:
    if np.isnan(value):
        return 0.0
    return float((value + 1.0) / 2.0)


def _log_error(log_path: Path, context: str, exc: Exception) -> None:
    with log_path.open("a", encoding="utf-8") as log_file:
        log_file.write(f"[{context}] {type(exc).__name__}: {exc}\n")
        log_file.write(traceback.format_exc())
        log_file.write("\n")
