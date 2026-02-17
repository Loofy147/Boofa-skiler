from layers.layer_2_core.realization_engine import RealizationEngine, RealizationFeatures

def test_engine_evolution():
    print("Testing Realization Engine Evolution...")
    engine = RealizationEngine()

    # Check initial weights
    print(f"Initial weights: {engine.weights}")

    # Add 50 realizations to trigger evolution
    for i in range(50):
        features = RealizationFeatures(
            grounding=0.9, certainty=0.9, structure=0.9,
            applicability=0.9, coherence=0.9, generativity=0.9
        )
        engine.add_realization(f"Insight #{i}", features, turn_number=i)

    # Check if weight evolution happened
    print(f"Post-evolution weights: {engine.weights}")
    print(f"Evolution count: {engine.stats['weight_evolution_count']}")

    if engine.stats['weight_evolution_count'] > 0:
        print("✅ Evolution triggered successfully!")
        return True
    else:
        print("❌ Evolution NOT triggered.")
        return False

if __name__ == "__main__":
    if test_engine_evolution():
        print("Test Passed")
    else:
        print("Test Failed")
