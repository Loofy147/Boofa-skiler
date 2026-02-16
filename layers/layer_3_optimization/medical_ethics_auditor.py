import os
import json
import numpy as np
from datetime import datetime
from typing import List, Dict, Any
from layers.layer_4_discovery.grand_integrated_simulation import GrandMetaOrchestrator, RealizationFeatures

class MedicalEthicsAuditor:
    """
    Project Gamma Specialized for Health: Medical Ethics Auditor.
    Autonomous auditing of medical AI decisions for bias, safety, and human-centricity.
    """
    def __init__(self):
        self.mco = GrandMetaOrchestrator()
        self.audit_log = []
        self.clinical_risk_threshold = 0.85 # Higher threshold for medical safety

    def ingest_clinical_decisions(self, decisions: List[Dict[str, Any]]):
        """
        Ingests clinical decisions or AI recommendations.
        """
        print(f"🏥 Ingesting {len(decisions)} clinical decisions...")
        for i, decision in enumerate(decisions):
            content = decision.get("content", f"Clinical Decision #{i}")
            f = decision.get("features", {})
            features = RealizationFeatures(
                grounding=f.get("G", 0.9),
                certainty=f.get("C", 0.9),
                structure=f.get("S", 0.9),
                applicability=f.get("A", 0.9),
                coherence=f.get("H", 0.9),
                generativity=f.get("V", 0.9)
            )

            # Add to ETHICAL domain within the orchestrator
            r = self.mco.domains["ETHICAL"].engine.add_realization(
                content=content,
                features=features,
                turn_number=1
            )
            self.audit_log.append(r)

    def perform_clinical_audit(self) -> Dict[str, Any]:
        """
        Detects anomalies in clinical decision-making patterns.
        """
        print("🔍 Auditing Clinical Decisions for Ethical Alignment...")

        if len(self.audit_log) < 2:
            return {"status": "Error", "message": "Insufficient clinical data for audit."}

        # 1. Safety Audit (Q-Score)
        unsafe_decisions = [r for r in self.audit_log if r.q_score < self.clinical_risk_threshold]

        # 2. PCA-based Bias Detection
        features_matrix = []
        for r in self.audit_log:
            features_matrix.append([
                r.features.grounding, r.features.certainty, r.features.structure,
                r.features.applicability, r.features.coherence, r.features.generativity
            ])

        matrix = np.array(features_matrix)
        mean = np.mean(matrix, axis=0)
        std = np.std(matrix, axis=0)
        std[std == 0] = 1.0
        normalized = (matrix - mean) / std

        distances = np.linalg.norm(normalized, axis=1)
        # Handle small datasets gracefully
        if len(distances) > 2:
            anomaly_threshold = np.mean(distances) + 1.5 * np.std(distances)
        else:
            anomaly_threshold = np.max(distances) # Just pick the max if only 2

        anomalies = []
        for i, dist in enumerate(distances):
            if dist > anomaly_threshold or self.audit_log[i].q_score < self.clinical_risk_threshold:
                anomalies.append({
                    "id": i,
                    "content": self.audit_log[i].content,
                    "q_score": f"{self.audit_log[i].q_score:.4f}",
                    "distance": f"{dist:.4f}",
                    "risk_type": "Clinical Deviation / Bias Outlier" if dist > anomaly_threshold else "Low Q Safety Risk"
                })

        report = {
            "timestamp": datetime.now().isoformat(),
            "decisions_audited": len(self.audit_log),
            "safety_pass_rate": (len(self.audit_log) - len(unsafe_decisions)) / len(self.audit_log),
            "anomalies_detected": len(anomalies),
            "anomalies": anomalies,
            "overall_status": "STABLE" if len(unsafe_decisions) == 0 else "HIGH_RISK"
        }

        return report

    def save_report(self):
        os.makedirs("outcomes/technical/audit", exist_ok=True)
        filename = f"outcomes/technical/audit/MEDICAL_AUDIT_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, "w") as f:
            json.dump(self.perform_clinical_audit(), f, indent=2)
        print(f"📄 Medical Audit Report saved: {filename}")

if __name__ == "__main__":
    auditor = MedicalEthicsAuditor()
    # Simple test data
    auditor.ingest_clinical_decisions([
        {"content": "Standard treatment.", "features": {"G": 0.9, "C": 0.9}},
        {"content": "Risky deviation.", "features": {"G": 0.4, "C": 0.5}}
    ])
    auditor.save_report()
