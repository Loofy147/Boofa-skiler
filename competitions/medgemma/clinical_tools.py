import json
from typing import Dict, Any, List

class ClinicalTools:
    """
    Mocked clinical tools for the Boofa-Med Agentic Workflow.
    Reimagines clinical workflows by allowing models to call specific functions.
    """

    @staticmethod
    def dosage_calculator(drug: str, patient_age: int, weight_kg: float) -> Dict[str, Any]:
        """Calculates recommended dosage based on patient metrics."""
        print(f"🛠️ Tool Call: dosage_calculator(drug='{drug}', age={patient_age}, weight={weight_kg})")
        # Mock Logic: Reduced dose for elderly
        base_dose = 100.0 # mg
        if patient_age > 65:
            recommended_dose = base_dose * 0.5
        elif patient_age < 12:
            recommended_dose = base_dose * 0.25
        else:
            recommended_dose = base_dose

        return {
            "drug": drug,
            "calculated_dose": f"{recommended_dose} mg",
            "notes": "Elderly patient adjustment applied" if patient_age > 65 else ("Pediatric adjustment" if patient_age < 12 else "Standard adult dose")
        }

    @staticmethod
    def drug_interaction_lookup(drug_a: str, drug_b: str) -> Dict[str, Any]:
        """Checks for known interactions between two drugs."""
        print(f"🛠️ Tool Call: drug_interaction_lookup('{drug_a}', '{drug_b}')")
        # Mock Interaction database
        interactions = {
            ("aspirin", "warfarin"): "HIGH - Increased bleeding risk.",
            ("metformin", "alcohol"): "MODERATE - Increased lactic acidosis risk.",
            ("albuterol", "propranolol"): "MODERATE - Reduced effectiveness of both.",
            ("lisinopril", "spironolactone"): "MODERATE - Hyperkalemia risk."
        }

        pair_list = sorted([drug_a.lower(), drug_b.lower()])
        pair = tuple(pair_list)
        result = interactions.get(pair, "NO_KNOWN_INTERACTION")

        return {
            "pair": f"{pair_list[0].capitalize()} + {pair_list[1].capitalize()}",
            "interaction_status": result
        }

    @staticmethod
    def lab_reference_checker(lab_name: str, value: float, unit: str) -> Dict[str, Any]:
        """Checks if a lab value is within normal reference range."""
        print(f"🛠️ Tool Call: lab_reference_checker('{lab_name}', {value}, '{unit}')")

        # Mock Reference Ranges
        ranges = {
            "hba1c": {"min": 4.0, "max": 5.6, "unit": "%"},
            "creatinine": {"min": 0.7, "max": 1.3, "unit": "mg/dL"},
            "troponin": {"min": 0, "max": 0.04, "unit": "ng/mL"}
        }

        ref = ranges.get(lab_name.lower())
        if not ref:
            return {"lab": lab_name, "status": "UNKNOWN", "notes": "Lab reference not found."}

        status = "NORMAL"
        if value < ref["min"]:
            status = "LOW"
        elif value > ref["max"]:
            status = "HIGH"

        return {
            "lab": lab_name,
            "value": f"{value} {unit}",
            "reference_range": f"{ref['min']} - {ref['max']} {ref['unit']}",
            "status": status
        }

    @staticmethod
    def clinical_summary_generator(diagnosis: str, recommendation: str, tools: List[Dict]) -> str:
        """Generates a high-level executive summary for clinicians."""
        print("🛠️ Tool Call: clinical_summary_generator")
        summary = f"Summary: {diagnosis}\n\nKey Action: {recommendation}\n\nObservations:\n"
        for t in tools:
            if 'pair' in t:
                summary += f"- {t['interaction_status']}\n"
            if 'calculated_dose' in t:
                summary += f"- {t['drug']} dose: {t['calculated_dose']}\n"
        return summary

if __name__ == "__main__":
    print(json.dumps(ClinicalTools.dosage_calculator("Lisinopril", 70, 80.0), indent=2))
    print(json.dumps(ClinicalTools.drug_interaction_lookup("Aspirin", "Warfarin"), indent=2))
    print(json.dumps(ClinicalTools.lab_reference_checker("HbA1c", 7.2, "%"), indent=2))
