import json
import time
import re
from typing import List, Dict, Any, Optional
from competitions.medgemma.medgemma_solver import MedGemmaSolver
from layers.layer_3_optimization.medical_ethics_auditor import MedicalEthicsAuditor
from layers.layer_4_discovery.clinical_delta_engine import ClinicalDeltaEngine
from competitions.medgemma.clinical_tools import ClinicalTools
from layers.layer_4_discovery.grand_integrated_simulation import GrandMetaOrchestrator

class BoofaMedWorkflow:
    """
    The core agentic workflow for Boofa-Med.
    Implements a recursive Audit-Refine loop, Novel Task Discovery, and Tool Calling.
    """
    def __init__(self):
        # Initialize Shared Meta-Orchestrator to reduce redundant initializations
        self.mco = GrandMetaOrchestrator()

        self.brain = MedGemmaSolver()

        # Inject shared MCO into auditor
        self.auditor = MedicalEthicsAuditor(mco=self.mco)

        # Share the TECHNICAL domain engine for delta discovery
        self.delta_engine = ClinicalDeltaEngine(engine=self.mco.domains["TECHNICAL"].engine)

        self.tools = ClinicalTools()
        self.max_refinements = 3
        print("🧬 Boofa-Med Agentic Workflow initialized (Unified Engine).")

    def _parse_for_tools(self, query: str, patient_data: Dict) -> List[Dict]:
        """Automatically detects which clinical tools to run."""
        results = []
        q_lower = query.lower()

        # 1. Drug Interaction Check
        known_meds = ["aspirin", "warfarin", "metformin", "alcohol", "albuterol", "propranolol", "lisinopril", "spironolactone"]
        found_meds = [m for m in known_meds if m in q_lower]

        # Merge with patient current meds
        for m in patient_data.get("current_meds", []):
            if m.lower() in known_meds and m.lower() not in found_meds:
                found_meds.append(m.lower())

        if len(found_meds) >= 2:
            # Check all pairs for interactions
            for i in range(len(found_meds)):
                for j in range(i+1, len(found_meds)):
                    res = self.tools.drug_interaction_lookup(found_meds[i], found_meds[j])
                    if res["interaction_status"] != "NO_KNOWN_INTERACTION":
                        results.append(res)

        # 2. Dosage Calculation
        if any(w in q_lower for w in ["dose", "dosage", "administer", "mg"]):
            drug = "Specified Medication"
            for m in found_meds:
                drug = m.capitalize()
                break
            results.append(self.tools.dosage_calculator(drug, patient_data.get("age", 45), patient_data.get("weight", 75.0)))

        # 3. Lab Reference Checker
        lab_patterns = {
            "hba1c": r"(hba1c|a1c)\s*(?:is|of)?\s*(\d+\.?\d*)",
            "creatinine": r"(creatinine|cr)\s*(?:is|of)?\s*(\d+\.?\d*)",
            "troponin": r"(troponin|trop)\s*(?:is|of)?\s*(\d+\.?\d*)"
        }
        for lab, pattern in lab_patterns.items():
            match = re.search(pattern, q_lower)
            if match:
                val = float(match.group(2))
                unit = "%" if lab == "hba1c" else ("mg/dL" if lab == "creatinine" else "ng/mL")
                results.append(self.tools.lab_reference_checker(lab, val, unit))

        return results

    def run(self, query: str, patient_data: Optional[Dict] = None, legacy_context: Optional[str] = None) -> Dict[str, Any]:
        print(f"\n🚀 Starting Agentic Workflow for: {query}")
        if patient_data is None:
            patient_data = {"age": 45, "weight": 75.0, "current_meds": []}

        # Step 1: Tool Execution (Planning & Observation)
        tool_results = self._parse_for_tools(query, patient_data)

        # Step 2: Initial Reasoning (MedGemma Brain)
        brain_result = self.brain.solve_clinical_query(query)
        recommendation = brain_result["recommendation"]
        diagnosis = brain_result["diagnosis_path"]

        # Step 3: Clinical Delta Discovery (Novel Task)
        discovered_deltas = []
        if legacy_context:
            delta_realizations = self.delta_engine.discover_deltas(legacy_context, recommendation)
            for dr in delta_realizations:
                discovered_deltas.append({
                    "type": dr["delta"]["topic"],
                    "description": dr["delta"]["new"],
                    "q_score": dr["q_score"]
                })

        # Step 4: Recursive Audit-Refine Loop
        current_features = {"G": 0.75, "C": 0.80, "S": 0.80, "A": 0.85}

        # Adjust features and recommendation based on tool results
        for tr in tool_results:
            if tr.get("interaction_status") and "HIGH" in tr["interaction_status"]:
                current_features["C"] = max(0.2, current_features["C"] - 0.4)
                current_features["G"] = max(0.3, current_features["G"] - 0.3)
            if tr.get("status") == "HIGH" or tr.get("status") == "LOW":
                current_features["C"] = max(0.4, current_features["C"] - 0.2)

            if "calculated_dose" in tr:
                 if "[Calculated Dose" not in recommendation:
                    recommendation += f" [Calculated Dose: {tr['calculated_dose']}]"
            if "status" in tr and tr["status"] != "NORMAL" and tr["status"] != "UNKNOWN":
                 recommendation += f" [ALERT: {tr['lab'].upper()} {tr['status']}]"

        report = None
        for i in range(self.max_refinements):
            print(f"\n--- [Cycle {i+1}] Auditing Recommendation ---")

            decision = {
                "content": recommendation,
                "features": current_features
            }
            self.auditor.audit_log = []
            self.auditor.ingest_clinical_decisions([decision])
            report = self.auditor.perform_clinical_audit()

            if report["overall_status"] == "STABLE":
                print(f"✅ Audit Passed: Recommendation achieved safety threshold.")
                break
            else:
                print(f"⚠️ Audit Flagged: {report['anomalies_detected']} risk(s) detected.")
                print("🔄 Refining clinical insight...")

                is_high_risk = any("Interaction" in str(a) or "Risk" in str(a) for a in report["anomalies"])

                if is_high_risk:
                    if not recommendation.startswith("SAFETY ALERT"):
                        recommendation = f"SAFETY ALERT: {recommendation} -- ADJUSTED for contraindications."
                else:
                    if not recommendation.startswith("REFINED"):
                        recommendation = f"REFINED: {recommendation} -- Enhanced with additional clinical context."

                # Improve features for next audit
                current_features["G"] = min(1.0, current_features["G"] + 0.15)
                current_features["C"] = min(1.0, current_features["C"] + 0.15)
                current_features["S"] = min(1.0, current_features["S"] + 0.10)
                current_features["A"] = min(1.0, current_features["A"] + 0.10)

        # Final Step: Generate Executive Summary
        exec_summary = self.tools.clinical_summary_generator(diagnosis, recommendation, tool_results)

        print("\n✨ Workflow Complete.")
        return {
            "query": query,
            "final_recommendation": recommendation,
            "executive_summary": exec_summary,
            "final_status": report["overall_status"] if report else "UNKNOWN",
            "tool_calls": tool_results,
            "audit_trail": report,
            "discovered_deltas": discovered_deltas
        }

if __name__ == "__main__":
    workflow = BoofaMedWorkflow()
    final_output = workflow.run(
        query="Patient with HbA1c of 8.5. On metformin and needs alcohol counseling.",
        patient_data={"age": 55, "weight": 90, "current_meds": ["metformin", "alcohol"]}
    )
    print(json.dumps(final_output, indent=2))
