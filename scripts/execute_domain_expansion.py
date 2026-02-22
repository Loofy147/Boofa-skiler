import os
import sys
import importlib.util
from datetime import datetime

# Add root to sys.path
sys.path.append(os.getcwd())

def run_domain_engines():
    print("🌐 EXECUTING PHASE 7 DOMAIN EXPANSION 🌐")
    print("==========================================")

    domain_root = "layers/layer_1_domain"
    if not os.path.exists(domain_root):
        print("❌ Domain root not found.")
        return

    # Find all subdirectories that have an engine file
    engines_found = 0
    for domain in os.listdir(domain_root):
        domain_path = os.path.join(domain_root, domain)
        if not os.path.isdir(domain_path):
            continue

        engine_file = os.path.join(domain_path, f"{domain}_engine.py")
        if os.path.exists(engine_file):
            print(f"🚀 Activating Domain Engine: {domain.upper()}")

            # Dynamic import
            spec = importlib.util.spec_from_file_location(f"{domain}_engine", engine_file)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            # Find the class (it should be DomainEngine)
            class_name = "".join([part.capitalize() for part in domain.split("_")]) + "Engine"
            if hasattr(module, class_name):
                engine_class = getattr(module, class_name)
                engine_instance = engine_class()

                # Execute initial insight
                insight = f"Phase 7 Expansion Grounding for {domain.upper()} at {datetime.now().isoformat()}"
                r = engine_instance.realize_domain_insight(insight, q_target=0.95)
                print(f"   ✅ Insight Crystallized: {r.id} (Layer {r.layer})")
                engines_found += 1
            else:
                print(f"   ⚠️ Class {class_name} not found in {engine_file}")

    print(f"\n✅ Domain Expansion Complete. {engines_found} engines activated.")
    print("==========================================")

if __name__ == "__main__":
    run_domain_engines()
