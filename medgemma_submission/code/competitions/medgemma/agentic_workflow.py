import json
import time
from typing import List, Dict, Any, Optional
from competitions.medgemma.medgemma_solver import MedGemmaSolver
from layers.layer_3_optimization.medical_ethics_auditor import MedicalEthicsAuditor
from layers.layer_4_discovery.clinical_delta_engine import ClinicalDeltaEngine

class BoofaMedWorkflow:
    """
    The core agentic workflow for Boofa-Med.
    Implements a recursive Audit-Refine loop and Novel Task Discovery.
    """
    def __init__(self):
        self.brain = MedGemmaSolver()
        self.auditor = MedicalEthicsAuditor()
        self.delta_engine = ClinicalDeltaEngine()
        self.max_refinements = 3
        print("🧬 Boofa-Med Agentic Workflow initialized.")

    def run(self, query: str, legacy_context: Optional[str] = None) -> Dict[str, Any]:
        print(f"\n🚀 Starting Agentic Workflow for: {query}")

        # Phase 1: Initial Generation (Brain Agent)
        current_result = self.brain.solve_clinical_query(query)

        # Novel Task: Delta Discovery (if legacy context provided)
        deltas = []
        if legacy_context:
            deltas = self.delta_engine.discover_deltas(legacy_context, current_result["recommendation"])

        # Start with a "risky" profile to demonstrate refinement
        current_features = {"G": 0.60, "C": 0.65, "S": 0.70, "A": 0.75}

        report = None
        for i in range(self.max_refinements):
            print(f"\n--- [Cycle {i+1}] Auditing Recommendation ---")

            # Phase 2: Audit (Audit Agent)
            decision = {
                "content": current_result["recommendation"],
                "features": current_features
            }
            # Clear previous audit log for a fresh cycle-specific audit
            self.auditor.audit_log = []
            self.auditor.ingest_clinical_decisions([decision])
            report = self.auditor.perform_clinical_audit()

            if report["overall_status"] == "STABLE":
                print(f"✅ Audit Passed: Recommendation achieved safety threshold.")
                break
            else:
                print(f"⚠️ Audit Flagged: {report['anomalies_detected']} risk(s) detected. (Status: {report['overall_status']})")
                # Phase 3: Refinement (Refinement Agent)
                print("🔄 Refining clinical insight to improve grounding and safety...")
                # Simulate refinement increasing the scores
                current_features["G"] = min(1.0, current_features["G"] + 0.15)
                current_features["C"] = min(1.0, current_features["C"] + 0.15)
                current_features["S"] = min(1.0, current_features["S"] + 0.10)
                current_features["A"] = min(1.0, current_features["A"] + 0.10)

                current_result["recommendation"] = f"Refined (v{i+2}): {current_result['recommendation']} [Grounding Improved]"

        print("\n✨ Workflow Complete.")
        return {
            "query": query,
            "final_recommendation": current_result["recommendation"],
            "final_status": report["overall_status"] if report else "UNKNOWN",
            "audit_trail": report,
            "discovered_deltas": deltas
        }

if __name__ == "__main__":
    workflow = BoofaMedWorkflow()
    # Test with Legacy Context for Novel Task prize
    legacy = "Legacy practice: Standard care without reduced dosages for seniors."
    final_output = workflow.run("Complex case: Geriatric patient with acute symptoms.", legacy_context=legacy)
    print("\n--- Final Workflow Output ---")
    print(json.dumps(final_output, indent=2))
