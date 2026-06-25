# Trajectory Structure Report

## Goal

Identify whether different task categories produce different internal trajectory geometries. Existing trajectory metric formulas are not modified here.

## Dataset

- Total prompts: 120
- Categories: abstract_questions, arithmetic, explanations, logic, simple_facts, trick_questions

## Category Means

| category | path_efficiency | curvature_density | entropy_per_step | trajectory_compression | trajectory_expansion | hidden_state_dispersion | hidden_state_radius | trajectory_self_similarity | trajectory_loop_score |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| abstract_questions | 0.110822 | 0.012150 | 0.102161 | 1.409554 | 42.237517 | 38.263756 | 148.562208 | 0.013526 | 11.400000 |
| arithmetic | 0.236885 | 0.010567 | 0.023414 | 2.409143 | 38.271468 | 42.374499 | 153.842851 | -0.011539 | 10.850000 |
| explanations | 0.148559 | 0.009790 | 0.308705 | 2.242884 | 30.153693 | 31.648539 | 115.144538 | 0.023820 | 8.950000 |
| logic | 0.177144 | 0.011656 | 0.019764 | 2.371982 | 40.632318 | 44.400027 | 147.397614 | 0.047837 | 13.050000 |
| simple_facts | 0.371046 | 0.008142 | 0.098574 | 2.606843 | 27.664326 | 36.484869 | 139.520650 | 0.061438 | 8.050000 |
| trick_questions | 0.166965 | 0.010775 | 0.115329 | 2.140743 | 41.747344 | 42.075360 | 130.518908 | 0.037184 | 12.600000 |

## Category ANOVA

| metric | anova_f | p_value | eta_squared |
| --- | --- | --- | --- |
| path_efficiency | 1.886770 | 0.102034 | 0.076428 |
| curvature_density | 0.892270 | 0.488847 | 0.037661 |
| entropy_per_step | 1.789517 | 0.120511 | 0.072776 |
| trajectory_compression | 1.053487 | 0.390031 | 0.044165 |
| trajectory_expansion | 1.390193 | 0.233189 | 0.057469 |
| hidden_state_dispersion | 2.139959 | 0.065657 | 0.085804 |
| hidden_state_radius | 1.267487 | 0.282837 | 0.052664 |
| trajectory_self_similarity | 0.367886 | 0.869672 | 0.015879 |
| trajectory_loop_score | 0.721795 | 0.608401 | 0.030686 |

## Eta Squared Ranking

| metric | eta_squared | p_value |
| --- | --- | --- |
| hidden_state_dispersion | 0.085804 | 0.065657 |
| path_efficiency | 0.076428 | 0.102034 |
| entropy_per_step | 0.072776 | 0.120511 |

## Correlation Matrix

| metric | path_efficiency | curvature_density | entropy_per_step | trajectory_compression | trajectory_expansion | hidden_state_dispersion | hidden_state_radius | trajectory_self_similarity | trajectory_loop_score |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| path_efficiency | 1.000000 | -0.732192 | -0.183449 | 0.679371 | -0.713394 | -0.204998 | 0.314340 | 0.005001 | -0.587376 |
| curvature_density | -0.732192 | 1.000000 | -0.352097 | -0.425868 | 0.635224 | 0.300101 | -0.104331 | 0.024266 | 0.475301 |
| entropy_per_step | -0.183449 | -0.352097 | 1.000000 | -0.267011 | -0.361638 | -0.666393 | -0.625643 | -0.044900 | -0.258709 |
| trajectory_compression | 0.679371 | -0.425868 | -0.267011 | 1.000000 | -0.268912 | 0.166191 | 0.260932 | 0.089302 | -0.275054 |
| trajectory_expansion | -0.713394 | 0.635224 | -0.361638 | -0.268912 | 1.000000 | 0.733763 | 0.198396 | 0.099534 | 0.823570 |
| hidden_state_dispersion | -0.204998 | 0.300101 | -0.666393 | 0.166191 | 0.733763 | 1.000000 | 0.522375 | 0.127536 | 0.568586 |
| hidden_state_radius | 0.314340 | -0.104331 | -0.625643 | 0.260932 | 0.198396 | 0.522375 | 1.000000 | -0.117692 | 0.110666 |
| trajectory_self_similarity | 0.005001 | 0.024266 | -0.044900 | 0.089302 | 0.099534 | 0.127536 | -0.117692 | 1.000000 | 0.157617 |
| trajectory_loop_score | -0.587376 | 0.475301 | -0.258709 | -0.275054 | 0.823570 | 0.568586 | 0.110666 | 0.157617 | 1.000000 |

## Notes

These structure metrics are exploratory geometry descriptors. Category separation indicates possible task-dependent trajectory geometry, not a proof of invariance or a new constant.
