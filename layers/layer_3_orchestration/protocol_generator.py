import json
import os
from typing import List, Dict
from datetime import datetime

class ProtocolGenerator:
    """Layer 3: Automated Protocol Generator"""

    def generate_protocol(self, roadmap: List[Dict], goal_id: str) -> Dict:
        print(f"📄 Generating executable protocol for Goal {goal_id}...")

        protocol = {
            "protocol_id": f"PROTO_{goal_id}_{datetime.now().strftime('%Y%m%d')}",
            "version": "1.0.0",
            "timestamp": datetime.now().isoformat(),
            "phases": []
        }

        # Group roadmap tasks into phases
        for i, task in enumerate(roadmap):
            phase = {
                "step": i + 1,
                "name": task['task'],
                "domain": task['domain'],
                "weight": task['weight'],
                "action": self._map_to_action(task['task']),
                "verification_metric": "Q_SCORE > 0.85"
            }
            protocol["phases"].append(phase)

        return protocol

    def _map_to_action(self, task_name: str) -> str:
        if "Kaggle" in task_name or "Data" in task_name:
            return "PIPELINE_EXECUTE_FETCH"
        if "Synthesis" in task_name:
            return "MCO_EXECUTE_SYNTHESIS"
        if "Deployment" in task_name or "Submission" in task_name:
            return "AUTONOMOUS_SUBMIT"
        return "GENERAL_COMPUTE"

    def save_protocol(self, protocol: Dict, path: str):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            json.dump(protocol, f, indent=2)
        print(f"✅ Protocol saved to {path}")

if __name__ == "__main__":
    gen = ProtocolGenerator()
    roadmap = [{"task": "Fetch Data", "domain": "TECHNICAL", "weight": 0.2}]
    proto = gen.generate_protocol(roadmap, "TEST_GOAL")
    gen.save_protocol(proto, "outcomes/integrated/TEST_PROTOCOL.json")
