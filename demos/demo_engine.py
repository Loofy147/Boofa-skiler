import os
import json
import sys
import numpy as np
from datetime import datetime
from layers.layer_3_optimization.pipeline import BoofaSkiler
from layers.layer_4_discovery.grand_integrated_simulation import GrandMetaOrchestrator, RealizationFeatures

class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer): return int(obj)
        if isinstance(obj, np.floating): return float(obj)
        if isinstance(obj, np.ndarray): return obj.tolist()
        if isinstance(obj, (np.bool_, bool)): return bool(obj)
        return super(NpEncoder, self).default(obj)

def run_synthesis_flow():
    k_token = os.getenv("KAGGLE_API_TOKEN")
    h_token = os.getenv("HF_TOKEN")

    if not k_token or not h_token:
        return "Error: API tokens not found.", {}

    # 1. Pipeline Execution
    skiler = BoofaSkiler(k_token, h_token)
    pipeline_results = skiler.execute()

    # 2. Synthesis Execution
    mco = GrandMetaOrchestrator()
    mco.feed_protocol("Boofa-Skiler Showcase Protocol", depth=3)

    model_name = pipeline_results.get('hf_model', {}).get('id', 'MiniMaxAI/MiniMax-M2.5')
    mco.domains["TECHNICAL"].engine.add_realization(
        content=f"Technical Foundation: {model_name} is the primary synthesis engine.",
        features=RealizationFeatures(0.99, 0.98, 0.97, 0.96, 0.98, 0.95),
        turn_number=1
    )

    mco.execute_and_merge(cycles=50)
    sim_report = mco.get_report()

    # 3. Project Identification
    top_values = sorted(sim_report.get("universal_values", []), key=lambda x: x['q'], reverse=True)[:5]
    project_names = [
        "Project Alpha: Autonomous Strategic Architect",
        "Project Beta: Global Realization Ledger",
        "Project Gamma: Predictive Institutional Auditor",
        "Project Delta: Cross-Domain Innovation Synthesizer",
        "Project Epsilon: Cognitive Operational Excellence Hub"
    ]
    projects = []
    for i, val in enumerate(top_values):
        projects.append({
            "name": project_names[i] if i < len(project_names) else f"Project {i+1}",
            "synthesis": val['content'],
            "q_score": val['q']
        })

    # 4. Final Report Generation (Markdown)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    highest_q = float(sim_report.get("highest_point", 0.0))

    report_md = f"""# 🚀 BOOFA-SKILER SHOWCASE REPORT

## 📅 {timestamp} | 📊 Peak Q: {highest_q:.4f}

---

### 1. HF/Kaggle Bridge
- **Model**: {model_name}
- **Downloads**: {pipeline_results.get('hf_model', {}).get('downloads', 'N/A')}

### 2. Cognitive Synthesis
"""
    for domain, data in sim_report.get("domains", {}).items():
        report_md += f"- **{domain}**: Avg Q = {float(data.get('avg_q', 0)):.4f}\n"

    report_md += "\n### 3. Business Projects\n"
    for p in projects:
        report_md += f"#### 🚀 {p['name']} (Q: {p['q_score']:.4f})\n> {p['synthesis']}\n\n"

    metrics = {
        "peak_q": highest_q,
        "domains": sim_report.get("domains", {}),
        "projects": projects
    }

    return report_md, metrics
