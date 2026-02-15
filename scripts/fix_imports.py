import os
import re

mappings = {
    r'from layers.layer_0_universal.foundation': 'from layers.layer_0_universal.foundation',
    r'import layer0_foundation': 'import layers.layer_0_universal.foundation as layer0_foundation',

    r'from layers.layer_1_domain.foundation': 'from layers.layer_1_domain.foundation',
    r'import layer1_skills': 'import layers.layer_1_domain.foundation as layer1_skills',

    r'from layers.layer_2_core.foundation': 'from layers.layer_2_core.foundation',
    r'import layer2_self_evolution': 'import layers.layer_2_core.foundation as layer2_self_evolution',

    r'from layers.layer_3_orchestration.foundation': 'from layers.layer_3_orchestration.foundation',
    r'import layer3_orchestration': 'import layers.layer_3_orchestration.foundation as layer3_orchestration',

    r'from layers.layer_3_optimization.pipeline': 'from layers.layer_3_optimization.pipeline',
    r'import pipeline': 'import layers.layer_3_optimization.pipeline as pipeline',

    r'from layers.layer_2_core.realization_engine': 'from layers.layer_2_core.realization_engine',
    r'from layers.layer_4_discovery.singularity_realization_engine': 'from layers.layer_4_discovery.singularity_realization_engine',
    r'from layers.layer_2_core.omega_v2': 'from layers.layer_2_core.omega_v2',
    r'from layers.layer_4_discovery.omega_evolved': 'from layers.layer_4_discovery.omega_evolved',
    r'from layers.layer_4_discovery.omega_full_power': 'from layers.layer_4_discovery.omega_full_power',
    r'from layers.layer_2_core.free_will_framework': 'from layers.layer_2_core.free_will_framework',
    r'from layers.layer_4_discovery.omega_meta_evolution': 'from layers.layer_4_discovery.omega_meta_evolution',
    r'from layers.layer_4_discovery.omega_production_trainer_final': 'from layers.layer_4_discovery.omega_production_trainer_final',
    r'from layers.layer_4_discovery.skill_weight_optimizer': 'from layers.layer_4_discovery.skill_weight_optimizer',
    r'from layers.layer_3_optimization.research_prompt_optimizer': 'from layers.layer_3_optimization.research_prompt_optimizer',
    r'from layers.layer_4_discovery.grand_integrated_simulation': 'from layers.layer_4_discovery.grand_integrated_simulation',
    r'from layers.layer_4_discovery.mco_simulation': 'from layers.layer_4_discovery.mco_simulation',
    r'from layers.layer_2_core.multi_dimensional_pattern_simulation': 'from layers.layer_2_core.multi_dimensional_pattern_simulation',
    r'from layers.layer_3_optimization.hard_test_designer': 'from layers.layer_3_optimization.hard_test_designer',
    r'from layers.layer_3_optimization.verify_study': 'from layers.layer_3_optimization.verify_study',
    r'from layers.layer_3_optimization.gather_comprehensive_data': 'from layers.layer_3_optimization.gather_comprehensive_data',
}

def fix_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    new_content = content
    # Handle the "from X import" pattern
    for pattern, replacement in mappings.items():
        if pattern.startswith('from'):
            new_content = re.sub(pattern, replacement, new_content)
        elif pattern.startswith('import'):
            # Only replace exact "import X" if it's not part of another word
            new_content = re.sub(r'(^|\s)' + re.escape(pattern) + r'(\s|$)', r'\1' + replacement + r'\2', new_content, flags=re.MULTILINE)

    if new_content != content:
        with open(filepath, 'w') as f:
            f.write(new_content)
        print(f"Fixed imports in {filepath}")

search_dirs = ['layers', 'competitions', 'demos', 'tests', 'scripts']
for d in search_dirs:
    for root, dirs, files in os.walk(d):
        for file in files:
            if file.endswith('.py'):
                fix_file(os.path.join(root, file))

# Also fix root files (though there shouldn't be many .py files left)
for file in os.listdir('.'):
    if file.endswith('.py'):
        fix_file(file)
