import os
import json
import sys
from datetime import datetime

# Add root to sys.path
sys.path.append(os.getcwd())

from layers.layer_3_optimization.institutional_auditor import InstitutionalAuditor

def main():
    print("🛡️ INITIALIZING RECURSIVE SELF-AUDIT PROTOCOL 🛡️")
    print("================================================")

    auditor = InstitutionalAuditor()
    ledger_path = "layers/layer_1_domain/comprehensive_realization_dataset.json"

    if not os.path.exists(ledger_path):
        print("⚠️ Ledger not found. Skipping audit.")
        return

    print(f"📖 Loading ledger from {ledger_path}...")
    with open(ledger_path, "r") as f:
        data = json.load(f)

    realizations = data.get("realizations", [])

    # Ingest system realizations for auditing
    audit_data = []
    for r in realizations:
        # Convert realization to audit point
        f = r.get('features', {})
        audit_data.append({
            "content": f"System Realization: {r['content'][:100]}...",
            "features": {
                "G": f.get('grounding', 0.8),
                "C": f.get('certainty', 0.8),
                "S": f.get('structure', 0.8),
                "A": f.get('applicability', 0.8),
                "H": f.get('coherence', 0.8),
                "V": f.get('generativity', 0.8)
            }
        })

    print(f"🕵️ Auditing {len(audit_data)} system-generated points...")
    auditor.ingest_institutional_data(audit_data)
    report = auditor.run_audit()
    auditor.save_audit_report(report)

    print("\n--- 📊 Audit Results Summary ---")
    print(f"Status: {report['status']}")
    print(f"Avg Ethical Q: {report.get('avg_ethical_q', 0.0):.4f}")
    print(f"Risk Incidents: {report.get('risk_incidents', 0)}")
    print(f"Anomalies Detected: {report.get('anomalies_detected', 0)}")

    if report['status'] != "PASS":
        print("\n⚠️ WARNING: Structural drift or bias detected in recursive loop.")
        for anomaly in report.get('anomalies', []):
            print(f"  - [{anomaly['type']}] {anomaly['content']}")
    else:
        print("\n✅ SYSTEM INTEGRITY VERIFIED: No major drift detected.")

    print("================================================")

if __name__ == "__main__":
    main()
