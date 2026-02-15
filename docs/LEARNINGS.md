# Boofa-skiler Learnings

## System Architecture
- The Boofa-skiler system uses a 6-layer cognitive architecture (L0-L5) for self-evolution.
- High-Q (Quality) outcomes are measured by a 6-dimensional Q-Score (G, C, S, A, H, V).
- PCA-driven dimension discovery is key to its self-improvement mechanism.

## Mock/Offline Mode
- Implementing a robust Mock Mode using sentinel values like "DUMMY" allows for seamless offline development and testing.
- Key components for a robust Mock Mode:
    - Explicit mode indicators and user feedback.
    - Helper methods for consistent mock data structure.
    - Default mock data fallbacks if external JSON resources are missing or corrupted.
    - Handling timeouts and CLI errors gracefully in production-like environments.

## AIMO 3 Competition
- The solver implements a dual-mode execution (Kaggle API vs. manual simulation).
- Self-verification and multi-sample consensus voting are used to ensure stability in non-negative integer math problems.

## Codebase Procedures
- Always verify changes with 'tests/full_system_test.py'.
- Use 'master_outcome_generator.py' for full system evolution runs.
- Maintain 'AGENTS.md' guidelines for layered discipline and Q-score prioritization.
