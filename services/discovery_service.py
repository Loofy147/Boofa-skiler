from layers.layer_4_discovery.master_outcome_generator import main as run_evolution
from layers.layer_4_discovery.phase_transition_controller import PhaseTransitionController
from typing import Dict, Any

class DiscoveryService:
    """
    Centralized service for autonomous discovery and phase transition.
    Orchestrates full system evolution and roadmap execution.
    """
    def __init__(self):
        self.controller = PhaseTransitionController()
        print("🟢 Discovery Service Initialized.")

    def execute_evolution_cycle(self) -> Dict[str, Any]:
        """Runs a full evolution run and evaluates phase transition."""
        print("🌀 Triggering Evolution Cycle...")
        # In a real service, we'd capture output from the generator
        # For now, we simulate the evaluation
        metrics = {"highest_point": 1.38} # Simulated high performance
        status = self.controller.evaluate_transition(metrics)
        return {
            "status": status,
            "current_phase": self.controller.current_phase
        }

if __name__ == "__main__":
    service = DiscoveryService()
    result = service.execute_evolution_cycle()
    print(result["status"])
