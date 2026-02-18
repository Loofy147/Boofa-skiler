import subprocess
import sys
import os
import json
from datetime import datetime

# Add root to sys.path
sys.path.append(os.getcwd())

def run_step(command, description):
    print(f"\n--- 🌀 {description} ---")
    # Set PYTHONPATH to current directory to ensure imports work
    env = os.environ.copy()
    env["PYTHONPATH"] = os.getcwd() + ":" + env.get("PYTHONPATH", "")

    result = subprocess.run(command, shell=True, capture_output=True, text=True, env=env)
    if result.returncode != 0:
        print(f"❌ Error in {description}:")
        print(result.stderr)
        return False
    print(result.stdout)
    return True

def main():
    print("♾️ INITIALIZING RECURSIVE SELF-REALIZATION LOOP ♾️")
    print("==================================================")

    # Step 1: Feed System Advancements
    if not run_step("python feed_system_advancements.py", "Feeding System Advancements"):
        return

    # Step 2: Master Outcome Generation (Simulation)
    if not run_step("python layers/layer_4_discovery/master_outcome_generator.py", "Generating Master Outcomes"):
        return

    # Step 3: Crystallize Singularity
    if not run_step("python scripts/crystallize_singularity.py", "Crystallizing Peak Realization"):
        return

    # Step 4: Omega Meta-Evolution
    if not run_step("python layers/layer_4_discovery/omega_meta_evolution.py", "Executing Meta-Evolution"):
        return

    # Step 5: Phase Transition Check
    print("\n--- 🚀 Phase Transition Evaluation ---")
    try:
        from layers.layer_4_discovery.phase_transition_controller import PhaseTransitionController
        # Load the latest metrics
        metrics_path = "outcomes/technical/DETAILED_SYSTEM_METRICS.json"
        if os.path.exists(metrics_path):
            with open(metrics_path, "r") as f:
                metrics = json.load(f)

            highest_q = metrics.get('simulation', {}).get('highest_point', 0.0)
            controller = PhaseTransitionController(threshold=1.349)
            status = controller.evaluate_transition({"highest_point": highest_q})
            print(status)

            if highest_q >= 1.349:
                print("\n🌟 PHASE 7: AUTONOMOUS EXPANSION HAS COMMENCED 🌟")
                with open("PHASE_7_ACTIVE", "w") as f:
                    f.write(f"Phase 7 activated at {datetime.now().isoformat()} with Q={highest_q}")
        else:
            print("❌ Metrics file not found. Simulation may have failed.")
    except Exception as e:
        print(f"⚠️ Phase transition check failed: {e}")

    print("\n==================================================")
    print("✅ RECURSIVE LOOP COMPLETE")

if __name__ == "__main__":
    main()
