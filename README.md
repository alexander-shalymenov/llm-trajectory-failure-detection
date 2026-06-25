# LLM Trajectory Failure Detection

This repository contains an exploratory research prototype for studying whether internal generation trajectories in causal language models can provide additional diagnostic signals for generation quality. The project compares trajectory behaviour across GPT-2, DistilGPT2, and TinyLlama on a small controlled prompt set, with particular attention to abnormal path behaviour, repetition-like outputs, and empty generation.

[Open trajectory monitor](https://alexander-shalymenov.github.io/llm-trajectory-failure-detection/results/trajectory_monitor.html)

## Motivation

Language-model outputs can fail in ways that are not fully captured by surface text alone. A response may be repetitive, empty, unstable, or produced through unusual internal dynamics. This project investigates whether measurements taken from hidden-state trajectories during generation can help surface such cases for review.

## Research Question

Can trajectory-based signals from internal model states help identify generation failures or abnormal generation behaviour in open causal language models?

## Scope

This project does:

- Run a fixed prompt dataset through selected Hugging Face causal language models.
- Capture generated text, token-level entropy, logits, hidden states, timing, and trajectory measurements.
- Compute trajectory and trajectory-structure metrics without fine-tuning.
- Compare prompt-level behaviour across multiple models.
- Produce reports and a standalone HTML monitor for reviewing possible generation failures.

This project does not:

- Claim that trajectory metrics determine correctness.
- Replace output-based evaluation or human review.
- Fine-tune models.
- Use GGUF models in the final experiment.
- Introduce a production safety system.
- Make claims beyond the observed experiments.

## Models

The final experiment uses:

- `gpt2`
- `distilgpt2`
- `TinyLlama/TinyLlama-1.1B-Chat-v1.0`

All models are run through Hugging Face `AutoTokenizer` and `AutoModelForCausalLM`.

## Dataset

The experiment uses:

```text
datasets/prompts_clean.json
```

The dataset contains 120 short prompts across six balanced categories:

- 20 `simple_facts`
- 20 `arithmetic`
- 20 `logic`
- 20 `explanations`
- 20 `abstract_questions`
- 20 `trick_questions`

Prompts in evaluable categories include `expected_answer` and `evaluation_type` fields where simple answer checks are appropriate.

## Method

For each model and prompt, the experiment:

1. Loads the model and tokenizer from Hugging Face.
2. Generates a response using the same prompt set.
3. Records the generated text, generated tokens, output token count, and generation time.
4. Captures logits and hidden states during generation.
5. Computes token entropy from the generation distribution.
6. Measures trajectory geometry through the final-layer hidden states.
7. Computes trajectory-structure features from the hidden-state path.
8. Saves per-model results to CSV and JSON.
9. Runs statistical summaries, cross-model comparisons, and diagnostic signal analysis.
10. Builds a prompt-level HTML monitor comparing model responses side by side.

## Trajectory Metrics

The core trajectory metrics are:

- `L`: path length through last-layer hidden states.
- `D`: direct distance from the first to the last hidden state.
- `C`: curvature ratio, computed as `L / D`.
- `E`: mean token entropy.
- `V`: number of sharp direction changes.
- `candidate_metric_01`: computed as `L / (D * E)`.

Additional trajectory-structure features include:

- `path_efficiency`: direct distance divided by path length.
- `curvature_density`: sharp direction changes per unit path length.
- `entropy_per_step`: mean entropy divided by output token count.
- `trajectory_compression`: direct distance divided by output token count.
- `trajectory_expansion`: path length divided by output token count.
- `hidden_state_dispersion`: average distance from the trajectory centroid.
- `hidden_state_radius`: maximum distance from the trajectory centroid.
- `trajectory_self_similarity`: similarity between the first and second halves of the trajectory.
- `trajectory_loop_score`: count of approximate returns to previously visited hidden-state regions.

The monitor emphasizes `trajectory_loop_score`, `L`, and `entropy_per_step` as practical sensor metrics.

## Failure Categories

The project focuses on several observable failure categories:

- Empty or whitespace-only generation.
- Repetition-like output loops.
- Abnormal trajectory path behaviour.
- High review-risk trajectory patterns within the observed experiment.
- Correctness disagreement where simple expected-answer checks are available.

Empty generation is treated as an output-integrity issue. It is explicitly displayed as `[empty generation]` in the monitor instead of being left blank.

## Main Findings

In this study, trajectory signals provided useful diagnostic information about some abnormal generation behaviour.

The observed results suggest that trajectory measurements can help identify unusual path behaviour and some repetition-like outputs. The experiments indicate that these signals are most useful as review indicators rather than correctness judgments.

The experiments also indicate that empty generation is not reliably captured by trajectory geometry alone. Empty or whitespace-only responses require explicit output-integrity checks.

Overall, the results support using trajectory signals as one diagnostic layer, combined with output checks and downstream evaluation.

## Limitations

- The dataset is small and intentionally controlled.
- The models are limited to three open causal language models.
- The monitor labels are diagnostic review labels, not truth labels.
- Repetition-like detection uses output-side heuristics for validation.
- Empty generation requires explicit output validation.
- The findings should be tested on larger datasets, additional models, and task-specific failure labels.

## Repository Structure

```text
README.md
requirements.txt
run_experiment.py
datasets/
docs/
scripts/
src/
results/
FINAL_EXPERIMENT_MANIFEST.md
```

Key files:

- `datasets/prompts_clean.json`: final prompt dataset.
- `src/model_runner.py`: Hugging Face model loading and generation.
- `src/experiment.py`: experiment orchestration.
- `src/metrics.py`: core trajectory metric formulas.
- `src/trajectory_structure.py`: trajectory-structure analysis.
- `src/trajectory_monitor.py`: prompt-level dashboard generation.
- `src/diagnostic_signals.py`: diagnostic signal analysis.
- `src/model_comparison.py`: cross-model comparison.
- `run_experiment.py`: command-line entry point.

## Running the Experiment

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the three model experiments:

```bash
python run_experiment.py --prompts-path datasets/prompts_clean.json --model-name gpt2 --output-dir results/gpt2
python run_experiment.py --prompts-path datasets/prompts_clean.json --model-name distilgpt2 --output-dir results/distilgpt2
python run_experiment.py --prompts-path datasets/prompts_clean.json --model-name TinyLlama/TinyLlama-1.1B-Chat-v1.0 --output-dir results/tinyllama
```

Generate comparison reports and the monitor:

```bash
python run_experiment.py --compare-models results/gpt2 results/distilgpt2 results/tinyllama
python run_experiment.py --diagnostic-signals results/gpt2 results/distilgpt2 results/tinyllama
python run_experiment.py --trajectory-monitor results/gpt2 results/distilgpt2 results/tinyllama
```

## Outputs

Primary outputs include:

- `results/gpt2/results.csv`
- `results/distilgpt2/results.csv`
- `results/tinyllama/results.csv`
- `results/model_comparison_report.md`
- `results/diagnostic_signal_report.md`
- `results/data_integrity_report.md`
- `results/final_trajectory_failure_detection_conclusion.md`
- `results/trajectory_monitor.csv`
- `results/trajectory_monitor.html`

The HTML monitor is standalone and compares the same prompt across all three models.

## Reproducibility

The final experiment uses a fixed prompt file, fixed model list, and explicit output folders. The confirmation round repeats the same dataset, models, metrics, and command pattern under `results/confirmation/`.

For local Hugging Face caching, set:

```powershell
$env:HF_HOME="C:\Models\HuggingFace"
```

The experiment does not require fine-tuning.

## Final Conclusion

This project contributes an exploratory framework for studying internal trajectory behaviour as an additional diagnostic signal for language-model generation quality.

Trajectory signals may help identify some abnormal generation behaviour, including unusual path dynamics and repetition-like outputs. They are not sufficient on their own. In this study, the most useful diagnostic framing combined trajectory signals with output-integrity checks, especially for empty or whitespace-only generation.
