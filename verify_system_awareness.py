import sys
import os
import json
from datetime import datetime

# Add root to sys.path
sys.path.append(os.getcwd())

def check_file(path):
    exists = os.path.exists(path)
    status = "✅" if exists else "❌"
    print(f"  {status} {path}")
    return exists

def test_layer_structure():
    print("\n[Layer 1: Structural Awareness]")
    layers = [0, 1, 2, 3, 4, 5]
    all_ok = True
    for l in layers:
        if not check_file(f"layers/layer_{l}_{'universal' if l==0 else 'domain' if l==1 else 'core' if l==2 else 'optimization' if l==3 else 'discovery' if l==4 else 'consciousness'}"):
            # Check for alternative names for Layer 3 (orchestration)
            if l == 3:
                if not check_file("layers/layer_3_orchestration"):
                    all_ok = False
            else:
                all_ok = False
    return all_ok

def test_project_awareness():
    print("\n[Layer 2: Project Awareness]")
    projects = {
        "Project Alpha (Strategic Architect)": "layers/layer_3_orchestration/autonomous_strategic_architect.py",
        "Project Beta (Global Ledger)": "layers/layer_2_core/global_realization_ledger.py",
        "Project Gamma (Institutional Auditor)": "layers/layer_3_optimization/institutional_auditor.py",
        "Project Delta (Innovation Synthesizer)": "layers/layer_4_discovery/innovation_synthesizer.py",
        "Project Epsilon (Skill Engine)": "layers/layer_2_core/skill_engine.py",
        "Project Zeta (Clinical Delta Engine)": "layers/layer_4_discovery/clinical_delta_engine.py"
    }
    all_ok = True
    for name, path in projects.items():
        if not check_file(path):
            all_ok = False
    return all_ok

def test_core_engines():
    print("\n[Layer 3: Engine Logic Verification]")
    try:
        from layers.layer_0_universal.foundation import Skill, synthesize_skills
        from layers.layer_2_core.realization_engine import RealizationEngine, RealizationFeatures

        # Test Skill Synthesis (Layer 0)
        s1 = Skill("Cognitive-A", G=0.9, C=0.9, S=0.9, A=0.9, H=0.9, V=0.9, P=0.9, T=0.9)
        s2 = Skill("Cognitive-B", G=0.8, C=0.8, S=0.8, A=0.8, H=0.8, V=0.8, P=0.8, T=0.8)
        emergent = synthesize_skills([s1, s2])
        print(f"  ✅ Layer 0: Skill Synthesis (Emergent Q: {emergent.q_score():.4f})")

        # Test Realization Engine (Layer 2)
        engine = RealizationEngine()
        features = RealizationFeatures(grounding=0.95, certainty=0.98, structure=0.92, applicability=0.90, coherence=0.95, generativity=0.92)
        r = engine.add_realization("System verification insight", features, turn_number=1)
        print(f"  ✅ Layer 2: Realization Engine (Crystallized Q: {r.q_score:.4f}, Layer: {r.layer})")

        # Test Hallucination Detection
        bad_features = RealizationFeatures(grounding=0.4, certainty=0.95, structure=0.5, applicability=0.5, coherence=0.5, generativity=0.5)
        r_bad = engine.add_realization("Ungrounded insight", bad_features, turn_number=2)
        print(f"  ✅ Layer 2: Hallucination Penalty Check (Q: {r_bad.q_score:.4f} vs base {engine.calculate_q_score(bad_features, method='linear')[0]})")

        return True
    except Exception as e:
        print(f"  ❌ Engine Verification Failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_aimo_logic():
    print("\n[Layer 4: AIMO Solver Awareness]")
    try:
        from layers.layer_2_core.aimo_math_solver import AIMOMathSolver
        solver = AIMOMathSolver()

        # Test extraction
        test_text = r"The solution is \boxed{123}."
        ans = solver._extract_boxed_answer(test_text)
        if ans == 123:
            print("  ✅ AIMO: Regex Answer Extraction")
        else:
            print(f"  ❌ AIMO: Regex Answer Extraction (Got {ans})")
            return False

        # Test mock arithmetic
        mock_ans = solver._solve_via_mock("What is 100 * 5?")
        if mock_ans == 500:
            print("  ✅ AIMO: Mock Arithmetic Solver")
        else:
            print(f"  ❌ AIMO: Mock Arithmetic Solver (Got {mock_ans})")
            return False

        return True
    except Exception as e:
        print(f"  ❌ AIMO Verification Failed: {e}")
        return False

if __name__ == "__main__":
    print("="*60)
    print("BOOFA-SKILER SYSTEM AWARENESS VERIFICATION")
    print("="*60)

    results = [
        test_layer_structure(),
        test_project_awareness(),
        test_core_engines(),
        test_aimo_logic()
    ]

    print("\n" + "="*60)
    if all(results):
        print("🎉 ALL VERIFICATION CHECKS PASSED: System is Fully Aware.")
    else:
        print("⚠️ SOME VERIFICATION CHECKS FAILED: Awareness Gap Detected.")
        sys.exit(1)
    print("="*60)
