import numpy as np
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, field
import json

@dataclass
class Skill:
    name: str
    G: float = 0.0
    C: float = 0.0
    S: float = 0.0
    A: float = 0.0
    H: float = 0.0
    V: float = 0.0
    P: float = 0.0
    T: float = 0.0
    priority: float = 0.5
    cost: float = 1.0
    embedding: Optional[np.ndarray] = None
    
    def __post_init__(self):
        if self.embedding is None:
            self.embedding = self.to_vector()
    
    def to_vector(self) -> np.ndarray:
        return np.array([self.G, self.C, self.S, self.A, self.H, self.V, self.P, self.T])
    
    def q_score(self) -> float:
        return (0.18 * self.G + 0.20 * self.C + 0.18 * self.S + 0.16 * self.A +
                0.12 * self.H + 0.08 * self.V + 0.05 * self.P + 0.03 * self.T)

def cosine_similarity(v1: np.ndarray, v2: np.ndarray) -> float:
    dot_product = np.dot(v1, v2)
    norm_product = np.linalg.norm(v1) * np.linalg.norm(v2)
    return dot_product / norm_product if norm_product != 0 else 0.0

def build_adjacency_matrix(skills: List[Skill]) -> np.ndarray:
    n = len(skills)
    A = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            A[i, j] = cosine_similarity(skills[i].embedding, skills[j].embedding)
    return A

def compute_interaction(s1: Skill, s2: Skill, alpha: float = 0.7, beta: float = 0.3) -> float:
    sim = cosine_similarity(s1.embedding, s2.embedding)
    q_diff = abs(s1.q_score() - s2.q_score())
    return alpha * sim + beta * (-q_diff)

def classify_interaction(interaction: float) -> str:
    if interaction > 0.7: return "SYNERGISTIC"
    if abs(interaction) < 0.3: return "INDEPENDENT"
    if interaction < -0.5: return "ANTAGONISTIC"
    return "NEUTRAL"

def synthesize_skills(parents: List[Skill], gamma: float = 0.35, custom_weights: Optional[List[float]] = None) -> Skill:
    if custom_weights is not None:
        weights = np.array(custom_weights) / np.sum(custom_weights)
    else:
        q_scores = np.array([s.q_score() for s in parents])
        weights = q_scores / q_scores.sum()
    
    vectors = np.array([s.to_vector() for s in parents])
    avg_vector = np.average(vectors, axis=0, weights=weights)
    normalized_vectors = vectors / np.linalg.norm(vectors, axis=1, keepdims=True)
    tensor_term = np.prod(normalized_vectors, axis=0) * gamma
    emergent_vector = np.clip(avg_vector + tensor_term, 0, 1)
    
    return Skill(
        name="+".join([s.name for s in parents]),
        G=emergent_vector[0], C=emergent_vector[1], S=emergent_vector[2],
        A=emergent_vector[3], H=emergent_vector[4], V=emergent_vector[5],
        P=emergent_vector[6], T=emergent_vector[7],
        priority=max(s.priority for s in parents),
        cost=sum(s.cost for s in parents) / len(parents)
    )

def compute_utility(skill: Skill, task_embedding: np.ndarray) -> float:
    sim = cosine_similarity(skill.embedding, task_embedding)
    return skill.q_score() * max(0, sim)

def select_skills(skills: List[Skill], task_embedding: np.ndarray, budget: float = 10.0, gamma: float = 0.1) -> List[int]:
    n = len(skills)
    selected_indices = []
    total_cost = 0.0
    A = build_adjacency_matrix(skills)
    utilities = np.array([compute_utility(s, task_embedding) for s in skills])
    remaining = list(range(n))
    while remaining and total_cost < budget:
        best_gain, best_idx = -np.inf, None
        for i in remaining:
            synergy = sum(A[i, j] for j in selected_indices) * gamma
            gain_per_cost = (utilities[i] + synergy) / skills[i].cost
            if gain_per_cost > best_gain:
                best_gain, best_idx = gain_per_cost, i
        if best_idx is None or total_cost + skills[best_idx].cost > budget: break
        selected_indices.append(best_idx)
        total_cost += skills[best_idx].cost
        remaining.remove(best_idx)
    return selected_indices

if __name__ == "__main__":
    meta_learning = Skill("Meta-Learning", G=0.95, C=0.92, S=0.95, A=0.98, H=0.95, V=0.92, P=0.90, T=0.90)
    transfer = Skill("Transfer-Learning", G=0.95, C=0.92, S=0.95, A=0.98, H=0.95, V=0.92, P=0.90, T=0.90)
    print(f"Parents Q avg: {(meta_learning.q_score() + transfer.q_score())/2:.3f}")
    emergent = synthesize_skills([meta_learning, transfer])
    print(f"Emergent Q: {emergent.q_score():.3f}")
    print(f"Delta: {emergent.q_score() - (meta_learning.q_score() + transfer.q_score())/2:.4f}")
