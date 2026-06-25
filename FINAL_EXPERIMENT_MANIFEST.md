# Final Experiment Manifest

## Reset Confirmation

- Old generated junk was permanently deleted from `C:\xampp\htdocs\Projects\cognitive-geometry-lab`.
- No backup folders were created.
- No archive folders were created.
- Nothing was moved outside the project folder.
- The cleanup did not touch:
  - `C:\Models\GPT4All`
  - `C:\Models\HuggingFace`
  - `C:\Users\Slon54\.cache\huggingface`

## Clean Project Contents

The project now keeps only the source files and fresh experiment outputs needed for this run:

```text
README.md
requirements.txt
run_experiment.py
FINAL_EXPERIMENT_MANIFEST.md
datasets/prompts_clean.json
docs/
scripts/
src/
results/
```

Removed from the active project:

```text
github_release/
old results/
old reports
old dashboards
old charts
old CSV/JSON outputs
partial files
GGUF code and outputs
raw_internal_data.npz
__pycache__/
temporary files
archive or backup folders
```

## Fresh Prompt Dataset

The experiment used only:

```text
datasets/prompts_clean.json
```

Prompt counts:

```text
simple_facts: 20
arithmetic: 20
logic: 20
explanations: 20
abstract_questions: 20
trick_questions: 20
total: 120
```

Evaluable prompt categories include `expected_answer` and `evaluation_type`.

## Exact Commands Used

The model runs were executed from:

```text
C:\xampp\htdocs\Projects\cognitive-geometry-lab
```

The process environment used the local Hugging Face cache path:

```powershell
$env:HF_HOME='C:\Models\HuggingFace'
$env:TRANSFORMERS_OFFLINE='1'
$env:HF_HUB_OFFLINE='1'
```

Fresh model runs:

```powershell
python run_experiment.py --prompts-path datasets/prompts_clean.json --model-name gpt2 --output-dir results/gpt2
python run_experiment.py --prompts-path datasets/prompts_clean.json --model-name distilgpt2 --output-dir results/distilgpt2
python run_experiment.py --prompts-path datasets/prompts_clean.json --model-name TinyLlama/TinyLlama-1.1B-Chat-v1.0 --output-dir results/tinyllama
```

Fresh reports:

```powershell
python run_experiment.py --compare-models results/gpt2 results/distilgpt2 results/tinyllama
python run_experiment.py --diagnostic-signals results/gpt2 results/distilgpt2 results/tinyllama
python run_experiment.py --trajectory-monitor results/gpt2 results/distilgpt2 results/tinyllama
```

## Fresh Results

`results/` contains only the new clean experiment:

```text
results/gpt2/
results/distilgpt2/
results/tinyllama/
results/model_comparison_report.md
results/diagnostic_signal_report.md
results/trajectory_monitor.html
results/trajectory_monitor.csv
```

Each model folder contains the fresh CSV/JSON outputs, summary report, trajectory structure report, analysis log, and generated charts for that model.

Raw tensor archives were removed after report generation:

```text
results/*/raw_internal_data.npz
```

## Main Result Summary

Fresh run row counts:

```text
gpt2: 120 rows
distilgpt2: 120 rows
tinyllama: 120 rows
trajectory_monitor.csv: 120 prompt-comparison rows
```

Mean sensor metrics:

```text
gpt2:       L=6102.5665, E=1.4084, trajectory_loop_score=29.6333
distilgpt2: L=1727.9787, E=0.9938, trajectory_loop_score=10.8167
tinyllama:  L=1242.7212, E=0.9181, trajectory_loop_score=1.5750
```

Prompt comparison monitor:

```text
risk status disagreements: 114
correctness disagreements: 17
highest-risk model counts: gpt2=114, distilgpt2=6, tinyllama=0
```

The regenerated `trajectory_monitor.html` uses prompt-level comparison tables with model columns:

```text
GPT-2 | DistilGPT2 | TinyLlama
```

No empty comparison table was published.

## Data Integrity Follow-Up

Data integrity check completed and monitor blank-response issue fixed.

- Report: `results/data_integrity_report.md`
- The model result CSV/JSON files were inspected without rerunning GPT-2, DistilGPT2, or TinyLlama.
- Empty or whitespace-only model generations are now shown as `[empty generation]` in `trajectory_monitor.csv` and `trajectory_monitor.html`.
- No silent blank Full response sections remain in the monitor.

## Final Project Direction

The final project direction is **LLM Trajectory Failure Detection**.

A confirmation round was run with the same dataset, same models, same metric formulas, and same generation settings. No new prompts, models, GGUF runs, or trajectory metrics were added.

Confirmation outputs:

```text
results/confirmation/gpt2/
results/confirmation/distilgpt2/
results/confirmation/tinyllama/
results/final_trajectory_failure_detection_conclusion.md
results/confirmation_summary.csv
results/confirmation_metric_stability.csv
results/confirmation_failure_summary.csv
```

Final conclusion:

- Trajectory signals can flag abnormal path behavior directly.
- Trajectory signals showed useful signal for repetition-like generation failures in this confirmation run.
- Empty generation is not reliably flagged by trajectory geometry alone and must be caught by an explicit output-integrity check.
- The recommended failure-detection layer combines trajectory signals with simple output checks for empty generation and obvious repetition.

## Publication Polish Pass

The experiment is finished. A publication-only polish pass was completed without rerunning experiments, regenerating reports, changing prompts, changing metrics, or modifying model outputs.

Edited files:

- `README.md`
- `results/trajectory_monitor.html`
- `FINAL_EXPERIMENT_MANIFEST.md`

The final public framing is **LLM Trajectory Failure Detection**.
