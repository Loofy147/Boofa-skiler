import os
import json
import networkx as nx
import matplotlib.pyplot as plt
from datetime import datetime
from layers.layer_4_discovery.grand_integrated_simulation import GrandMetaOrchestrator

class InnovationSynthesizer:
    """
    Project Delta: Cross-Domain Innovation Synthesizer
    Goal: Triggering "Innovation Events" by merging disparate domain facts.
    """
    def __init__(self):
        self.mco = GrandMetaOrchestrator()
        self.innovation_events = []
        self.graph = nx.DiGraph()

    def synthesize_innovations(self, protocol_name: str, cycles: int = 100):
        print(f"🚀 Synthesizing innovations for: {protocol_name}...")
        self.mco.feed_protocol(protocol_name, depth=3)
        self.mco.execute_and_merge(cycles=cycles)

        # Identify "Innovation Events"
        for ur in self.mco.universal_realizations:
            if ur.q_score > 1.25:
                self.innovation_events.append(ur)

        self._build_knowledge_graph()

    def _build_knowledge_graph(self):
        print("🕸️ Building Knowledge Graph...")

        # Add Universal Nodes (Innovations)
        for ur in self.mco.universal_realizations:
            self.graph.add_node(ur.id, label=ur.content, q=ur.q_score, type='universal')
            for pid in ur.parents:
                self.graph.add_edge(pid, ur.id)

        # Add Domain Nodes
        for name, domain in self.mco.domains.items():
            for rid, r in domain.engine.index.items():
                if r.q_score > 0.8: # Only high-quality patterns
                    self.graph.add_node(rid, label=r.content, q=r.q_score, type='domain', domain=name)

    def visualize_graph(self, filename: str = "innovation_graph.png"):
        print(f"🎨 Visualizing Innovation Graph: {filename}")
        plt.figure(figsize=(15, 10))

        pos = nx.spring_layout(self.graph, k=0.5)

        # Nodes colored by Q-score
        nodes = list(self.graph.nodes())
        colors = [self.graph.nodes[n].get('q', 0.5) for n in nodes]

        # Draw nodes
        sc = nx.draw_networkx_nodes(self.graph, pos, node_color=colors, cmap=plt.cm.viridis,
                                   node_size=100, alpha=0.7)

        # Draw edges
        nx.draw_networkx_edges(self.graph, pos, alpha=0.3, arrows=True)

        plt.title("Boofa-Skiler: Cross-Domain Innovation Graph")
        plt.colorbar(sc, label='Quality Score (Q)')

        os.makedirs("outcomes/technical/graph", exist_ok=True)
        path = f"outcomes/technical/graph/{filename}"
        plt.savefig(path)
        plt.close()
        print(f"✅ Visualization saved: {path}")

    def save_innovation_report(self):
        report = {
            "timestamp": datetime.now().isoformat(),
            "total_innovations": len(self.innovation_events),
            "peak_q": self.mco.stats["highest_point"],
            "events": [{"content": e.content, "q": e.q_score, "parents": e.parents} for e in self.innovation_events]
        }

        os.makedirs("outcomes/strategic/delta", exist_ok=True)
        path = f"outcomes/strategic/delta/INNOVATION_REPORT_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(path, "w") as f:
            json.dump(report, f, indent=2)
        print(f"📄 Innovation Report saved: {path}")

if __name__ == "__main__":
    synthesizer = InnovationSynthesizer()
    synthesizer.synthesize_innovations("AIMO 3 Cross-Domain Synthesis", cycles=100)
    synthesizer.visualize_graph(f"AIMO_INNOVATION_{datetime.now().strftime('%H%M%S')}.png")
    synthesizer.save_innovation_report()
