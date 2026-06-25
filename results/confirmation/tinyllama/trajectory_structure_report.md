# Trajectory Structure Report

## Goal

Identify whether different task categories produce different internal trajectory geometries. Existing trajectory metric formulas are not modified here.

## Dataset

- Total prompts: 120
- Categories: abstract_questions, arithmetic, explanations, logic, simple_facts, trick_questions

## Category Means

| category | path_efficiency | curvature_density | entropy_per_step | trajectory_compression | trajectory_expansion | hidden_state_dispersion | hidden_state_radius | trajectory_self_similarity | trajectory_loop_score |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| abstract_questions | 0.011097 | 0.003770 | 0.710093 | 0.934607 | 29.602704 | 24.345803 | 32.159153 | -0.006748 | 0.300000 |
| arithmetic | 0.021328 | 0.004395 | 0.578447 | 1.688851 | 32.372176 | 26.477639 | 33.772163 | 0.060707 | 2.200000 |
| explanations | 0.002897 | 0.001075 | 0.620208 | 0.250172 | 8.643582 | 7.130215 | 8.999982 | -0.000020 | 0.050000 |
| logic | 0.020417 | 0.008534 | 0.366412 | 1.681694 | 61.838196 | 51.473011 | 67.610568 | -0.015235 | 3.750000 |
| simple_facts | 0.004274 | 0.001582 | 0.588052 | 0.381398 | 13.335571 | 10.672379 | 13.568748 | -0.002659 | 0.550000 |
| trick_questions | 0.023641 | 0.006814 | 0.413843 | 2.013314 | 56.863209 | 46.015518 | 56.563061 | 0.004931 | 2.600000 |

## Category ANOVA

| metric | anova_f | p_value | eta_squared |
| --- | --- | --- | --- |
| path_efficiency | 3.140173 | 0.010797 | 0.121054 |
| curvature_density | 7.376557 | 0.000005 | 0.244447 |
| entropy_per_step | 1.401675 | 0.228952 | 0.057916 |
| trajectory_compression | 3.289709 | 0.008206 | 0.126092 |
| trajectory_expansion | 6.857847 | 0.000013 | 0.231232 |
| hidden_state_dispersion | 6.955778 | 0.000011 | 0.233762 |
| hidden_state_radius | 6.936640 | 0.000011 | 0.233269 |
| trajectory_self_similarity | 2.061809 | 0.075306 | 0.082931 |
| trajectory_loop_score | 3.475956 | 0.005826 | 0.132287 |

## Eta Squared Ranking

| metric | eta_squared | p_value |
| --- | --- | --- |
| curvature_density | 0.244447 | 0.000005 |
| hidden_state_dispersion | 0.233762 | 0.000011 |
| hidden_state_radius | 0.233269 | 0.000011 |

## Correlation Matrix

| metric | path_efficiency | curvature_density | entropy_per_step | trajectory_compression | trajectory_expansion | hidden_state_dispersion | hidden_state_radius | trajectory_self_similarity | trajectory_loop_score |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| path_efficiency | 1.000000 | 0.669733 | -0.566651 | 0.997826 | 0.693743 | 0.679961 | 0.666084 | 0.142230 | 0.209296 |
| curvature_density | 0.669733 | 1.000000 | -0.835612 | 0.694806 | 0.987640 | 0.989494 | 0.992270 | 0.093564 | 0.541985 |
| entropy_per_step | -0.566651 | -0.835612 | 1.000000 | -0.590543 | -0.835078 | -0.835341 | -0.834492 | -0.080016 | -0.446758 |
| trajectory_compression | 0.997826 | 0.694806 | -0.590543 | 1.000000 | 0.724862 | 0.710538 | 0.695347 | 0.134690 | 0.221347 |
| trajectory_expansion | 0.693743 | 0.987640 | -0.835078 | 0.724862 | 1.000000 | 0.998138 | 0.993041 | 0.093243 | 0.509184 |
| hidden_state_dispersion | 0.679961 | 0.989494 | -0.835341 | 0.710538 | 0.998138 | 1.000000 | 0.995484 | 0.092270 | 0.501755 |
| hidden_state_radius | 0.666084 | 0.992270 | -0.834492 | 0.695347 | 0.993041 | 0.995484 | 1.000000 | 0.076780 | 0.510209 |
| trajectory_self_similarity | 0.142230 | 0.093564 | -0.080016 | 0.134690 | 0.093243 | 0.092270 | 0.076780 | 1.000000 | 0.299917 |
| trajectory_loop_score | 0.209296 | 0.541985 | -0.446758 | 0.221347 | 0.509184 | 0.501755 | 0.510209 | 0.299917 | 1.000000 |

## Notes

These structure metrics are exploratory geometry descriptors. Category separation indicates possible task-dependent trajectory geometry, not a proof of invariance or a new constant.
