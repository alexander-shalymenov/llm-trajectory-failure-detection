# GPT-2 Trajectory Summary

## Dataset

- Total prompts: 120
- Categories: abstract_questions, arithmetic, explanations, logic, simple_facts, trick_questions

## Metric Summary

| metric | mean | median | std |
| --- | --- | --- | --- |
| L | 1242.721245 | 0.000000 | 1726.026154 |
| D | 34.327529 | 0.000000 | 44.778338 |
| C | 14.234906 | 0.000000 | 18.839152 |
| E | 0.918119 | 0.900313 | 0.332323 |
| V | 13.741667 | 0.000000 | 19.175657 |
| candidate_metric_01 | 17.126802 | 0.000000 | 26.513134 |

## Category Separation

One-way ANOVA is used as a first-pass category separation test. Eta squared is included as an effect-size estimate. The exploratory threshold is p < 0.05 and eta_squared >= 0.06.

| metric | anova_f | p_value | eta_squared | meaningful_separation |
| --- | --- | --- | --- | --- |
| L | 6.208567 | 0.000040 | 0.214025 | True |
| D | 6.611079 | 0.000019 | 0.224782 | True |
| C | 6.738414 | 0.000015 | 0.228124 | True |
| E | 7.932479 | 0.000002 | 0.258114 | True |
| V | 6.280218 | 0.000035 | 0.215962 | True |
| candidate_metric_01 | 4.192387 | 0.001557 | 0.155317 | True |

## Validation Verdict

The following current metrics meet the exploratory threshold for category separation: L, D, C, E, V, candidate_metric_01. This is evidence for follow-up testing, not proof of invariance.

## Correlations

| metric | candidate_metric_01 | output_token_count | E | generation_time_seconds |
| --- | --- | --- | --- | --- |
| candidate_metric_01 | 1.000000 | 0.830038 | -0.170477 | 0.828984 |
| output_token_count | 0.830038 | 1.000000 | 0.065271 | 0.999731 |
| E | -0.170477 | 0.065271 | 1.000000 | 0.067633 |
| generation_time_seconds | 0.828984 | 0.999731 | 0.067633 | 1.000000 |

## Category-Level Metric Summary

| category | C_mean | C_median | C_std | D_mean | D_median | D_std | E_mean | E_median | E_std | L_mean | L_median | L_std | V_mean | V_median | V_std | candidate_metric_01_mean | candidate_metric_01_median | candidate_metric_01_std |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| abstract_questions | 11.831236 | 0.000000 | 17.216694 | 28.259380 | 0.000000 | 43.093599 | 1.128042 | 1.187749 | 0.362592 | 1014.076224 | 0.000000 | 1653.944620 | 11.150000 | 0.000000 | 18.397011 | 9.868047 | 0.000000 | 14.781093 |
| arithmetic | 12.913526 | 0.000000 | 18.821566 | 34.620947 | 0.000000 | 44.478961 | 0.852945 | 0.876156 | 0.266359 | 1133.503363 | 0.000000 | 1691.100970 | 12.950000 | 0.000000 | 19.586448 | 23.837272 | 0.000000 | 41.359910 |
| explanations | 3.457200 | 0.000000 | 10.649764 | 8.449178 | 0.000000 | 28.204389 | 0.720812 | 0.726256 | 0.188989 | 296.575043 | 0.000000 | 1002.262223 | 3.200000 | 0.000000 | 10.846295 | 3.368249 | 0.000000 | 10.501057 |
| logic | 27.796626 | 35.382494 | 16.767181 | 64.399951 | 73.009037 | 43.914220 | 1.057619 | 0.999608 | 0.347112 | 2374.398273 | 2765.918823 | 1607.816135 | 27.050000 | 30.500000 | 18.474663 | 31.656856 | 35.533059 | 22.187016 |
| simple_facts | 5.386318 | 0.000000 | 13.323327 | 11.992896 | 0.000000 | 30.119336 | 0.702712 | 0.648668 | 0.320436 | 440.785535 | 0.000000 | 1153.490223 | 4.650000 | 0.000000 | 12.166715 | 8.313051 | 0.000000 | 21.826812 |
| trick_questions | 24.024533 | 24.206915 | 22.204856 | 58.242824 | 68.165894 | 47.632230 | 1.046586 | 0.968026 | 0.227720 | 2196.989032 | 1946.190308 | 2037.153966 | 23.450000 | 21.500000 | 21.830628 | 25.717335 | 23.548269 | 26.660551 |

## Answer Quality Analysis

Correctness scoring is applied only where `expected_answer` and `evaluation_type` are present. Explanations and abstract questions are excluded for now. These tests ask whether trajectory metrics contain a usable answer-quality signal; they do not prove a new constant.

- Evaluable prompts: 80
- Correct prompts: 9
- Incorrect prompts: 71

### Correct vs Incorrect Metric Summary

| is_correct | metric | mean | median | std | count |
| --- | --- | --- | --- | --- | --- |
| False | L | 1318.570799 | 0.000000 | 1769.723491 | 71 |
| False | D | 36.307502 | 0.000000 | 44.959740 | 71 |
| False | C | 15.178183 | 0.000000 | 19.811438 | 71 |
| False | E | 0.931140 | 0.929996 | 0.335148 | 71 |
| False | V | 14.563380 | 0.000000 | 19.676478 | 71 |
| False | candidate_metric_01 | 18.950806 | 0.000000 | 29.369644 | 71 |
| True | L | 3254.999702 | 3584.536865 | 1026.147993 | 9 |
| True | D | 89.699966 | 100.131226 | 24.260220 | 9 |
| True | C | 36.085452 | 36.370210 | 4.670093 | 9 |
| True | E | 0.787367 | 0.808549 | 0.186107 | 9 |
| True | V | 36.444444 | 43.000000 | 10.875559 | 9 |
| True | candidate_metric_01 | 49.442560 | 44.982050 | 17.850935 | 9 |

### Correctness Separation Tests

| metric | anova_f | p_value | eta_squared | notes |
| --- | --- | --- | --- | --- |
| L | 10.261836 | 0.001967 | 0.116266 | One-way ANOVA across correct vs incorrect answers. |
| D | 12.147960 | 0.000810 | 0.134756 | One-way ANOVA across correct vs incorrect answers. |
| C | 9.849650 | 0.002398 | 0.112119 | One-way ANOVA across correct vs incorrect answers. |
| E | 1.582148 | 0.212204 | 0.019881 | One-way ANOVA across correct vs incorrect answers. |
| V | 10.635191 | 0.001647 | 0.119988 | One-way ANOVA across correct vs incorrect answers. |
| candidate_metric_01 | 9.204825 | 0.003278 | 0.105554 | One-way ANOVA across correct vs incorrect answers. |

### Correctness Correlations

| metric | pearson_correlation_with_correctness |
| --- | --- |
| L | 0.340978 |
| D | 0.367091 |
| C | 0.334842 |
| E | -0.140999 |
| V | 0.346393 |
| candidate_metric_01 | 0.324891 |

## Charts

- `results/charts/metric_vs_prompt_category.png`
- `results/charts/entropy_vs_curvature.png`
- `results/charts/output_length_vs_candidate_metric_01.png`
- `results/charts/correlation_heatmap.png`
- `results/charts/boxplot_<metric>.png`
- `results/charts/histogram_<metric>.png`
- `results/charts/candidate_metric_01_by_correctness.png`
- `results/charts/E_by_correctness.png`
- `results/charts/L_by_correctness.png`
