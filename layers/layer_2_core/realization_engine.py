"""
REALIZATION ENGINE
==================
Implementation of the crystallization framework discovered in our conversation.

Core Concepts:
- Realizations have quality scores (Q) based on multi-dimensional features
- Realizations crystallize into layers based on Q scores
- Layers form a hierarchy (0 > 1 > 2 > N)
- Retrieval follows O(log n) pattern: check highest layer first, descend if not found
- Dynamic Weights: Supports evolving quality dimensions via Singularity Engine
"""

import json
import re
import math
import numpy as np
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict, field
from datetime import datetime
import hashlib


@dataclass
class RealizationFeatures:
    """The features that determine realization quality"""
    grounding: float      # 0-1: How rooted in facts/rules
    certainty: float      # 0-1: Precision auto quality (self-certifying)
    structure: float      # 0-1: Crystallization clarity
    applicability: float  # 0-1: Actionability/usefulness
    coherence: float      # 0-1: Consistency with prior layers
    generativity: float   # 0-1: Daughters potential (بنات افكار)
    
    # Optional extended features for Evolved Logic
    extra_features: Dict[str, float] = field(default_factory=dict)

    def validate(self):
        """Ensure all features are in valid range"""
        for name, value in asdict(self).items():
            if name == "extra_features":
                for k, v in value.items():
                    if not 0 <= v <= 1:
                        raise ValueError(f"Extra feature {k} must be between 0 and 1, got {v}")
                continue

            if not isinstance(value, (int, float)):
                raise ValueError(f"{name} must be numeric, got {type(value)}")
            if not 0 <= value <= 1:
                raise ValueError(f"{name} must be between 0 and 1, got {value}")

    def to_dict(self) -> Dict[str, float]:
        """Convert to flat dictionary for calculations"""
        d = {
            'G': self.grounding,
            'C': self.certainty,
            'S': self.structure,
            'A': self.applicability,
            'H': self.coherence,
            'V': self.generativity
        }
        # Add extra features with their keys
        for k, v in self.extra_features.items():
            d[k] = v
        return d


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
    """
    
    # Default Weights (Human Baseline)
    DEFAULT_WEIGHTS = {
        'G': 0.18,  # grounding
        'C': 0.22,  # certainty (Highest - certainty IS the realization signal)
        'S': 0.20,  # structure
        'A': 0.18,  # applicability
        'H': 0.12,  # coherence
        'V': 0.10   # generativity
    }
    
    def __init__(self, weights: Optional[Dict[str, float]] = None):
        # Initial weights
        self.weights = weights or self.DEFAULT_WEIGHTS.copy()

        # Storage: layer -> {id -> Realization}
        self.layers = {
            0: {},    # Universal rules
            1: {},    # Domain facts
            2: {},    # Patterns
            3: {},    # Situational
            'N': {}   # Ephemeral
        }
        
        # Index for fast lookup
        self.index = {}  # id -> Realization
        
        # Metadata
        self.stats = {
            'total_realizations': 0,
            'layer_distribution': {0: 0, 1: 0, 2: 0, 3: 0, 'N': 0},
            'avg_q_score': 0.0,
            'weight_evolution_count': 0
        }

    def update_weights(self, new_weights: Dict[str, float]):
        """Update the engine weights (called by Singularity Engine)"""
        self.weights.update(new_weights)
        self.stats['weight_evolution_count'] += 1
        print(f"🔄 Realization Engine Weights Updated (Evolution #{self.stats['weight_evolution_count']})")
    
    def calculate_q_score(self, features: RealizationFeatures, method: str = "integrated") -> Tuple[float, str]:
        """
        Calculate quality score.

        Methods:
            - 'linear': Simple weighted sum.
            - 'integrated': (Recommended) Non-linear boost + Geo-mean coherence + Penalties.
        """
        features.validate()
        f_dict = features.to_dict()

        # Map internal feature names to weight keys if necessary
        # Features: grounding, certainty, structure, applicability, coherence, generativity
        mapping = {
            'grounding': 'G', 'certainty': 'C', 'structure': 'S',
            'applicability': 'A', 'coherence': 'H', 'generativity': 'V'
        }

        # Normalize weights to sum to 1.0 (or whatever the target is)
        current_weights = self.weights
        weight_sum = sum(current_weights.values())
        
        if method == "linear":
            total = 0.0
            calc_parts = []
            for feat_name, feat_val in f_dict.items():
                # Check if we have a weight for this feature (either by full name or shorthand)
                weight = current_weights.get(feat_name) or current_weights.get(mapping.get(feat_name, ''))
                if weight:
                    contribution = weight * feat_val
                    total += contribution
                    calc_parts.append(f"{weight}×{feat_val:.2f}")

            calc_string = " + ".join(calc_parts) + f" = {total:.4f}"
            return round(total, 4), calc_string

        else: # Integrated Method (from Phase 6/7 Roadmap)
            # 1. Weighted Non-linear Sum
            weighted_sum = 0.0
            for feat_name, feat_val in f_dict.items():
                weight = current_weights.get(feat_name) or current_weights.get(mapping.get(feat_name, ''))
                if weight:
                    if feat_val >= 0.9:
                        weighted_sum += weight * (feat_val ** 1.5) # Boost high-quality signals
                    else:
                        weighted_sum += weight * feat_val

            # 2. Geometric Mean (Coherence Factor)
            # Ensures all dimensions have at least some quality
            vals = [max(v, 0.01) for v in f_dict.values() if isinstance(v, (int, float))]
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
    
    def assign_layer(self, q_score: float, features: RealizationFeatures) -> Any:
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
        
        # Phase 7: Sync with Global Ledger
        try:
            from layers.layer_2_core.global_realization_ledger import GlobalRealizationLedger
            ledger = GlobalRealizationLedger()
            ledger.add_realization(
                content=content,
                layer=layer if isinstance(layer, int) else 3,
                features=features.to_dict(),
                q_score=q_score,
                parents=parents,
                metadata={"engine": "RealizationEngine", "turn": turn_number}
            )
        except Exception as e:
            print(f"⚠️ Ledger Sync Failed: {e}")

        # Update stats
        self.stats['total_realizations'] += 1
        self.stats['layer_distribution'][layer] += 1
        self._update_avg_q()
        
        print(f"✅ Crystallized: {content[:60]}...")
        print(f"   Q = {q_score:.4f} ({calc_string})")
        print(f"   Layer {layer}")
        print()
        
        # Check for evolution (every 50 realizations)
        if self.stats['total_realizations'] % 50 == 0:
            self._trigger_evolution()

        return realization
    
    def _trigger_evolution(self):
        """Trigger Singularity evolution cycle"""
        try:
            from layers.layer_4_discovery.singularity_realization_engine import SingularityRealizationEngine
            s_engine = SingularityRealizationEngine(self)

            # Use recent realizations for evolution
            recent_ids = list(self.index.keys())[-100:]
            recent_realizations = [self.index[rid] for rid in recent_ids]
            recent_qs = [r.q_score for r in recent_realizations]

            analysis = s_engine.evolve(recent_realizations, recent_qs)

            # Update weights if evolution was successful
            evolved_weights = {dim_id: dim.weight for dim_id, dim in s_engine.dimensions.items()}
            self.update_weights(evolved_weights)

        except ImportError:
            # Avoid circular import issues if running in limited environment
            pass
        except Exception as e:
            print(f"⚠️ Evolution Trigger Failed: {e}")

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
        print(f"Weight Evolutions: {self.stats['weight_evolution_count']}")
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
    
    engine.print_stats()
