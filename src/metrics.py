from __future__ import annotations

from dataclasses import dataclass

import numpy as np


EPSILON = 1e-12


@dataclass(frozen=True)
class TrajectoryMetrics:
    L: float
    D: float
    C: float
    E: float
    V: int
    candidate_metric_01: float


def token_entropy_from_logits(logits: np.ndarray) -> np.ndarray:
    """Compute entropy for each generated-token logit vector."""
    if logits.size == 0:
        return np.array([], dtype=np.float64)

    shifted = logits - np.max(logits, axis=-1, keepdims=True)
    exp_logits = np.exp(shifted)
    probs = exp_logits / np.sum(exp_logits, axis=-1, keepdims=True)
    log_probs = np.log(probs + EPSILON)
    return -np.sum(probs * log_probs, axis=-1)


def path_length(hidden_states: np.ndarray) -> float:
    if len(hidden_states) < 2:
        return 0.0
    step_vectors = np.diff(hidden_states, axis=0)
    return float(np.linalg.norm(step_vectors, axis=1).sum())


def direct_distance(hidden_states: np.ndarray) -> float:
    if len(hidden_states) < 2:
        return 0.0
    return float(np.linalg.norm(hidden_states[-1] - hidden_states[0]))


def sharp_direction_changes(hidden_states: np.ndarray, angle_threshold_degrees: float = 90.0) -> int:
    if len(hidden_states) < 3:
        return 0

    vectors = np.diff(hidden_states, axis=0)
    norms = np.linalg.norm(vectors, axis=1)
    valid_pairs = (norms[:-1] > EPSILON) & (norms[1:] > EPSILON)
    if not np.any(valid_pairs):
        return 0

    dots = np.sum(vectors[:-1] * vectors[1:], axis=1)
    cosines = np.zeros_like(dots)
    cosines[valid_pairs] = dots[valid_pairs] / (norms[:-1][valid_pairs] * norms[1:][valid_pairs])
    cosines = np.clip(cosines, -1.0, 1.0)
    angles = np.degrees(np.arccos(cosines[valid_pairs]))
    return int(np.sum(angles >= angle_threshold_degrees))


def compute_trajectory_metrics(
    hidden_states: np.ndarray,
    token_entropy: np.ndarray,
    angle_threshold_degrees: float = 90.0,
) -> TrajectoryMetrics:
    L = path_length(hidden_states)
    D = direct_distance(hidden_states)
    C = float(L / max(D, EPSILON))
    E = float(np.mean(token_entropy)) if token_entropy.size else 0.0
    V = sharp_direction_changes(hidden_states, angle_threshold_degrees=angle_threshold_degrees)
    candidate_metric_01 = float(L / max(D * E, EPSILON))
    return TrajectoryMetrics(L=L, D=D, C=C, E=E, V=V, candidate_metric_01=candidate_metric_01)
