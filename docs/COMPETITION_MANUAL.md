# ⚔️ AIMO 3 Competition Battle Plan: Rules & Implementation

Strategic manual for dominating the AI Mathematical Olympiad Progress Prize 3.

---

## 1. Official Competition Rules & Constraints
- **Time Limits**: CPU sessions (9h), GPU sessions (5h).
- **Network**: Internet access must be DISABLED during inference.
- **Output**: Submissions must produce `submission.parquet`.
- **API**: Evaluation is driven by the synchronous `kaggle_evaluation` API.
- **Hardware**: Access to H100 machines for authorized sessions.

---

## 2. Technical Implementation: The RTC Pattern
The system uses **Reasoning-through-Coding (RTC)**. Instead of predicting the answer directly, the solver:
1.  **Analyzes** the problem to identify mathematical axioms.
2.  **Architects** a Python script to solve the problem numerically or symbolically.
3.  **Executes** the code in a deterministic sandbox.
4.  **Extracts** the integer answer (0-99999).

---

## 3. High-Q Reasoning Engine
- **Solver**: `layers/layer_2_core/aimo_math_solver.py`
- **Certainty (C)**: High signal achieved through code execution verification.
- **Grounding (G)**: Rooted in Python's standard mathematical libraries and MiniMax-M2.5 logic.

---

## 4. Execution Workflow
1.  **Local Dev**: Run `python3 aimo_submission.py` to test against `test.csv`.
2.  **Kaggle Push**: Use `kaggle kernels push` with `submission.py`.
3.  **Validation**: Ensure `submission.parquet` is generated even in failure modes.

---
**Target Prize: $2,207,152** 🏆
**Verified by Jules | Strategic Command**
