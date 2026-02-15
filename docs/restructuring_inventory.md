# Repository Inventory & Restructuring Plan

## Root Files -> New Locations
- submission.py -> competitions/aimo/submission.py
- aimo_submission.py -> competitions/aimo/aimo_submission.py
- aimo_3_gateway.py -> competitions/aimo/aimo_3_gateway.py
- aimo_3_inference_server.py -> competitions/aimo/aimo_3_inference_server.py
- generate_submission_notebook.py -> competitions/aimo/generate_notebook.py
- submission.ipynb -> competitions/aimo/submission.ipynb
- reference.csv -> competitions/aimo/reference.csv
- sample_submission.csv -> competitions/aimo/sample_submission.csv
- numina_examples.txt -> competitions/aimo/numina_examples.txt
- kernel-metadata.json -> competitions/aimo/kernel-metadata.json

- showcase_demo.py -> demos/showcase_demo.py
- demo_engine.py -> demos/demo_engine.py
- app.py -> demos/app.py

- test_pipeline.py -> tests/test_pipeline.py
- full_system_test.py -> tests/full_system_test.py

- fix_imports.py -> scripts/fix_imports.py

- layer0_foundation.py -> layers/layer_0_universal/foundation.py
- layer1_skills.py -> layers/layer_1_domain/foundation.py
- layer2_self_evolution.py -> layers/layer_2_core/foundation.py
- layer3_orchestration.py -> layers/layer_3_orchestration/foundation.py
- pipeline.py -> layers/layer_3_optimization/pipeline.py
- master_outcome_generator.py -> layers/layer_4_discovery/master_outcome_generator.py
- business_opportunity_engine.py -> layers/layer_4_discovery/business_opportunity_engine.py

- BENCHMARK_RESULTS.md -> docs/BENCHMARK_RESULTS.md
- BOOFA_SKILER_README.md -> docs/BOOFA_SKILER_README.md

## Legacy/Redundant Files to Archive/Delete
- grand_integrated_outcomes.json (Root) -> Already in layers/layer_0_universal/
- model-metadata.json -> data/model-metadata.json
