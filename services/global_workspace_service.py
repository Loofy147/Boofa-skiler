from typing import List, Dict, Any, Optional
from layers.layer_2_core.realization_engine import Realization, RealizationEngine
import threading

class GlobalWorkspaceService:
    """
    Architectural Service: Global Workspace
    Goal: Enabling real-time informational sharing between specialized domain brains.
    Pattern: Global Workspace Theory (GWT) + Perspective Architecture.
    """
    def __init__(self):
        self.workspace_realizations: List[Realization] = []
        self._lock = threading.Lock()
        self.current_perspective = "SOLVER" # SOLVER, AUDITOR, OBSERVER
        print("🌐 Global Workspace Service Initialized.")

    def broadcast(self, realization: Realization):
        """Broadcasts a high-Q realization to the workspace."""
        if realization.q_score > 0.85:
            with self._lock:
                self.workspace_realizations.append(realization)
                # Maintain finite context window (last 20 realizations)
                if len(self.workspace_realizations) > 20:
                    self.workspace_realizations.pop(0)
            print(f"📡 [GWT] Broadcasted: {realization.id} (Q={realization.q_score:.4f})")

    def retrieve_shared_context(self) -> List[Realization]:
        """Retrieves all realizations currently in the global workspace."""
        with self._lock:
            return list(self.workspace_realizations)

    def switch_perspective(self, new_perspective: str):
        """Switches the system's operational perspective."""
        allowed = ["SOLVER", "AUDITOR", "OBSERVER", "STRATEGIST"]
        if new_perspective.upper() in allowed:
            self.current_perspective = new_perspective.upper()
            print(f"🎭 Perspective Shift: Now operating as {self.current_perspective}")
        else:
            print(f"⚠️ Invalid perspective: {new_perspective}")

    def get_context_summary(self) -> str:
        """Generates a summary of the global workspace for domain injection."""
        realizations = self.retrieve_shared_context()
        if not realizations:
            return "Global workspace is empty."

        summary = f"System Perspective: {self.current_perspective}\n"
        summary += "Active Realizations:\n"
        for r in realizations:
            summary += f"- {r.content[:100]} (Q={r.q_score:.2f})\n"
        return summary

if __name__ == "__main__":
    from layers.layer_2_core.realization_engine import RealizationFeatures

    workspace = GlobalWorkspaceService()

    # Simulate a solver realization
    r = Realization(
        id="R_SOLVE_01",
        content="Technical insight: Recursive ensembling minimizes variance.",
        features=RealizationFeatures(0.95, 0.92, 0.90, 0.85, 0.90, 0.95),
        q_score=0.924,
        layer=2,
        timestamp="2026-02-18",
        parents=[],
        children=[],
        turn_number=1
    )

    workspace.broadcast(r)
    workspace.switch_perspective("AUDITOR")
    print("\nWorkspace Summary:")
    print(workspace.get_context_summary())
