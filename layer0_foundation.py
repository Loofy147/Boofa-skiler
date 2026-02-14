#!/usr/bin/env python3
"""
Layer 0: Core Mathematical Framework
Based on math-skills.txt and skill-ecosystem-integration-guide.md

This is the FOUNDATION - all other layers build on this.
"""

import numpy as np
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, field
import json

# ============================================================================
# SKILL REPRESENTATION (From math-skills.txt)
# ============================================================================

@dataclass
class Skill:
    """
    8-dimensional skill representation in ℝ⁸
    
    s = (G, C, S, A, H, V, P, T) ∈ ℝ⁸
    """
    name: str
    
    # 8 dimensions with weights
    G: float = 0.0  # Grounding (18%)
    C: float = 0.0  # Certainty (20%)
    S: float = 0.0  # Structure (18%)
    A: float = 0.0  # Applicability (16%)
    H: float = 0.0  # Coherence (12%)
    V: float = 0.0  # Generativity (8%)
    P: float = 0.0  # Presentation (5%)
    T: float = 0.0  # Temporal (3%)
    
    # Metadata
    priority: float = 0.5
    cost: float = 1.0
    embedding: Optional[np.ndarray] = None
    
    def __post_init__(self):
        if self.embedding is None:
            # Create embedding from 8 dimensions
            self.embedding = self.to_vector()
    
    def to_vector(self) -> np.ndarray:
        """Convert to vector representation"""
        return np.array([self.G, self.C, self.S, self.A, self.H, self.V, self.P, self.T])
    
    def q_score(self) -> float:
        """
        Calculate Q-score:
        Q = 0.18×G + 0.20×C + 0.18×S + 0.16×A + 0.12×H + 0.08×V + 0.05×P + 0.03×T
        """
        return (
            0.18 * self.G +
            0.20 * self.C +
            0.18 * self.S +
            0.16 * self.A +
            0.12 * self.H +
            0.08 * self.V +
            0.05 * self.P +
            0.03 * self.T
        )

# ============================================================================
# SIMILARITY FUNCTIONS (From math-skills.txt)
# ============================================================================

def cosine_similarity(v1: np.ndarray, v2: np.ndarray) -> float:
    """
    Cosine similarity:
    sim(vᵢ, vⱼ) = (vᵢ · vⱼ) / (||vᵢ|| · ||vⱼ||)
    """
    dot_product = np.dot(v1, v2)
    norm_product = np.linalg.norm(v1) * np.linalg.norm(v2)
    
    if norm_product == 0:
        return 0.0
    
    return dot_product / norm_product

def build_adjacency_matrix(skills: List[Skill]) -> np.ndarray:
    """
    Adjacency matrix A where:
    A_ij = sim(vᵢ, vⱼ)
    """
    n = len(skills)
    A = np.zeros((n, n))
    
    for i in range(n):
        for j in range(n):
            A[i, j] = cosine_similarity(skills[i].embedding, skills[j].embedding)
    
    return A

# ============================================================================
# INTERACTION TENSOR (From skill-ecosystem-integration-guide.md)
# ============================================================================

def compute_interaction(s1: Skill, s2: Skill, alpha: float = 0.7, beta: float = 0.3) -> float:
    """
    Interaction strength:
    I(i,j,k) = α · sim(vᵢ,vⱼ) + β · ∇²ₖE(sᵢ, sⱼ)
    
    Classification:
    - I > 0.7:  SYNERGISTIC
    - |I| < 0.3: INDEPENDENT
    - I < -0.5: ANTAGONISTIC
    """
    sim = cosine_similarity(s1.embedding, s2.embedding)
    
    # Simplified curvature term (for now just use Q-score difference)
    q_diff = abs(s1.q_score() - s2.q_score())
    curvature = -q_diff  # Negative because large difference = antagonistic
    
    interaction = alpha * sim + beta * curvature
    
    return interaction

def classify_interaction(interaction: float) -> str:
    """Classify interaction type"""
    if interaction > 0.7:
        return "SYNERGISTIC"
    elif abs(interaction) < 0.3:
        return "INDEPENDENT"
    elif interaction < -0.5:
        return "ANTAGONISTIC"
    else:
        return "NEUTRAL"

# ============================================================================
# SKILL SYNTHESIS (From math-skills.txt)
# ============================================================================

def synthesize_skills(parents: List[Skill], gamma: float = 0.20) -> Skill:
    """
    Emergent skill synthesis:
    s_emergent = Σᵢ αᵢsᵢ + γ · (s₁ ⊗ s₂ ⊗ ... ⊗ sₖ)
    
    For now: weighted average + tensor product term
    """
    # Calculate weights based on Q-scores
    q_scores = np.array([s.q_score() for s in parents])
    weights = q_scores / q_scores.sum()
    
    # Weighted average of dimensions
    vectors = np.array([s.to_vector() for s in parents])
    avg_vector = np.average(vectors, axis=0, weights=weights)
    
    # Tensor product term (simplified: element-wise product of normalized vectors)
    normalized_vectors = vectors / np.linalg.norm(vectors, axis=1, keepdims=True)
    tensor_term = np.prod(normalized_vectors, axis=0) * gamma
    
    # Combine
    emergent_vector = avg_vector + tensor_term
    
    # Clip to [0, 1]
    emergent_vector = np.clip(emergent_vector, 0, 1)
    
    # Create emergent skill
    emergent = Skill(
        name="+".join([s.name for s in parents]),
        G=emergent_vector[0],
        C=emergent_vector[1],
        S=emergent_vector[2],
        A=emergent_vector[3],
        H=emergent_vector[4],
        V=emergent_vector[5],
        P=emergent_vector[6],
        T=emergent_vector[7],
        priority=max(s.priority for s in parents),
        cost=sum(s.cost for s in parents) / len(parents)
    )
    
    return emergent

# ============================================================================
# UTILITY CALCULATION (From math-skills.txt)
# ============================================================================

def compute_utility(skill: Skill, task_embedding: np.ndarray) -> float:
    """
    Utility of skill for task:
    U_i(t) = q_i · g(sim(v_i, t))
    
    where g(s) = max(0, s) for simplicity
    """
    sim = cosine_similarity(skill.embedding, task_embedding)
    g = max(0, sim)  # Activation function
    
    utility = skill.q_score() * g
    
    return utility

# ============================================================================
# SKILL SELECTION (From math-skills.txt)
# ============================================================================

def select_skills(
    skills: List[Skill],
    task_embedding: np.ndarray,
    budget: float = 10.0,
    gamma: float = 0.1
) -> List[int]:
    """
    Greedy skill selection:
    max_x x^T U + (γ/2) x^T A x  subject to c^T x ≤ B
    
    Greedy approximation: rank by marginal gain / cost
    """
    n = len(skills)
    selected = []
    selected_indices = []
    total_cost = 0.0
    
    # Build adjacency matrix
    A = build_adjacency_matrix(skills)
    
    # Compute utilities
    utilities = np.array([compute_utility(s, task_embedding) for s in skills])
    
    # Greedy selection
    remaining = list(range(n))
    
    while remaining and total_cost < budget:
        best_gain = -np.inf
        best_idx = None
        
        for i in remaining:
            # Marginal utility
            u_i = utilities[i]
            
            # Synergy with selected skills
            synergy = 0
            for j in selected_indices:
                synergy += A[i, j]
            synergy *= gamma
            
            # Total marginal gain
            marginal_gain = u_i + synergy
            
            # Per-cost gain
            gain_per_cost = marginal_gain / skills[i].cost
            
            if gain_per_cost > best_gain:
                best_gain = gain_per_cost
                best_idx = i
        
        if best_idx is None:
            break
        
        # Add if within budget
        if total_cost + skills[best_idx].cost <= budget:
            selected_indices.append(best_idx)
            selected.append(skills[best_idx])
            total_cost += skills[best_idx].cost
            remaining.remove(best_idx)
        else:
            break
    
    return selected_indices

# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("LAYER 0: MATHEMATICAL FOUNDATION TESTS")
    print("=" * 60)
    
    # Create test skills from research documents
    meta_learning = Skill("Meta-Learning", G=0.95, C=0.92, S=0.95, A=0.98, H=0.95, V=0.92, P=0.90, T=0.90)
    transfer = Skill("Transfer-Learning", G=0.95, C=0.92, S=0.95, A=0.98, H=0.95, V=0.92, P=0.90, T=0.90)
    problem_solving = Skill("Universal-PS", G=0.95, C=0.92, S=0.95, A=0.98, H=0.95, V=0.92, P=0.90, T=0.90)
    
    print("\n[Test 1] Q-Score Calculation")
    print(f"  Meta-Learning Q: {meta_learning.q_score():.3f}")
    print(f"  Transfer Q: {transfer.q_score():.3f}")
    print(f"  Problem-Solving Q: {problem_solving.q_score():.3f}")
    
    print("\n[Test 2] Similarity Matrix")
    skills = [meta_learning, transfer, problem_solving]
    A = build_adjacency_matrix(skills)
    print(f"  Adjacency matrix:\n{A}")
    
    print("\n[Test 3] Interaction Classification")
    interaction = compute_interaction(meta_learning, transfer)
    classification = classify_interaction(interaction)
    print(f"  Meta-Learning ↔ Transfer: {interaction:.3f} ({classification})")
    
    print("\n[Test 4] Skill Synthesis")
    emergent = synthesize_skills([meta_learning, transfer])
    print(f"  Parents: {[s.name for s in [meta_learning, transfer]]}")
    print(f"  Parent Q avg: {np.mean([s.q_score() for s in [meta_learning, transfer]]):.3f}")
    print(f"  Emergent: {emergent.name}")
    print(f"  Emergent Q: {emergent.q_score():.3f}")
    print(f"  δ (gain): {emergent.q_score() - np.mean([s.q_score() for s in [meta_learning, transfer]]):.4f}")
    
    print("\n[Test 5] Skill Selection")
    task = np.array([0.9, 0.9, 0.8, 0.95, 0.85, 0.8, 0.75, 0.7])  # Task embedding
    selected_indices = select_skills(skills, task, budget=5.0)
    print(f"  Selected skills: {[skills[i].name for i in selected_indices]}")
    
    print("\n" + "=" * 60)
    print("ALL LAYER 0 TESTS COMPLETE")
    print("=" * 60)
