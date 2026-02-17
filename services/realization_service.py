from layers.layer_2_core.realization_engine import RealizationEngine, RealizationFeatures
from typing import List, Dict, Any, Optional

class RealizationService:
    """
    Centralized service for managing knowledge realizations across all domains.
    Provides a High-Q interface for crystallization.
    """
    def __init__(self, engine: Optional[RealizationEngine] = None):
        self.engine = engine or RealizationEngine()
        print("🟢 Realization Service Initialized.")

    def add_insight(self, content: str, G: float, C: float, S: float, A: float) -> Dict[str, Any]:
        """Adds a new realization and returns its status."""
        features = RealizationFeatures(
            grounding=G, certainty=C, structure=S,
            applicability=A, coherence=0.9, generativity=0.8
        )
        r = self.engine.add_realization(content=content, features=features, turn_number=1)
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

if __name__ == "__main__":
    service = RealizationService()
    status = service.add_insight("Test insight", 0.95, 0.92, 0.90, 0.85)
    print(status)
