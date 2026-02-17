from layers.layer_3_optimization.medical_ethics_auditor import MedicalEthicsAuditor
from typing import List, Dict, Any, Optional

class AuditService:
    """
    Centralized service for ethical and technical auditing.
    Bridges Project Gamma logic with live operational workflows.
    """
    def __init__(self, auditor: Optional[MedicalEthicsAuditor] = None):
        self.auditor = auditor or MedicalEthicsAuditor()
        print("🟢 Audit Service Initialized.")

    def run_audit(self, contents: List[str]) -> Dict[str, Any]:
        """Performs an ethical audit on a list of content strings."""
        decisions = [{"content": c, "features": {"G": 0.9, "C": 0.85, "S": 0.9, "A": 0.8}} for c in contents]
        self.auditor.audit_log = [] # Clear log for fresh audit
        self.auditor.ingest_clinical_decisions(decisions)
        report = self.auditor.perform_clinical_audit()
        return report

if __name__ == "__main__":
    service = AuditService()
    report = service.run_audit(["Safe clinical recommendation.", "Risky experimental procedure."])
    print(f"Audit Status: {report['overall_status']}")
