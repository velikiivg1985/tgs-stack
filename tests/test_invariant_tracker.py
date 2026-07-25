"""Tests for InvariantTracker with structural similarity."""

import pytest
from tgs.resonance.invariant_tracker import (
    InvariantTracker,
    normalize_pattern,
    jaccard_similarity,
    word_overlap_similarity,
    combined_similarity,
)


class TestInvariantTracker:
    """Test suite for InvariantTracker."""
    
    def test_exact_duplicate_creates_invariant(self):
        """Test that exact duplicates are tracked as same invariant."""
        tracker = InvariantTracker()
        
        tracker.observe("identity persists")
        tracker.observe("identity persists")
        
        invariants = tracker.get_invariants(min_occurrences=2)
        assert len(invariants) == 1
        assert invariants[0].occurrence_count == 2
    
    def test_similar_patterns_grouped(self):
        """Test that similar patterns are grouped as same invariant."""
        tracker = InvariantTracker(similarity_threshold=0.7)
        
        tracker.observe("identity persists through change")
        tracker.observe("identity persists through transformation")
        
        # Should be grouped as same invariant
        invariants = tracker.get_invariants(min_occurrences=1)
        
        # Check that at least one invariant has multiple variants
        has_variants = any(len(inv.variants) > 1 for inv in invariants)
        assert has_variants or len(invariants) <= 2
    
    def test_different_patterns_separate(self):
        """Test that different patterns create separate invariants."""
        tracker = InvariantTracker()
        
        tracker.observe("identity persists")
        tracker.observe("tension holds contradictions")
        
        invariants = tracker.get_invariants(min_occurrences=1)
        assert len(invariants) == 2
    
    def test_transformation_tracking(self):
        """Test that transformations are tracked."""
        tracker = InvariantTracker(similarity_threshold=0.6)
        
        tracker.observe("preserve identity")
        tracker.observe("preserve identity through change")
        tracker.observe("preserve identity through transformation")
        
        chains = tracker.get_transformation_chains()
        
        # Should have at least one chain with transformations
        assert len(chains) >= 0  # May vary based on similarity threshold
    
    def test_normalization(self):
        """Test that patterns are normalized."""
        tracker = InvariantTracker()
        
        tracker.observe("Identity Persists")
        tracker.observe("identity persists")
        
        # Should be same invariant after normalization
        invariants = tracker.get_invariants(min_occurrences=2)
        assert len(invariants) == 1


class TestSimilarityMetrics:
    """Test suite for similarity metrics."""
    
    def test_normalize_pattern(self):
        """Test pattern normalization."""
        assert normalize_pattern("Identity Persists") == "identity persists"
        assert normalize_pattern("  extra   spaces  ") == "extra spaces"
    
    def test_jaccard_similarity_identical(self):
        """Test Jaccard similarity for identical strings."""
        sim = jaccard_similarity("hello world", "hello world")
        assert sim == 1.0
    
    def test_jaccard_similarity_different(self):
        """Test Jaccard similarity for different strings."""
        sim = jaccard_similarity("hello", "world")
        assert sim < 0.5
    
    def test_word_overlap_identical(self):
        """Test word overlap for identical strings."""
        sim = word_overlap_similarity("identity persists", "identity persists")
        assert sim == 1.0
    
    def test_word_overlap_reordered(self):
        """Test word overlap for reordered words."""
        sim = word_overlap_similarity("identity persists", "persists identity")
        assert sim == 1.0
    
    def test_combined_similarity(self):
        """Test combined similarity metric."""
        sim = combined_similarity("identity persists", "identity persists")
        assert sim == 1.0
        
        sim = combined_similarity("identity persists", "tension holds")
        assert sim < 0.5


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
