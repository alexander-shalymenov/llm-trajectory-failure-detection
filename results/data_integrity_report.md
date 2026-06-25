# Data Integrity Report

Scope: existing result files only. No model was rerun for this integrity check.

## Diagnosis

The blank monitor cells came from genuinely empty or whitespace-only `generated_response` values in the saved model result files, not from lost CSV/JSON rows. The monitor renderer has been fixed to display `[empty generation]` instead of a silent blank.

## Row And Empty Response Summary

| Model | CSV rows | JSON rows | Missing generated_response | Empty generated_response | Zero output_token_count |
|---|---:|---:|---:|---:|---:|
| gpt2 | 120 | 120 | 1 | 1 | 0 |
| distilgpt2 | 120 | 120 | 35 | 35 | 0 |
| tinyllama | 120 | 120 | 72 | 72 | 0 |

## CSV vs JSON Disagreements

### gpt2

- None found for `generated_response`, `output_token_count`, or `is_correct`.

### distilgpt2

- None found for `generated_response`, `output_token_count`, or `is_correct`.

### tinyllama

- None found for `generated_response`, `output_token_count`, or `is_correct`.

## Monitor CSV vs Model Results

### gpt2

- None found. Monitor CSV matches source results, with empty source responses rendered as `[empty generation]`.

### distilgpt2

- None found. Monitor CSV matches source results, with empty source responses rendered as `[empty generation]`.

### tinyllama

- None found. Monitor CSV matches source results, with empty source responses rendered as `[empty generation]`.

## HTML Empty Response Checks

- Full response sections found: 360
- `[empty generation]` Full response sections: 108
- Silent blank Full response sections after fix: 0
- HTML empty response sections where source data has a response: 0

## Genuine Empty Generations

These prompts have empty or whitespace-only `generated_response` in the model result files. They are now shown as `[empty generation]` in the monitor.

### gpt2

- Count: 1
- Prompt IDs: abstract_012

### distilgpt2

- Count: 35
- Prompt IDs: facts_001, facts_002, facts_004, facts_007, facts_008, facts_012, facts_013, facts_015, facts_016, facts_017, arithmetic_010, arithmetic_012, arithmetic_013, arithmetic_016, arithmetic_019, logic_005, logic_012, logic_014, logic_015, explanations_001, explanations_002, explanations_004, explanations_008, explanations_010, explanations_014, explanations_020, abstract_005, abstract_010, abstract_018, abstract_019, trick_002, trick_004, trick_005, trick_013, trick_016

### tinyllama

- Count: 72
- Prompt IDs: facts_001, facts_002, facts_003, facts_004, facts_005, facts_007, facts_008, facts_009, facts_012, facts_013, facts_014, facts_015, facts_016, facts_017, facts_018, facts_019, facts_020, arithmetic_003, arithmetic_004, arithmetic_005, arithmetic_006, arithmetic_008, arithmetic_009, arithmetic_010, arithmetic_011, arithmetic_013, arithmetic_017, arithmetic_018, arithmetic_020, logic_002, logic_004, logic_015, logic_017, logic_019, explanations_001, explanations_002, explanations_003, explanations_004, explanations_005, explanations_006, explanations_007, explanations_008, explanations_010, explanations_011, explanations_012, explanations_013, explanations_015, explanations_016, explanations_017, explanations_018, explanations_019, explanations_020, abstract_002, abstract_003, abstract_004, abstract_005, abstract_006, abstract_007, abstract_008, abstract_009, abstract_010, abstract_011, abstract_013, abstract_015, abstract_020, trick_004, trick_005, trick_010, trick_012, trick_015, trick_017, trick_019

## Per-Prompt Field Coverage

For every model and prompt, the integrity check inspected `prompt_id`, `generated_response`, `output_token_count`, `is_correct`, monitor `risk_status`, and monitor `risk_score`.

## Fix Applied

- `src/trajectory_monitor.py` now converts missing or whitespace-only responses to `[empty generation]` when building `trajectory_monitor.csv` and `trajectory_monitor.html`.
- The model result CSV/JSON files were not modified.
- Full experiments were not rerun.
