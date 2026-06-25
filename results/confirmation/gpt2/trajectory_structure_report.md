# Trajectory Structure Report

## Goal

Identify whether different task categories produce different internal trajectory geometries. Existing trajectory metric formulas are not modified here.

## Dataset

- Total prompts: 120
- Categories: abstract_questions, arithmetic, explanations, logic, simple_facts, trick_questions

## Category Means

| category | path_efficiency | curvature_density | entropy_per_step | trajectory_compression | trajectory_expansion | hidden_state_dispersion | hidden_state_radius | trajectory_self_similarity | trajectory_loop_score |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| abstract_questions | 0.023258 | 0.007034 | 0.090355 | 2.358160 | 97.375882 | 71.179536 | 334.281345 | -0.052576 | 29.450000 |
| arithmetic | 0.030318 | 0.004553 | 0.022604 | 4.656288 | 188.744467 | 139.144078 | 445.219876 | -0.037678 | 33.000000 |
| explanations | 0.023813 | 0.006820 | 0.031986 | 2.726928 | 114.680611 | 83.827231 | 402.485755 | -0.052386 | 26.300000 |
| logic | 0.021633 | 0.005908 | 0.027162 | 2.828526 | 134.331470 | 101.305119 | 393.229515 | 0.044157 | 31.200000 |
| simple_facts | 0.022819 | 0.006669 | 0.029707 | 2.884947 | 117.136061 | 87.996958 | 373.018207 | -0.004229 | 29.400000 |
| trick_questions | 0.020363 | 0.006602 | 0.031687 | 2.312094 | 110.552320 | 83.860750 | 411.585869 | -0.049814 | 28.450000 |

## Category ANOVA

| metric | anova_f | p_value | eta_squared |
| --- | --- | --- | --- |
| path_efficiency | 0.637192 | 0.671751 | 0.027187 |
| curvature_density | 3.878739 | 0.002774 | 0.145387 |
| entropy_per_step | 1.189372 | 0.318823 | 0.049579 |
| trajectory_compression | 2.286525 | 0.050661 | 0.091146 |
| trajectory_expansion | 7.088321 | 0.000008 | 0.237160 |
| hidden_state_dispersion | 7.538415 | 0.000004 | 0.248478 |
| hidden_state_radius | 1.626509 | 0.158576 | 0.066588 |
| trajectory_self_similarity | 0.600331 | 0.699751 | 0.025655 |
| trajectory_loop_score | 2.426954 | 0.039429 | 0.096205 |

## Eta Squared Ranking

| metric | eta_squared | p_value |
| --- | --- | --- |
| hidden_state_dispersion | 0.248478 | 0.000004 |
| trajectory_expansion | 0.237160 | 0.000008 |
| curvature_density | 0.145387 | 0.002774 |

## Correlation Matrix

| metric | path_efficiency | curvature_density | entropy_per_step | trajectory_compression | trajectory_expansion | hidden_state_dispersion | hidden_state_radius | trajectory_self_similarity | trajectory_loop_score |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| path_efficiency | 1.000000 | 0.076086 | -0.121113 | 0.863022 | -0.044560 | 0.033098 | -0.050680 | -0.087659 | -0.019453 |
| curvature_density | 0.076086 | 1.000000 | -0.214379 | -0.313164 | -0.728656 | -0.725033 | -0.521424 | 0.047396 | -0.392964 |
| entropy_per_step | -0.121113 | -0.214379 | 1.000000 | -0.136729 | -0.246917 | -0.258037 | -0.282605 | 0.014378 | -0.432774 |
| trajectory_compression | 0.863022 | -0.313164 | -0.136729 | 1.000000 | 0.378772 | 0.442549 | 0.156545 | -0.139793 | 0.245836 |
| trajectory_expansion | -0.044560 | -0.728656 | -0.246917 | 0.378772 | 1.000000 | 0.968002 | 0.451707 | -0.124681 | 0.616765 |
| hidden_state_dispersion | 0.033098 | -0.725033 | -0.258037 | 0.442549 | 0.968002 | 1.000000 | 0.397989 | -0.111319 | 0.566577 |
| hidden_state_radius | -0.050680 | -0.521424 | -0.282605 | 0.156545 | 0.451707 | 0.397989 | 1.000000 | -0.020478 | 0.289766 |
| trajectory_self_similarity | -0.087659 | 0.047396 | 0.014378 | -0.139793 | -0.124681 | -0.111319 | -0.020478 | 1.000000 | -0.180095 |
| trajectory_loop_score | -0.019453 | -0.392964 | -0.432774 | 0.245836 | 0.616765 | 0.566577 | 0.289766 | -0.180095 | 1.000000 |

## Notes

These structure metrics are exploratory geometry descriptors. Category separation indicates possible task-dependent trajectory geometry, not a proof of invariance or a new constant.
