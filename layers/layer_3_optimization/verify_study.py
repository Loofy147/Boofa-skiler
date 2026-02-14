import sys
import os

# Add root to sys.path
sys.path.append(os.getcwd())

def test_imports():
    print("Testing imports from new structure...")
    try:
        from layers.layer_2_core.realization_engine import RealizationEngine
        print("✅ layers.layer_2_core.realization_engine")
    except ImportError as e:
        print(f"❌ layers.layer_2_core.realization_engine: {e}")
        return False

    try:
        from layers.layer_4_discovery.singularity_realization_engine import SingularityRealizationEngine
        print("✅ layers.layer_4_discovery.singularity_realization_engine")
    except ImportError as e:
        print(f"❌ layers.layer_4_discovery.singularity_realization_engine: {e}")
        return False

    return True

def test_realization_engine():
    print("\nTesting RealizationEngine...")
    from layers.layer_2_core.realization_engine import RealizationEngine, RealizationFeatures

    engine = RealizationEngine()
    features = RealizationFeatures(0.9, 0.9, 0.9, 0.9, 0.9, 0.9)
    engine.add_realization("Test realization", features, turn_number=1)

    if engine.stats['total_realizations'] == 1:
        print("✅ RealizationEngine works, Q=0.9")
        return True
    return False

def test_singularity_engine():
    print("\nTesting SingularityRealizationEngine...")
    from layers.layer_2_core.realization_engine import RealizationEngine, RealizationFeatures
    from layers.layer_4_discovery.singularity_realization_engine import SingularityRealizationEngine

    base_engine = RealizationEngine()
    realizations = []
    q_scores = []
    for i in range(10):
        features = RealizationFeatures(0.8 + (i*0.01), 0.8 - (i*0.01), 0.8, 0.8, 0.8, 0.8)
        r = base_engine.add_realization(f"R{i}", features, turn_number=i)
        realizations.append(r)
        q_scores.append(r.q_score)

    s_engine = SingularityRealizationEngine(base_engine=base_engine)
    s_engine.evolve(realizations, q_scores)
    print("✅ SingularityRealizationEngine evolve works")
    return True

if __name__ == "__main__":
    if all([test_imports(), test_realization_engine(), test_singularity_engine()]):
        print("\n✅ VERIFICATION SUCCESSFUL")
    else:
        print("\n❌ VERIFICATION FAILED")
        sys.exit(1)
