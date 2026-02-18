from layers.layer_2_core.realization_engine import RealizationEngine, RealizationFeatures, Realization
from services.global_workspace_service import GlobalWorkspaceService
from typing import List, Dict, Any, Optional

class RealizationService:
    """
    Centralized service for managing knowledge realizations across all domains.
    Provides a High-Q interface for crystallization and Global Workspace sharing.
    """
    def __init__(self, engine: Optional[RealizationEngine] = None, workspace: Optional[GlobalWorkspaceService] = None):
        self.engine = engine or RealizationEngine()
        self.workspace = workspace or GlobalWorkspaceService()
        print("🟢 Realization Service Initialized (GWT-Enabled).")

    def add_insight(self, content: str, G: float, C: float, S: float, A: float, broadcast: bool = True) -> Dict[str, Any]:
        """Adds a new realization and returns its status."""
        features = RealizationFeatures(
            grounding=G, certainty=C, structure=S,
            applicability=A, coherence=0.9, generativity=0.8
        )
        r = self.engine.add_realization(content=content, features=features, turn_number=1)

        if broadcast and r.q_score > 0.85:
            self.workspace.broadcast(r)

        return {
            "id": r.id,
            "q_score": r.q_score,
            "layer": r.layer,
            "status": "CRYSTALLIZED"
        }

    def query_knowledge(self, query: str) -> List[Dict[str, Any]]:
        """Retrieves realizations matching the query."""
        results = self.engine.retrieve(query)
        return [{"id": r.id, "content": r.content, "q": r.q_score} for r in results]

    def get_system_context(self) -> str:
        """Gets current shared context from the global workspace."""
        return self.workspace.get_context_summary()

if __name__ == "__main__":
    service = RealizationService()
    status = service.add_insight("Integrated cross-domain awareness breakthrough.", 0.98, 0.95, 0.92, 0.90)
    print(f"\nStatus: {status}")
    print(f"\nShared Context:\n{service.get_system_context()}")
