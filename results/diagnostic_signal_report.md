# Diagnostic Signal Report

## Goal

Compare completed model runs to identify trajectory metrics that are diagnostically useful across models. The goal is diagnostic usefulness, not proving a new constant.

## Models

- gpt2, distilgpt2, tinyllama

## Portable Signal Ranking

| metric | portable_signal_score | classification | min_eta_squared | mean_eta_squared | max_eta_squared | category_ranking_similarity | correlation_pattern_similarity | correctness_relationship_similarity |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| hidden_state_dispersion | 0.871907 | strong reusable diagnostic signal | 0.085804 | 0.189348 | 0.248478 | 0.695238 | 0.640556 | 0.648756 |
| candidate_metric_01 | 0.813493 | strong reusable diagnostic signal | 0.072872 | 0.109365 | 0.155317 | 0.161905 | 0.668162 | 0.591881 |
| entropy_per_step | 0.805153 | strong reusable diagnostic signal | 0.049579 | 0.060090 | 0.072776 | 0.676190 | 0.610964 | 0.704238 |
| L | 0.785674 | strong reusable diagnostic signal | 0.070427 | 0.173871 | 0.237160 | 0.123810 | 0.449352 | 0.614158 |
| E | 0.783406 | strong reusable diagnostic signal | 0.056288 | 0.178048 | 0.258114 | 0.409524 | 0.127709 | 0.841586 |
| D | 0.772191 | strong reusable diagnostic signal | 0.076959 | 0.130962 | 0.224782 | 0.276190 | 0.391877 | 0.470580 |
| hidden_state_radius | 0.759766 | strong reusable diagnostic signal | 0.052664 | 0.117507 | 0.233269 | 0.200000 | 0.654856 | 0.545443 |
| trajectory_expansion | 0.753840 | strong reusable diagnostic signal | 0.057469 | 0.175287 | 0.237160 | 0.085714 | 0.381271 | 0.596541 |
| trajectory_compression | 0.713933 | strong reusable diagnostic signal | 0.044165 | 0.087134 | 0.126092 | 0.200000 | 0.568415 | 0.689655 |
| trajectory_loop_score | 0.657599 | weak reusable diagnostic signal | 0.030686 | 0.086393 | 0.132287 | 0.504762 | 0.588577 | 0.693172 |
| path_efficiency | 0.564359 | model-specific signal | 0.027187 | 0.074890 | 0.121054 | -0.085714 | 0.457311 | 0.730121 |
| curvature_density | 0.557629 | weak reusable diagnostic signal | 0.037661 | 0.142498 | 0.244447 | 0.009524 | -0.023942 | 0.557318 |
| C | 0.535190 | model-specific signal | 0.020955 | 0.101024 | 0.228124 | 0.352381 | 0.429041 | 0.544127 |
| V | 0.455691 | model-specific signal | 0.015909 | 0.097884 | 0.215962 | -0.333333 | 0.576518 | 0.572666 |
| trajectory_self_similarity | 0.420649 | model-specific signal | 0.015879 | 0.041488 | 0.082931 | -0.028571 | -0.040142 | 0.651088 |

## Category Separation Within Each Model

| model | metric | p_value | eta_squared | category_mean_ranking |
| --- | --- | --- | --- | --- |
| gpt2 | L | 0.000008 | 0.237160 | arithmetic (9059.7344) > logic (6447.9106) > simple_facts (5622.5309) > explanations (5504.6693) > trick_questions (5306.5114) > abstract_questions (4674.0423) |
| gpt2 | D | 0.050661 | 0.091146 | arithmetic (223.5018) > simple_facts (138.4775) > logic (135.7692) > explanations (130.8925) > abstract_questions (113.1917) > trick_questions (110.9805) |
| gpt2 | C | 0.784627 | 0.020955 | trick_questions (69.8728) > logic (69.4789) > explanations (68.4165) > simple_facts (65.6106) > abstract_questions (58.6763) > arithmetic (54.9312) |
| gpt2 | E | 0.000027 | 0.219742 | abstract_questions (1.5791) > explanations (1.5353) > trick_questions (1.5210) > simple_facts (1.4259) > logic (1.3038) > arithmetic (1.0850) |
| gpt2 | V | 0.869208 | 0.015909 | explanations (34.6000) > simple_facts (33.7500) > arithmetic (33.5500) > trick_questions (33.4500) > logic (33.0000) > abstract_questions (32.9000) |
| gpt2 | candidate_metric_01 | 0.119991 | 0.072872 | arithmetic (71.5597) > logic (65.0323) > simple_facts (46.9574) > trick_questions (45.5886) > explanations (45.0033) > abstract_questions (37.6856) |
| gpt2 | path_efficiency | 0.671751 | 0.027187 | arithmetic (0.0303) > explanations (0.0238) > abstract_questions (0.0233) > simple_facts (0.0228) > logic (0.0216) > trick_questions (0.0204) |
| gpt2 | curvature_density | 0.002774 | 0.145387 | abstract_questions (0.0070) > explanations (0.0068) > simple_facts (0.0067) > trick_questions (0.0066) > logic (0.0059) > arithmetic (0.0046) |
| gpt2 | entropy_per_step | 0.318823 | 0.049579 | abstract_questions (0.0904) > explanations (0.0320) > trick_questions (0.0317) > simple_facts (0.0297) > logic (0.0272) > arithmetic (0.0226) |
| gpt2 | trajectory_compression | 0.050661 | 0.091146 | arithmetic (4.6563) > simple_facts (2.8849) > logic (2.8285) > explanations (2.7269) > abstract_questions (2.3582) > trick_questions (2.3121) |
| gpt2 | trajectory_expansion | 0.000008 | 0.237160 | arithmetic (188.7445) > logic (134.3315) > simple_facts (117.1361) > explanations (114.6806) > trick_questions (110.5523) > abstract_questions (97.3759) |
| gpt2 | hidden_state_dispersion | 0.000004 | 0.248478 | arithmetic (139.1441) > logic (101.3051) > simple_facts (87.9970) > trick_questions (83.8607) > explanations (83.8272) > abstract_questions (71.1795) |
| gpt2 | hidden_state_radius | 0.158576 | 0.066588 | arithmetic (445.2199) > trick_questions (411.5859) > explanations (402.4858) > logic (393.2295) > simple_facts (373.0182) > abstract_questions (334.2813) |
| gpt2 | trajectory_self_similarity | 0.699751 | 0.025655 | logic (0.0442) > simple_facts (-0.0042) > arithmetic (-0.0377) > trick_questions (-0.0498) > explanations (-0.0524) > abstract_questions (-0.0526) |
| gpt2 | trajectory_loop_score | 0.039429 | 0.096205 | arithmetic (33.0000) > logic (31.2000) > abstract_questions (29.4500) > simple_facts (29.4000) > trick_questions (28.4500) > explanations (26.3000) |
| distilgpt2 | L | 0.133897 | 0.070427 | abstract_questions (2027.4008) > trick_questions (2003.8725) > logic (1950.3513) > arithmetic (1782.9397) > simple_facts (1316.4849) > explanations (1286.8232) |
| distilgpt2 | D | 0.099569 | 0.076959 | simple_facts (116.2383) > logic (113.8551) > arithmetic (110.1326) > trick_questions (102.7556) > explanations (75.1553) > abstract_questions (67.6586) |
| distilgpt2 | C | 0.268338 | 0.053993 | abstract_questions (42.1202) > trick_questions (30.5530) > logic (29.1363) > arithmetic (26.0453) > explanations (25.3671) > simple_facts (24.9576) |
| distilgpt2 | E | 0.244692 | 0.056288 | abstract_questions (1.3052) > explanations (0.9923) > arithmetic (0.9766) > logic (0.9487) > trick_questions (0.9321) > simple_facts (0.8081) |
| distilgpt2 | V | 0.194890 | 0.061782 | abstract_questions (27.9500) > logic (26.2000) > trick_questions (25.0500) > arithmetic (22.4000) > explanations (18.2500) > simple_facts (17.4500) |
| distilgpt2 | candidate_metric_01 | 0.032728 | 0.099905 | trick_questions (51.2945) > abstract_questions (35.3669) > logic (30.4179) > explanations (27.9458) > arithmetic (24.7980) > simple_facts (23.3161) |
| distilgpt2 | path_efficiency | 0.102034 | 0.076428 | simple_facts (0.3710) > arithmetic (0.2369) > logic (0.1771) > trick_questions (0.1670) > explanations (0.1486) > abstract_questions (0.1108) |
| distilgpt2 | curvature_density | 0.488847 | 0.037661 | abstract_questions (0.0122) > logic (0.0117) > trick_questions (0.0108) > arithmetic (0.0106) > explanations (0.0098) > simple_facts (0.0081) |
| distilgpt2 | entropy_per_step | 0.120511 | 0.072776 | explanations (0.3087) > trick_questions (0.1153) > abstract_questions (0.1022) > simple_facts (0.0986) > arithmetic (0.0234) > logic (0.0198) |
| distilgpt2 | trajectory_compression | 0.390031 | 0.044165 | simple_facts (2.6068) > arithmetic (2.4091) > logic (2.3720) > explanations (2.2429) > trick_questions (2.1407) > abstract_questions (1.4096) |
| distilgpt2 | trajectory_expansion | 0.233189 | 0.057469 | abstract_questions (42.2375) > trick_questions (41.7473) > logic (40.6323) > arithmetic (38.2715) > explanations (30.1537) > simple_facts (27.6643) |
| distilgpt2 | hidden_state_dispersion | 0.065657 | 0.085804 | logic (44.4000) > arithmetic (42.3745) > trick_questions (42.0754) > abstract_questions (38.2638) > simple_facts (36.4849) > explanations (31.6485) |
| distilgpt2 | hidden_state_radius | 0.282837 | 0.052664 | arithmetic (153.8429) > abstract_questions (148.5622) > logic (147.3976) > simple_facts (139.5206) > trick_questions (130.5189) > explanations (115.1445) |
| distilgpt2 | trajectory_self_similarity | 0.869672 | 0.015879 | simple_facts (0.0614) > logic (0.0478) > trick_questions (0.0372) > explanations (0.0238) > abstract_questions (0.0135) > arithmetic (-0.0115) |
| distilgpt2 | trajectory_loop_score | 0.608401 | 0.030686 | logic (13.0500) > trick_questions (12.6000) > abstract_questions (11.4000) > arithmetic (10.8500) > explanations (8.9500) > simple_facts (8.0500) |
| tinyllama | L | 0.000040 | 0.214025 | logic (2374.3983) > trick_questions (2196.9890) > arithmetic (1133.5034) > abstract_questions (1014.0762) > simple_facts (440.7855) > explanations (296.5750) |
| tinyllama | D | 0.000019 | 0.224782 | logic (64.4000) > trick_questions (58.2428) > arithmetic (34.6209) > abstract_questions (28.2594) > simple_facts (11.9929) > explanations (8.4492) |
| tinyllama | C | 0.000015 | 0.228124 | logic (27.7966) > trick_questions (24.0245) > arithmetic (12.9135) > abstract_questions (11.8312) > simple_facts (5.3863) > explanations (3.4572) |
| tinyllama | E | 0.000002 | 0.258114 | abstract_questions (1.1280) > logic (1.0576) > trick_questions (1.0466) > arithmetic (0.8529) > explanations (0.7208) > simple_facts (0.7027) |
| tinyllama | V | 0.000035 | 0.215962 | logic (27.0500) > trick_questions (23.4500) > arithmetic (12.9500) > abstract_questions (11.1500) > simple_facts (4.6500) > explanations (3.2000) |
| tinyllama | candidate_metric_01 | 0.001557 | 0.155317 | logic (31.6569) > trick_questions (25.7173) > arithmetic (23.8373) > abstract_questions (9.8680) > simple_facts (8.3131) > explanations (3.3682) |
| tinyllama | path_efficiency | 0.010797 | 0.121054 | trick_questions (0.0236) > arithmetic (0.0213) > logic (0.0204) > abstract_questions (0.0111) > simple_facts (0.0043) > explanations (0.0029) |
| tinyllama | curvature_density | 0.000005 | 0.244447 | logic (0.0085) > trick_questions (0.0068) > arithmetic (0.0044) > abstract_questions (0.0038) > simple_facts (0.0016) > explanations (0.0011) |
| tinyllama | entropy_per_step | 0.228952 | 0.057916 | abstract_questions (0.7101) > explanations (0.6202) > simple_facts (0.5881) > arithmetic (0.5784) > trick_questions (0.4138) > logic (0.3664) |
| tinyllama | trajectory_compression | 0.008206 | 0.126092 | trick_questions (2.0133) > arithmetic (1.6889) > logic (1.6817) > abstract_questions (0.9346) > simple_facts (0.3814) > explanations (0.2502) |
| tinyllama | trajectory_expansion | 0.000013 | 0.231232 | logic (61.8382) > trick_questions (56.8632) > arithmetic (32.3722) > abstract_questions (29.6027) > simple_facts (13.3356) > explanations (8.6436) |
| tinyllama | hidden_state_dispersion | 0.000011 | 0.233762 | logic (51.4730) > trick_questions (46.0155) > arithmetic (26.4776) > abstract_questions (24.3458) > simple_facts (10.6724) > explanations (7.1302) |
| tinyllama | hidden_state_radius | 0.000011 | 0.233269 | logic (67.6106) > trick_questions (56.5631) > arithmetic (33.7722) > abstract_questions (32.1592) > simple_facts (13.5687) > explanations (9.0000) |
| tinyllama | trajectory_self_similarity | 0.075306 | 0.082931 | arithmetic (0.0607) > trick_questions (0.0049) > explanations (-0.0000) > simple_facts (-0.0027) > abstract_questions (-0.0067) > logic (-0.0152) |
| tinyllama | trajectory_loop_score | 0.005826 | 0.132287 | logic (3.7500) > trick_questions (2.6000) > arithmetic (2.2000) > simple_facts (0.5500) > abstract_questions (0.3000) > explanations (0.0500) |

## Category Ranking Similarity

| metric | category_ranking_similarity | pairwise_category_ranking_similarity | gpt2_ranking | distilgpt2_ranking | tinyllama_ranking |
| --- | --- | --- | --- | --- | --- |
| L | 0.123810 | gpt2 vs distilgpt2: -0.4857; gpt2 vs tinyllama: 0.2571; distilgpt2 vs tinyllama: 0.6000 | arithmetic (9059.7344) > logic (6447.9106) > simple_facts (5622.5309) > explanations (5504.6693) > trick_questions (5306.5114) > abstract_questions (4674.0423) | abstract_questions (2027.4008) > trick_questions (2003.8725) > logic (1950.3513) > arithmetic (1782.9397) > simple_facts (1316.4849) > explanations (1286.8232) | logic (2374.3983) > trick_questions (2196.9890) > arithmetic (1133.5034) > abstract_questions (1014.0762) > simple_facts (440.7855) > explanations (296.5750) |
| D | 0.276190 | gpt2 vs distilgpt2: 0.6571; gpt2 vs tinyllama: -0.0857; distilgpt2 vs tinyllama: 0.2571 | arithmetic (223.5018) > simple_facts (138.4775) > logic (135.7692) > explanations (130.8925) > abstract_questions (113.1917) > trick_questions (110.9805) | simple_facts (116.2383) > logic (113.8551) > arithmetic (110.1326) > trick_questions (102.7556) > explanations (75.1553) > abstract_questions (67.6586) | logic (64.4000) > trick_questions (58.2428) > arithmetic (34.6209) > abstract_questions (28.2594) > simple_facts (11.9929) > explanations (8.4492) |
| C | 0.352381 | gpt2 vs distilgpt2: 0.1429; gpt2 vs tinyllama: 0.3714; distilgpt2 vs tinyllama: 0.5429 | trick_questions (69.8728) > logic (69.4789) > explanations (68.4165) > simple_facts (65.6106) > abstract_questions (58.6763) > arithmetic (54.9312) | abstract_questions (42.1202) > trick_questions (30.5530) > logic (29.1363) > arithmetic (26.0453) > explanations (25.3671) > simple_facts (24.9576) | logic (27.7966) > trick_questions (24.0245) > arithmetic (12.9135) > abstract_questions (11.8312) > simple_facts (5.3863) > explanations (3.4572) |
| E | 0.409524 | gpt2 vs distilgpt2: 0.4857; gpt2 vs tinyllama: 0.2571; distilgpt2 vs tinyllama: 0.4857 | abstract_questions (1.5791) > explanations (1.5353) > trick_questions (1.5210) > simple_facts (1.4259) > logic (1.3038) > arithmetic (1.0850) | abstract_questions (1.3052) > explanations (0.9923) > arithmetic (0.9766) > logic (0.9487) > trick_questions (0.9321) > simple_facts (0.8081) | abstract_questions (1.1280) > logic (1.0576) > trick_questions (1.0466) > arithmetic (0.8529) > explanations (0.7208) > simple_facts (0.7027) |
| V | -0.333333 | gpt2 vs distilgpt2: -0.9429; gpt2 vs tinyllama: -0.6571; distilgpt2 vs tinyllama: 0.6000 | explanations (34.6000) > simple_facts (33.7500) > arithmetic (33.5500) > trick_questions (33.4500) > logic (33.0000) > abstract_questions (32.9000) | abstract_questions (27.9500) > logic (26.2000) > trick_questions (25.0500) > arithmetic (22.4000) > explanations (18.2500) > simple_facts (17.4500) | logic (27.0500) > trick_questions (23.4500) > arithmetic (12.9500) > abstract_questions (11.1500) > simple_facts (4.6500) > explanations (3.2000) |
| candidate_metric_01 | 0.161905 | gpt2 vs distilgpt2: -0.4857; gpt2 vs tinyllama: 0.4857; distilgpt2 vs tinyllama: 0.4857 | arithmetic (71.5597) > logic (65.0323) > simple_facts (46.9574) > trick_questions (45.5886) > explanations (45.0033) > abstract_questions (37.6856) | trick_questions (51.2945) > abstract_questions (35.3669) > logic (30.4179) > explanations (27.9458) > arithmetic (24.7980) > simple_facts (23.3161) | logic (31.6569) > trick_questions (25.7173) > arithmetic (23.8373) > abstract_questions (9.8680) > simple_facts (8.3131) > explanations (3.3682) |
| path_efficiency | -0.085714 | gpt2 vs distilgpt2: -0.0286; gpt2 vs tinyllama: -0.3714; distilgpt2 vs tinyllama: 0.1429 | arithmetic (0.0303) > explanations (0.0238) > abstract_questions (0.0233) > simple_facts (0.0228) > logic (0.0216) > trick_questions (0.0204) | simple_facts (0.3710) > arithmetic (0.2369) > logic (0.1771) > trick_questions (0.1670) > explanations (0.1486) > abstract_questions (0.1108) | trick_questions (0.0236) > arithmetic (0.0213) > logic (0.0204) > abstract_questions (0.0111) > simple_facts (0.0043) > explanations (0.0029) |
| curvature_density | 0.009524 | gpt2 vs distilgpt2: 0.0857; gpt2 vs tinyllama: -0.6571; distilgpt2 vs tinyllama: 0.6000 | abstract_questions (0.0070) > explanations (0.0068) > simple_facts (0.0067) > trick_questions (0.0066) > logic (0.0059) > arithmetic (0.0046) | abstract_questions (0.0122) > logic (0.0117) > trick_questions (0.0108) > arithmetic (0.0106) > explanations (0.0098) > simple_facts (0.0081) | logic (0.0085) > trick_questions (0.0068) > arithmetic (0.0044) > abstract_questions (0.0038) > simple_facts (0.0016) > explanations (0.0011) |
| entropy_per_step | 0.676190 | gpt2 vs distilgpt2: 0.7714; gpt2 vs tinyllama: 0.7143; distilgpt2 vs tinyllama: 0.5429 | abstract_questions (0.0904) > explanations (0.0320) > trick_questions (0.0317) > simple_facts (0.0297) > logic (0.0272) > arithmetic (0.0226) | explanations (0.3087) > trick_questions (0.1153) > abstract_questions (0.1022) > simple_facts (0.0986) > arithmetic (0.0234) > logic (0.0198) | abstract_questions (0.7101) > explanations (0.6202) > simple_facts (0.5881) > arithmetic (0.5784) > trick_questions (0.4138) > logic (0.3664) |
| trajectory_compression | 0.200000 | gpt2 vs distilgpt2: 0.8857; gpt2 vs tinyllama: -0.1429; distilgpt2 vs tinyllama: -0.1429 | arithmetic (4.6563) > simple_facts (2.8849) > logic (2.8285) > explanations (2.7269) > abstract_questions (2.3582) > trick_questions (2.3121) | simple_facts (2.6068) > arithmetic (2.4091) > logic (2.3720) > explanations (2.2429) > trick_questions (2.1407) > abstract_questions (1.4096) | trick_questions (2.0133) > arithmetic (1.6889) > logic (1.6817) > abstract_questions (0.9346) > simple_facts (0.3814) > explanations (0.2502) |
| trajectory_expansion | 0.085714 | gpt2 vs distilgpt2: -0.5429; gpt2 vs tinyllama: 0.2571; distilgpt2 vs tinyllama: 0.5429 | arithmetic (188.7445) > logic (134.3315) > simple_facts (117.1361) > explanations (114.6806) > trick_questions (110.5523) > abstract_questions (97.3759) | abstract_questions (42.2375) > trick_questions (41.7473) > logic (40.6323) > arithmetic (38.2715) > explanations (30.1537) > simple_facts (27.6643) | logic (61.8382) > trick_questions (56.8632) > arithmetic (32.3722) > abstract_questions (29.6027) > simple_facts (13.3356) > explanations (8.6436) |
| hidden_state_dispersion | 0.695238 | gpt2 vs distilgpt2: 0.6571; gpt2 vs tinyllama: 0.4857; distilgpt2 vs tinyllama: 0.9429 | arithmetic (139.1441) > logic (101.3051) > simple_facts (87.9970) > trick_questions (83.8607) > explanations (83.8272) > abstract_questions (71.1795) | logic (44.4000) > arithmetic (42.3745) > trick_questions (42.0754) > abstract_questions (38.2638) > simple_facts (36.4849) > explanations (31.6485) | logic (51.4730) > trick_questions (46.0155) > arithmetic (26.4776) > abstract_questions (24.3458) > simple_facts (10.6724) > explanations (7.1302) |
| hidden_state_radius | 0.200000 | gpt2 vs distilgpt2: -0.0286; gpt2 vs tinyllama: 0.2571; distilgpt2 vs tinyllama: 0.3714 | arithmetic (445.2199) > trick_questions (411.5859) > explanations (402.4858) > logic (393.2295) > simple_facts (373.0182) > abstract_questions (334.2813) | arithmetic (153.8429) > abstract_questions (148.5622) > logic (147.3976) > simple_facts (139.5206) > trick_questions (130.5189) > explanations (115.1445) | logic (67.6106) > trick_questions (56.5631) > arithmetic (33.7722) > abstract_questions (32.1592) > simple_facts (13.5687) > explanations (9.0000) |
| trajectory_self_similarity | -0.028571 | gpt2 vs distilgpt2: 0.6000; gpt2 vs tinyllama: -0.2000; distilgpt2 vs tinyllama: -0.4857 | logic (0.0442) > simple_facts (-0.0042) > arithmetic (-0.0377) > trick_questions (-0.0498) > explanations (-0.0524) > abstract_questions (-0.0526) | simple_facts (0.0614) > logic (0.0478) > trick_questions (0.0372) > explanations (0.0238) > abstract_questions (0.0135) > arithmetic (-0.0115) | arithmetic (0.0607) > trick_questions (0.0049) > explanations (-0.0000) > simple_facts (-0.0027) > abstract_questions (-0.0067) > logic (-0.0152) |
| trajectory_loop_score | 0.504762 | gpt2 vs distilgpt2: 0.3143; gpt2 vs tinyllama: 0.4857; distilgpt2 vs tinyllama: 0.7143 | arithmetic (33.0000) > logic (31.2000) > abstract_questions (29.4500) > simple_facts (29.4000) > trick_questions (28.4500) > explanations (26.3000) | logic (13.0500) > trick_questions (12.6000) > abstract_questions (11.4000) > arithmetic (10.8500) > explanations (8.9500) > simple_facts (8.0500) | logic (3.7500) > trick_questions (2.6000) > arithmetic (2.2000) > simple_facts (0.5500) > abstract_questions (0.3000) > explanations (0.0500) |

## Correlation Pattern Similarity

| metric | correlation_pattern_similarity | pairwise_correlation_pattern_similarity |
| --- | --- | --- |
| L | 0.449352 | gpt2 vs distilgpt2: 0.3307; gpt2 vs tinyllama: 0.4828; distilgpt2 vs tinyllama: 0.5346 |
| D | 0.391877 | gpt2 vs distilgpt2: 0.8117; gpt2 vs tinyllama: 0.2277; distilgpt2 vs tinyllama: 0.1362 |
| C | 0.429041 | gpt2 vs distilgpt2: 0.7561; gpt2 vs tinyllama: 0.1773; distilgpt2 vs tinyllama: 0.3538 |
| E | 0.127709 | gpt2 vs distilgpt2: 0.3109; gpt2 vs tinyllama: 0.1186; distilgpt2 vs tinyllama: -0.0464 |
| V | 0.576518 | gpt2 vs distilgpt2: 0.4380; gpt2 vs tinyllama: 0.8578; distilgpt2 vs tinyllama: 0.4338 |
| candidate_metric_01 | 0.668162 | gpt2 vs distilgpt2: 0.8172; gpt2 vs tinyllama: 0.5270; distilgpt2 vs tinyllama: 0.6603 |
| path_efficiency | 0.457311 | gpt2 vs distilgpt2: 0.6740; gpt2 vs tinyllama: 0.4221; distilgpt2 vs tinyllama: 0.2758 |
| curvature_density | -0.023942 | gpt2 vs distilgpt2: 0.0658; gpt2 vs tinyllama: -0.3836; distilgpt2 vs tinyllama: 0.2460 |
| entropy_per_step | 0.610964 | gpt2 vs distilgpt2: 0.4757; gpt2 vs tinyllama: 0.4757; distilgpt2 vs tinyllama: 0.8815 |
| trajectory_compression | 0.568415 | gpt2 vs distilgpt2: 0.8061; gpt2 vs tinyllama: 0.4771; distilgpt2 vs tinyllama: 0.4220 |
| trajectory_expansion | 0.381271 | gpt2 vs distilgpt2: 0.3136; gpt2 vs tinyllama: 0.4449; distilgpt2 vs tinyllama: 0.3853 |
| hidden_state_dispersion | 0.640556 | gpt2 vs distilgpt2: 0.6803; gpt2 vs tinyllama: 0.4473; distilgpt2 vs tinyllama: 0.7941 |
| hidden_state_radius | 0.654856 | gpt2 vs distilgpt2: 0.6514; gpt2 vs tinyllama: 0.4965; distilgpt2 vs tinyllama: 0.8167 |
| trajectory_self_similarity | -0.040142 | gpt2 vs distilgpt2: -0.6067; gpt2 vs tinyllama: -0.2642; distilgpt2 vs tinyllama: 0.7506 |
| trajectory_loop_score | 0.588577 | gpt2 vs distilgpt2: 0.4882; gpt2 vs tinyllama: 0.6917; distilgpt2 vs tinyllama: 0.5858 |

## Correctness Relationship Similarity

| metric | correctness_relationship_similarity | correctness_correlation_by_model |
| --- | --- | --- |
| C | 0.544127 | gpt2: -0.1210; distilgpt2: 0.2144; tinyllama: 0.3348 |
| D | 0.470580 | gpt2: 0.1083; distilgpt2: -0.1623; tinyllama: 0.3671 |
| E | 0.841586 | gpt2: -0.0943; distilgpt2: 0.0174; tinyllama: -0.1410 |
| L | 0.614158 | gpt2: -0.0449; distilgpt2: 0.1011; tinyllama: 0.3410 |
| V | 0.572666 | gpt2: -0.0809; distilgpt2: 0.1388; tinyllama: 0.3464 |
| candidate_metric_01 | 0.591881 | gpt2: -0.0702; distilgpt2: 0.3379; tinyllama: 0.3249 |
| curvature_density | 0.557318 | gpt2: -0.0569; distilgpt2: 0.1212; tinyllama: 0.3858 |
| entropy_per_step | 0.704238 | gpt2: -0.0943; distilgpt2: -0.0309; tinyllama: -0.3266 |
| hidden_state_dispersion | 0.648756 | gpt2: 0.0097; distilgpt2: 0.0391; tinyllama: 0.3610 |
| hidden_state_radius | 0.545443 | gpt2: -0.0823; distilgpt2: -0.0269; tinyllama: 0.3723 |
| path_efficiency | 0.730121 | gpt2: 0.1325; distilgpt2: -0.1281; tinyllama: 0.1418 |
| trajectory_compression | 0.689655 | gpt2: 0.1083; distilgpt2: -0.1592; tinyllama: 0.1511 |
| trajectory_expansion | 0.596541 | gpt2: -0.0449; distilgpt2: 0.0993; tinyllama: 0.3586 |
| trajectory_loop_score | 0.693172 | gpt2: 0.0865; distilgpt2: 0.0475; tinyllama: 0.3543 |
| trajectory_self_similarity | 0.651088 | gpt2: 0.2422; distilgpt2: -0.0896; tinyllama: -0.1067 |

## Model-Specific Signals

| metric | model_specific_pattern |
| --- | --- |
| L | strong in gpt2, distilgpt2, tinyllama, weak in  |
| D | strong in gpt2, distilgpt2, tinyllama, weak in  |
| V | strong in distilgpt2, tinyllama, weak in gpt2 |
| candidate_metric_01 | strong in gpt2, distilgpt2, tinyllama, weak in  |
| path_efficiency | strong in distilgpt2, tinyllama, weak in gpt2 |
| hidden_state_dispersion | strong in gpt2, distilgpt2, tinyllama, weak in  |
| trajectory_self_similarity | strong in tinyllama, weak in gpt2, distilgpt2 |

## Plain-English Conclusion

- What worked: hidden_state_dispersion, candidate_metric_01, entropy_per_step, L, E, D, hidden_state_radius, trajectory_expansion, trajectory_compression showed the best cross-model diagnostic behavior.
- Model-specific behavior: L (strong in gpt2, distilgpt2, tinyllama, weak in ); D (strong in gpt2, distilgpt2, tinyllama, weak in ); V (strong in distilgpt2, tinyllama, weak in gpt2); candidate_metric_01 (strong in gpt2, distilgpt2, tinyllama, weak in ); path_efficiency (strong in distilgpt2, tinyllama, weak in gpt2); hidden_state_dispersion (strong in gpt2, distilgpt2, tinyllama, weak in ); trajectory_self_similarity (strong in tinyllama, weak in gpt2, distilgpt2).
- What to test next: run the same prompt set on additional causal language models and check whether the top-ranked diagnostics preserve category ranking, correlation fingerprints, and correctness relationships.
