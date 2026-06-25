from __future__ import annotations

import re
import string
from dataclasses import dataclass
from typing import Any

import pandas as pd


EVALUATION_COLUMNS = [
    "expected_answer",
    "evaluation_type",
    "is_evaluable",
    "is_correct",
    "evaluation_notes",
]


@dataclass(frozen=True)
class EvaluationResult:
    is_evaluable: bool
    is_correct: bool | None
    evaluation_notes: str


def evaluate_response(
    generated_response: Any,
    expected_answer: Any,
    evaluation_type: Any,
) -> EvaluationResult:
    if pd.isna(evaluation_type) or evaluation_type in {"", None}:
        return EvaluationResult(False, None, "No evaluation_type provided.")
    if _is_missing_expected_answer(expected_answer):
        return EvaluationResult(False, None, "No expected_answer provided.")

    response = _normalize_text(generated_response)
    expected_values = _expected_values(expected_answer)
    normalized_expected = [_normalize_text(value) for value in expected_values]
    evaluation_type = str(evaluation_type)

    if evaluation_type == "exact":
        is_correct = response in normalized_expected
    elif evaluation_type == "contains":
        is_correct = any(value and value in response for value in normalized_expected)
    elif evaluation_type == "yes_no":
        is_correct = _extract_yes_no(response) in normalized_expected
    elif evaluation_type == "multiple_acceptable":
        is_correct = any(_answer_matches(response, value) for value in normalized_expected)
    else:
        return EvaluationResult(False, None, f"Unknown evaluation_type: {evaluation_type}")

    note = "Matched expected answer." if is_correct else "Did not match expected answer."
    return EvaluationResult(True, bool(is_correct), note)


def enrich_frame_with_evaluation(frame: pd.DataFrame, prompts: list[dict[str, Any]]) -> pd.DataFrame:
    prompt_metadata = pd.DataFrame(
        [
            {
                "id": item["id"],
                "expected_answer": item.get("expected_answer"),
                "evaluation_type": item.get("evaluation_type"),
            }
            for item in prompts
        ]
    )

    enriched = frame.drop(columns=[column for column in EVALUATION_COLUMNS if column in frame.columns], errors="ignore")
    enriched = enriched.merge(prompt_metadata, on="id", how="left")

    evaluations = [
        evaluate_response(row.generated_response, row.expected_answer, row.evaluation_type)
        for row in enriched.itertuples(index=False)
    ]
    enriched["is_evaluable"] = [result.is_evaluable for result in evaluations]
    enriched["is_correct"] = [result.is_correct for result in evaluations]
    enriched["evaluation_notes"] = [result.evaluation_notes for result in evaluations]
    return enriched


def _is_missing_expected_answer(expected_answer: Any) -> bool:
    if expected_answer is None:
        return True
    if isinstance(expected_answer, float) and pd.isna(expected_answer):
        return True
    if isinstance(expected_answer, str):
        return expected_answer.strip() == "" or expected_answer.strip().lower() == "nan"
    if isinstance(expected_answer, list):
        return len(expected_answer) == 0
    return False


def _expected_values(expected_answer: Any) -> list[str]:
    if isinstance(expected_answer, list):
        return [str(value) for value in expected_answer]
    if isinstance(expected_answer, str) and expected_answer.strip().startswith("["):
        try:
            import ast

            parsed = ast.literal_eval(expected_answer)
            if isinstance(parsed, list):
                return [str(value) for value in parsed]
        except (ValueError, SyntaxError):
            pass
    return [str(expected_answer)]


def _normalize_text(value: Any) -> str:
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return ""
    text = str(value).lower().strip()
    text = text.replace("’", "'")
    text = re.sub(r"\s+", " ", text)
    text = text.strip(string.punctuation + " ")
    return text


def _extract_yes_no(response: str) -> str:
    tokens = re.findall(r"[a-z]+", response)
    for token in tokens[:12]:
        if token in {"yes", "true"}:
            return "yes"
        if token in {"no", "false"}:
            return "no"
    return ""


def _answer_matches(response: str, expected: str) -> bool:
    return response == expected or bool(expected and expected in response)
