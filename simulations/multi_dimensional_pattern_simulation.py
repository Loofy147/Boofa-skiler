import numpy as np
from core.realization_engine import RealizationEngine, RealizationFeatures, Realization
from core.singularity_realization_engine import SingularityRealizationEngine
from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Tuple
import json
import time

@dataclass
class SimulationConfig:
    name: str
    logic_type: str
    weight_adaptation_rate: float
    meta_synergy_enabled: bool
    description: str

class PatternSimulator:
    def __init__(self, config: SimulationConfig):
        self.config = config
        self.base_engine = RealizationEngine()
        self.singularity = SingularityRealizationEngine(self.base_engine)

    def calculate_q_new_logic(self, features: RealizationFeatures) -> float:
        f_dict = asdict(features)
        weights = {dim.id: dim.weight for dim in self.singularity.dimensions.values()}
        mapping = {'grounding': 'G', 'certainty': 'C', 'structure': 'S', 'applicability': 'A', 'coherence': 'H', 'generativity': 'V'}

        if self.config.logic_type == 'linear':
            return sum(weights[mapping[k]] * f_dict[k] for k in mapping)
        elif self.config.logic_type == 'product':
            weighted_sum = sum(weights[mapping[k]] * f_dict[k] for k in mapping)
            geo_mean = np.exp(np.mean([np.log(max(v, 0.01)) for v in f_dict.values()]))
            return weighted_sum * (0.6 + 0.4 * geo_mean)
        elif self.config.logic_type == 'threshold_exponential':
            total = 0.0
            for k, m in mapping.items():
                w = weights[m]
                val = f_dict[k]
                if val >= 0.9: total += w * (val ** 1.5)
                else: total += w * val
            return min(total, 1.0)
        return 0.0

    def apply_meta_synergy(self, q_score: float, features: RealizationFeatures) -> float:
        if not self.config.meta_synergy_enabled: return q_score
        factor = 1.0
        if features.certainty > features.grounding + 0.2: factor *= 0.7
        if features.structure > 0.9 and features.generativity > 0.9: factor *= 1.1
        return min(q_score * factor, 1.0)

    def run(self, dataset: List[Dict]):
        print(f"\n--- {self.config.name} ---")
        realizations = []
        actual_qs = []
        for i, data in enumerate(dataset):
            features = RealizationFeatures(**data['features'])
            q = self.apply_meta_synergy(self.calculate_q_new_logic(features), features)
            r = self.base_engine.add_realization(content=f"{data['content']} {i}", features=features, turn_number=1)
            actual_qs.append(q)
            realizations.append(r)

        print(f"Dataset size: {len(realizations)}")
        analysis = self.singularity.evolve(realizations, actual_qs)

        # Second pass to see weight adaptation
        print("\nSecond pass for adaptation...")
        analysis = self.singularity.evolve(realizations, actual_qs)

        return {
            'config': asdict(self.config),
            'avg_q': np.mean(actual_qs),
            'final_weights': {dim.name: dim.weight for dim in self.singularity.dimensions.values()},
            'variance_explained': analysis.get('variance_explained', {})
        }

def generate_large_dataset(n=30):
    ds = []
    for i in range(n):
        if i % 3 == 0: # High Grounding
            ds.append({'content': "Science", 'features': {'grounding': 0.95, 'certainty': 0.70, 'structure': 0.85, 'applicability': 0.90, 'coherence': 0.95, 'generativity': 0.80}})
        elif i % 3 == 1: # Overconfident
            ds.append({'content': "Hype", 'features': {'grounding': 0.15, 'certainty': 0.99, 'structure': 0.90, 'applicability': 0.40, 'coherence': 0.30, 'generativity': 0.70}})
        else: # Balanced
            ds.append({'content': "Logic", 'features': {'grounding': 0.90, 'certainty': 0.90, 'structure': 0.90, 'applicability': 0.90, 'coherence': 0.90, 'generativity': 0.90}})
    return ds

if __name__ == "__main__":
    dataset = generate_large_dataset(30)
    configs = [
        SimulationConfig("Baseline", "linear", 0.1, False, "Standard."),
        SimulationConfig("Synergy", "product", 0.2, True, "Synergistic."),
        SimulationConfig("Excellence", "threshold_exponential", 0.2, True, "Excellence.")
    ]
    results = [PatternSimulator(cfg).run(dataset) for cfg in configs]
    with open('simulation_final_results.json', 'w') as f: json.dump(results, f, indent=2)
    print("\n✅ Simulation Complete.")
