from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import traceback

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.feature_selection import f_classif

from src.analysis import _dataframe_to_markdown
from src.utils import ensure_dir


EPSILON = 1e-12
STRUCTURE_METRIC_COLUMNS = [
    "path_efficiency",
    "curvature_density",
    "entropy_per_step",
    "trajectory_compression",
    "trajectory_expansion",
    "hidden_state_dispersion",
    "hidden_state_radius",
    "trajectory_self_similarity",
    "trajectory_loop_score",
]


@dataclass(frozen=True)
class TrajectoryStructureFeatures:
    path_efficiency: float
    curvature_density: float
    entropy_per_step: float
    trajectory_compression: float
    trajectory_expansion: float
    hidden_state_dispersion: float
    hidden_state_radius: float
    trajectory_self_similarity: float
    trajectory_loop_score: int


def run_trajectory_structure_analysis(results_dir: str | Path) -> dict[str, pd.DataFrame]:
    results_path = Path(results_dir)
    log_path = results_path / "analysis.log"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    log_path.touch(exist_ok=True)

    try:
        frame = pd.read_csv(results_path / "results.csv")
        frame = _coerce_numeric_columns(frame)
        frame = add_structure_features_to_frame(frame, results_path / "raw_internal_data.npz")
        frame.to_csv(results_path / "results.csv", index=False)

        category_means = frame.groupby("category")[STRUCTURE_METRIC_COLUMNS].mean().reset_index()
        anova = _category_anova(frame)
        correlations = frame[STRUCTURE_METRIC_COLUMNS].corr(method="pearson")
        _write_structure_report(
            results_path / "trajectory_structure_report.md",
            frame,
            category_means,
            anova,
            correlations,
        )
        _save_structure_charts(frame, results_path / "charts", log_path)

        return {
            "category_means": category_means,
            "anova": anova,
            "correlations": correlations,
        }
    except Exception as exc:
        _log_error(log_path, "trajectory_structure_analysis", exc)
        raise


def add_structure_features_to_frame(frame: pd.DataFrame, raw_data_path: str | Path) -> pd.DataFrame:
    raw_data = np.load(raw_data_path)
    rows = []

    for row in frame.itertuples(index=False):
        prompt_id = getattr(row, "id")
        hidden_key = f"{prompt_id}__hidden_states"
        if hidden_key not in raw_data:
            rows.append(_empty_features())
            continue

        hidden_states = raw_data[hidden_key]
        features = compute_structure_features(
            hidden_states=hidden_states,
            L=float(getattr(row, "L")),
            D=float(getattr(row, "D")),
            E=float(getattr(row, "E")),
            V=float(getattr(row, "V")),
            output_token_count=float(getattr(row, "output_token_count")),
        )
        rows.append(asdict(features))

    feature_frame = pd.DataFrame(rows)
    return pd.concat(
        [frame.drop(columns=STRUCTURE_METRIC_COLUMNS, errors="ignore"), feature_frame],
        axis=1,
    )


def compute_structure_features(
    hidden_states: np.ndarray,
    L: float,
    D: float,
    E: float,
    V: float,
    output_token_count: float,
) -> TrajectoryStructureFeatures:
    token_count = max(float(output_token_count), EPSILON)
    hidden_states = np.asarray(hidden_states, dtype=np.float64)

    dispersion, radius = _centroid_distances(hidden_states)
    return TrajectoryStructureFeatures(
        path_efficiency=float(D / max(L, EPSILON)),
        curvature_density=float(V / max(L, EPSILON)),
        entropy_per_step=float(E / token_count),
        trajectory_compression=float(D / token_count),
        trajectory_expansion=float(L / token_count),
        hidden_state_dispersion=dispersion,
        hidden_state_radius=radius,
        trajectory_self_similarity=_trajectory_self_similarity(hidden_states),
        trajectory_loop_score=_trajectory_loop_score(hidden_states),
    )


def _centroid_distances(hidden_states: np.ndarray) -> tuple[float, float]:
    if hidden_states.size == 0:
        return 0.0, 0.0
    centroid = np.mean(hidden_states, axis=0)
    distances = np.linalg.norm(hidden_states - centroid, axis=1)
    return float(np.mean(distances)), float(np.max(distances))


def _trajectory_self_similarity(hidden_states: np.ndarray) -> float:
    if len(hidden_states) < 4:
        return 0.0

    midpoint = len(hidden_states) // 2
    first_half = hidden_states[:midpoint]
    second_half = hidden_states[midpoint:]
    pair_count = min(len(first_half) - 1, len(second_half) - 1)
    if pair_count <= 0:
        return 0.0

    first_steps = np.diff(first_half, axis=0)[:pair_count]
    second_steps = np.diff(second_half, axis=0)[:pair_count]
    first_vector = first_steps.reshape(-1)
    second_vector = second_steps.reshape(-1)
    denominator = np.linalg.norm(first_vector) * np.linalg.norm(second_vector)
    if denominator <= EPSILON:
        return 0.0
    return float(np.dot(first_vector, second_vector) / denominator)


def _trajectory_loop_score(hidden_states: np.ndarray) -> int:
    if len(hidden_states) < 4:
        return 0

    step_distances = np.linalg.norm(np.diff(hidden_states, axis=0), axis=1)
    positive_steps = step_distances[step_distances > EPSILON]
    if positive_steps.size == 0:
        return 0

    threshold = float(np.median(positive_steps) * 0.5)
    min_gap = 3
    loop_count = 0
    for index in range(min_gap, len(hidden_states)):
        prior = hidden_states[: index - min_gap]
        if prior.size == 0:
            continue
        distances = np.linalg.norm(prior - hidden_states[index], axis=1)
        if np.any(distances <= threshold):
            loop_count += 1
    return int(loop_count)


def _category_anova(frame: pd.DataFrame) -> pd.DataFrame:
    category_codes = frame["category"].astype("category").cat.codes.to_numpy()
    rows = []
    for metric in STRUCTURE_METRIC_COLUMNS:
        values = frame[[metric]].replace([np.inf, -np.inf], np.nan).fillna(0.0)
        f_values, p_values = f_classif(values, category_codes)
        rows.append(
            {
                "metric": metric,
                "anova_f": float(f_values[0]),
                "p_value": float(p_values[0]),
                "eta_squared": _eta_squared(frame, metric),
            }
        )
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
    return float(ss_between / ss_total)


def _write_structure_report(
    path: Path,
    frame: pd.DataFrame,
    category_means: pd.DataFrame,
    anova: pd.DataFrame,
    correlations: pd.DataFrame,
) -> None:
    strongest = anova.sort_values("eta_squared", ascending=False).head(3)
    lines = [
        "# Trajectory Structure Report",
        "",
        "## Goal",
        "",
        "Identify whether different task categories produce different internal trajectory geometries. Existing trajectory metric formulas are not modified here.",
        "",
        "## Dataset",
        "",
        f"- Total prompts: {len(frame)}",
        f"- Categories: {', '.join(sorted(frame['category'].unique()))}",
        "",
        "## Category Means",
        "",
        _dataframe_to_markdown(category_means),
        "",
        "## Category ANOVA",
        "",
        _dataframe_to_markdown(anova),
        "",
        "## Eta Squared Ranking",
        "",
        _dataframe_to_markdown(strongest[["metric", "eta_squared", "p_value"]]),
        "",
        "## Correlation Matrix",
        "",
        _dataframe_to_markdown(correlations.reset_index(names="metric")),
        "",
        "## Notes",
        "",
        "These structure metrics are exploratory geometry descriptors. Category separation indicates possible task-dependent trajectory geometry, not a proof of invariance or a new constant.",
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _save_structure_charts(frame: pd.DataFrame, charts_dir: str | Path, log_path: Path) -> None:
    charts_path = ensure_dir(charts_dir)
    _safe_chart("structure_heatmap", lambda: _plot_structure_heatmap(frame, charts_path), log_path)


def _plot_structure_heatmap(frame: pd.DataFrame, charts_dir: Path) -> None:
    correlations = frame[STRUCTURE_METRIC_COLUMNS].corr(method="pearson")
    fig, ax = plt.subplots(figsize=(10, 8))
    image = ax.imshow(correlations.to_numpy(), vmin=-1.0, vmax=1.0, cmap="coolwarm")
    ax.set_xticks(range(len(correlations.columns)), labels=correlations.columns, rotation=40, ha="right")
    ax.set_yticks(range(len(correlations.index)), labels=correlations.index)
    ax.set_title("Trajectory structure correlation matrix")
    fig.colorbar(image, ax=ax, fraction=0.046, pad=0.04)
    fig.tight_layout()
    fig.savefig(charts_dir / "trajectory_structure_correlation_heatmap.png", dpi=160)
    plt.close(fig)


def _safe_chart(name: str, chart_function, log_path: Path) -> None:
    try:
        chart_function()
    except Exception as exc:
        _log_error(log_path, f"chart:{name}", exc)


def _coerce_numeric_columns(frame: pd.DataFrame) -> pd.DataFrame:
    columns = [
        "L",
        "D",
        "E",
        "V",
        "output_token_count",
        *STRUCTURE_METRIC_COLUMNS,
    ]
    for column in columns:
        if column in frame.columns:
            frame[column] = pd.to_numeric(frame[column], errors="coerce")
    return frame


def _empty_features() -> dict[str, float]:
    return {column: np.nan for column in STRUCTURE_METRIC_COLUMNS}


def _log_error(log_path: Path, context: str, exc: Exception) -> None:
    with log_path.open("a", encoding="utf-8") as log_file:
        log_file.write(f"[{context}] {type(exc).__name__}: {exc}\n")
        log_file.write(traceback.format_exc())
        log_file.write("\n")
