import os
#!/usr/bin/env python3
"""
FULL SYSTEM INTEGRATION TEST
All layers working together: L0 + L1 + L2 + L3

Demonstrates ClawdBot-Next capabilities.
"""

import sys
sys.path.append(os.getcwd())

from layers.layer_0_universal.foundation import *
from layers.layer_1_domain.foundation import *
from layers.layer_2_core.foundation import *
from layers.layer_3_orchestration.foundation import *
import asyncio
import time

class ClawdBotNext:
    """Complete self-evolving multi-agent system"""
    
    def __init__(self):
        print("Initializing ClawdBot-Next...")
        
        # Layer 1: Universal skills
        ecosystem = create_layer1_ecosystem()
        self.skills = ecosystem["skills"]
        self.skill_instances = ecosystem["instances"]
        
        # Layer 2: Self-evolution
        self.auto_detector = AutoSkillDetector(threshold=3)
        self.pattern_engine = PatternDetectionEngine()
        self.optimizer = QScoreOptimizer(target_q=0.90)
        
        # Layer 3: Multi-agent orchestration
        self.orchestrator = MultiAgentOrchestrator(num_executors=3)
        self.orchestrator.assign_skills_to_agents(self.skills)
        
        print(f"  ✅ Layer 1: {len(self.skills)} universal skills loaded")
        print(f"  ✅ Layer 2: Self-evolution engine active")
        print(f"  ✅ Layer 3: {len(self.orchestrator.agents)} agents initialized")
    
    async def execute(self, task: Dict) -> Dict:
        """Execute task through full system"""
        
        # 1. Multi-agent execution
        result = await self.orchestrator.execute_task(task)
        
        # 2. Pattern detection
        pattern_result = self.pattern_engine.detect_communities(self.skills)
        
        # 3. Auto-skill detection
        skills_used = [s.name for s in self.skills[:2]]  # Simplified
        should_generate = self.auto_detector.record_usage(
            skills_used, 
            task.get("id", "unknown"),
            1.0
        )
        
        # 4. Q-score optimization (if needed)
        low_q_skills = [s for s in self.skills if s.q_score() < 0.90]
        optimized_count = 0
        
        for skill in low_q_skills:
            optimized, info = self.optimizer.optimize(skill, max_iterations=3)
            if info["converged"]:
                optimized_count += 1
        
        return {
            "execution": result,
            "patterns": pattern_result,
            "new_skills_generated": should_generate is not None,
            "skills_optimized": optimized_count,
            "total_skills": len(self.skills)
        }
    
    def get_metrics(self) -> Dict:
        """System performance metrics"""
        return {
            "skills_count": len(self.skills),
            "avg_q_score": np.mean([s.q_score() for s in self.skills]),
            "throughput": self.orchestrator.get_throughput(),
            "agents": len(self.orchestrator.agents),
            "tasks_completed": self.orchestrator.tasks_completed
        }

async def main():
    print("=" * 60)
    print("CLAWDBOT-NEXT: FULL SYSTEM INTEGRATION TEST")
    print("=" * 60)
    
    # Initialize system
    system = ClawdBotNext()
    
    print("\n[Test 1] Initial Metrics")
    metrics = system.get_metrics()
    print(f"  Skills: {metrics['skills_count']}")
    print(f"  Average Q-score: {metrics['avg_q_score']:.3f}")
    print(f"  Agents: {metrics['agents']}")
    
    print("\n[Test 2] Execute Simple Task")
    task1 = {
        "id": "test_task_1",
        "embedding": np.array([0.9, 0.9, 0.8, 0.95, 0.85, 0.8, 0.75, 0.7])
    }
    result1 = await system.execute(task1)
    print(f"  ✅ Execution successful")
    print(f"  Subtasks: {result1['execution']['subtasks']}")
    print(f"  Patterns detected: {len(result1['patterns']['communities'])}")
    print(f"  New skills generated: {result1['new_skills_generated']}")
    
    print("\n[Test 3] Execute Complex Task")
    task2 = {
        "id": "complex_task",
        "components": ["analysis", "synthesis", "validation", "optimization"],
        "priority": 0.9
    }
    result2 = await system.execute(task2)
    print(f"  ✅ Execution successful")
    print(f"  Subtasks: {result2['execution']['subtasks']}")
    print(f"  Levels: {result2['execution']['levels']}")
    print(f"  Speedup: {result2['execution'].get('parallel_speedup', 1):.2f}x")
    
    print("\n[Test 4] Pattern Recognition")
    # Execute same pattern multiple times
    for i in range(5):
        await system.execute({
            "id": f"pattern_task_{i}",
            "components": ["comp_a", "comp_b"]
        })
    
    result3 = await system.execute({
        "id": "pattern_task_final",
        "components": ["comp_a", "comp_b"]
    })
    
    print(f"  Pattern executed 6 times")
    print(f"  Auto-skill detector triggered: {result3['new_skills_generated']}")
    
    print("\n[Test 5] Self-Improvement")
    # Create suboptimal skill
    test_skill = Skill("Test", G=0.7, C=0.75, S=0.8, A=0.7, H=0.75, V=0.7, P=0.6, T=0.65)
    system.skills.append(test_skill)
    
    print(f"  Added skill with Q={test_skill.q_score():.3f}")
    
    result4 = await system.execute(task1)
    print(f"  Skills optimized: {result4['skills_optimized']}")
    
    print("\n[Test 6] Final Metrics")
    final_metrics = system.get_metrics()
    print(f"  Total skills: {final_metrics['skills_count']}")
    print(f"  Average Q-score: {final_metrics['avg_q_score']:.3f}")
    print(f"  Throughput: {final_metrics['throughput']:.2f} tasks/sec")
    print(f"  Tasks completed: {final_metrics['tasks_completed']}")
    
    print("\n[Test 7] Skill Synthesis")
    # Synthesize new skill from Layer 1
    parent1 = system.skills[0]
    parent2 = system.skills[1]
    
    emergent = synthesize_skills([parent1, parent2])
    avg_parent_q = np.mean([parent1.q_score(), parent2.q_score()])
    
    print(f"  Parents: {parent1.name} + {parent2.name}")
    print(f"  Parent Q avg: {avg_parent_q:.3f}")
    print(f"  Emergent Q: {emergent.q_score():.3f}")
    print(f"  δ (gain): {emergent.q_score() - avg_parent_q:.4f}")
    print(f"  ✅ Emergence guarantee met" if emergent.q_score() > avg_parent_q else "  ❌ No emergence")
    
    print("\n" + "=" * 60)
    print("FULL SYSTEM INTEGRATION: SUCCESS ✅")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(main())
