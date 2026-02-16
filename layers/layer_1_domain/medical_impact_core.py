import json
import os
from datetime import datetime
from typing import List, Dict, Any
from layers.layer_2_core.realization_engine import RealizationEngine, RealizationFeatures

class MedicalImpactCore:
    """
    Project Zeta: Cognitive Healthcare Catalyst.
    Focuses on human-centered AI for healthcare.
    """
    def __init__(self):
        self.engine = RealizationEngine()
        self.domain_file = "layers/layer_1_domain/medical_realizations.json"
        print("💉 Project Zeta (Medical Impact Core) Active.")

    def add_human_centered_realization(self, content: str, context: str, q_scores: Dict[str, float]):
        """
        Adds a high-integrity medical realization focused on human-centered values.
        """
        features = RealizationFeatures(
            grounding=q_scores.get("G", 0.9),
            certainty=q_scores.get("C", 0.9),
            structure=q_scores.get("S", 0.9),
            applicability=q_scores.get("A", 0.9),
            coherence=q_scores.get("H", 0.9),
            generativity=q_scores.get("V", 0.9)
        )

        r = self.engine.add_realization(
            content=content,
            features=features,
            turn_number=1
        )

        return r

if __name__ == "__main__":
    core = MedicalImpactCore()
    r = core.add_human_centered_realization(
        "AI-driven clinical decision support must maintain clinician-in-the-loop to ensure human accountability.",
        "Medical Ethics",
        {"G": 0.98, "C": 0.95, "S": 0.92, "A": 0.99, "H": 0.96, "V": 0.90}
    )
    print(f"Added Realization: {r.id} | Q-Score: {r.q_score:.4f}")
