import sys
import os
import json
from datetime import datetime

# Add root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from layers.layer_2_core.realization_engine import RealizationEngine, RealizationFeatures

def load_dataset():
    path = "layers/layer_1_domain/comprehensive_realization_dataset.json"
    with open(path, "r") as f:
        return json.load(f)

def save_dataset(data):
    path = "layers/layer_1_domain/comprehensive_realization_dataset.json"
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def main():
    print("🚀 Feeding Research Paper: AI Unit Economics 2026...")

    engine = RealizationEngine()

    findings = [
        {
            "content": "AI Inference Cost Collapse: GPT-4 class inference cost fell from $20/M tokens in 2022 to $0.40/M tokens in 2026 (50x reduction).",
            "features": RealizationFeatures(0.99, 1.0, 0.98, 0.95, 0.99, 0.92)
        },
        {
            "content": "Optimization Stack ROI: A combination of routing, caching, RAG, and quantization delivers 60–98% cost reduction in production.",
            "features": RealizationFeatures(0.95, 0.98, 0.95, 1.0, 0.96, 0.94)
        },
        {
            "content": "Self-Hosting Break-Even: For premium APIs, self-hosting break-even is 5–10M tokens/month; for budget APIs, it's 50–100M tokens/month.",
            "features": RealizationFeatures(0.94, 0.92, 0.96, 0.98, 0.95, 0.88)
        },
        {
            "content": "Automation Ratio Metric: Gross margin in AI apps is determined by the proportion of AI output delivered with minimal human oversight (Automation Ratio).",
            "features": RealizationFeatures(0.92, 0.95, 0.98, 0.96, 0.94, 0.95)
        },
        {
            "content": "AI SaaS Margin Compression: AI-first B2B SaaS gross margins are 55–70% (vs 78–85% traditional SaaS) due to variable inference costs.",
            "features": RealizationFeatures(0.98, 0.99, 0.95, 0.92, 0.97, 0.90)
        },
        {
            "content": "The Data Moat (2026): Proprietary, domain-specific labeled data and correction signals are the true capital of the 2026 AI economy.",
            "features": RealizationFeatures(0.96, 0.95, 0.94, 0.98, 0.95, 0.98)
        },
        {
            "content": "Vertical AI Valuation: Vertical AI solutions command revenue multiples of 44.1x vs 12x for traditional software, reflecting the market's price for specialization.",
            "features": RealizationFeatures(0.99, 0.98, 0.96, 0.94, 0.98, 0.92)
        }
    ]

    dataset = load_dataset()

    new_realizations = []
    for finding in findings:
        r = engine.add_realization(
            content=finding["content"],
            features=finding["features"],
            turn_number=1, # Initial injection
            context="Research Paper: AI Unit Economics 2026"
        )

        # Convert to the format expected by the JSON
        r_dict = {
            "id": r.id,
            "timestamp": r.timestamp,
            "layer": r.layer,
            "title": finding["content"][:50] + "...",
            "signature": f"ECON-{r.id[:4]}",
            "content": r.content,
            "scores": {
                "grounding": r.features.grounding,
                "certainty": r.features.certainty,
                "structure": r.features.structure,
                "applicability": r.features.applicability,
                "coherence": r.features.coherence,
                "generativity": r.features.generativity,
                "presentation": 0.95, # Default high for research paper
                "temporal": 1.0 # Current 2026 data
            },
            "q_score": r.q_score,
            "parents": [],
            "children": [],
            "context": r.context,
            "evidence": ["AI_Unit_Economics_Research_2026.docx"]
        }
        new_realizations.append(r_dict)

    # Merge with existing realizations
    # Avoid duplicates by checking content
    existing_contents = {r["content"] for r in dataset["realizations"]}
    added_count = 0

    # First, clean up the corrupted ones if they exist
    dataset["realizations"] = [r for r in dataset["realizations"] if "0/M tokens in 2022 to -bash.40/M tokens" not in r["content"]]

    for nr in new_realizations:
        if nr["content"] not in existing_contents:
            dataset["realizations"].append(nr)
            added_count += 1

    # Update stats
    dataset["stats"]["total_realizations"] = len(dataset["realizations"])
    # Re-calculate layer distribution
    layer_dist = {str(i): 0 for i in range(4)}
    layer_dist["N"] = 0
    for r in dataset["realizations"]:
        l = str(r["layer"])
        layer_dist[l] = layer_dist.get(l, 0) + 1
    dataset["stats"]["layer_distribution"] = layer_dist

    # Re-calculate avg q_score
    total_q = sum(r["q_score"] for r in dataset["realizations"])
    dataset["stats"]["avg_q_score"] = total_q / len(dataset["realizations"])

    save_dataset(dataset)
    print(f"✅ Successfully injected {added_count} new realizations from the research paper.")

if __name__ == "__main__":
    main()
