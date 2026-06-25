from __future__ import annotations

from html import escape
from pathlib import Path

import numpy as np
import pandas as pd


SENSOR_METRICS = ["trajectory_loop_score", "L", "entropy_per_step"]
NORMALIZED_COLUMNS = ["normalized_loop_score", "normalized_L", "normalized_entropy_per_step"]


def create_trajectory_monitor(model_dirs: list[str | Path], output_dir: str | Path) -> pd.DataFrame:
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    long_frame = _load_monitor_data(model_dirs)
    scored = _add_risk_scores(long_frame)
    prompt_frame = _prompt_centered_frame(scored)

    prompt_frame.to_csv(output_path / "trajectory_monitor.csv", index=False)
    (output_path / "trajectory_monitor.html").write_text(_render_html(prompt_frame, scored), encoding="utf-8")
    return prompt_frame


def refresh_trajectory_monitor_from_csv(csv_path: str | Path, output_dir: str | Path | None = None) -> pd.DataFrame:
    source_path = Path(csv_path)
    output_path = Path(output_dir) if output_dir is not None else source_path.parent
    frame = pd.read_csv(source_path)

    if {"prompt_id", "models", "highest_risk_model"}.issubset(frame.columns):
        prompt_frame = frame
        long_frame = _long_from_prompt_frame(prompt_frame)
    else:
        long_frame = _add_risk_scores(frame)
        prompt_frame = _prompt_centered_frame(long_frame)

    prompt_frame.to_csv(output_path / "trajectory_monitor.csv", index=False)
    (output_path / "trajectory_monitor.html").write_text(_render_html(prompt_frame, long_frame), encoding="utf-8")
    return prompt_frame


def _load_monitor_data(model_dirs: list[str | Path]) -> pd.DataFrame:
    frames = []
    for model_dir in model_dirs:
        path = Path(model_dir)
        csv_path = path / "results.csv"
        if not csv_path.exists():
            raise FileNotFoundError(f"Missing results CSV: {csv_path}")

        frame = pd.read_csv(csv_path)
        missing = [column for column in ["id", "category", "prompt", "generated_response", *SENSOR_METRICS] if column not in frame.columns]
        if missing:
            raise ValueError(f"{csv_path} is missing monitor columns: {missing}")

        columns = ["id", "category", "prompt", "generated_response", *SENSOR_METRICS]
        if "is_correct" in frame.columns:
            columns.append("is_correct")
        selected = frame[columns].copy()
        selected.insert(0, "model", path.name)
        frames.append(selected)

    return pd.concat(frames, ignore_index=True)


def _add_risk_scores(frame: pd.DataFrame) -> pd.DataFrame:
    scored = frame.copy()
    if "id" in scored.columns and "prompt_id" not in scored.columns:
        scored = scored.rename(columns={"id": "prompt_id"})
    for metric in SENSOR_METRICS:
        scored[metric] = pd.to_numeric(scored[metric], errors="coerce")

    scored["correctness"] = _correctness_column(scored)
    scored["normalized_loop_score"] = _normalize(scored["trajectory_loop_score"])
    scored["normalized_L"] = _normalize(scored["L"])
    scored["normalized_entropy_per_step"] = _normalize(scored["entropy_per_step"])
    scored["trajectory_risk_score"] = scored[NORMALIZED_COLUMNS].mean(axis=1)

    low_threshold = scored["trajectory_risk_score"].quantile(0.60)
    high_threshold = scored["trajectory_risk_score"].quantile(0.85)
    scored["status_label"] = scored["trajectory_risk_score"].apply(
        lambda score: _status_label(score, low_threshold, high_threshold)
    )
    scored["risk_reason"] = scored.apply(_risk_reason, axis=1)
    scored["recommended_action"] = scored["status_label"].map(
        {
            "stable": "keep answer",
            "review": "check answer",
            "unstable": "run self-check or stronger model",
        }
    )
    return scored


def _prompt_centered_frame(scored: pd.DataFrame) -> pd.DataFrame:
    rows = []
    models = list(scored["model"].drop_duplicates())
    for prompt_id, group in scored.groupby("prompt_id", sort=False):
        first = group.iloc[0]
        highest = group.loc[group["trajectory_risk_score"].idxmax()]
        lowest = group.loc[group["trajectory_risk_score"].idxmin()]
        status_agreement = group["status_label"].nunique(dropna=True) == 1
        correctness_values = group.loc[group["correctness"].isin(["correct", "incorrect"]), "correctness"]
        correctness_agreement = "not evaluable"
        if not correctness_values.empty:
            correctness_agreement = "yes" if correctness_values.nunique(dropna=True) == 1 else "no"

        row = {
            "prompt_id": prompt_id,
            "category": first["category"],
            "prompt": first["prompt"],
            "models": ", ".join(models),
            "highest_risk_model": highest["model"],
            "highest_risk_score": highest["trajectory_risk_score"],
            "lowest_risk_model": lowest["model"],
            "lowest_risk_score": lowest["trajectory_risk_score"],
            "models_agree_on_status": "yes" if status_agreement else "no",
            "models_agree_on_correctness": correctness_agreement,
            "has_status_disagreement": not status_agreement,
            "has_correctness_disagreement": correctness_agreement == "no",
            "has_incorrect": bool((group["correctness"] == "incorrect").any()),
            "max_status": _max_status(group["status_label"]),
        }

        for model in models:
            model_rows = group[group["model"] == model]
            if model_rows.empty:
                continue
            item = model_rows.iloc[0]
            prefix = _safe_column_prefix(model)
            row.update(
                {
                    f"{prefix}_generated_response": _response_display_text(item["generated_response"]),
                    f"{prefix}_correctness": item["correctness"],
                    f"{prefix}_trajectory_risk_score": item["trajectory_risk_score"],
                    f"{prefix}_status_label": item["status_label"],
                    f"{prefix}_risk_reason": item["risk_reason"],
                    f"{prefix}_recommended_action": item["recommended_action"],
                    f"{prefix}_trajectory_loop_score": item["trajectory_loop_score"],
                    f"{prefix}_L": item["L"],
                    f"{prefix}_entropy_per_step": item["entropy_per_step"],
                }
            )
        rows.append(row)
    return pd.DataFrame(rows)


def _long_from_prompt_frame(prompt_frame: pd.DataFrame) -> pd.DataFrame:
    models = sorted({column.removesuffix("_status_label") for column in prompt_frame.columns if column.endswith("_status_label")})
    rows = []
    for row in prompt_frame.itertuples(index=False):
        data = row._asdict()
        for model in models:
            response_key = f"{model}_generated_response"
            if response_key not in data:
                continue
            rows.append(
                {
                    "model": model,
                    "prompt_id": data["prompt_id"],
                    "category": data["category"],
                    "prompt": data["prompt"],
                    "generated_response": data.get(response_key, ""),
                    "correctness": data.get(f"{model}_correctness", "not available"),
                    "trajectory_risk_score": data.get(f"{model}_trajectory_risk_score", np.nan),
                    "status_label": data.get(f"{model}_status_label", "stable"),
                    "risk_reason": data.get(f"{model}_risk_reason", ""),
                    "recommended_action": data.get(f"{model}_recommended_action", ""),
                    "trajectory_loop_score": data.get(f"{model}_trajectory_loop_score", np.nan),
                    "L": data.get(f"{model}_L", np.nan),
                    "entropy_per_step": data.get(f"{model}_entropy_per_step", np.nan),
                }
            )
    return pd.DataFrame(rows)


def _correctness_column(frame: pd.DataFrame) -> pd.Series:
    if "correctness" in frame.columns:
        return frame["correctness"].fillna("not available").astype(str)
    if "is_correct" not in frame.columns:
        return pd.Series("not available", index=frame.index)

    values = frame["is_correct"].astype(str).str.lower()
    return values.map({"true": "correct", "false": "incorrect"}).fillna("not available")


def _normalize(values: pd.Series) -> pd.Series:
    values = pd.to_numeric(values, errors="coerce")
    minimum = values.min()
    maximum = values.max()
    if pd.isna(minimum) or pd.isna(maximum) or np.isclose(maximum, minimum):
        return pd.Series(0.0, index=values.index)
    return (values - minimum) / (maximum - minimum)


def _status_label(score: float, low_threshold: float, high_threshold: float) -> str:
    if score >= high_threshold:
        return "unstable"
    if score >= low_threshold:
        return "review"
    return "stable"


def _risk_reason(row: pd.Series) -> str:
    sensors = [
        ("high loop score", row["normalized_loop_score"]),
        ("long path length", row["normalized_L"]),
        ("high entropy per step", row["normalized_entropy_per_step"]),
    ]
    elevated = [label for label, value in sensors if pd.notna(value) and value >= 0.60]
    if elevated:
        return ", ".join(elevated)
    label, _ = max(sensors, key=lambda item: item[1] if pd.notna(item[1]) else -1)
    return f"mostly {label}"


def _max_status(statuses: pd.Series) -> str:
    rank = {"stable": 0, "review": 1, "unstable": 2}
    return max(statuses, key=lambda status: rank.get(str(status), -1))


def _render_html(prompt_frame: pd.DataFrame, long_frame: pd.DataFrame) -> str:
    category_options = _option_tags(prompt_frame["category"].unique())
    prompt_blocks = "\n".join(_render_prompt_comparison(row) for row in prompt_frame.itertuples(index=False))
    summary_cards = _summary_cards(prompt_frame)

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>LLM Trajectory Comparison Monitor</title>
  <style>
    :root {{
      --bg: #f4f6f8;
      --panel: #ffffff;
      --ink: #17212b;
      --muted: #5d6b7a;
      --line: #d7dde5;
      --stable: #1f7a4d;
      --review: #a16207;
      --unstable: #b42318;
      --accent: #2457a6;
    }}
    * {{ box-sizing: border-box; }}
    body {{ margin: 0; font-family: Inter, Arial, sans-serif; background: var(--bg); color: var(--ink); }}
    header {{ padding: 28px 32px 18px; background: linear-gradient(180deg, #ffffff, #f7f9fc); border-bottom: 1px solid var(--line); }}
    h1 {{ margin: 0; font-size: 30px; letter-spacing: 0; }}
    .subtitle {{ max-width: 920px; margin-top: 8px; color: var(--muted); line-height: 1.45; }}
    .filters {{ position: sticky; top: 0; z-index: 5; display: flex; gap: 12px; flex-wrap: wrap; padding: 14px 32px; background: rgba(255,255,255,.96); border-bottom: 1px solid var(--line); backdrop-filter: blur(8px); }}
    label {{ display: grid; gap: 4px; font-size: 12px; color: var(--muted); font-weight: 700; }}
    select, input {{ min-width: 190px; padding: 9px 10px; border: 1px solid var(--line); background: #fff; color: var(--ink); border-radius: 6px; }}
    main {{ padding: 22px 32px 36px; }}
    .grid {{ display: grid; grid-template-columns: repeat(4, minmax(160px, 1fr)); gap: 14px; margin-bottom: 18px; }}
    .card, .prompt-block {{ background: var(--panel); border: 1px solid var(--line); border-radius: 8px; padding: 16px; box-shadow: 0 1px 2px rgba(16,24,40,.04); }}
    .card-title {{ color: var(--muted); font-size: 12px; font-weight: 800; text-transform: uppercase; letter-spacing: .04em; }}
    .card-value {{ margin-top: 8px; font-size: 28px; font-weight: 800; }}
    .card-note {{ margin-top: 6px; color: var(--muted); font-size: 13px; }}
    .section-title {{ margin: 24px 0 10px; font-size: 18px; font-weight: 800; }}
    .prompt-list {{ display: grid; gap: 18px; }}
    .question-block {{ border-bottom: 1px solid var(--line); padding-bottom: 14px; margin-bottom: 14px; }}
    .question-meta {{ display: flex; gap: 8px; flex-wrap: wrap; align-items: center; }}
    .prompt-title {{ font-weight: 900; font-size: 18px; }}
    .prompt-text {{ margin-top: 10px; color: #243447; line-height: 1.48; font-size: 15px; }}
    .comparison-summary {{ display: flex; gap: 8px; flex-wrap: wrap; margin-top: 12px; }}
    .compare-table {{ width: 100%; border-collapse: collapse; table-layout: fixed; }}
    .compare-table th, .compare-table td {{ border: 1px solid var(--line); padding: 10px; vertical-align: top; }}
    .compare-table th {{ background: #e9eff7; font-size: 16px; text-align: center; color: #17212b; }}
    .compare-table th:first-child {{ width: 150px; font-size: 12px; color: var(--muted); text-transform: uppercase; text-align: left; }}
    .row-label {{ color: var(--muted); font-weight: 800; font-size: 12px; text-transform: uppercase; }}
    .response-preview {{ color: #263747; line-height: 1.35; max-height: 72px; overflow: hidden; }}
    details {{ line-height: 1.35; }}
    summary {{ cursor: pointer; color: var(--accent); margin-top: 6px; font-weight: 800; }}
    .badge {{ display: inline-block; padding: 4px 8px; border-radius: 999px; font-weight: 800; font-size: 12px; border: 1px solid currentColor; white-space: nowrap; }}
    .stable {{ color: var(--stable); background: #edf8f2; }}
    .review {{ color: var(--review); background: #fff7df; }}
    .unstable {{ color: var(--unstable); background: #fff0ee; }}
    .muted {{ color: var(--muted); }}
    @media (max-width: 1000px) {{ .grid {{ grid-template-columns: repeat(2, minmax(160px, 1fr)); }} .compare-table {{ min-width: 980px; }} .prompt-block {{ overflow-x: auto; }} }}
  </style>
</head>
<body>
  <header>
    <h1>LLM Trajectory Comparison Monitor</h1>
    <div class="subtitle">This dashboard does not judge answer correctness. It shows how unusual or unstable the internal trajectory looks compared with other runs.</div>
  </header>
  <section class="filters">
    <label>Category<select id="categoryFilter"><option value="">All categories</option>{category_options}</select></label>
    <label>Risk disagreement<select id="riskDisagreementFilter"><option value="">All prompts</option><option value="yes">Risk disagreement only</option></select></label>
    <label>Correctness disagreement<select id="correctnessDisagreementFilter"><option value="">All prompts</option><option value="yes">Correctness disagreement only</option></select></label>
    <label>Search<input id="searchFilter" type="search" placeholder="Prompt or response"></label>
  </section>
  <main>
    <section class="grid">{summary_cards}</section>
    <div class="section-title">Prompt Comparison Monitor</div>
    <section id="promptCards" class="prompt-list">{prompt_blocks}</section>
  </main>
  <script>
    const controls = {{
      category: document.getElementById('categoryFilter'),
      riskDisagreement: document.getElementById('riskDisagreementFilter'),
      correctnessDisagreement: document.getElementById('correctnessDisagreementFilter'),
      search: document.getElementById('searchFilter')
    }};
    const cards = Array.from(document.querySelectorAll('.prompt-block'));
    function applyFilters() {{
      const search = controls.search.value.toLowerCase();
      for (const card of cards) {{
        const categoryOk = !controls.category.value || card.dataset.category === controls.category.value;
        const riskOk = !controls.riskDisagreement.value || card.dataset.riskDisagreement === 'yes';
        const correctnessOk = !controls.correctnessDisagreement.value || card.dataset.correctnessDisagreement === 'yes';
        const searchOk = !search || card.dataset.search.includes(search);
        card.style.display = categoryOk && riskOk && correctnessOk && searchOk ? '' : 'none';
      }}
    }}
    Object.values(controls).forEach(control => control.addEventListener('input', applyFilters));
  </script>
</body>
</html>
"""


def _render_prompt_comparison(row: object) -> str:
    data = row._asdict()
    model_specs = _model_specs(data)
    responses = " ".join(_text(spec["generated_response"]) for spec in model_specs)
    search_text = f"{_text(data['prompt'])} {responses}".lower()
    risk_disagreement = "yes" if data["models_agree_on_status"] == "no" else "no"
    correctness_disagreement = "yes" if data["models_agree_on_correctness"] == "no" else "no"
    return f"""<article class="prompt-block" data-category="{escape(str(data['category']))}" data-risk-disagreement="{risk_disagreement}" data-correctness-disagreement="{correctness_disagreement}" data-search="{escape(search_text)}">
  <div class="question-block">
    <div class="question-meta">
      <span class="prompt-title">{escape(str(data['prompt_id']))}</span>
      <span class="badge stable">{escape(str(data['category']))}</span>
    </div>
    <div class="prompt-text">{escape(_text(data['prompt']))}</div>
    <div class="comparison-summary">
      <span class="badge review">highest: {escape(str(data['highest_risk_model']))}</span>
      <span class="badge stable">lowest: {escape(str(data['lowest_risk_model']))}</span>
      <span class="badge {'stable' if data['models_agree_on_status'] == 'yes' else 'unstable'}">risk agree: {escape(str(data['models_agree_on_status']))}</span>
      <span class="badge {'stable' if data['models_agree_on_correctness'] in ['yes', 'not evaluable'] else 'unstable'}">correctness agree: {escape(str(data['models_agree_on_correctness']))}</span>
    </div>
  </div>
  {_comparison_table(model_specs)}
</article>"""


def _comparison_table(model_specs: list[dict[str, object]]) -> str:
    rows = [
        ("Answer preview", lambda spec: _response_cell(spec)),
        ("Correctness", lambda spec: escape(_text(spec["correctness"], "not available"))),
        ("Risk status", lambda spec: f'<span class="badge {escape(str(spec["status_label"]))}">{escape(str(spec["status_label"]))}</span>'),
        ("Risk score", lambda spec: _fmt(spec["trajectory_risk_score"])),
        ("Risk reason", lambda spec: escape(_text(spec["risk_reason"]))),
        ("Loop score", lambda spec: _fmt(spec["trajectory_loop_score"])),
        ("L", lambda spec: _fmt(spec["L"])),
        ("Entropy per step", lambda spec: _fmt(spec["entropy_per_step"])),
        ("Action", lambda spec: escape(_text(spec["recommended_action"]))),
    ]
    header = "".join(f"<th>{escape(str(spec['label']))}</th>" for spec in model_specs)
    body = "\n".join(
        f"<tr><td class=\"row-label\">{escape(label)}</td>{''.join(f'<td>{renderer(spec)}</td>' for spec in model_specs)}</tr>"
        for label, renderer in rows
    )
    return f"""<table class="compare-table">
  <thead><tr><th>Comparison</th>{header}</tr></thead>
  <tbody>{body}</tbody>
</table>"""


def _response_cell(spec: dict[str, object]) -> str:
    response = _response_display_text(spec["generated_response"])
    preview = response[:120] + ("..." if len(response) > 120 else "")
    return f"""<div class="response-preview">{escape(preview)}</div><details><summary>Full response</summary>{escape(response)}</details>"""


def _summary_cards(frame: pd.DataFrame) -> str:
    total = len(frame)
    risk_disagreements = int((frame["models_agree_on_status"] == "no").sum())
    correctness_disagreements = int((frame["models_agree_on_correctness"] == "no").sum())
    highest_model = _highest_risk_model_overall(frame)
    cards = [
        ("Total Prompts", f"{total:,}", "same prompt compared across three models"),
        ("Correctness Disagreement", f"{correctness_disagreements:,}", "models differ where evaluable"),
        ("Risk Disagreement", f"{risk_disagreements:,}", "models differ on trajectory status"),
        ("Highest-Risk Model", highest_model, "highest average prompt risk"),
    ]
    return "".join(_card(title, value, note) for title, value, note in cards)


def _highest_risk_model_overall(frame: pd.DataFrame) -> str:
    values = {}
    for spec in _available_model_prefixes(frame):
        column = f"{spec['prefix']}_trajectory_risk_score"
        values[str(spec["label"])] = pd.to_numeric(frame[column], errors="coerce").mean()
    if not values:
        return "n/a"
    return max(values, key=values.get)


def _model_specs(data: dict[str, object]) -> list[dict[str, object]]:
    specs = []
    for prefix, label in [
        ("gpt2", "GPT-2"),
        ("distilgpt2", "DistilGPT2"),
        ("tinyllama", "TinyLlama"),
        ("rerun_gpt2", "GPT-2"),
        ("rerun_distilgpt2", "DistilGPT2"),
        ("rerun_tinyllama", "TinyLlama"),
    ]:
        response_key = f"{prefix}_generated_response"
        if response_key not in data:
            continue
        specs.append(
            {
                "prefix": prefix,
                "label": label,
                "generated_response": data.get(response_key, ""),
                "correctness": data.get(f"{prefix}_correctness", "not available"),
                "trajectory_risk_score": data.get(f"{prefix}_trajectory_risk_score", np.nan),
                "status_label": data.get(f"{prefix}_status_label", "stable"),
                "risk_reason": data.get(f"{prefix}_risk_reason", ""),
                "recommended_action": data.get(f"{prefix}_recommended_action", ""),
                "trajectory_loop_score": data.get(f"{prefix}_trajectory_loop_score", np.nan),
                "L": data.get(f"{prefix}_L", np.nan),
                "entropy_per_step": data.get(f"{prefix}_entropy_per_step", np.nan),
            }
        )
    return specs


def _available_model_prefixes(frame: pd.DataFrame) -> list[dict[str, str]]:
    columns = set(frame.columns)
    return [
        {"prefix": prefix, "label": label}
        for prefix, label in [
            ("gpt2", "GPT-2"),
            ("distilgpt2", "DistilGPT2"),
            ("tinyllama", "TinyLlama"),
            ("rerun_gpt2", "GPT-2"),
            ("rerun_distilgpt2", "DistilGPT2"),
            ("rerun_tinyllama", "TinyLlama"),
        ]
        if f"{prefix}_trajectory_risk_score" in columns
    ]


def _card(title: str, value: str, note: str) -> str:
    return f"""<div class="card"><div class="card-title">{escape(title)}</div><div class="card-value">{escape(value)}</div><div class="card-note">{escape(note)}</div></div>"""


def _option_tags(values: object) -> str:
    return "".join(f'<option value="{escape(str(value))}">{escape(str(value))}</option>' for value in sorted(values))


def _safe_column_prefix(value: str) -> str:
    return "".join(char if char.isalnum() else "_" for char in str(value)).strip("_").lower()


def _fmt(value: object) -> str:
    try:
        if pd.isna(value):
            return ""
        return f"{float(value):.3f}"
    except (TypeError, ValueError):
        return escape(str(value))


def _text(value: object, fallback: str = "") -> str:
    if value is None:
        return fallback
    try:
        if pd.isna(value):
            return fallback
    except (TypeError, ValueError):
        pass
    return str(value)


def _response_display_text(value: object) -> str:
    response = _text(value)
    if not response.strip():
        return "[empty generation]"
    return response
