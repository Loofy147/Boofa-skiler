import os
import re

mappings = {
    r'from core\.realization_engine': 'from layers.layer_2_core.realization_engine',
    r'from realization_engine': 'from layers.layer_2_core.realization_engine',
    r'from \.realization_engine': 'from layers.layer_2_core.realization_engine',
    r'from core\.singularity_realization_engine': 'from layers.layer_4_discovery.singularity_realization_engine',
    r'from core\.omega_v2': 'from layers.layer_2_core.omega_v2',
    r'from core\.omega_evolved': 'from layers.layer_4_discovery.omega_evolved',
    r'from core\.omega_full_power': 'from layers.layer_4_discovery.omega_full_power',
    r'from core\.free_will_framework': 'from layers.layer_2_core.free_will_framework',
    r'from free_will_framework': 'from layers.layer_2_core.free_will_framework',
    r'from engines\.omega_meta_evolution': 'from layers.layer_4_discovery.omega_meta_evolution',
    r'from engines\.omega_production_trainer_final': 'from layers.layer_4_discovery.omega_production_trainer_final',
    r'from engines\.skill_weight_optimizer': 'from layers.layer_4_discovery.skill_weight_optimizer',
    r'from engines\.research_prompt_optimizer': 'from layers.layer_3_optimization.research_prompt_optimizer',
    r'from simulations\.grand_integrated_simulation': 'from layers.layer_4_discovery.grand_integrated_simulation',
    r'from simulations\.mco_simulation': 'from layers.layer_4_discovery.mco_simulation',
    r'from simulations\.multi_dimensional_pattern_simulation': 'from layers.layer_2_core.multi_dimensional_pattern_simulation',
    r'from tests\.hard_test_designer': 'from layers.layer_3_optimization.hard_test_designer',
    r'from tests\.verify_study': 'from layers.layer_3_optimization.verify_study',
}

def fix_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    new_content = content
    for pattern, replacement in mappings.items():
        new_content = re.sub(pattern, replacement, new_content)

    if new_content != content:
        with open(filepath, 'w') as f:
            f.write(new_content)
        print(f"Fixed imports in {filepath}")

for root, dirs, files in os.walk('layers'):
    for file in files:
        if file.endswith('.py'):
            fix_file(os.path.join(root, file))
