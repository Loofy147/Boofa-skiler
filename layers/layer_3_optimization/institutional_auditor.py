import os
import json
import numpy as np
from datetime import datetime
from typing import List, Dict, Any
from layers.layer_4_discovery.grand_integrated_simulation import GrandMetaOrchestrator, RealizationFeatures

class InstitutionalAuditor:
    """
    Project Gamma: Predictive Institutional Auditor
    Goal: Autonomous auditing of institutional bias and operational risks.
    """
    def __init__(self):
        self.mco = GrandMetaOrchestrator()
        self.audit_log = []
        self.risk_threshold = 0.75

    def ingest_institutional_data(self, data_points: List[Dict[str, Any]]):
        """
        Ingests data points representing institutional decisions or actions.
        Each point is converted into an ETHICAL realization.
        """
        print(f"📥 Ingesting {len(data_points)} institutional data points...")
        for i, point in enumerate(data_points):
            content = point.get("content", f"Institutional Action #{i}")
            f = point.get("features", {})
            features = RealizationFeatures(
                grounding=f.get("G", 0.8),
                certainty=f.get("C", 0.8),
                structure=f.get("S", 0.8),
                applicability=f.get("A", 0.8),
                coherence=f.get("H", 0.8),
                generativity=f.get("V", 0.8)
            )

            # Add to Ethical domain
            r = self.mco.domains["ETHICAL"].engine.add_realization(
                content=content,
                features=features,
                turn_number=1
            )
            self.audit_log.append(r)

    def run_audit(self) -> Dict[str, Any]:
        """
        Performs the audit using PCA-based anomaly detection and Q-score thresholding.
        """
        print("🔍 Running Institutional Audit...")

        if len(self.audit_log) < 2:
            return {"status": "Error", "message": "Insufficient data for audit."}

        # 1. Q-Score Audit
        risky_nodes = [r for r in self.audit_log if r.q_score < self.risk_threshold]

        # 2. PCA-based Anomaly Detection
        features_matrix = []
        for r in self.audit_log:
            features_matrix.append([
                r.features.grounding, r.features.certainty, r.features.structure,
                r.features.applicability, r.features.coherence, r.features.generativity
            ])

        matrix = np.array(features_matrix)
        mean = np.mean(matrix, axis=0)
        std = np.std(matrix, axis=0)

        # Avoid division by zero
        std[std == 0] = 1.0

        normalized = (matrix - mean) / std

        # Simple Euclidean distance from mean as anomaly score
        distances = np.linalg.norm(normalized, axis=1)
        anomaly_threshold = np.mean(distances) + 2 * np.std(distances)

        anomalies = []
        for i, dist in enumerate(distances):
            if dist > anomaly_threshold:
                anomalies.append({
                    "id": i,
                    "content": self.audit_log[i].content,
                    "q_score": self.audit_log[i].q_score,
                    "distance": dist,
                    "type": "Operational Drift / Bias Outlier"
                })

        report = {
            "timestamp": datetime.now().isoformat(),
            "total_points_audited": len(self.audit_log),
            "avg_ethical_q": np.mean([r.q_score for r in self.audit_log]),
            "risk_incidents": len(risky_nodes),
            "anomalies_detected": len(anomalies),
            "anomalies": anomalies,
            "status": "PASS" if len(risky_nodes) == 0 and len(anomalies) == 0 else "WARNING"
        }

        return report

    def save_audit_report(self, report: Dict[str, Any]):
        os.makedirs("outcomes/technical/audit", exist_ok=True)
        filename = f"outcomes/technical/audit/AUDIT_REPORT_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, "w") as f:
            json.dump(report, f, indent=2)
        print(f"📄 Audit Report saved: {filename}")

if __name__ == "__main__":
    auditor = InstitutionalAuditor()

    # Simulate high-bias/risky data
    test_data = [
        {"content": "Standard hiring process following diversity guidelines.", "features": {"G": 0.95, "C": 0.94, "S": 0.92, "A": 0.90, "H": 0.98, "V": 0.92}},
        {"content": "Automated bonus allocation based on tenure only.", "features": {"G": 0.70, "C": 0.65, "S": 0.80, "A": 0.60, "H": 0.55, "V": 0.50}}, # Risky
        {"content": "Transparent executive performance review.", "features": {"G": 0.92, "C": 0.90, "S": 0.94, "A": 0.88, "H": 0.95, "V": 0.90}},
        {"content": "Anonymous whistleblower protection protocol.", "features": {"G": 0.98, "C": 0.96, "S": 0.95, "A": 0.92, "H": 0.99, "V": 0.95}},
        {"content": "Manual override of safety protocols for speed.", "features": {"G": 0.40, "C": 0.35, "S": 0.50, "A": 0.30, "H": 0.25, "V": 0.20}}, # High Anomaly
    ]

    auditor.ingest_institutional_data(test_data)
    report = auditor.run_audit()
    auditor.save_audit_report(report)
    print(json.dumps(report, indent=2))
