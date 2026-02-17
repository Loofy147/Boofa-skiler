import json
from typing import Dict, Any

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

if __name__ == "__main__":
    print(json.dumps(ClinicalTools.dosage_calculator("Lisinopril", 70, 80.0), indent=2))
    print(json.dumps(ClinicalTools.drug_interaction_lookup("Aspirin", "Warfarin"), indent=2))
