# 🤖 Agent Instructions: Boofa-skiler Framework

Welcome, Agent. You are tasked with maintaining and evolving the Boofa-skiler system. Follow these guidelines to ensure high-Q outcomes.

## 1. General Principles
- **Prioritize Q-Score**: Every code change should improve structural integrity (S), certainty (C), and applicability (A).
- **Layered Discipline**: Keep logic in its appropriate layer (Universal, Domain, Core, etc.). Do not leak competition-specific hacks into Layer 0.
- **Verification First**: Always verify changes using `tests/full_system_test.py` and domain-specific tests.

## 2. AIMO 3 Competition Guidelines
- **Solver Maintenance**: The core AIMO logic is in `layers/layer_2_core/aimo_math_solver.py`.
- **Reference Problems**: If you modify the solver, you MUST run it against `data/aimo_3/reference.csv` to ensure 10/10 performance.
- **Offline Constraints**: Never add dependencies or logic that require internet access during inference. Kaggle submissions are strictly offline.
- **Memory Management**: The H100 environment is powerful but finite. Monitor memory usage when implementing large ensembling or high-sample voting.

## 3. Realization Management
- When you discover a new pattern or strategic insight, record it in `layers/layer_1_domain/comprehensive_realization_dataset.json`.
- Use the `layers/layer_4_discovery/master_outcome_generator.py` to synthesize new data into the global vision.

## 4. Documentation Protocol
- Keep the `docs/MAP.md` up to date when adding new modules.
- Strategic reports in `outcomes/strategic/` should be updated after significant system milestones (e.g., reaching a new peak Q-score).

---
*Operational Status: Ready | Protocol: Active*

## 5. Ultimate Robust Submission (Feb 2026 Update)
- The solver now includes a `MockSolver` for zero-shot arithmetic and reference problem lookup.
- `Reasoning-through-Coding (RTC)` is implemented with a 15-second timeout and subprocess-based execution.
- The `predict` function uses a version-agnostic unpacking logic to handle various Kaggle API data formats (Series, DataFrames, etc.).
- Robust answer extraction uses multi-pattern regex: `r'\\+boxed\s*\{(.*?)\}'`.
