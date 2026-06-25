# GPT-2 Trajectory Summary

## Dataset

- Total prompts: 120
- Categories: abstract_questions, arithmetic, explanations, logic, simple_facts, trick_questions

## Metric Summary

| metric | mean | median | std |
| --- | --- | --- | --- |
| L | 1727.978735 | 2020.601074 | 1178.700358 |
| D | 97.632593 | 70.762524 | 69.243410 |
| C | 29.696583 | 27.865397 | 25.562735 |
| E | 0.993838 | 1.159683 | 0.641011 |
| V | 22.883333 | 31.000000 | 15.870369 |
| candidate_metric_01 | 32.189856 | 26.781960 | 29.848901 |

## Category Separation

One-way ANOVA is used as a first-pass category separation test. Eta squared is included as an effect-size estimate. The exploratory threshold is p < 0.05 and eta_squared >= 0.06.

| metric | anova_f | p_value | eta_squared | meaningful_separation |
| --- | --- | --- | --- | --- |
| L | 1.727387 | 0.133897 | 0.070427 | False |
| D | 1.900973 | 0.099569 | 0.076959 | False |
| C | 1.301301 | 0.268338 | 0.053993 | False |
| E | 1.359911 | 0.244692 | 0.056288 | False |
| V | 1.501400 | 0.194890 | 0.061782 | False |
| candidate_metric_01 | 2.530653 | 0.032728 | 0.099905 | True |

## Validation Verdict

The following current metrics meet the exploratory threshold for category separation: candidate_metric_01. This is evidence for follow-up testing, not proof of invariance.

## Correlations

| metric | candidate_metric_01 | output_token_count | E | generation_time_seconds |
| --- | --- | --- | --- | --- |
| candidate_metric_01 | 1.000000 | 0.304632 | -0.120950 | 0.296141 |
| output_token_count | 0.304632 | 1.000000 | -0.200053 | 0.990302 |
| E | -0.120950 | -0.200053 | 1.000000 | -0.208265 |
| generation_time_seconds | 0.296141 | 0.990302 | -0.208265 | 1.000000 |

## Category-Level Metric Summary

| category | C_mean | C_median | C_std | D_mean | D_median | D_std | E_mean | E_median | E_std | L_mean | L_median | L_std | V_mean | V_median | V_std | candidate_metric_01_mean | candidate_metric_01_median | candidate_metric_01_std |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| abstract_questions | 42.120177 | 43.634136 | 24.661750 | 67.658578 | 54.115520 | 51.960294 | 1.305239 | 1.575935 | 0.623966 | 2027.400807 | 2216.311401 | 1085.889745 | 27.950000 | 34.000000 | 14.336097 | 35.366889 | 30.439991 | 21.563191 |
| arithmetic | 26.045334 | 24.796747 | 21.562240 | 110.132589 | 101.908195 | 60.618617 | 0.976588 | 0.979594 | 0.645115 | 1782.939706 | 1972.951233 | 1155.599032 | 22.400000 | 31.000000 | 14.879870 | 24.798012 | 21.490758 | 15.490954 |
| explanations | 25.367070 | 14.630196 | 31.214840 | 75.155270 | 45.672422 | 70.976593 | 0.992328 | 1.187587 | 0.536046 | 1286.823204 | 860.135040 | 1200.424257 | 18.250000 | 16.500000 | 17.651226 | 27.945757 | 16.448504 | 28.091166 |
| logic | 29.136322 | 24.336459 | 23.212529 | 113.855141 | 98.370590 | 69.952205 | 0.948664 | 1.036057 | 0.593622 | 1950.351288 | 2179.350586 | 1019.024714 | 26.200000 | 31.000000 | 14.277697 | 30.417892 | 26.597569 | 19.142544 |
| simple_facts | 24.957604 | 14.071011 | 26.472787 | 116.238340 | 107.723862 | 78.329500 | 0.808127 | 0.800942 | 0.668804 | 1316.484871 | 1101.630585 | 1183.627623 | 17.450000 | 14.500000 | 17.771873 | 23.316122 | 19.210612 | 17.805447 |
| trick_questions | 30.552993 | 28.860685 | 24.178040 | 102.755640 | 91.279873 | 72.647069 | 0.932078 | 0.968458 | 0.732192 | 2003.872532 | 2129.425293 | 1301.469843 | 25.050000 | 31.500000 | 14.894277 | 51.294467 | 30.146265 | 53.340318 |

## Answer Quality Analysis

Correctness scoring is applied only where `expected_answer` and `evaluation_type` are present. Explanations and abstract questions are excluded for now. These tests ask whether trajectory metrics contain a usable answer-quality signal; they do not prove a new constant.

- Evaluable prompts: 80
- Correct prompts: 3
- Incorrect prompts: 77

### Correct vs Incorrect Metric Summary

| is_correct | metric | mean | median | std | count |
| --- | --- | --- | --- | --- | --- |
| False | L | 1740.031479 | 2016.763672 | 1193.502043 | 77 |
| False | D | 112.958723 | 98.718422 | 69.673854 | 77 |
| False | C | 26.681817 | 24.318699 | 23.241083 | 77 |
| False | E | 0.914136 | 0.948172 | 0.655486 | 77 |
| False | V | 22.350649 | 31.000000 | 15.733610 | 77 |
| False | candidate_metric_01 | 30.325920 | 25.547773 | 28.748400 | 77 |
| True | L | 2363.514689 | 2228.225098 | 436.557625 | 3 |
| True | D | 53.937498 | 34.041618 | 36.906971 | 3 |
| True | C | 53.115039 | 64.345083 | 20.420565 | 3 |
| True | E | 0.973562 | 1.325307 | 0.691177 | 3 |
| True | V | 33.666667 | 35.000000 | 3.214550 | 3 |
| True | candidate_metric_01 | 87.144673 | 49.389229 | 68.901270 | 3 |

### Correctness Separation Tests

| metric | anova_f | p_value | eta_squared | notes |
| --- | --- | --- | --- | --- |
| L | 0.805897 | 0.372099 | 0.010226 | One-way ANOVA across correct vs incorrect answers. |
| D | 2.110983 | 0.150257 | 0.026351 | One-way ANOVA across correct vs incorrect answers. |
| C | 3.757126 | 0.056201 | 0.045955 | One-way ANOVA across correct vs incorrect answers. |
| E | 0.023665 | 0.878138 | 0.000303 | One-way ANOVA across correct vs incorrect answers. |
| V | 1.531287 | 0.219632 | 0.019254 | One-way ANOVA across correct vs incorrect answers. |
| candidate_metric_01 | 10.055935 | 0.002171 | 0.114199 | One-way ANOVA across correct vs incorrect answers. |

### Correctness Correlations

| metric | pearson_correlation_with_correctness |
| --- | --- |
| L | 0.101125 |
| D | -0.162329 |
| C | 0.214371 |
| E | 0.017416 |
| V | 0.138758 |
| candidate_metric_01 | 0.337934 |

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
