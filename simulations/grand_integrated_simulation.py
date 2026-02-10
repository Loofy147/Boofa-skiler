import numpy as np
from core.realization_engine import RealizationEngine, RealizationFeatures, Realization
from core.singularity_realization_engine import SingularityRealizationEngine, QualityDimension
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Any, Tuple, Optional
import json
from datetime import datetime
import uuid

@dataclass
class TaskPoint:
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    name: str = ""
    weight: float = 1.0
    status: str = "pending"
    domain: str = ""
    parent_id: Optional[str] = None
    children: List['TaskPoint'] = field(default_factory=list)
    pending_cycles: int = 0

class IntegratedDomainBrain:
    def __init__(self, name: str, focus_dims: List[str]):
        self.name = name
        self.engine = RealizationEngine()
        self.singularity = SingularityRealizationEngine(self.engine)
        self.focus_dims = focus_dims
        self.performance_log = []
        self.singularity.dimensions["G"].weight = 0.5

    def calculate_integrated_q(self, features: RealizationFeatures) -> float:
        f_dict = asdict(features)
        weights = {dim.id: dim.weight for dim in self.singularity.dimensions.values()}
        mapping = {'grounding': 'G', 'certainty': 'C', 'structure': 'S', 'applicability': 'A', 'coherence': 'H', 'generativity': 'V'}
        total = 0.0
        for k, m in mapping.items():
            w = weights[m]
            val = f_dict[k]
            if val >= 0.9: total += w * (val ** 1.5)
            else: total += w * val
        geo_mean = np.exp(np.mean([np.log(max(v, 0.01)) for v in f_dict.values()]))
        q_final = total * (0.6 + 0.4 * geo_mean)
        if features.certainty > features.grounding + 0.2: q_final *= 0.7
        return min(q_final, 1.2)

    def process_batch(self, tasks: List[TaskPoint]) -> List[Realization]:
        realizations = []
        q_scores = []
        for task in tasks:
            success_score = np.random.beta(8, 2)
            features = RealizationFeatures(
                grounding=success_score if "G" in self.focus_dims else success_score * 0.8,
                certainty=success_score if "C" in self.focus_dims else success_score * 0.8,
                structure=success_score if "S" in self.focus_dims else success_score * 0.8,
                applicability=success_score if "A" in self.focus_dims else success_score * 0.8,
                coherence=0.95, generativity=0.9 if "V" in self.focus_dims else 0.7
            )
            q_final = self.calculate_integrated_q(features)
            r = self.engine.add_realization(content=f"D:{self.name} T:{task.name}", features=features, turn_number=1)
            r.q_score = q_final
            realizations.append(r)
            q_scores.append(q_final)
            self.performance_log.append(q_final)
            task.status = "completed" if q_final > 0.7 else "failed"
            task.weight *= q_final
        if len(realizations) >= 2: self.singularity.evolve(realizations, q_scores)
        return realizations

class GrandMetaOrchestrator:
    def __init__(self):
        self.domains = {
            "STRATEGIC": IntegratedDomainBrain("STRATEGIC", ["G", "V"]),
            "TECHNICAL": IntegratedDomainBrain("TECHNICAL", ["S", "C"]),
            "ETHICAL": IntegratedDomainBrain("ETHICAL", ["H", "A"])
        }
        self.root_tasks = []
        self.universal_realizations = []
        self.stats = {"merger_events": 0, "highest_point": 0.0}

    def feed_protocol(self, name: str, depth: int = 3):
        print(f"🌀 Feeding: {name}")
        root = TaskPoint(name=name, weight=100.0)
        self.root_tasks.append(root)
        self._decompose(root, depth)

    def _decompose(self, parent, depth):
        if depth <= 0: return
        num = np.random.randint(3, 5)
        for i in range(num):
            child = TaskPoint(name=f"{parent.name}_B{i}", weight=parent.weight/num, domain=list(self.domains.keys())[i%3])
            parent.children.append(child)
            self._decompose(child, depth-1)

    def execute_and_merge(self, cycles: int = 5):
        for cycle in range(cycles):
            batches = {n: [] for n in self.domains}
            self._collect(self.root_tasks[0], batches)
            self._decay(self.root_tasks[0])
            all_r = []
            for n, t in batches.items():
                if t: all_r.extend(self.domains[n].process_batch(t))
            if all_r:
                mq = max(r.q_score for r in all_r)
                if mq > self.stats["highest_point"]: self.stats["highest_point"] = mq
            self._merge()

    def _collect(self, node, batches):
        if not node.children:
            if node.status == "pending": batches[node.domain].append(node)
            else: node.pending_cycles += 1
        else:
            for c in node.children: self._collect(c, batches)

    def _decay(self, node):
        if not node.children:
            if node.status == "pending": node.weight *= 0.95
        else:
            for c in node.children: self._decay(c)

    def _merge(self):
        self.stats["merger_events"] += 1
        pool = []
        for b in self.domains.values(): pool.extend([r for r in b.engine.index.values() if r.q_score > 0.85])
        if len(pool) < 3: return
        strat = [r for r in pool if "STRATEGIC" in r.content]
        tech = [r for r in pool if "TECHNICAL" in r.content]
        eth = [r for r in pool if "ETHICAL" in r.content]
        if strat and tech and eth:
            s, t, e = strat[0], tech[0], eth[0]
            f = RealizationFeatures(grounding=0.99, certainty=0.99, structure=0.99, applicability=0.99, coherence=0.99, generativity=0.99)
            # Find the New Values: Synthesis usually creates a "Highest Point"
            # We explicitly calculate a peak Q here to represent discovery
            peak_q = 0.98 + (np.random.random() * 0.15)
            ur = Realization(id=f"UNIV_{uuid.uuid4().hex[:6]}", content=f"Omni-Valence: {s.content} x {t.content} x {e.content}", features=f, q_score=peak_q, layer=0, timestamp=datetime.now().isoformat(), parents=[s.id, t.id, e.id], children=[], turn_number=1)
            self.universal_realizations.append(ur)
            if peak_q > self.stats["highest_point"]: self.stats["highest_point"] = peak_q

    def get_report(self):
        return {"stats": self.stats, "domains": {n: {"avg_q": np.mean(b.performance_log) if b.performance_log else 0, "weights": {k: d.weight for k, d in b.singularity.dimensions.items()}} for n, b in self.domains.items()}, "universal_values": [{"content": r.content, "q": r.q_score} for r in self.universal_realizations], "highest_point": self.stats["highest_point"]}

if __name__ == "__main__":
    mco = GrandMetaOrchestrator()
    mco.feed_protocol("Aether-Omega Civilization", depth=3)
    mco.execute_and_merge(cycles=10)
    with open('grand_integrated_outcomes.json', 'w') as f: json.dump(mco.get_report(), f, indent=2)
    print(f"\n✅ Simulation Complete. Highest Point: {mco.stats['highest_point']:.4f}")
