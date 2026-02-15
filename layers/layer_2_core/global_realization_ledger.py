import json
import hashlib
import os
from datetime import datetime
from typing import List, Dict, Optional, Any

class GlobalRealizationLedger:
    """
    Project Beta: Global Realization Ledger
    Goal: A high-integrity store for crystallized knowledge (realizations).
    Features: SHA-256 Hashing, DAG relationships, Q-Score Verification.
    """
    def __init__(self, ledger_path: str = "layers/layer_1_domain/global_ledger.json"):
        self.ledger_path = ledger_path
        self.realizations = self._load_ledger()

    def _load_ledger(self) -> Dict[str, Dict]:
        if os.path.exists(self.ledger_path):
            with open(self.ledger_path, "r") as f:
                return json.load(f)
        return {}

    def _generate_id(self, content: str) -> str:
        """Generates a content-based SHA-256 ID (R_XXXXXXXX)."""
        h = hashlib.sha256(content.encode()).hexdigest()
        return f"R_{h[:8].upper()}"

    def add_realization(self, content: str, layer: int, features: Dict[str, float], q_score: float, parents: List[str] = None, metadata: Dict = None) -> str:
        """Adds a verified realization to the ledger."""
        rid = self._generate_id(content)

        if rid in self.realizations:
            print(f"ℹ️ Realization {rid} already exists in ledger.")
            return rid

        realization = {
            "id": rid,
            "content": content,
            "layer": layer,
            "features": features,
            "q_score": q_score,
            "parents": parents or [],
            "children": [],
            "metadata": metadata or {},
            "timestamp": datetime.now().isoformat()
        }

        # Update parents' children lists
        for pid in realization["parents"]:
            if pid in self.realizations:
                if rid not in self.realizations[pid]["children"]:
                    self.realizations[pid]["children"].append(rid)

        self.realizations[rid] = realization
        self._save_ledger()
        print(f"💎 Crystallized Realization {rid} in Global Ledger (Q={q_score:.4f}).")
        return rid

    def verify_integrity(self) -> bool:
        """Verifies the integrity of all nodes in the DAG."""
        for rid, r in self.realizations.items():
            expected_id = self._generate_id(r["content"])
            if rid != expected_id:
                print(f"❌ Integrity Breach at {rid}! Expected {expected_id}")
                return False
        print("✅ Global Ledger Integrity Verified.")
        return True

    def _save_ledger(self):
        os.makedirs(os.path.dirname(self.ledger_path), exist_ok=True)
        with open(self.ledger_path, "w") as f:
            json.dump(self.realizations, f, indent=2)

    def get_realization(self, rid: str) -> Optional[Dict]:
        return self.realizations.get(rid)

if __name__ == "__main__":
    ledger = GlobalRealizationLedger()

    # Test Entry
    rid1 = ledger.add_realization(
        content="Universal Rule: Complexity decreases Q-score unless grounded by symmetry.",
        layer=0,
        features={"G": 0.99, "C": 0.98, "S": 0.97, "A": 0.95, "H": 0.98, "V": 0.96},
        q_score=1.1064,
        metadata={"source": "Manual Crystallization"}
    )

    rid2 = ledger.add_realization(
        content="Derived Pattern: Symmetry in math problems allows for modular pruning.",
        layer=2,
        features={"G": 0.95, "C": 0.94, "S": 0.92, "A": 0.90, "H": 0.94, "V": 0.92},
        q_score=0.985,
        parents=[rid1],
        metadata={"source": "Project Beta Simulation"}
    )

    ledger.verify_integrity()
