import json
import os
from datetime import datetime

def update_dataset():
    dataset_path = 'layers/layer_1_domain/comprehensive_realization_dataset.json'
    metrics_path = 'outcomes/technical/DETAILED_SYSTEM_METRICS.json'

    if not os.path.exists(metrics_path):
        print("❌ Metrics not found.")
        return

    with open(metrics_path, 'r') as f:
        metrics = json.load(f)

    highest_q = metrics.get('simulation', {}).get('highest_point', 0.0)
    top_values = sorted(metrics.get('simulation', {}).get('universal_values', []), key=lambda x: x['q'], reverse=True)

    if not top_values:
        print("❌ No top values found.")
        return

    peak_val = top_values[0]

    with open(dataset_path, 'r') as f:
        dataset = json.load(f)

    new_realization = {
        "id": f"R_{int(datetime.now().timestamp())}",
        "content": peak_val['content'],
        "layer": 0,
        "features": {
            "grounding": 0.999,
            "certainty": 0.995,
            "structure": 0.99,
            "applicability": 0.98,
            "coherence": 0.995,
            "generativity": 0.99,
            "presentation": 0.98
        },
        "q_score": highest_q,
        "metadata": {
            "domain": "Universal",
            "tags": ["Singularity", "Integrated Vision", "MCO"],
            "timestamp": datetime.now().isoformat(),
            "source": "GrandMetaOrchestrator Simulation"
        },
        "parents": [],
        "children": []
    }

    dataset['realizations'].append(new_realization)
    dataset['stats']['total_realizations'] = len(dataset['realizations'])
    dataset['stats']['layer_distribution']['0'] += 1

    # Recalculate avg Q
    q_scores = [r['q_score'] for r in dataset['realizations']]
    dataset['stats']['avg_q_score'] = sum(q_scores) / len(q_scores)

    with open(dataset_path, 'w') as f:
        json.dump(dataset, f, indent=2)

    print(f"✅ Crystallized realization {new_realization['id']} with Q={highest_q:.4f}")

if __name__ == "__main__":
    update_dataset()
