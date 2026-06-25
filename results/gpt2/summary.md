# GPT-2 Trajectory Summary

## Dataset

- Total prompts: 120
- Categories: abstract_questions, arithmetic, explanations, logic, simple_facts, trick_questions

## Metric Summary

| metric | mean | median | std |
| --- | --- | --- | --- |
| L | 6102.566486 | 5278.009033 | 2931.477893 |
| D | 142.135542 | 89.178352 | 125.995342 |
| C | 64.497721 | 60.966337 | 39.618247 |
| E | 1.408357 | 1.493317 | 0.364586 |
| V | 33.541667 | 33.500000 | 4.453109 |
| candidate_metric_01 | 51.971158 | 41.649037 | 44.866512 |

## Category Separation

One-way ANOVA is used as a first-pass category separation test. Eta squared is included as an effect-size estimate. The exploratory threshold is p < 0.05 and eta_squared >= 0.06.

| metric | anova_f | p_value | eta_squared | meaningful_separation |
| --- | --- | --- | --- | --- |
| L | 7.088321 | 0.000008 | 0.237160 | True |
| D | 2.286525 | 0.050661 | 0.091146 | False |
| C | 0.488010 | 0.784627 | 0.020955 | False |
| E | 6.421122 | 0.000027 | 0.219742 | True |
| V | 0.368587 | 0.869208 | 0.015909 | False |
| candidate_metric_01 | 1.792060 | 0.119991 | 0.072872 | False |

## Validation Verdict

The following current metrics meet the exploratory threshold for category separation: L, E. This is evidence for follow-up testing, not proof of invariance.

## Correlations

| metric | candidate_metric_01 | output_token_count | E | generation_time_seconds |
| --- | --- | --- | --- | --- |
| candidate_metric_01 | 1.000000 | 0.106631 | -0.536095 | 0.075220 |
| output_token_count | 0.106631 | 1.000000 | 0.059278 | 0.936482 |
| E | -0.536095 | 0.059278 | 1.000000 | 0.054018 |
| generation_time_seconds | 0.075220 | 0.936482 | 0.054018 | 1.000000 |

## Category-Level Metric Summary

| category | C_mean | C_median | C_std | D_mean | D_median | D_std | E_mean | E_median | E_std | L_mean | L_median | L_std | V_mean | V_median | V_std | candidate_metric_01_mean | candidate_metric_01_median | candidate_metric_01_std |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| abstract_questions | 58.676318 | 64.457870 | 30.673978 | 113.191697 | 68.317993 | 122.060523 | 1.579142 | 1.659813 | 0.261409 | 4674.042346 | 4830.425537 | 1636.389192 | 32.900000 | 35.000000 | 8.181494 | 37.685601 | 42.315882 | 21.155391 |
| arithmetic | 54.931204 | 44.553870 | 35.524643 | 223.501824 | 200.379509 | 131.857826 | 1.084977 | 1.305792 | 0.418876 | 9059.734399 | 7725.911377 | 4736.890923 | 33.550000 | 33.500000 | 3.017057 | 71.559733 | 48.105020 | 68.337255 |
| explanations | 68.416455 | 56.080032 | 43.012575 | 130.892522 | 80.681152 | 147.498836 | 1.535327 | 1.526963 | 0.202799 | 5504.669312 | 5357.245605 | 1709.085872 | 34.600000 | 34.500000 | 2.909151 | 45.003290 | 35.788833 | 30.367721 |
| logic | 69.478899 | 70.954098 | 42.459915 | 135.769239 | 81.523521 | 109.098482 | 1.303789 | 1.497713 | 0.430590 | 6447.910571 | 6012.997314 | 2851.996887 | 33.000000 | 32.500000 | 2.790963 | 65.032317 | 49.750694 | 61.836075 |
| simple_facts | 65.610648 | 63.654316 | 39.332227 | 138.477458 | 68.544807 | 134.760307 | 1.425917 | 1.484611 | 0.260966 | 5622.530920 | 5152.569580 | 1710.596600 | 33.750000 | 33.500000 | 3.905125 | 46.957414 | 38.341037 | 32.819870 |
| trick_questions | 69.872804 | 52.229511 | 47.136375 | 110.980514 | 87.115799 | 79.121901 | 1.520989 | 1.599012 | 0.333388 | 5306.511365 | 4993.373535 | 1400.462927 | 33.450000 | 33.500000 | 3.831655 | 45.588592 | 40.327673 | 27.357653 |

## Answer Quality Analysis

Correctness scoring is applied only where `expected_answer` and `evaluation_type` are present. Explanations and abstract questions are excluded for now. These tests ask whether trajectory metrics contain a usable answer-quality signal; they do not prove a new constant.

- Evaluable prompts: 80
- Correct prompts: 8
- Incorrect prompts: 72

### Correct vs Incorrect Metric Summary

| is_correct | metric | mean | median | std | count |
| --- | --- | --- | --- | --- | --- |
| False | L | 6657.853590 | 5494.716064 | 3429.723587 | 72 |
| False | D | 147.826134 | 95.163837 | 120.426557 | 72 |
| False | C | 66.616816 | 64.417433 | 41.343606 | 72 |
| False | E | 1.346282 | 1.464288 | 0.401054 | 72 |
| False | V | 33.527778 | 33.000000 | 3.241336 | 72 |
| False | candidate_metric_01 | 58.472285 | 45.660078 | 52.252254 | 72 |
| True | L | 6171.035828 | 6591.067627 | 1246.884102 | 8 |
| True | D | 191.387385 | 170.007385 | 131.997538 | 8 |
| True | C | 50.182545 | 34.940022 | 36.736641 | 8 |
| True | E | 1.222645 | 1.234633 | 0.350307 | 8 |
| True | V | 32.625000 | 32.500000 | 4.533605 | 8 |
| True | candidate_metric_01 | 46.594580 | 33.014137 | 40.256662 | 8 |

### Correctness Separation Tests

| metric | anova_f | p_value | eta_squared | notes |
| --- | --- | --- | --- | --- |
| L | 0.157312 | 0.692727 | 0.002013 | One-way ANOVA across correct vs incorrect answers. |
| D | 0.925357 | 0.339045 | 0.011724 | One-way ANOVA across correct vs incorrect answers. |
| C | 1.159571 | 0.284874 | 0.014649 | One-way ANOVA across correct vs incorrect answers. |
| E | 0.699137 | 0.405628 | 0.008884 | One-way ANOVA across correct vs incorrect answers. |
| V | 0.514383 | 0.475390 | 0.006551 | One-way ANOVA across correct vs incorrect answers. |
| candidate_metric_01 | 0.386122 | 0.536157 | 0.004926 | One-way ANOVA across correct vs incorrect answers. |

### Correctness Correlations

| metric | pearson_correlation_with_correctness |
| --- | --- |
| L | -0.044864 |
| D | 0.108280 |
| C | -0.121031 |
| E | -0.094253 |
| V | -0.080941 |
| candidate_metric_01 | -0.070185 |

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
