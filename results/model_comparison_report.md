# Model Comparison Report

## Goal

Test whether trajectory geometry signals are model-specific or behave similarly across Hugging Face causal language models. This report does not claim a universal constant.

## Category Means by Model

| model | category | path_efficiency | curvature_density | entropy_per_step | trajectory_compression | trajectory_expansion | hidden_state_dispersion | hidden_state_radius | trajectory_self_similarity | trajectory_loop_score |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| gpt2 | abstract_questions | 0.023258 | 0.007034 | 0.090355 | 2.358160 | 97.375882 | 71.179536 | 334.281345 | -0.052576 | 29.450000 |
| gpt2 | arithmetic | 0.030318 | 0.004553 | 0.022604 | 4.656288 | 188.744467 | 139.144078 | 445.219876 | -0.037678 | 33.000000 |
| gpt2 | explanations | 0.023813 | 0.006820 | 0.031986 | 2.726928 | 114.680611 | 83.827231 | 402.485755 | -0.052386 | 26.300000 |
| gpt2 | logic | 0.021633 | 0.005908 | 0.027162 | 2.828526 | 134.331470 | 101.305119 | 393.229515 | 0.044157 | 31.200000 |
| gpt2 | simple_facts | 0.022819 | 0.006669 | 0.029707 | 2.884947 | 117.136061 | 87.996958 | 373.018207 | -0.004229 | 29.400000 |
| gpt2 | trick_questions | 0.020363 | 0.006602 | 0.031687 | 2.312094 | 110.552320 | 83.860750 | 411.585869 | -0.049814 | 28.450000 |
| distilgpt2 | abstract_questions | 0.110822 | 0.012150 | 0.102161 | 1.409554 | 42.237517 | 38.263756 | 148.562208 | 0.013526 | 11.400000 |
| distilgpt2 | arithmetic | 0.236885 | 0.010567 | 0.023414 | 2.409143 | 38.271468 | 42.374499 | 153.842851 | -0.011539 | 10.850000 |
| distilgpt2 | explanations | 0.148559 | 0.009790 | 0.308705 | 2.242884 | 30.153693 | 31.648539 | 115.144538 | 0.023820 | 8.950000 |
| distilgpt2 | logic | 0.177144 | 0.011656 | 0.019764 | 2.371982 | 40.632318 | 44.400027 | 147.397614 | 0.047837 | 13.050000 |
| distilgpt2 | simple_facts | 0.371046 | 0.008142 | 0.098574 | 2.606843 | 27.664326 | 36.484869 | 139.520650 | 0.061438 | 8.050000 |
| distilgpt2 | trick_questions | 0.166965 | 0.010775 | 0.115329 | 2.140743 | 41.747344 | 42.075360 | 130.518908 | 0.037184 | 12.600000 |
| tinyllama | abstract_questions | 0.011097 | 0.003770 | 0.710093 | 0.934607 | 29.602704 | 24.345803 | 32.159153 | -0.006748 | 0.300000 |
| tinyllama | arithmetic | 0.021328 | 0.004395 | 0.578447 | 1.688851 | 32.372176 | 26.477639 | 33.772163 | 0.060707 | 2.200000 |
| tinyllama | explanations | 0.002897 | 0.001075 | 0.620208 | 0.250172 | 8.643582 | 7.130215 | 8.999982 | -0.000020 | 0.050000 |
| tinyllama | logic | 0.020417 | 0.008534 | 0.366412 | 1.681694 | 61.838196 | 51.473011 | 67.610568 | -0.015235 | 3.750000 |
| tinyllama | simple_facts | 0.004274 | 0.001582 | 0.588052 | 0.381398 | 13.335571 | 10.672379 | 13.568748 | -0.002659 | 0.550000 |
| tinyllama | trick_questions | 0.023641 | 0.006814 | 0.413843 | 2.013314 | 56.863209 | 46.015518 | 56.563061 | 0.004931 | 2.600000 |

## ANOVA p-values and Eta Squared by Model

| model | metric | p_value | eta_squared | anova_f |
| --- | --- | --- | --- | --- |
| gpt2 | path_efficiency | 0.671751 | 0.027187 | 0.637192 |
| gpt2 | curvature_density | 0.002774 | 0.145387 | 3.878739 |
| gpt2 | entropy_per_step | 0.318823 | 0.049579 | 1.189372 |
| gpt2 | trajectory_compression | 0.050661 | 0.091146 | 2.286525 |
| gpt2 | trajectory_expansion | 0.000008 | 0.237160 | 7.088321 |
| gpt2 | hidden_state_dispersion | 0.000004 | 0.248478 | 7.538415 |
| gpt2 | hidden_state_radius | 0.158576 | 0.066588 | 1.626509 |
| gpt2 | trajectory_self_similarity | 0.699751 | 0.025655 | 0.600331 |
| gpt2 | trajectory_loop_score | 0.039429 | 0.096205 | 2.426954 |
| distilgpt2 | path_efficiency | 0.102034 | 0.076428 | 1.886770 |
| distilgpt2 | curvature_density | 0.488847 | 0.037661 | 0.892270 |
| distilgpt2 | entropy_per_step | 0.120511 | 0.072776 | 1.789517 |
| distilgpt2 | trajectory_compression | 0.390031 | 0.044165 | 1.053487 |
| distilgpt2 | trajectory_expansion | 0.233189 | 0.057469 | 1.390193 |
| distilgpt2 | hidden_state_dispersion | 0.065657 | 0.085804 | 2.139959 |
| distilgpt2 | hidden_state_radius | 0.282837 | 0.052664 | 1.267487 |
| distilgpt2 | trajectory_self_similarity | 0.869672 | 0.015879 | 0.367886 |
| distilgpt2 | trajectory_loop_score | 0.608401 | 0.030686 | 0.721795 |
| tinyllama | path_efficiency | 0.010797 | 0.121054 | 3.140173 |
| tinyllama | curvature_density | 0.000005 | 0.244447 | 7.376557 |
| tinyllama | entropy_per_step | 0.228952 | 0.057916 | 1.401675 |
| tinyllama | trajectory_compression | 0.008206 | 0.126092 | 3.289709 |
| tinyllama | trajectory_expansion | 0.000013 | 0.231232 | 6.857847 |
| tinyllama | hidden_state_dispersion | 0.000011 | 0.233762 | 6.955778 |
| tinyllama | hidden_state_radius | 0.000011 | 0.233269 | 6.936640 |
| tinyllama | trajectory_self_similarity | 0.075306 | 0.082931 | 2.061809 |
| tinyllama | trajectory_loop_score | 0.005826 | 0.132287 | 3.475956 |

## Strongest Metric Stability

A metric is considered stable here only if it appears in the top three eta-squared trajectory-structure metrics for every compared model.

| metric | models_where_top_metric | model_count | stable_across_all_models |
| --- | --- | --- | --- |
| curvature_density | gpt2, tinyllama | 2 | False |
| entropy_per_step | distilgpt2 | 1 | False |
| hidden_state_dispersion | distilgpt2, gpt2, tinyllama | 3 | True |
| hidden_state_radius | tinyllama | 1 | False |
| path_efficiency | distilgpt2 | 1 | False |
| trajectory_expansion | gpt2 | 1 | False |

## Correlation Matrices by Model

| model | metric | path_efficiency | curvature_density | entropy_per_step | trajectory_compression | trajectory_expansion | hidden_state_dispersion | hidden_state_radius | trajectory_self_similarity | trajectory_loop_score |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| gpt2 | path_efficiency | 1.000000 | 0.076086 | -0.121113 | 0.863022 | -0.044560 | 0.033098 | -0.050680 | -0.087659 | -0.019453 |
| gpt2 | curvature_density | 0.076086 | 1.000000 | -0.214379 | -0.313164 | -0.728656 | -0.725033 | -0.521424 | 0.047396 | -0.392964 |
| gpt2 | entropy_per_step | -0.121113 | -0.214379 | 1.000000 | -0.136729 | -0.246917 | -0.258037 | -0.282605 | 0.014378 | -0.432774 |
| gpt2 | trajectory_compression | 0.863022 | -0.313164 | -0.136729 | 1.000000 | 0.378772 | 0.442549 | 0.156545 | -0.139793 | 0.245836 |
| gpt2 | trajectory_expansion | -0.044560 | -0.728656 | -0.246917 | 0.378772 | 1.000000 | 0.968002 | 0.451707 | -0.124681 | 0.616765 |
| gpt2 | hidden_state_dispersion | 0.033098 | -0.725033 | -0.258037 | 0.442549 | 0.968002 | 1.000000 | 0.397989 | -0.111319 | 0.566577 |
| gpt2 | hidden_state_radius | -0.050680 | -0.521424 | -0.282605 | 0.156545 | 0.451707 | 0.397989 | 1.000000 | -0.020478 | 0.289766 |
| gpt2 | trajectory_self_similarity | -0.087659 | 0.047396 | 0.014378 | -0.139793 | -0.124681 | -0.111319 | -0.020478 | 1.000000 | -0.180095 |
| gpt2 | trajectory_loop_score | -0.019453 | -0.392964 | -0.432774 | 0.245836 | 0.616765 | 0.566577 | 0.289766 | -0.180095 | 1.000000 |
| distilgpt2 | path_efficiency | 1.000000 | -0.732192 | -0.183449 | 0.679371 | -0.713394 | -0.204998 | 0.314340 | 0.005001 | -0.587376 |
| distilgpt2 | curvature_density | -0.732192 | 1.000000 | -0.352097 | -0.425868 | 0.635224 | 0.300101 | -0.104331 | 0.024266 | 0.475301 |
| distilgpt2 | entropy_per_step | -0.183449 | -0.352097 | 1.000000 | -0.267011 | -0.361638 | -0.666393 | -0.625643 | -0.044900 | -0.258709 |
| distilgpt2 | trajectory_compression | 0.679371 | -0.425868 | -0.267011 | 1.000000 | -0.268912 | 0.166191 | 0.260932 | 0.089302 | -0.275054 |
| distilgpt2 | trajectory_expansion | -0.713394 | 0.635224 | -0.361638 | -0.268912 | 1.000000 | 0.733763 | 0.198396 | 0.099534 | 0.823570 |
| distilgpt2 | hidden_state_dispersion | -0.204998 | 0.300101 | -0.666393 | 0.166191 | 0.733763 | 1.000000 | 0.522375 | 0.127536 | 0.568586 |
| distilgpt2 | hidden_state_radius | 0.314340 | -0.104331 | -0.625643 | 0.260932 | 0.198396 | 0.522375 | 1.000000 | -0.117692 | 0.110666 |
| distilgpt2 | trajectory_self_similarity | 0.005001 | 0.024266 | -0.044900 | 0.089302 | 0.099534 | 0.127536 | -0.117692 | 1.000000 | 0.157617 |
| distilgpt2 | trajectory_loop_score | -0.587376 | 0.475301 | -0.258709 | -0.275054 | 0.823570 | 0.568586 | 0.110666 | 0.157617 | 1.000000 |
| tinyllama | path_efficiency | 1.000000 | 0.669733 | -0.566651 | 0.997826 | 0.693743 | 0.679961 | 0.666084 | 0.142230 | 0.209296 |
| tinyllama | curvature_density | 0.669733 | 1.000000 | -0.835612 | 0.694806 | 0.987640 | 0.989494 | 0.992270 | 0.093564 | 0.541985 |
| tinyllama | entropy_per_step | -0.566651 | -0.835612 | 1.000000 | -0.590543 | -0.835078 | -0.835341 | -0.834492 | -0.080016 | -0.446758 |
| tinyllama | trajectory_compression | 0.997826 | 0.694806 | -0.590543 | 1.000000 | 0.724862 | 0.710538 | 0.695347 | 0.134690 | 0.221347 |
| tinyllama | trajectory_expansion | 0.693743 | 0.987640 | -0.835078 | 0.724862 | 1.000000 | 0.998138 | 0.993041 | 0.093243 | 0.509184 |
| tinyllama | hidden_state_dispersion | 0.679961 | 0.989494 | -0.835341 | 0.710538 | 0.998138 | 1.000000 | 0.995484 | 0.092270 | 0.501755 |
| tinyllama | hidden_state_radius | 0.666084 | 0.992270 | -0.834492 | 0.695347 | 0.993041 | 0.995484 | 1.000000 | 0.076780 | 0.510209 |
| tinyllama | trajectory_self_similarity | 0.142230 | 0.093564 | -0.080016 | 0.134690 | 0.093243 | 0.092270 | 0.076780 | 1.000000 | 0.299917 |
| tinyllama | trajectory_loop_score | 0.209296 | 0.541985 | -0.446758 | 0.221347 | 0.509184 | 0.501755 | 0.510209 | 0.299917 | 1.000000 |

## Interpretation Guardrail

Similar rankings across models suggest a reusable geometry signal. Divergent rankings suggest the signal may be architecture, scale, or run dependent. Neither result proves a universal constant.
