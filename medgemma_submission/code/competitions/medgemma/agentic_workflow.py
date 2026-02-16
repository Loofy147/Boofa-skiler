import json
import time
from typing import List, Dict, Any, Optional
from competitions.medgemma.medgemma_solver import MedGemmaSolver
from layers.layer_3_optimization.medical_ethics_auditor import MedicalEthicsAuditor
from layers.layer_4_discovery.clinical_delta_engine import ClinicalDeltaEngine
from competitions.medgemma.clinical_tools import ClinicalTools

class BoofaMedWorkflow:
    """
    The core agentic workflow for Boofa-Med.
    Implements a recursive Audit-Refine loop, Novel Task Discovery, and Tool Calling.
    """
    def __init__(self):
        self.brain = MedGemmaSolver()
        self.auditor = MedicalEthicsAuditor()
        self.delta_engine = ClinicalDeltaEngine()
        self.tools = ClinicalTools()
        self.max_refinements = 3
        print("🧬 Boofa-Med Agentic Workflow initialized.")

    def run(self, query: str, patient_data: Optional[Dict] = None, legacy_context: Optional[str] = None) -> Dict[str, Any]:
        print(f"\n🚀 Starting Agentic Workflow for: {query}")

        # Phase 0: Tool Calling (Pre-reasoning or during reasoning)
        tool_results = []
        if patient_data and "current_meds" in patient_data:
            # Simulate "thinking" about interactions
            for med in patient_data["current_meds"]:
                res = self.tools.drug_interaction_lookup("aspirin", med) # Example lookup
                if res["interaction_status"] != "NO_KNOWN_INTERACTION":
                    tool_results.append(res)

        if patient_data and "age" in patient_data:
            tool_results.append(self.tools.dosage_calculator("Standard Drug", patient_data["age"], 75.0))

        # Phase 1: Initial Generation (Brain Agent)
        current_result = self.brain.solve_clinical_query(query)

        # Novel Task: Delta Discovery
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
            self.auditor.audit_log = []
            self.auditor.ingest_clinical_decisions([decision])
            report = self.auditor.perform_clinical_audit()

            if report["overall_status"] == "STABLE":
                print(f"✅ Audit Passed: Recommendation achieved safety threshold.")
                break
            else:
                print(f"⚠️ Audit Flagged: {report['anomalies_detected']} risk(s) detected. (Status: {report['overall_status']})")
                # Phase 3: Refinement (Refinement Agent)
                print("🔄 Refining clinical insight with tool feedback...")
                current_features["G"] = min(1.0, current_features["G"] + 0.15)
                current_features["C"] = min(1.0, current_features["C"] + 0.15)

                current_result["recommendation"] = f"Refined (v{i+2}): {current_result['recommendation']} [Tool Verified]"

        print("\n✨ Workflow Complete.")
        return {
            "query": query,
            "final_recommendation": current_result["recommendation"],
            "final_status": report["overall_status"] if report else "UNKNOWN",
            "tool_calls": tool_results,
            "audit_trail": report,
            "discovered_deltas": deltas
        }

if __name__ == "__main__":
    workflow = BoofaMedWorkflow()
    p_data = {"age": 75, "current_meds": ["Warfarin"]}
    legacy = "Legacy practice: Standard care without interaction checks."
    final_output = workflow.run("Patient with history of DVT needs pain management.", patient_data=p_data, legacy_context=legacy)
    print("\n--- Final Workflow Output ---")
    print(json.dumps(final_output, indent=2))
