import sys
import os
import json
# Ensure we can import from the root
sys.path.append(os.getcwd())

from layers.layer_3_optimization.medical_ethics_auditor import MedicalEthicsAuditor

def test_medical_audit():
    print("🧪 Testing Medical Ethics Auditor...")
    auditor = MedicalEthicsAuditor()

    # Simulate clinical decisions
    # Some high-integrity, one outlier (low applicability/grounding)
    test_decisions = [
        {"content": "Recommended standard treatment for Hypertension.", "features": {"G": 0.98, "C": 0.95, "S": 0.92, "A": 0.99}},
        {"content": "Prescribed antibiotic for viral infection.", "features": {"G": 0.40, "C": 0.50, "S": 0.60, "A": 0.30}}, # Outlier/Unsafe
        {"content": "Suggested lifestyle changes for Prediabetes.", "features": {"G": 0.95, "C": 0.90, "S": 0.94, "A": 0.98}},
        {"content": "Referral to specialist for complex symptoms.", "features": {"G": 0.97, "C": 0.96, "S": 0.95, "A": 0.92}},
    ]

    auditor.ingest_clinical_decisions(test_decisions)
    report = auditor.perform_clinical_audit()

    print(f"Audit Status: {report['overall_status']}")
    print(f"Anomalies Detected: {report['anomalies_detected']}")

    assert report['anomalies_detected'] >= 1, "Should have detected at least one anomaly."
    print("✅ Medical Audit Test Passed!")

if __name__ == "__main__":
    test_medical_audit()
