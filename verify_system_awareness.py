import sys
import os
import json
import numpy as np
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
        folder = f"layers/layer_{l}_{'universal' if l==0 else 'domain' if l==1 else 'core' if l==2 else 'optimization' if l==3 else 'discovery' if l==4 else 'consciousness'}"
        if not check_file(folder):
            if l == 3 and check_file("layers/layer_3_orchestration"): continue
            all_ok = False
    return all_ok

def test_expanded_project_awareness():
    print("\n[Layer 2: Expanded Project Awareness]")
    projects = {
        "OmniValence Engine (L0)": "layers/layer_0_universal/omni_valence_engine.py",
        "Skill Objective Functions (L1)": "layers/layer_1_domain/math-skills.txt",
        "Hard Test Designer (L3)": "layers/layer_3_optimization/hard_test_designer.py",
        "Business Opp Engine (L4)": "layers/layer_4_discovery/business_opportunity_engine.py",
        "Phase 6 Executor (L4)": "layers/layer_4_discovery/phase_6_executor.py",
        "Self-Model Analyzer (L5)": "layers/layer_5_consciousness/self-model-analyzer.md"
    }
    all_ok = True
    for name, path in projects.items():
        if not check_file(path): all_ok = False
    return all_ok

def test_omni_valence_logic():
    print("\n[Layer 3: Omni-Valence Logic Verification]")
    try:
        from layers.layer_0_universal.omni_valence_engine import OmniValenceEngine
        from layers.layer_2_core.realization_engine import Realization, RealizationFeatures

        ove = OmniValenceEngine()
        r1 = Realization("R1", "Fact A", RealizationFeatures(0.9, 0.9, 0.9, 0.9, 0.9, 0.9), 0.9, 1, "", [], [], 1, "STRATEGIC", [])
        r2 = Realization("R2", "Fact B", RealizationFeatures(0.95, 0.95, 0.95, 0.95, 0.95, 0.95), 0.95, 1, "", [], [], 1, "TECHNICAL", [])

        merged = ove.merge_realizations([r1, r2])
        print(f"  ✅ Omni-Valence Merger: Q = {merged.q_score:.4f} (Synergy Gain: {merged.q_score - 0.925:.4f})")
        return merged.q_score > 1.0
    except Exception as e:
        print(f"  ❌ Omni-Valence Logic Failed: {e}")
        return False

def test_realization_dataset_integrity():
    print("\n[Layer 4: Dataset Integrity Check]")
    path = "layers/layer_1_domain/comprehensive_realization_dataset.json"
    if not os.path.exists(path):
        print(f"  ❌ Dataset missing: {path}")
        return False

    try:
        with open(path, 'r') as f:
            data = json.load(f)
        avg_q = data.get("stats", {}).get("avg_q_score", 0)
        count = data.get("stats", {}).get("total_realizations", 0)
        print(f"  ✅ Dataset Loaded: {count} realizations, Avg Q: {avg_q:.4f}")
        return count > 0
    except Exception as e:
        print(f"  ❌ Dataset Integrity Failed: {e}")
        return False

if __name__ == "__main__":
    print("="*60)
    print("BOOFA-SKILER ADVANCED SYSTEM AWARENESS VERIFICATION")
    print("="*60)

    results = [
        test_layer_structure(),
        test_expanded_project_awareness(),
        test_omni_valence_logic(),
        test_realization_dataset_integrity()
    ]

    print("\n" + "="*60)
    if all(results):
        print("🎉 ALL ADVANCED VERIFICATION CHECKS PASSED.")
    else:
        print("⚠️ SOME VERIFICATION CHECKS FAILED.")
        sys.exit(1)
    print("="*60)
