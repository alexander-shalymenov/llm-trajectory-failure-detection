# Final Conclusion: LLM Trajectory Failure Detection

This confirmation round used the same dataset, same models, same metric formulas, and same generation settings as the fresh run. No GGUF models, new prompts, new models, or new trajectory metrics were introduced.

## Confirmation Commands

```powershell
python run_experiment.py --prompts-path datasets/prompts_clean.json --model-name gpt2 --output-dir results/confirmation/gpt2
python run_experiment.py --prompts-path datasets/prompts_clean.json --model-name distilgpt2 --output-dir results/confirmation/distilgpt2
python run_experiment.py --prompts-path datasets/prompts_clean.json --model-name TinyLlama/TinyLlama-1.1B-Chat-v1.0 --output-dir results/confirmation/tinyllama
python run_experiment.py --compare-models results/confirmation/gpt2 results/confirmation/distilgpt2 results/confirmation/tinyllama
python run_experiment.py --diagnostic-signals results/confirmation/gpt2 results/confirmation/distilgpt2 results/confirmation/tinyllama
python run_experiment.py --trajectory-monitor results/confirmation/gpt2 results/confirmation/distilgpt2 results/confirmation/tinyllama
```

## Original vs Confirmation Summary

| Run | Model | Rows | Empty generations | Repetition-like outputs | Review/unstable | Unstable | Mean risk | Mean L | Mean loop score | Mean entropy/step |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| original | gpt2 | 120 | 1 | 56 | 112 | 52 | 0.3434 | 6102.5665 | 29.6333 | 0.038917 |
| original | distilgpt2 | 120 | 35 | 44 | 23 | 2 | 0.1330 | 1727.9787 | 10.8167 | 0.111324 |
| original | tinyllama | 120 | 72 | 7 | 9 | 0 | 0.1269 | 1242.7212 | 1.5750 | 0.546176 |
| confirmation | gpt2 | 120 | 1 | 56 | 112 | 52 | 0.3434 | 6102.5665 | 29.6333 | 0.038917 |
| confirmation | distilgpt2 | 120 | 35 | 44 | 23 | 2 | 0.1330 | 1727.9787 | 10.8167 | 0.111324 |
| confirmation | tinyllama | 120 | 72 | 7 | 9 | 0 | 0.1269 | 1242.7212 | 1.5750 | 0.546176 |

## Run-to-Run Agreement

| Model | Empty generation label agreement | Repetition-like label agreement | Exact response match |
|---|---:|---:|---:|
| gpt2 | 100.0% | 100.0% | 100.0% |
| distilgpt2 | 100.0% | 100.0% | 100.0% |
| tinyllama | 100.0% | 100.0% | 100.0% |

## Existing Trajectory Signal Stability

| Model | Metric | Original-confirmation correlation | Mean absolute delta |
|---|---|---:|---:|
| gpt2 | L | 1.0000 | 0.000000 |
| gpt2 | trajectory_loop_score | 1.0000 | 0.000000 |
| gpt2 | entropy_per_step | 1.0000 | 0.000000 |
| distilgpt2 | L | 1.0000 | 0.000000 |
| distilgpt2 | trajectory_loop_score | 1.0000 | 0.000000 |
| distilgpt2 | entropy_per_step | 1.0000 | 0.000000 |
| tinyllama | L | 1.0000 | 0.000000 |
| tinyllama | trajectory_loop_score | 1.0000 | 0.000000 |
| tinyllama | entropy_per_step | 1.0000 | 0.000000 |

## Failure Labels vs Trajectory Risk

Failure labels here are output-side diagnostic labels used only for validation: empty generation means blank or whitespace-only decoded output; repetition-like means obvious repeated word/phrase loops. They are not new trajectory metrics.

| Run | Failure label | Count | Mean risk failed | Mean risk not failed | Failed review/unstable | Non-failed review/unstable |
|---|---|---:|---:|---:|---:|---:|
| original | empty_generation | 108 | 0.1201 | 0.2358 | 13.0% | 51.6% |
| original | repetition_like | 107 | 0.2844 | 0.1659 | 63.6% | 30.0% |
| confirmation | empty_generation | 108 | 0.1201 | 0.2358 | 13.0% | 51.6% |
| confirmation | repetition_like | 107 | 0.2844 | 0.1659 | 63.6% | 30.0% |

## Final Answer

Partially, with an important boundary. The existing trajectory signals can flag abnormal path behavior directly, because the monitor is built from `trajectory_loop_score`, `L`, and `entropy_per_step`. They also show useful signal for repetition-like outputs in this run: repetition-like generations had higher mean trajectory risk and a higher review/unstable rate than non-repetition outputs.

Empty generation is different. The confirmation data shows that empty or whitespace-only decoded responses are not reliably high-risk under the trajectory sensors alone. Across the combined model outputs, empty generations had lower mean trajectory risk than non-empty generations and were less often marked review/unstable. So empty generation must be caught by an explicit output-integrity guard, not by trajectory geometry alone. The monitor now does this by rendering `[empty generation]` instead of a silent blank.

The final conclusion is diagnostic, not theoretical: trajectory signals are useful as one failure-detection layer, especially for abnormal path behavior and repetition-like loops, but robust LLM failure detection should combine trajectory signals with simple output checks for empty generation and obvious repetition. These signals should route answers to review, self-check, or stronger-model fallback; they should not be treated as proof that an answer is wrong or that a universal law has been found.

Final project direction: **LLM Trajectory Failure Detection**.
