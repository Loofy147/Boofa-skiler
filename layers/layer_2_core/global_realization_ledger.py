import json
import hashlib
import os
from datetime import datetime
from typing import List, Dict, Optional, Any
from collections import defaultdict

class GlobalRealizationLedger:
    """
    Project Beta: Global Realization Ledger (Phase 7 Scaled Version)
    Goal: High-integrity, high-throughput store for knowledge DAGs.
    """
    def __init__(self, ledger_path: str = "layers/layer_1_domain/global_ledger.json"):
        self.ledger_path = ledger_path
        self.realizations = self._load_ledger()
        self.layer_index = defaultdict(list)
        self._rebuild_index()
        self.buffer = []
        print(f"💎 Scaled Ledger Active: {len(self.realizations)} nodes indexed.")

    def _load_ledger(self) -> Dict[str, Dict]:
        if os.path.exists(self.ledger_path):
            with open(self.ledger_path, "r") as f:
                try:
                    return json.load(f)
                except:
                    return {}
        return {}

    def _rebuild_index(self):
        self.layer_index.clear()
        for rid, r in self.realizations.items():
            self.layer_index[r.get("layer", "N")].append(rid)

    def _generate_id(self, content: str) -> str:
        h = hashlib.sha256(content.encode()).hexdigest()
        return f"R_{h[:8].upper()}"

    def add_realization(self, content: str, layer: int, features: Dict[str, float], q_score: float, parents: List[str] = None, metadata: Dict = None, immediate_save: bool = True) -> str:
        rid = self._generate_id(content)
        if rid in self.realizations: return rid

        realization = {
            "id": rid, "content": content, "layer": layer, "features": features,
            "q_score": q_score, "parents": parents or [], "children": [],
            "metadata": metadata or {}, "timestamp": datetime.now().isoformat()
        }

        for pid in realization["parents"]:
            if pid in self.realizations:
                if rid not in self.realizations[pid]["children"]:
                    self.realizations[pid]["children"].append(rid)

        self.realizations[rid] = realization
        self.layer_index[layer].append(rid)

        if immediate_save:
            self._save_ledger()
        else:
            self.buffer.append(rid)
            if len(self.buffer) >= 10:
                self.flush_buffer()

        return rid

    def flush_buffer(self):
        if self.buffer:
            self._save_ledger()
            self.buffer = []
            print(f"📦 Ledger Buffer Flushed.")

    def verify_integrity(self) -> bool:
        for rid, r in self.realizations.items():
            if rid != self._generate_id(r["content"]): return False
        return True

    def _save_ledger(self):
        os.makedirs(os.path.dirname(self.ledger_path), exist_ok=True)
        with open(self.ledger_path, "w") as f:
            json.dump(self.realizations, f, indent=2)

    def get_realization(self, rid: str) -> Optional[Dict]:
        return self.realizations.get(rid)

    def query_layer(self, layer: int) -> List[Dict]:
        return [self.realizations[rid] for rid in self.layer_index.get(layer, [])]

if __name__ == "__main__":
    ledger = GlobalRealizationLedger()
    rid = ledger.add_realization("Scaled Ledger Integration Fact", 1, {"G": 0.9}, 0.92)
    print(f"Integrity: {ledger.verify_integrity()}")
