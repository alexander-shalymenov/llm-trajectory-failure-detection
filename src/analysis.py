from __future__ import annotations

from pathlib import Path
import traceback

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.feature_selection import f_classif

from src.evaluation import enrich_frame_with_evaluation
from src.utils import ensure_dir


METRIC_COLUMNS = ["L", "D", "C", "E", "V", "candidate_metric_01"]
CORRELATION_COLUMNS = ["candidate_metric_01", "output_token_count", "E", "generation_time_seconds"]


def run_statistical_analysis(frame: pd.DataFrame, results_dir: str | Path) -> dict[str, pd.DataFrame]:
    results_path = ensure_dir(results_dir)
    charts_dir = ensure_dir(results_path / "charts")
    log_path = results_path / "analysis.log"
    log_path.write_text("", encoding="utf-8")

    try:
        metric_summary = _metric_summary(frame)
        category_summary = _category_metric_summary(frame)
        correlations = frame[CORRELATION_COLUMNS].corr(method="pearson")
        separation = _category_separation_tests(frame)
        quality_summary = _answer_quality_summary(frame)
        quality_tests = _correctness_separation_tests(frame)
        correctness_correlations = _correctness_correlations(frame)
    except Exception as exc:
        _log_error(log_path, "statistical_analysis", exc)
        raise

    _write_summary_report(
        results_path / "summary.md",
        frame,
        metric_summary,
        category_summary,
        correlations,
        separation,
        quality_summary,
        quality_tests,
        correctness_correlations,
    )
    _save_analysis_charts(frame, charts_dir, correlations, log_path)

    return {
        "metric_summary": metric_summary,
        "category_summary": category_summary,
        "correlations": correlations,
        "category_separation": separation,
        "answer_quality_summary": quality_summary,
        "answer_quality_tests": quality_tests,
        "correctness_correlations": correctness_correlations,
    }


def load_results_csv(path: str | Path) -> pd.DataFrame:
    frame = pd.read_csv(path)
    numeric_columns = sorted(set(METRIC_COLUMNS + CORRELATION_COLUMNS + ["mean_token_entropy"]))
    for column in numeric_columns:
        if column in frame.columns:
            frame[column] = pd.to_numeric(frame[column], errors="coerce")
    return frame


def load_results_with_evaluation(results_dir: str | Path, prompts_path: str | Path) -> pd.DataFrame:
    from src.utils import load_json, write_json

    results_path = Path(results_dir)
    frame = load_results_csv(results_path / "results.csv")
    prompts = load_json(prompts_path)
    frame = enrich_frame_with_evaluation(frame, prompts)

    csv_frame = frame.copy()
    for column in ["generated_tokens", "generated_token_ids", "token_entropy", "logits_shape", "hidden_states_shape"]:
        if column in csv_frame.columns:
            csv_frame[column] = csv_frame[column].apply(lambda value: repr(value) if not isinstance(value, str) else value)
    csv_frame.to_csv(results_path / "results.csv", index=False)

    json_path = results_path / "results.json"
    if json_path.exists():
        records = load_json(json_path)
        by_id = frame.set_index("id").to_dict(orient="index")
        for record in records:
            values = by_id.get(record.get("id"), {})
            for column in ["expected_answer", "evaluation_type", "is_evaluable", "is_correct", "evaluation_notes"]:
                record[column] = _json_safe(values.get(column))
        write_json(json_path, records)

    return frame


def _metric_summary(frame: pd.DataFrame) -> pd.DataFrame:
    return frame[METRIC_COLUMNS].agg(["mean", "median", "std"]).T.reset_index(names="metric")


def _category_metric_summary(frame: pd.DataFrame) -> pd.DataFrame:
    summary = (
        frame.groupby("category")[METRIC_COLUMNS]
        .agg(["mean", "median", "std"])
        .sort_index(axis=1)
        .reset_index()
    )
    summary.columns = [
        column if isinstance(column, str) else "_".join(part for part in column if part)
        for column in summary.columns
    ]
    return summary


def _category_separation_tests(frame: pd.DataFrame) -> pd.DataFrame:
    category_codes = frame["category"].astype("category").cat.codes.to_numpy()
    rows = []

    for metric in METRIC_COLUMNS:
        values = frame[[metric]].replace([np.inf, -np.inf], np.nan).fillna(0.0)
        f_values, p_values = f_classif(values, category_codes)
        eta_squared = _eta_squared(frame, metric)
        rows.append(
            {
                "metric": metric,
                "anova_f": float(f_values[0]),
                "p_value": float(p_values[0]),
                "eta_squared": float(eta_squared),
                "meaningful_separation": bool(p_values[0] < 0.05 and eta_squared >= 0.06),
            }
        )

    return pd.DataFrame(rows)


def _answer_quality_summary(frame: pd.DataFrame) -> pd.DataFrame:
    evaluable = _evaluable_frame(frame)
    if evaluable.empty:
        return pd.DataFrame(columns=["is_correct", "metric", "mean", "median", "std", "count"])

    rows = []
    for is_correct, group in evaluable.groupby("is_correct"):
        for metric in METRIC_COLUMNS:
            values = group[metric].to_numpy(dtype=float)
            rows.append(
                {
                    "is_correct": bool(is_correct),
                    "metric": metric,
                    "mean": float(np.mean(values)),
                    "median": float(np.median(values)),
                    "std": float(np.std(values, ddof=1)) if len(values) > 1 else 0.0,
                    "count": int(len(values)),
                }
            )
    return pd.DataFrame(rows)


def _correctness_separation_tests(frame: pd.DataFrame) -> pd.DataFrame:
    evaluable = _evaluable_frame(frame)
    if evaluable.empty or evaluable["is_correct"].nunique() < 2:
        return pd.DataFrame(
            [
                {
                    "metric": metric,
                    "anova_f": np.nan,
                    "p_value": np.nan,
                    "eta_squared": np.nan,
                    "notes": "Need both correct and incorrect answers.",
                }
                for metric in METRIC_COLUMNS
            ]
        )

    groups = evaluable["is_correct"].astype(int).to_numpy()
    rows = []
    for metric in METRIC_COLUMNS:
        values = evaluable[[metric]].replace([np.inf, -np.inf], np.nan).fillna(0.0)
        try:
            f_values, p_values = f_classif(values, groups)
            eta_squared = _eta_squared_by_group(evaluable, metric, "is_correct")
            rows.append(
                {
                    "metric": metric,
                    "anova_f": float(f_values[0]),
                    "p_value": float(p_values[0]),
                    "eta_squared": float(eta_squared),
                    "notes": "One-way ANOVA across correct vs incorrect answers.",
                }
            )
        except Exception as exc:
            rows.append(
                {
                    "metric": metric,
                    "anova_f": np.nan,
                    "p_value": np.nan,
                    "eta_squared": np.nan,
                    "notes": f"Test failed: {type(exc).__name__}: {exc}",
                }
            )
    return pd.DataFrame(rows)


def _correctness_correlations(frame: pd.DataFrame) -> pd.DataFrame:
    evaluable = _evaluable_frame(frame)
    if evaluable.empty:
        return pd.DataFrame(columns=["metric", "pearson_correlation_with_correctness"])

    rows = []
    correctness = evaluable["is_correct"].astype(int)
    for metric in METRIC_COLUMNS:
        correlation = correctness.corr(evaluable[metric])
        rows.append({"metric": metric, "pearson_correlation_with_correctness": correlation})
    return pd.DataFrame(rows)


def _eta_squared(frame: pd.DataFrame, metric: str) -> float:
    values = frame[metric].to_numpy(dtype=float)
    grand_mean = float(np.mean(values))
    ss_total = float(np.sum((values - grand_mean) ** 2))
    if ss_total <= 0.0:
        return 0.0

    ss_between = 0.0
    for _, group in frame.groupby("category"):
        group_values = group[metric].to_numpy(dtype=float)
        ss_between += len(group_values) * float((np.mean(group_values) - grand_mean) ** 2)
    return ss_between / ss_total


def _eta_squared_by_group(frame: pd.DataFrame, metric: str, group_column: str) -> float:
    values = frame[metric].to_numpy(dtype=float)
    grand_mean = float(np.mean(values))
    ss_total = float(np.sum((values - grand_mean) ** 2))
    if ss_total <= 0.0:
        return 0.0

    ss_between = 0.0
    for _, group in frame.groupby(group_column):
        group_values = group[metric].to_numpy(dtype=float)
        ss_between += len(group_values) * float((np.mean(group_values) - grand_mean) ** 2)
    return ss_between / ss_total


def _evaluable_frame(frame: pd.DataFrame) -> pd.DataFrame:
    if "is_evaluable" not in frame.columns or "is_correct" not in frame.columns:
        return pd.DataFrame(columns=frame.columns)
    evaluable = frame[(frame["is_evaluable"] == True) & frame["is_correct"].notna()].copy()
    if evaluable.empty:
        return evaluable
    evaluable["is_correct"] = evaluable["is_correct"].astype(bool)
    return evaluable


def _save_analysis_charts(
    frame: pd.DataFrame,
    charts_dir: Path,
    correlations: pd.DataFrame,
    log_path: Path,
) -> None:
    _safe_chart("set_matplotlib_style", lambda: plt.style.use("seaborn-v0_8-whitegrid"), log_path)
    _safe_chart("metric_vs_prompt_category", lambda: _plot_metric_vs_category(frame, charts_dir), log_path)
    _safe_chart("entropy_vs_curvature", lambda: _plot_entropy_vs_curvature(frame, charts_dir), log_path)
    _safe_chart(
        "output_length_vs_candidate_metric_01",
        lambda: _plot_output_length_vs_candidate_metric(frame, charts_dir),
        log_path,
    )
    _safe_chart("boxplots_by_category", lambda: _plot_boxplots_by_category(frame, charts_dir), log_path)
    _safe_chart("histograms", lambda: _plot_histograms(frame, charts_dir), log_path)
    _safe_chart("correlation_heatmap", lambda: _plot_correlation_heatmap(correlations, charts_dir), log_path)
    _safe_chart("correctness_candidate_metric_01", lambda: _plot_metric_by_correctness(frame, charts_dir, "candidate_metric_01"), log_path)
    _safe_chart("correctness_E", lambda: _plot_metric_by_correctness(frame, charts_dir, "E"), log_path)
    _safe_chart("correctness_L", lambda: _plot_metric_by_correctness(frame, charts_dir, "L"), log_path)


def _safe_chart(name: str, chart_function, log_path: Path) -> None:
    try:
        chart_function()
    except Exception as exc:
        _log_error(log_path, f"chart:{name}", exc)


def _plot_metric_vs_category(frame: pd.DataFrame, charts_dir: Path) -> None:
    grouped = frame.groupby("category", as_index=False)["candidate_metric_01"].mean()
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(grouped["category"], grouped["candidate_metric_01"], color="#4c78a8")
    ax.set_xlabel("Prompt category")
    ax.set_ylabel("Mean candidate_metric_01")
    ax.set_title("Metric vs prompt category")
    ax.tick_params(axis="x", rotation=30)
    fig.tight_layout()
    fig.savefig(charts_dir / "metric_vs_prompt_category.png", dpi=160)
    plt.close(fig)


def _plot_entropy_vs_curvature(frame: pd.DataFrame, charts_dir: Path) -> None:
    fig, ax = plt.subplots(figsize=(7, 5))
    for category, group in frame.groupby("category"):
        ax.scatter(group["E"], group["C"], label=category, s=55)
    ax.set_xlabel("Mean token entropy (E)")
    ax.set_ylabel("Curvature ratio (C)")
    ax.set_title("Entropy vs curvature")
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(charts_dir / "entropy_vs_curvature.png", dpi=160)
    plt.close(fig)


def _plot_output_length_vs_candidate_metric(frame: pd.DataFrame, charts_dir: Path) -> None:
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.scatter(frame["output_token_count"], frame["candidate_metric_01"], color="#f58518", s=55)
    ax.set_xlabel("Output token count")
    ax.set_ylabel("candidate_metric_01")
    ax.set_title("Output length vs candidate_metric_01")
    fig.tight_layout()
    fig.savefig(charts_dir / "output_length_vs_candidate_metric_01.png", dpi=160)
    plt.close(fig)


def _plot_boxplots_by_category(frame: pd.DataFrame, charts_dir: Path) -> None:
    categories = sorted(frame["category"].unique())
    for metric in METRIC_COLUMNS:
        data = [frame.loc[frame["category"] == category, metric].to_numpy() for category in categories]
        fig, ax = plt.subplots(figsize=(11, 5))
        ax.boxplot(data, tick_labels=categories, patch_artist=True)
        ax.set_title(f"{metric} by category")
        ax.set_xlabel("Prompt category")
        ax.set_ylabel(metric)
        ax.tick_params(axis="x", rotation=30)
        fig.tight_layout()
        fig.savefig(charts_dir / f"boxplot_{metric}.png", dpi=160)
        plt.close(fig)


def _plot_histograms(frame: pd.DataFrame, charts_dir: Path) -> None:
    for metric in METRIC_COLUMNS:
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.hist(frame[metric].to_numpy(dtype=float), bins=24, color="#54a24b", edgecolor="white")
        ax.set_title(f"{metric} distribution")
        ax.set_xlabel(metric)
        ax.set_ylabel("Count")
        fig.tight_layout()
        fig.savefig(charts_dir / f"histogram_{metric}.png", dpi=160)
        plt.close(fig)


def _plot_correlation_heatmap(correlations: pd.DataFrame, charts_dir: Path) -> None:
    fig, ax = plt.subplots(figsize=(7, 6))
    image = ax.imshow(correlations.to_numpy(), vmin=-1.0, vmax=1.0, cmap="coolwarm")
    ax.set_xticks(range(len(correlations.columns)), labels=correlations.columns, rotation=35, ha="right")
    ax.set_yticks(range(len(correlations.index)), labels=correlations.index)

    for row_index in range(len(correlations.index)):
        for column_index in range(len(correlations.columns)):
            value = correlations.iloc[row_index, column_index]
            ax.text(column_index, row_index, f"{value:.2f}", ha="center", va="center", color="black")

    ax.set_title("Correlation heatmap")
    fig.colorbar(image, ax=ax, fraction=0.046, pad=0.04)
    fig.tight_layout()
    fig.savefig(charts_dir / "correlation_heatmap.png", dpi=160)
    plt.close(fig)


def _plot_metric_by_correctness(frame: pd.DataFrame, charts_dir: Path, metric: str) -> None:
    evaluable = _evaluable_frame(frame)
    if evaluable.empty or evaluable["is_correct"].nunique() < 2:
        raise ValueError(f"Cannot plot {metric} by correctness without both correct and incorrect rows.")

    labels = ["incorrect", "correct"]
    data = [
        evaluable.loc[evaluable["is_correct"] == False, metric].to_numpy(),
        evaluable.loc[evaluable["is_correct"] == True, metric].to_numpy(),
    ]
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.boxplot(data, tick_labels=labels, patch_artist=True)
    ax.set_title(f"{metric} by correctness")
    ax.set_xlabel("Answer correctness")
    ax.set_ylabel(metric)
    fig.tight_layout()
    fig.savefig(charts_dir / f"{metric}_by_correctness.png", dpi=160)
    plt.close(fig)


def _write_summary_report(
    path: Path,
    frame: pd.DataFrame,
    metric_summary: pd.DataFrame,
    category_summary: pd.DataFrame,
    correlations: pd.DataFrame,
    separation: pd.DataFrame,
    quality_summary: pd.DataFrame,
    quality_tests: pd.DataFrame,
    correctness_correlations: pd.DataFrame,
) -> None:
    meaningful = separation[separation["meaningful_separation"]]
    if meaningful.empty:
        verdict = (
            "No current metric meets the exploratory threshold for statistically meaningful "
            "category separation. Treat any visual category differences as hypotheses."
        )
    else:
        metric_names = ", ".join(meaningful["metric"].tolist())
        verdict = (
            "The following current metrics meet the exploratory threshold for category separation: "
            f"{metric_names}. This is evidence for follow-up testing, not proof of invariance."
        )

    lines = [
        "# GPT-2 Trajectory Summary",
        "",
        "## Dataset",
        "",
        f"- Total prompts: {len(frame)}",
        f"- Categories: {', '.join(sorted(frame['category'].unique()))}",
        "",
        "## Metric Summary",
        "",
        _dataframe_to_markdown(metric_summary),
        "",
        "## Category Separation",
        "",
        "One-way ANOVA is used as a first-pass category separation test. Eta squared is included as an effect-size estimate. The exploratory threshold is p < 0.05 and eta_squared >= 0.06.",
        "",
        _dataframe_to_markdown(separation),
        "",
        "## Validation Verdict",
        "",
        verdict,
        "",
        "## Correlations",
        "",
        _dataframe_to_markdown(correlations.reset_index(names="metric")),
        "",
        "## Category-Level Metric Summary",
        "",
        _dataframe_to_markdown(category_summary),
        "",
        "## Answer Quality Analysis",
        "",
        "Correctness scoring is applied only where `expected_answer` and `evaluation_type` are present. Explanations and abstract questions are excluded for now. These tests ask whether trajectory metrics contain a usable answer-quality signal; they do not prove a new constant.",
        "",
        f"- Evaluable prompts: {int(_evaluable_frame(frame).shape[0])}",
        f"- Correct prompts: {int(_evaluable_frame(frame)['is_correct'].sum()) if not _evaluable_frame(frame).empty else 0}",
        f"- Incorrect prompts: {int((~_evaluable_frame(frame)['is_correct']).sum()) if not _evaluable_frame(frame).empty else 0}",
        "",
        "### Correct vs Incorrect Metric Summary",
        "",
        _dataframe_to_markdown(quality_summary),
        "",
        "### Correctness Separation Tests",
        "",
        _dataframe_to_markdown(quality_tests),
        "",
        "### Correctness Correlations",
        "",
        _dataframe_to_markdown(correctness_correlations),
        "",
        "## Charts",
        "",
        "- `results/charts/metric_vs_prompt_category.png`",
        "- `results/charts/entropy_vs_curvature.png`",
        "- `results/charts/output_length_vs_candidate_metric_01.png`",
        "- `results/charts/correlation_heatmap.png`",
        "- `results/charts/boxplot_<metric>.png`",
        "- `results/charts/histogram_<metric>.png`",
        "- `results/charts/candidate_metric_01_by_correctness.png`",
        "- `results/charts/E_by_correctness.png`",
        "- `results/charts/L_by_correctness.png`",
    ]

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _dataframe_to_markdown(frame: pd.DataFrame) -> str:
    headers = [str(column) for column in frame.columns]
    rows = [[_format_markdown_value(value) for value in row] for row in frame.to_numpy()]
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(row) + " |")
    return "\n".join(lines)


def _format_markdown_value(value: object) -> str:
    if isinstance(value, (float, np.floating)):
        return f"{float(value):.6f}"
    if isinstance(value, (bool, np.bool_)):
        return str(bool(value))
    return str(value)


def _json_safe(value: object) -> object:
    if isinstance(value, np.generic):
        return value.item()
    if pd.isna(value) if not isinstance(value, list) else False:
        return None
    return value


def _log_error(log_path: Path, context: str, exc: Exception) -> None:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("a", encoding="utf-8") as log_file:
        log_file.write(f"[{context}] {type(exc).__name__}: {exc}\n")
        log_file.write(traceback.format_exc())
        log_file.write("\n")
