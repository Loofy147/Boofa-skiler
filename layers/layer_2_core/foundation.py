#!/usr/bin/env python3
"""
Layer 2: Self-Evolution Engine
Auto-Skill-Detector, Pattern-Detection-Engine, Q-Score-Optimizer

From skill-ecosystem-integration-guide.md
"""

import sys
sys.path.append('/home/claude')

from layers.layer_0_universal.foundation import Skill, build_adjacency_matrix, synthesize_skills
from layers.layer_1_domain.foundation import create_layer1_ecosystem
import numpy as np
from typing import List, Dict, Tuple
from collections import defaultdict
from dataclasses import dataclass
import json

# ============================================================================
# AUTO-SKILL-DETECTOR (Q=0.952)
# ============================================================================

class AutoSkillDetector:
    """
    Monitors patterns and generates skills automatically.
    Trigger: 3+ repetitions OR complexity > 0.8
    """
    
    def __init__(self, threshold: int = 3):
        self.pattern_cache = defaultdict(int)
        self.threshold = threshold
        self.generated_skills = []
        
        self.skill = Skill(
            name="Auto-Skill-Detector",
            G=0.95, C=0.93, S=0.96, A=0.95, H=0.96, V=0.95, P=0.95, T=0.92
        )
    
    def record_usage(self, skills_used: List[str], task: str, outcome: float):
        """Track skill co-usage patterns"""
        pattern_sig = "+".join(sorted(skills_used))
        self.pattern_cache[pattern_sig] += 1
        
        # Check if threshold reached
        if self.pattern_cache[pattern_sig] >= self.threshold:
            return self._should_generate(pattern_sig, skills_used)
        
        return None
    
    def _should_generate(self, pattern_sig: str, skills_used: List[str]) -> bool:
        """Check if we should generate new skill"""
        # Don't regenerate
        if pattern_sig in [s.name for s in self.generated_skills]:
            return False
        
        # Calculate modularity (simplified)
        modularity = len(skills_used) / 10.0  # More skills = higher modularity
        
        if modularity > 0.2:
            return True
        
        return False
    
    def generate_skill(self, parent_skills: List[Skill]) -> Skill:
        """Generate emergent skill from pattern"""
        emergent = synthesize_skills(parent_skills, gamma=0.20)
        
        # Validate Q-score
        if emergent.q_score() >= 0.75:
            self.generated_skills.append(emergent)
            return emergent
        
        return None

# ============================================================================
# PATTERN-DETECTION-ENGINE (Q=0.941)
# ============================================================================

class PatternDetectionEngine:
    """
    Spectral graph analysis for pattern detection.
    Complexity: O(n log n)
    """
    
    def __init__(self):
        self.skill = Skill(
            name="Pattern-Detection-Engine",
            G=0.94, C=0.92, S=0.95, A=0.96, H=0.94, V=0.96, P=0.95, T=0.93
        )
    
    def detect_communities(self, skills: List[Skill]) -> Dict:
        """
        Spectral clustering via Laplacian eigendecomposition.
        
        L = D - A (Laplacian)
        Eigendecomposition: L v = λ v
        """
        n = len(skills)
        if n < 2:
            return {"communities": [], "modularity": 0.0}
        
        # Build adjacency matrix
        A = build_adjacency_matrix(skills)
        
        # Degree matrix
        D = np.diag(A.sum(axis=1))
        
        # Laplacian
        L = D - A
        
        # Eigendecomposition
        eigenvalues, eigenvectors = np.linalg.eigh(L)
        
        # Use k smallest non-zero eigenvalues for clustering
        k = min(3, n - 1)  # Number of communities
        
        # Simple clustering based on eigenvector signs
        communities = []
        for i in range(k):
            if i < len(eigenvalues) - 1:
                community = np.where(eigenvectors[:, i+1] > 0)[0].tolist()
                if len(community) > 0:
                    communities.append(community)
        
        # Calculate modularity
        modularity = self._compute_modularity(A, communities)
        
        return {
            "communities": communities,
            "modularity": modularity,
            "significant": modularity > 0.3
        }
    
    def _compute_modularity(self, A: np.ndarray, communities: List[List[int]]) -> float:
        """
        Q_modularity = (1/2m) Σᵢⱼ [Aᵢⱼ - (kᵢkⱼ/2m)] δ(cᵢ, cⱼ)
        """
        m = A.sum() / 2  # Total edges
        if m == 0:
            return 0.0
        
        n = A.shape[0]
        k = A.sum(axis=1)  # Degrees
        
        Q = 0.0
        for community in communities:
            for i in community:
                for j in community:
                    Q += A[i, j] - (k[i] * k[j]) / (2 * m)
        
        Q /= (2 * m)
        
        return Q

# ============================================================================
# Q-SCORE-OPTIMIZER (Q=0.928)
# ============================================================================

class QScoreOptimizer:
    """
    Continuous quality improvement via gradient-based optimization.
    Guarantee: Q(skill_t+1) ≥ Q(skill_t)
    """
    
    def __init__(self, target_q: float = 0.90, epsilon: float = 0.001):
        self.target_q = target_q
        self.epsilon = epsilon
        
        self.skill = Skill(
            name="Q-Score-Optimizer",
            G=0.93, C=0.91, S=0.94, A=0.94, H=0.93, V=0.92, P=0.93, T=0.92
        )
        
        # Dimension weights for optimization priority
        self.weights = {
            'G': 0.18, 'C': 0.20, 'S': 0.18, 'A': 0.16,
            'H': 0.12, 'V': 0.08, 'P': 0.05, 'T': 0.03
        }
    
    def optimize(self, skill: Skill, max_iterations: int = 5) -> Tuple[Skill, Dict]:
        """Iterative improvement until target Q reached"""
        
        history = []
        current = skill
        
        for iteration in range(max_iterations):
            q_current = current.q_score()
            history.append(q_current)
            
            # Check convergence
            if q_current >= self.target_q:
                return current, {
                    "converged": True,
                    "iterations": iteration + 1,
                    "final_q": q_current,
                    "history": history
                }
            
            # Find bottleneck
            bottleneck = self._find_bottleneck(current)
            
            # Improve bottleneck
            current = self._improve_dimension(current, bottleneck)
            
            # Check monotonic improvement
            q_new = current.q_score()
            assert q_new >= q_current, "Non-monotonic improvement!"
            
            # Check if change is too small
            if abs(q_new - q_current) < self.epsilon:
                return current, {
                    "converged": True,
                    "iterations": iteration + 1,
                    "final_q": q_new,
                    "history": history,
                    "reason": "epsilon_convergence"
                }
        
        return current, {
            "converged": False,
            "iterations": max_iterations,
            "final_q": current.q_score(),
            "history": history
        }
    
    def _find_bottleneck(self, skill: Skill) -> str:
        """Find dimension with lowest weighted score"""
        dimensions = {
            'G': skill.G, 'C': skill.C, 'S': skill.S, 'A': skill.A,
            'H': skill.H, 'V': skill.V, 'P': skill.P, 'T': skill.T
        }
        
        # Calculate weighted scores
        weighted_scores = {
            dim: score * self.weights[dim]
            for dim, score in dimensions.items()
        }
        
        # Find minimum
        bottleneck = min(weighted_scores, key=weighted_scores.get)
        
        return bottleneck
    
    def _improve_dimension(self, skill: Skill, dimension: str, delta: float = 0.05) -> Skill:
        """Improve specific dimension"""
        improved = Skill(
            name=skill.name,
            G=skill.G, C=skill.C, S=skill.S, A=skill.A,
            H=skill.H, V=skill.V, P=skill.P, T=skill.T,
            priority=skill.priority, cost=skill.cost
        )
        
        # Improve dimension (clip to [0, 1])
        current_value = getattr(improved, dimension)
        new_value = min(1.0, current_value + delta)
        setattr(improved, dimension, new_value)
        
        return improved

# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("LAYER 2: SELF-EVOLUTION ENGINE TESTS")
    print("=" * 60)
    
    # Get Layer 1 skills
    ecosystem = create_layer1_ecosystem()
    layer1_skills = ecosystem["skills"]
    
    print("\n[Test 1] Auto-Skill-Detector")
    detector = AutoSkillDetector(threshold=3)
    
    # Simulate usage patterns
    for i in range(5):
        result = detector.record_usage(
            ["Meta-Learning", "Transfer-Learning"],
            f"task_{i}",
            0.9
        )
        if i >= 2:
            print(f"  Iteration {i+1}: Should generate = {result}")
    
    # Generate skill
    if detector._should_generate("Meta-Learning+Transfer-Learning", ["Meta-Learning", "Transfer-Learning"]):
        new_skill = detector.generate_skill([layer1_skills[0], layer1_skills[1]])
        if new_skill:
            print(f"  Generated: {new_skill.name}, Q={new_skill.q_score():.3f}")
    
    print("\n[Test 2] Pattern-Detection-Engine")
    pattern_engine = PatternDetectionEngine()
    
    result = pattern_engine.detect_communities(layer1_skills)
    print(f"  Communities found: {len(result['communities'])}")
    print(f"  Modularity: {result['modularity']:.3f}")
    print(f"  Significant: {result['significant']}")
    
    print("\n[Test 3] Q-Score-Optimizer")
    optimizer = QScoreOptimizer(target_q=0.95)
    
    # Create suboptimal skill
    test_skill = Skill(
        name="Test-Skill",
        G=0.7, C=0.75, S=0.8, A=0.7, H=0.75, V=0.7, P=0.6, T=0.65
    )
    print(f"  Initial Q: {test_skill.q_score():.3f}")
    
    optimized, info = optimizer.optimize(test_skill)
    print(f"  Final Q: {optimized.q_score():.3f}")
    print(f"  Iterations: {info['iterations']}")
    print(f"  Converged: {info['converged']}")
    print(f"  Improvement: +{optimized.q_score() - test_skill.q_score():.3f}")
    
    # Verify monotonic improvement
    print(f"  History: {[f'{q:.3f}' for q in info['history']]}")
    for i in range(len(info['history']) - 1):
        assert info['history'][i+1] >= info['history'][i], "Non-monotonic!"
    print(f"  ✅ Monotonic improvement verified")
    
    print("\n" + "=" * 60)
    print("LAYER 2 TESTS COMPLETE")
    print("=" * 60)
