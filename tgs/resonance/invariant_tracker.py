"""
Invariant Tracker - identifies structural invariants, not just repeated strings.

Key fixes:
- Pattern normalization (case, punctuation)
- Structural similarity (not exact string matching)
- Transformation tracking
- Explicit invariant lifecycle
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field


@dataclass
class Pattern:
    """Raw pattern with metadata."""
    text: str
    normalized: str
    timestamp: int
    source: str = "default"


@dataclass
class Invariant:
    """
    Structural invariant - a pattern that persists through transformations.
    
    Unlike simple string matching, invariants are groups of similar patterns
    that represent the same underlying structure.
    """
    
    id: str
    canonical_form: str  # Representative pattern
    variants: list[str] = field(default_factory=list)  # All observed forms
    occurrence_count: int = 0
    first_seen: int = 0
    last_seen: int = 0
    transformations: list[tuple[str, str]] = field(default_factory=list)
    
    def add_variant(self, pattern: str, timestamp: int) -> None:
        """Add a new variant of this invariant."""
        if pattern not in self.variants:
            # Track transformation from last variant
            if self.variants:
                last = self.variants[-1]
                if last != pattern:
                    self.transformations.append((last, pattern))
            self.variants.append(pattern)
        
        self.occurrence_count += 1
        self.last_seen = timestamp
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "canonical_form": self.canonical_form,
            "variants": self.variants,
            "occurrence_count": self.occurrence_count,
            "first_seen": self.first_seen,
            "last_seen": self.last_seen,
            "transformation_count": len(self.transformations),
        }


def normalize_pattern(text: str) -> str:
    """
    Normalize pattern for structural comparison.
    
    - Lowercase
    - Remove extra whitespace
    - Remove punctuation (optional, can be tuned)
    """
    text = text.lower().strip()
    text = re.sub(r'\s+', ' ', text)  # Normalize whitespace
    # Keep punctuation for now - it can be meaningful
    return text


def jaccard_similarity(text_a: str, text_b: str, n: int = 2) -> float:
    """
    Calculate Jaccard similarity between two texts using n-grams.
    
    This captures structural similarity better than exact matching.
    """
    def get_ngrams(text: str, n: int) -> set[str]:
        """Extract character n-grams from text."""
        return {text[i:i+n] for i in range(len(text) - n + 1)}
    
    ngrams_a = get_ngrams(text_a, n)
    ngrams_b = get_ngrams(text_b, n)
    
    if not ngrams_a or not ngrams_b:
        return 0.0
    
    intersection = len(ngrams_a & ngrams_b)
    union = len(ngrams_a | ngrams_b)
    
    return intersection / union if union > 0 else 0.0


def word_overlap_similarity(text_a: str, text_b: str) -> float:
    """
    Calculate word overlap similarity.
    
    Captures semantic similarity when words are reordered.
    """
    words_a = set(text_a.lower().split())
    words_b = set(text_b.lower().split())
    
    if not words_a or not words_b:
        return 0.0
    
    intersection = len(words_a & words_b)
    union = len(words_a | words_b)
    
    return intersection / union if union > 0 else 0.0


def combined_similarity(text_a: str, text_b: str) -> float:
    """
    Combined similarity metric using multiple approaches.
    
    This is a simple heuristic - for production, use embeddings.
    """
    # Normalize both texts
    norm_a = normalize_pattern(text_a)
    norm_b = normalize_pattern(text_b)
    
    # Exact match after normalization
    if norm_a == norm_b:
        return 1.0
    
    # Calculate multiple similarity scores
    jaccard = jaccard_similarity(norm_a, norm_b, n=3)
    word_overlap = word_overlap_similarity(norm_a, norm_b)
    
    # Weighted combination
    return 0.6 * jaccard + 0.4 * word_overlap


class InvariantTracker:
    """
    Tracks structural invariants across observations.
    
    An invariant is a pattern that persists through transformations.
    Unlike simple counting, this identifies patterns that are
    structurally similar even if not identical.
    """
    
    SIMILARITY_THRESHOLD = 0.7  # Threshold for considering patterns as same invariant
    
    def __init__(self, similarity_threshold: float | None = None):
        if similarity_threshold is not None:
            self.SIMILARITY_THRESHOLD = similarity_threshold
        
        self.invariants: dict[str, Invariant] = {}
        self.patterns: list[Pattern] = []
        self.step = 0
    
    def observe(self, text: str, source: str = "default") -> Invariant | None:
        """
        Record a pattern observation and update invariants.
        
        Returns the Invariant this pattern belongs to, or None if new.
        """
        # Normalize pattern
        normalized = normalize_pattern(text)
        
        # Create Pattern object
        pattern = Pattern(
            text=text,
            normalized=normalized,
            timestamp=self.step,
            source=source,
        )
        self.patterns.append(pattern)
        
        # Find matching invariant
        invariant = self._find_or_create_invariant(normalized, self.step)
        
        self.step += 1
        return invariant
    
    def _find_or_create_invariant(self, normalized: str, timestamp: int) -> Invariant:
        """Find existing invariant or create new one."""
        # Check similarity with existing invariants
        best_match = None
        best_similarity = 0.0
        
        for inv in self.invariants.values():
            similarity = combined_similarity(normalized, inv.canonical_form)
            if similarity > best_similarity:
                best_similarity = similarity
                best_match = inv
        
        # If similarity above threshold, add to existing invariant
        if best_match and best_similarity >= self.SIMILARITY_THRESHOLD:
            best_match.add_variant(normalized, timestamp)
            return best_match
        
        # Otherwise, create new invariant
        invariant_id = f"inv_{len(self.invariants):04d}"
        invariant = Invariant(
            id=invariant_id,
            canonical_form=normalized,
            variants=[normalized],
            occurrence_count=1,
            first_seen=timestamp,
            last_seen=timestamp,
        )
        self.invariants[invariant_id] = invariant
        
        return invariant
    
    def get_invariants(self, min_occurrences: int = 2) -> list[Invariant]:
        """
        Return invariants that occurred at least min_occurrences times.
        
        This filters out one-off observations.
        """
        return [
            inv for inv in self.invariants.values()
            if inv.occurrence_count >= min_occurrences
        ]
    
    def get_persistent_invariants(self, min_occurrences: int = 3) -> list[Invariant]:
        """
        Return highly persistent invariants.
        
        These are patterns that truly persist through change.
        """
        return self.get_invariants(min_occurrences)
    
    def get_transformation_chains(self) -> list[list[str]]:
        """
        Return sequences of transformations for each invariant.
        
        This shows how patterns evolve while maintaining identity.
        """
        chains = []
        for inv in self.invariants.values():
            if len(inv.variants) > 1:
                chains.append(inv.variants)
        return chains
    
    def get_invariant_count(self) -> int:
        """Return total number of invariants."""
        return len(self.invariants)
    
    def to_dict(self) -> dict:
        return {
            "invariant_count": len(self.invariants),
            "pattern_count": len(self.patterns),
            "invariants": {
                inv_id: inv.to_dict()
                for inv_id, inv in self.invariants.items()
            },
        }
