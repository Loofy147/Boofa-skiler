import os
import json
from datetime import datetime
from layers.layer_3_orchestration.autonomous_strategic_architect import AutonomousStrategicArchitect
from layers.layer_2_core.global_realization_ledger import GlobalRealizationLedger
from layers.layer_3_optimization.institutional_auditor import InstitutionalAuditor
from layers.layer_4_discovery.innovation_synthesizer import InnovationSynthesizer
from layers.layer_2_core.skill_engine import SkillEngine

def execute_phase_6():
    print("🌟 EXECUTING PHASE 6: MASTER PRACTICAL REALIZATION 🌟")

    # 1. Project Alpha: Autonomous Strategic Planning
    print("\n--- Project Alpha: Autonomous Strategic Architect ---")
    architect = AutonomousStrategicArchitect()
    sim_report = architect.execute_autonomous_planning(cycles=100)
    architect.save_strategic_output()

    # 2. Project Beta: Ledger Crystallization
    print("\n--- Project Beta: Global Realization Ledger ---")
    ledger = GlobalRealizationLedger()
    top_val = sorted(sim_report.get("universal_values", []), key=lambda x: x['q'], reverse=True)[0]
    rid = ledger.add_realization(
        content=top_val['content'],
        layer=0,
        features=top_val.get('features', {"G": 0.9, "C": 0.9, "S": 0.9, "A": 0.9, "H": 0.9, "V": 0.9}),
        q_score=top_val['q'],
        metadata={"project": "Alpha", "phase": "Practical Realization"}
    )
    ledger.verify_integrity()

    # 3. Project Gamma: Institutional Auditor
    print("\n--- Project Gamma: Institutional Auditor ---")
    auditor = InstitutionalAuditor()
    # Feed all universal realizations from Alpha for auditing
    audit_data = [{"content": r['content'], "features": {"G": 0.9, "C": 0.9, "S": 0.9, "A": 0.9, "H": 0.9, "V": 0.9}} for r in sim_report.get("universal_values", [])]
    auditor.ingest_institutional_data(audit_data)
    audit_report = auditor.run_audit()
    auditor.save_audit_report(audit_report)

    # 4. Project Delta: Innovation Synthesizer
    print("\n--- Project Delta: Innovation Synthesizer ---")
    synthesizer = InnovationSynthesizer()
    synthesizer.synthesize_innovations("Phase 6 Master Integration", cycles=50)
    synthesizer.visualize_graph(f"MASTER_INTEGRATION_{datetime.now().strftime('%H%M%S')}.png")
    synthesizer.save_innovation_report()

    # 5. Project Epsilon: Skill Engine
    print("\n--- Project Epsilon: Skill Engine ---")
    skill_engine = SkillEngine()
    # Collect all universal realizations for skill detection
    all_universal = architect.mco.universal_realizations + synthesizer.mco.universal_realizations
    new_skills = skill_engine.detect_and_generate_skills(all_universal)

    # 6. Final Master Summary
    os.makedirs("outcomes/integrated", exist_ok=True)
    summary = {
        "phase": 6,
        "timestamp": datetime.now().isoformat(),
        "status": "Crystallized",
        "projects_realized": ["Alpha", "Beta", "Gamma", "Delta", "Epsilon"],
        "metrics": {
            "alpha_peak_q": sim_report.get("highest_point"),
            "beta_ledger_node": rid,
            "gamma_audit_status": audit_report["status"],
            "delta_innovation_count": len(synthesizer.innovation_events),
            "epsilon_skills_generated": new_skills
        }
    }

    with open("outcomes/integrated/PHASE_6_MASTER_SUMMARY.json", "w") as f:
        json.dump(summary, f, indent=2)

    print(f"\n✅ Phase 6 Master Execution Complete.")
    print(f"📄 Summary: outcomes/integrated/PHASE_6_MASTER_SUMMARY.json")

if __name__ == "__main__":
    execute_phase_6()
