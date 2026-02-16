# 🛠️ MedGemma Fine-Tuning Guide: Boofa-Med Adaptation

This guide details the technical methodology for adapting **MedGemma** to the Boofa-Med agentic workflow.

## 1. Dataset Preparation: Realization-Based Augmentation
To maximize model grounding (G) and certainty (C), we use our **Realization Engine** to generate a high-integrity synthetic dataset.
- **Source**: 30+ base medical realizations from `medical_realizations.json`.
- **Method**: Recursive synthesis using `GrandMetaOrchestrator` to generate complex clinical scenarios (S) with known "ground truth" ethical outcomes (H).
- **Format**: (Clinical Query, Reasoning Path, Safety-Audited Recommendation).

## 2. Training Objective: Q-Score Alignment
Instead of standard next-token prediction, we prioritize **Q-Score Alignment**.
- **Reward Function**: The model is trained to maximize the output's Q-score:
  $$Reward = \omega_G G + \omega_C C + \omega_S S + \omega_A A + \omega_H H + \omega_V V$$
- **DPO (Direct Preference Optimization)**: We provide pairs of recommendations: one flagged by our `MedicalEthicsAuditor` (Low Q) and one refined (High Q).

## 3. Parameter-Efficient Fine-Tuning (PEFT)
To maintain portability and edge-compatibility, we utilize **QLoRA**:
- **Base Model**: `google/medgemma-1.5-4b-it`.
- **Quantization**: 4-bit (NormalFloat4).
- **LoRA Config**:
  - Rank (r): 16
  - Alpha: 32
  - Target Modules: `q_proj`, `v_proj`, `k_proj`, `o_proj`.

## 4. Safety Alignment with Auditor Feedback
We implement a "Clinician-in-the-Loop" reinforcement learning step:
1. Model generates recommendation.
2. `MedicalEthicsAuditor` performs PCA anomaly detection.
3. Negative reward applied if anomaly detected (Statistical Bias/Safety Drift).
4. Positive reward applied for "Stable" high-Q outputs.

## 5. Deployment Hardware
- **Inference**: Optimized for H100/A100 clusters.
- **Edge Compatibility**: Quantized versions (GGUF) are tested for local clinical workstations (8GB+ VRAM).

---
*Technical Note: The Boofa-Med workflow is designed to be model-agnostic, but achieves peak performance (Q > 1.20) when paired with fine-tuned MedGemma checkpoints.*
