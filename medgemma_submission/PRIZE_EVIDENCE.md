# 🏆 Boofa-Med: Prize Track Evidence

## 1. Agentic Workflow Prize Track
**Target**: Reimagining complex workflows by deploying HAI-DEF models as intelligent agents.

### Core Agentic Architecture
Boofa-Med replaces the "prompt-response" paradigm with a **Recursive Multi-Agent Loop**:
- **MedGemma Brain Agent**: Performs specialized clinical reasoning.
- **Callable Tools**: The Brain Agent is integrated with clinical tools (`dosage_calculator`, `drug_interaction_lookup`) to ground its reasoning in real-world data.
- **Boofa Auditor Agent**: Performs PCA-based anomaly detection on the reasoning path.
- **Refinement Agent**: Recursively improves the recommendation if safety thresholds (Q-Score < 0.85) are not met.

### Impact on Efficiency
This workflow automates the "second-opinion" process, ensuring that every AI recommendation is pre-audited against institutional protocols before reaching a human clinician.

---

## 2. Novel Task Prize Track
**Target**: Adapting a HAI-DEF model to perform a useful task for which it was not originally trained.

### Novel Task: Clinical Guideline Delta Discovery
We have adapted MedGemma to perform **High-Integrity Delta Discovery** between legacy practices and new clinical guidelines.
- **Engine**: `layers/layer_4_discovery/clinical_delta_engine.py`
- **Methodology**: Rather than diagnostic inference, the model is tasked with semantic difference detection across large-scale protocol documents, flagging discrepancies that could lead to medical errors if legacy practices persist.
- **Utility**: Provides an automated mechanism for "protocol-drift" detection in hospitals.

---

## 3. Edge AI Prize Track (Secondary)
**Boofa-Med** is optimized for offline inference (4-bit quantization via QLoRA), enabling its agentic safety net to run on local clinical workstations without internet connectivity, ensuring 100% patient data privacy.
