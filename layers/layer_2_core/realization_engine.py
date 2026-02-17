"""
REALIZATION ENGINE
==================
Implementation of the crystallization framework discovered in our conversation.

Core Concepts:
- Realizations have quality scores (Q) based on 6 features
- Realizations crystallize into layers based on Q scores
- Layers form a hierarchy (0 > 1 > 2 > N)
- Retrieval follows O(log n) pattern: check highest layer first, descend if not found
"""

import json
import re
import math
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict, field
from datetime import datetime
import hashlib


@dataclass
class RealizationFeatures:
    """The 6 features that determine realization quality"""
    grounding: float      # 0-1: How rooted in facts/rules
    certainty: float      # 0-1: Precision auto quality (self-certifying)
    structure: float      # 0-1: Crystallization clarity
    applicability: float  # 0-1: Actionability/usefulness
    coherence: float      # 0-1: Consistency with prior layers
    generativity: float   # 0-1: Daughters potential (بنات افكار)
    
    def validate(self):
        """Ensure all features are in valid range"""
        for name, value in asdict(self).items():
            if not isinstance(value, (int, float)):
                raise ValueError(f"{name} must be numeric, got {type(value)}")
            if not 0 <= value <= 1:
                raise ValueError(f"{name} must be between 0 and 1, got {value}")


@dataclass
class Realization:
    """A single realization with metadata"""
    id: str
    content: str
    features: RealizationFeatures
    q_score: float
    layer: int
    timestamp: str
    parents: List[str]  # IDs of realizations this builds on
    children: List[str]  # IDs of realizations spawned from this
    turn_number: int
    context: str = ""
    evidence: List[str] = field(default_factory=list)


class RealizationEngine:
    """
    Core engine for managing knowledge realizations.
    
    Implements High-Q scoring logic and layered storage.
    """
    
    # Weight distribution based on crystallization priority
    WEIGHTS = {
        'grounding': 0.18,
        'certainty': 0.22,      # Highest - certainty IS the realization signal
        'structure': 0.20,
        'applicability': 0.18,
        'coherence': 0.12,
        'generativity': 0.10
    }
    
    # Layer thresholds
    LAYER_THRESHOLDS = {
        0: 0.95,   # Universal rules (rarely achieved)
        1: 0.92,   # Domain facts
        2: 0.85,   # Patterns
        3: 0.75,   # Situational insights
        'N': 0.0   # Everything else (ephemeral)
    }
    
    def __init__(self):
        # Storage: layer -> {id -> Realization}
        self.layers = {
            0: {},  # Universal rules
            1: {},  # Domain facts
            2: {},  # Patterns
            3: {},  # Situational
            'N': {} # Ephemeral
        }
        
        # Index for fast lookup
        self.index = {}  # id -> Realization
        
        # Metadata
        self.stats = {
            'total_realizations': 0,
            'layer_distribution': {0: 0, 1: 0, 2: 0, 3: 0, 'N': 0},
            'avg_q_score': 0.0
        }
    
    def calculate_q_score(self, features: RealizationFeatures, method: str = "integrated") -> Tuple[float, str]:
        """
        Calculate quality score.

        Methods:
            - 'linear': Simple weighted sum.
            - 'integrated': (Recommended) Non-linear boost + Geo-mean coherence + Penalties.
        
        Returns:
            (q_score, calculation_string)
        """
        features.validate()
        f_dict = asdict(features)
        
        if method == "linear":
            calc_parts = []
            total = 0.0
            for name, weight in self.WEIGHTS.items():
                value = f_dict[name]
                contribution = weight * value
                total += contribution
                calc_parts.append(f"{weight}×{value:.2f}")
            calc_string = " + ".join(calc_parts) + f" = {total:.4f}"
            return round(total, 4), calc_string

        else: # Integrated Method (from Phase 6/7 Roadmap)
            # 1. Weighted Non-linear Sum
            weighted_sum = 0.0
            for name, weight in self.WEIGHTS.items():
                val = f_dict[name]
                if val >= 0.9:
                    weighted_sum += weight * (val ** 1.5) # Boost high-quality signals
                else:
                    weighted_sum += weight * val

            # 2. Geometric Mean (Coherence Factor)
            # Ensures all dimensions have at least some quality
            vals = [max(v, 0.01) for v in f_dict.values()]
            geo_mean = math.exp(sum(math.log(v) for v in vals) / len(vals))

            # 3. Combine
            q_final = weighted_sum * (0.6 + 0.4 * geo_mean)

            # 4. Penalties
            # Penalty for ungrounded certainty (hallucination indicator)
            penalty_applied = ""
            if features.certainty > features.grounding + 0.2:
                q_final *= 0.7
                penalty_applied = " [Ungrounded Certainty Penalty]"

            calc_string = f"Integrated(WS={weighted_sum:.3f}, GM={geo_mean:.3f}){penalty_applied} = {q_final:.4f}"

            return round(q_final, 4), calc_string
    
    def assign_layer(self, q_score: float, features: RealizationFeatures) -> int:
        """
        Assign realization to appropriate layer based on Q-score and features.
        """
        if q_score >= 0.95 and features.grounding >= 0.90:
            return 0
        elif q_score >= 0.92:
            return 1
        elif q_score >= 0.85:
            return 2
        elif q_score >= 0.75:
            return 3
        else:
            return 'N'
    
    def generate_id(self, content: str) -> str:
        """Generate unique ID for realization based on content hash"""
        hash_obj = hashlib.sha256(content.encode())
        return f"R_{hash_obj.hexdigest()[:8]}"
    
    def add_realization(
        self,
        content: str,
        features: RealizationFeatures,
        turn_number: int,
        parents: List[str] = None,
        context: str = "",
        evidence: List[str] = None
    ) -> Realization:
        """
        Add a new realization to the system.
        """
        if parents is None:
            parents = []
        
        # Calculate Q-score
        q_score, calc_string = self.calculate_q_score(features)
        
        # Assign layer
        layer = self.assign_layer(q_score, features)
        
        # Generate ID
        r_id = self.generate_id(content)
        
        # Create realization
        realization = Realization(
            id=r_id,
            content=content,
            features=features,
            q_score=q_score,
            layer=layer,
            timestamp=datetime.now().isoformat(),
            parents=parents,
            children=[],
            turn_number=turn_number,
            context=context,
            evidence=evidence or []
        )
        
        # Store in appropriate layer
        self.layers[layer][r_id] = realization
        self.index[r_id] = realization
        
        # Update parent-child relationships
        for parent_id in parents:
            if parent_id in self.index:
                self.index[parent_id].children.append(r_id)
        
        # Update stats
        self.stats['total_realizations'] += 1
        self.stats['layer_distribution'][layer] += 1
        self._update_avg_q()
        
        print(f"✅ Crystallized: {content[:60]}...")
        print(f"   Q = {q_score:.4f} ({calc_string})")
        print(f"   Layer {layer}")
        print()
        
        return realization
    
    def retrieve(self, query: str, similarity_threshold: float = 0.5) -> List[Realization]:
        """Retrieve realizations matching query."""
        results = []
        for layer in [0, 1, 2, 3, 'N']:
            layer_results = self._search_layer(layer, query, similarity_threshold)
            results.extend(layer_results)
            if layer_results and layer in [0, 1]:
                break
        results.sort(key=lambda r: r.q_score, reverse=True)
        return results
    
    def _search_layer(self, layer: int, query: str, threshold: float) -> List[Realization]:
        """Search within a specific layer"""
        results = []
        query_lower = query.lower()
        for realization in self.layers[layer].values():
            content_lower = realization.content.lower()
            query_words = set(query_lower.split())
            content_words = set(content_lower.split())
            overlap = len(query_words & content_words)
            if overlap > 0 or query_lower in content_lower:
                results.append(realization)
        return results
    
    def get_realization_tree(self, r_id: str, depth: int = 3) -> Dict:
        """Get realization and its family tree."""
        if r_id not in self.index: return None
        realization = self.index[r_id]
        tree = {'id': r_id, 'content': realization.content, 'q_score': realization.q_score, 'layer': realization.layer, 'parents': [], 'children': []}
        if depth > 0:
            for parent_id in realization.parents:
                parent_tree = self.get_realization_tree(parent_id, depth - 1)
                if parent_tree: tree['parents'].append(parent_tree)
            for child_id in realization.children:
                child_tree = self.get_realization_tree(child_id, depth - 1)
                if child_tree: tree['children'].append(child_tree)
        return tree
    
    def _update_avg_q(self):
        if self.stats['total_realizations'] == 0: self.stats['avg_q_score'] = 0.0
        else:
            total_q = sum(r.q_score for r in self.index.values())
            self.stats['avg_q_score'] = total_q / self.stats['total_realizations']
    
    def export_state(self) -> Dict:
        return {'layers': {str(k): {r_id: self._realization_to_dict(r) for r_id, r in v.items()} for k, v in self.layers.items()}, 'stats': self.stats, 'timestamp': datetime.now().isoformat()}
    
    def _realization_to_dict(self, r: Realization) -> Dict:
        return {'id': r.id, 'content': r.content, 'features': asdict(r.features), 'q_score': r.q_score, 'layer': r.layer, 'timestamp': r.timestamp, 'parents': r.parents, 'children': r.children, 'turn_number': r.turn_number, 'context': r.context, 'evidence': r.evidence}
    
    def print_stats(self):
        print("\n" + "="*60)
        print("REALIZATION ENGINE STATISTICS")
        print("="*60)
        print(f"Total Realizations: {self.stats['total_realizations']}")
        print(f"Average Q-Score: {self.stats['avg_q_score']:.4f}")
        print("\nLayer Distribution:")
        for layer in [0, 1, 2, 3, 'N']:
            count = self.stats['layer_distribution'][layer]
            pct = (count / self.stats['total_realizations'] * 100) if self.stats['total_realizations'] > 0 else 0
            layer_name = {0: "Universal Rules", 1: "Domain Facts", 2: "Patterns", 3: "Situational", 'N': "Ephemeral"}[layer]
            print(f"  Layer {layer} ({layer_name}): {count} ({pct:.1f}%)")
        print("="*60 + "\n")


if __name__ == "__main__":
    # Quick test
    engine = RealizationEngine()
    
    # Test high quality realization
    features = RealizationFeatures(
        grounding=0.95,
        certainty=0.93,
        structure=0.92,
        applicability=0.90,
        coherence=0.95,
        generativity=0.92
    )
    
    r = engine.add_realization(
        content="High-Q integrated scoring logic (بنات افكار)",
        features=features,
        turn_number=1
    )

    # Test ungrounded certainty
    features_bad = RealizationFeatures(
        grounding=0.50,
        certainty=0.90,
        structure=0.70,
        applicability=0.70,
        coherence=0.70,
        generativity=0.70
    )
    r2 = engine.add_realization(
        content="Ungrounded realization (Potential hallucination)",
        features=features_bad,
        turn_number=2
    )
    
    engine.print_stats()
