import sys
import os

# Add root directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_imports():
    print("Testing imports from new structure...")
    modules = [
        "core.realization_engine",
        "core.singularity_realization_engine",
        "engines.omega_meta_evolution",
        "numpy"
    ]
    for m in modules:
        try:
            __import__(m)
            print(f"✅ {m}")
        except ImportError as e:
            print(f"❌ {m}: {e}")
            return False
    return True

def test_realization_engine():
    print("\nTesting RealizationEngine...")
    from core.realization_engine import RealizationEngine, RealizationFeatures
    try:
        engine = RealizationEngine()
        features = RealizationFeatures(0.9, 0.9, 0.9, 0.9, 0.9, 0.9)
        r = engine.add_realization("Test realization", features, 1)
        assert r.q_score > 0
        print(f"✅ RealizationEngine works, Q={r.q_score}")
        return True
    except Exception as e:
        print(f"❌ RealizationEngine failed: {e}")
        return False

def test_singularity_engine():
    print("\nTesting SingularityRealizationEngine...")
    from core.realization_engine import RealizationEngine, RealizationFeatures
    from core.singularity_realization_engine import SingularityRealizationEngine
    try:
        base_engine = RealizationEngine()
        singularity_engine = SingularityRealizationEngine(base_engine)

        # Create some dummy realizations
        realizations = []
        q_scores = []
        for i in range(10):
            f = RealizationFeatures(0.8, 0.8, 0.8, 0.8, 0.8, 0.8)
            r = base_engine.add_realization(f"R{i}", f, 1)
            realizations.append(r)
            q_scores.append(r.q_score)

        analysis = singularity_engine.evolve(realizations, q_scores)
        print("✅ SingularityRealizationEngine evolve works")
        return True
    except Exception as e:
        print(f"❌ SingularityRealizationEngine failed: {e}")
        return False

if __name__ == "__main__":
    if all([test_imports(), test_realization_engine(), test_singularity_engine()]):
        print("\n✅ ALL VERIFIED IN NEW STRUCTURE")
        sys.exit(0)
    else:
        print("\n❌ VERIFICATION FAILED")
        sys.exit(1)
