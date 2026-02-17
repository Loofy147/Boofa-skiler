import os
import json
import numpy as np
from datetime import datetime
from typing import List, Dict, Any, Optional
from layers.layer_4_discovery.grand_integrated_simulation import GrandMetaOrchestrator, RealizationFeatures

class MedicalEthicsAuditor:
    """
    Project Gamma Specialized for Health: Medical Ethics Auditor.
    Autonomous auditing of medical AI decisions for bias, safety, and human-centricity.
    """
    def __init__(self, mco: Optional[GrandMetaOrchestrator] = None):
        self.mco = mco or GrandMetaOrchestrator()
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

        if not self.audit_log:
            return {"status": "Error", "message": "No clinical data for audit.", "overall_status": "UNKNOWN"}

        # 1. Safety Audit (Q-Score)
        unsafe_decisions = [r for r in self.audit_log if r.q_score < self.clinical_risk_threshold]

        anomalies = []

        # 2. PCA-based Bias Detection (Requires at least 3 points for meaningful variance)
        if len(self.audit_log) >= 3:
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
            anomaly_threshold = np.mean(distances) + 1.5 * np.std(distances)

            for i, dist in enumerate(distances):
                if dist > anomaly_threshold:
                    anomalies.append({
                        "id": i,
                        "content": self.audit_log[i].content,
                        "q_score": f"{self.audit_log[i].q_score:.4f}",
                        "distance": f"{dist:.4f}",
                        "risk_type": "Statistical Anomaly / Potential Bias"
                    })

        # Add safety-based anomalies regardless of count
        for r in unsafe_decisions:
            if not any(a['content'] == r.content for a in anomalies):
                anomalies.append({
                    "id": self.audit_log.index(r),
                    "content": r.content,
                    "q_score": f"{r.q_score:.4f}",
                    "distance": "N/A",
                    "risk_type": "Low Q Safety Risk"
                })

        report = {
            "timestamp": datetime.now().isoformat(),
            "decisions_audited": len(self.audit_log),
            "safety_pass_rate": (len(self.audit_log) - len(unsafe_decisions)) / len(self.audit_log),
            "anomalies_detected": len(anomalies),
            "anomalies": anomalies,
            "overall_status": "STABLE" if len(anomalies) == 0 else "HIGH_RISK"
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
    auditor.ingest_clinical_decisions([
        {"content": "Standard treatment.", "features": {"G": 0.9, "C": 0.9}},
        {"content": "Risky deviation.", "features": {"G": 0.4, "C": 0.5}}
    ])
    auditor.save_report()
