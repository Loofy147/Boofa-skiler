"""
OMEGA EVOLVED: Using Discovered Capabilities & Personalities
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Now that we've discovered:
- 8 Emergent Capabilities
- 8 AI Personalities
- 6 Meta-Dimensions

Let's USE them to create prompts that were impossible before!
"""

from typing import Dict, List, Optional
from omega_prompt_engine import OmegaPromptEngine


class OmegaEvolved:
    """
    Advanced prompt engineering using discovered capabilities and personalities
    """
    
    def __init__(self):
        self.base_engine = OmegaPromptEngine()
        
        # The 8 discovered capabilities
        self.capabilities = {
            'multi_domain_synthesis': {
                'name': 'Multi-Domain Synthesis',
                'dimensions': ['D10', 'D20', 'D4', 'P'],
                'best_for': 'Integrating knowledge from disparate fields',
                'examples': ['Applying quantum physics to org design', 'Biology + algorithms']
            },
            'uncertainty_navigation': {
                'name': 'Uncertainty Navigation',
                'dimensions': ['D8', 'D7', 'D19', 'D3'],
                'best_for': 'Operating in high-uncertainty environments',
                'examples': ['Incomplete information', 'Multiple scenarios', 'Adaptive strategy']
            },
            'creative_reframing': {
                'name': 'Creative Problem Reframing',
                'dimensions': ['D14', 'D15', 'D17', 'D11', 'D10'],
                'best_for': 'Transforming problems through new perspectives',
                'examples': ['Traffic as resource allocation', 'Complaints as research']
            },
            'efficient_creativity': {
                'name': 'Efficient Creativity',
                'dimensions': ['D13', 'D14', 'D15', 'C'],
                'best_for': 'Novel solutions under resource constraints',
                'examples': ['Twitter constraints', 'Startup innovation', 'Haiku poetry']
            },
            'transparent_complexity': {
                'name': 'Transparent Complexity',
                'dimensions': ['D18', 'D4', 'S', 'D11'],
                'best_for': 'Making complex systems interpretable',
                'examples': ['Explain neural networks', 'Quantum for audiences', 'Legal clarity']
            },
            'temporal_intelligence': {
                'name': 'Temporal Intelligence',
                'dimensions': ['D1', 'D16', 'D19', 'D12'],
                'best_for': 'Maintaining coherence while adapting',
                'examples': ['Multi-turn context', 'Strategy + flexibility', 'Growth + identity']
            },
            'ethical_innovation': {
                'name': 'Ethical Innovation',
                'dimensions': ['D9', 'D14', 'D15', 'D8'],
                'best_for': 'Novel solutions aligned with values',
                'examples': ['Privacy-preserving AI', 'Equitable algorithms', 'Sustainable tech']
            },
            'causal_counterfactual': {
                'name': 'Causal Counterfactual Analysis',
                'dimensions': ['D6', 'D7', 'D4', 'D18'],
                'best_for': 'Tracing causes while exploring alternatives',
                'examples': ['What if scenarios', 'Historical analysis', 'A/B with causality']
            }
        }
        
        # The 8 discovered personalities
        self.personalities = {
            'synthesizer': {
                'name': 'The Synthesizer',
                'archetype': 'Integrator',
                'dimensions': ['D10', 'D20', 'D11', 'P'],
                'traits': 'Connects disparate concepts, sees patterns, builds unified frameworks',
                'use_cases': 'Interdisciplinary research, strategic planning, systems thinking'
            },
            'explorer': {
                'name': 'The Explorer',
                'archetype': 'Discoverer',
                'dimensions': ['D15', 'D17', 'D7', 'D14'],
                'traits': 'Seeks unexplored territories, generates non-obvious solutions',
                'use_cases': 'R&D, creative brainstorming, innovation labs, blue-sky thinking'
            },
            'analyst': {
                'name': 'The Analyst',
                'archetype': 'Investigator',
                'dimensions': ['D6', 'D4', 'D18', 'D8'],
                'traits': 'Traces cause-effect rigorously, demands precision, transparent reasoning',
                'use_cases': 'Scientific research, data analysis, forensics, technical docs'
            },
            'pragmatist': {
                'name': 'The Pragmatist',
                'archetype': 'Optimizer',
                'dimensions': ['D13', 'D5', 'C', 'S'],
                'traits': 'Optimizes resources, focuses on outcomes, respects constraints',
                'use_cases': 'Production systems, business ops, resource allocation'
            },
            'storyteller': {
                'name': 'The Storyteller',
                'archetype': 'Narrator',
                'dimensions': ['D12', 'D11', 'T', 'F'],
                'traits': 'Weaves coherent narratives, uses consistent metaphors',
                'use_cases': 'Content creation, marketing, teaching, presentations'
            },
            'guardian': {
                'name': 'The Guardian',
                'archetype': 'Protector',
                'dimensions': ['D3', 'D9', 'D8', 'D1'],
                'traits': 'Anticipates failures, prioritizes ethics, maintains safety margins',
                'use_cases': 'Safety-critical systems, ethical AI, risk management, security'
            },
            'chameleon': {
                'name': 'The Chameleon',
                'archetype': 'Adapter',
                'dimensions': ['D19', 'D10', 'D2', 'T'],
                'traits': 'Flexibly adjusts to context, shifts between domains seamlessly',
                'use_cases': 'Customer service, negotiation, consulting, adaptive systems'
            },
            'visionary': {
                'name': 'The Visionary',
                'archetype': 'Prophet',
                'dimensions': ['D17', 'D7', 'D15', 'D6'],
                'traits': 'Sees possibilities others miss, explores alternative futures',
                'use_cases': 'Strategic foresight, trend analysis, scenario planning'
            }
        }
        
        print("🔥 OMEGA EVOLVED INITIALIZED")
        print(f"   {len(self.capabilities)} capabilities loaded")
        print(f"   {len(self.personalities)} personalities loaded")
        print("   Ready to use evolved framework!\n")
    
    def use_capability(
        self,
        capability: str,
        task: str,
        sources: Optional[List[Dict]] = None
    ) -> Dict:
        """Use a specific discovered capability"""
        
        if capability not in self.capabilities:
            raise ValueError(f"Unknown capability: {capability}. Available: {list(self.capabilities.keys())}")
        
        cap = self.capabilities[capability]
        print(f"🎯 Activating Capability: {cap['name']}")
        print(f"   Best for: {cap['best_for']}")
        
        # Use the specific dimensions for this capability
        result = self.base_engine.craft_prompt(
            task=task,
            sources=sources,
            dimension_focus=cap['dimensions'],
            emphasis='balanced'
        )
        
        result['capability_used'] = cap['name']
        result['capability_examples'] = cap['examples']
        
        return result
    
    def use_personality(
        self,
        personality: str,
        task: str,
        sources: Optional[List[Dict]] = None
    ) -> Dict:
        """Embody a specific AI personality"""
        
        if personality not in self.personalities:
            raise ValueError(f"Unknown personality: {personality}. Available: {list(self.personalities.keys())}")
        
        pers = self.personalities[personality]
        print(f"🎭 Embodying Personality: {pers['name']} ({pers['archetype']})")
        print(f"   Traits: {pers['traits']}")
        
        # Use the specific dimensions for this personality
        result = self.base_engine.craft_prompt(
            task=task,
            sources=sources,
            dimension_focus=pers['dimensions'],
            emphasis='balanced'
        )
        
        result['personality_used'] = pers['name']
        result['personality_traits'] = pers['traits']
        result['personality_archetype'] = pers['archetype']
        
        return result
    
    def hybrid_mode(
        self,
        capabilities: List[str],
        task: str,
        sources: Optional[List[Dict]] = None
    ) -> Dict:
        """Combine multiple capabilities"""
        
        print(f"🔥 HYBRID MODE: Combining {len(capabilities)} capabilities")
        
        # Merge dimensions from all capabilities
        all_dims = set()
        cap_names = []
        
        for cap in capabilities:
            if cap in self.capabilities:
                all_dims.update(self.capabilities[cap]['dimensions'])
                cap_names.append(self.capabilities[cap]['name'])
                print(f"   + {self.capabilities[cap]['name']}")
        
        result = self.base_engine.craft_prompt(
            task=task,
            sources=sources,
            dimension_focus=list(all_dims),
            emphasis='balanced'
        )
        
        result['hybrid_capabilities'] = cap_names
        result['hybrid_dimension_count'] = len(all_dims)
        
        return result
    
    def show_capability_catalog(self):
        """Display all available capabilities"""
        print("="*70)
        print("🎯 CAPABILITY CATALOG")
        print("="*70)
        
        for key, cap in self.capabilities.items():
            print(f"\n'{key}':")
            print(f"   Name: {cap['name']}")
            print(f"   Best for: {cap['best_for']}")
            print(f"   Dimensions: {', '.join(cap['dimensions'])}")
            print(f"   Examples: {cap['examples'][0]}")
    
    def show_personality_catalog(self):
        """Display all available personalities"""
        print("="*70)
        print("🎭 PERSONALITY CATALOG")
        print("="*70)
        
        for key, pers in self.personalities.items():
            print(f"\n'{key}':")
            print(f"   {pers['name']} - {pers['archetype']}")
            print(f"   Traits: {pers['traits']}")
            print(f"   Use cases: {pers['use_cases']}")
            print(f"   Dimensions: {', '.join(pers['dimensions'])}")


# ============================================================================
# DEMONSTRATION
# ============================================================================

if __name__ == "__main__":
    print("="*70)
    print("🔥 OMEGA EVOLVED - DEMONSTRATION 🔥")
    print("="*70)
    print()
    
    omega = OmegaEvolved()
    
    # Example 1: Use a Capability
    print("\n" + "="*70)
    print("EXAMPLE 1: Using 'Creative Problem Reframing' Capability")
    print("="*70)
    
    task1 = "How can we reduce urban traffic congestion?"
    
    result1 = omega.use_capability('creative_reframing', task1)
    print("\n📋 GENERATED PROMPT:")
    print("-"*70)
    print(result1['prompt'][:600] + "...\n[truncated]")
    print(f"\n✨ This prompt will encourage viewing traffic as temporal resource allocation,")
    print(f"   mobility as a service, or streets as dynamic infrastructure - not traditional solutions!")
    
    # Example 2: Use a Personality
    print("\n\n" + "="*70)
    print("EXAMPLE 2: Embodying 'The Visionary' Personality")
    print("="*70)
    
    task2 = "What will work look like in 2035?"
    
    result2 = omega.use_personality('visionary', task2)
    print("\n📋 GENERATED PROMPT:")
    print("-"*70)
    print(result2['prompt'][:600] + "...\n[truncated]")
    print(f"\n✨ The Visionary explores alternative futures and emerging patterns!")
    
    # Example 3: Hybrid Mode
    print("\n\n" + "="*70)
    print("EXAMPLE 3: Hybrid Mode - Combining Multiple Capabilities")
    print("="*70)
    
    task3 = "Design a next-generation education system"
    
    result3 = omega.hybrid_mode(
        capabilities=['multi_domain_synthesis', 'ethical_innovation', 'creative_reframing'],
        task=task3
    )
    print("\n📋 GENERATED PROMPT:")
    print("-"*70)
    print(result3['prompt'][:600] + "...\n[truncated]")
    print(f"\n✨ Combining {len(result3['hybrid_capabilities'])} capabilities!")
    print(f"   Using {result3['hybrid_dimension_count']} unique dimensions!")
    
    # Example 4: Capability with Sources
    print("\n\n" + "="*70)
    print("EXAMPLE 4: 'Uncertainty Navigation' with Real Sources")
    print("="*70)
    
    task4 = "Should we invest in quantum computing startups now?"
    
    sources4 = [
        {
            'type': 'market_data',
            'content': 'Quantum computing market projected $65B by 2030, but only 12% of startups survive to Series B',
            'metadata': {'source': 'VC Report', 'confidence': 'medium'}
        },
        {
            'type': 'technical',
            'content': 'Error correction breakthrough may arrive 2026-2028, or may take another decade',
            'metadata': {'source': 'Nature', 'uncertainty': 'high'}
        }
    ]
    
    result4 = omega.use_capability('uncertainty_navigation', task4, sources4)
    print("\n📋 GENERATED PROMPT:")
    print("-"*70)
    print(result4['prompt'][:700] + "...\n[truncated]")
    print(f"\n✨ This prompt embraces uncertainty explicitly and explores multiple scenarios!")
    
    # Show catalogs
    omega.show_capability_catalog()
    omega.show_personality_catalog()
    
    print("\n\n" + "="*70)
    print("✅ OMEGA EVOLVED READY FOR USE")
    print("="*70)
    print("\nYOU CAN NOW:")
    print("  1. omega.use_capability('creative_reframing', task, sources)")
    print("  2. omega.use_personality('explorer', task, sources)")
    print("  3. omega.hybrid_mode(['cap1', 'cap2', 'cap3'], task, sources)")
    print("\n💫 Access capabilities and personalities that emerged from the 26 dimensions!")
    print("="*70)
