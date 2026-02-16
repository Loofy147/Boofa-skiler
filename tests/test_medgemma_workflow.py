import sys
import os
import json
sys.path.append(os.getcwd())

from competitions.medgemma.agentic_workflow import BoofaMedWorkflow

def test_medgemma_workflow():
    print("🧪 Testing Boofa-Med Agentic Workflow Integration...")
    workflow = BoofaMedWorkflow()
    result = workflow.run("Test query for verification.")

    print(f"Final Status: {result['final_status']}")
    assert result['final_status'] == "STABLE", "Workflow should reach a stable state."
    print("✅ Boofa-Med Workflow Test Passed!")

if __name__ == "__main__":
    test_medgemma_workflow()
