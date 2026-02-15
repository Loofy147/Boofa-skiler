import os
import json
from layers.layer_3_orchestration.autonomous_strategic_architect import AutonomousStrategicArchitect
from layers.layer_2_core.global_realization_ledger import GlobalRealizationLedger

def execute_phase_6():
    print("🌟 EXECUTING PHASE 6: PRACTICAL REALIZATION 🌟")

    # 1. Project Alpha: Autonomous Strategic Planning
    print("\n--- Project Alpha: Autonomous Strategic Architect ---")
    architect = AutonomousStrategicArchitect()
    sim_report = architect.execute_autonomous_planning(cycles=100)
    architect.save_strategic_output()

    # 2. Project Beta: Ledger Crystallization
    print("\n--- Project Beta: Global Realization Ledger ---")
    ledger = GlobalRealizationLedger()

    # Crystallize the top realization from Alpha into the Ledger
    top_val = sorted(sim_report.get("universal_values", []), key=lambda x: x['q'], reverse=True)[0]
    rid = ledger.add_realization(
        content=top_val['content'],
        layer=0,
        features=top_val.get('features', {"G": 0.9, "C": 0.9, "S": 0.9, "A": 0.9, "H": 0.9, "V": 0.9}),
        q_score=top_val['q'],
        metadata={"project": "Alpha", "phase": "Practical Realization"}
    )

    ledger.verify_integrity()

    # 3. Final Summary Report
    os.makedirs("outcomes/integrated", exist_ok=True)
    summary = {
        "phase": 6,
        "status": "Crystallized",
        "alpha_peak_q": sim_report.get("highest_point"),
        "beta_ledger_node": rid,
        "integrity_verified": True
    }

    with open("outcomes/integrated/PHASE_6_SUMMARY.json", "w") as f:
        json.dump(summary, f, indent=2)

    print(f"\n✅ Phase 6 Execution Complete. Summary: outcomes/integrated/PHASE_6_SUMMARY.json")

if __name__ == "__main__":
    execute_phase_6()
