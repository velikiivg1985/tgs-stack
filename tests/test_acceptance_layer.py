"""Tests for AcceptanceLayer with deterministic hashing."""

import pytest
from tgs.tension.acceptance_layer import (
    AcceptanceLayer,
    KeywordContradictionDetector,
    Tension,
)


class TestAcceptanceLayer:
    """Test suite for AcceptanceLayer."""
    
    def test_detects_contradiction(self):
        """Test that contradictory patterns create tension."""
        layer = AcceptanceLayer()
        tension = layer.accept("preserve identity", "change identity")
        
        assert tension is not None
        assert tension.pole_a == "preserve identity"
        assert tension.pole_b == "change identity"
    
    def test_does_not_detect_non_contradiction(self):
        """Test that non-contradictory patterns don't create tension."""
        layer = AcceptanceLayer()
        tension = layer.accept("observe pattern", "recognize invariant")
        
        assert tension is None
    
    def test_deterministic_id_generation(self):
        """Test that same pair always generates same ID."""
        layer1 = AcceptanceLayer()
        layer2 = AcceptanceLayer()
        
        t1 = layer1.accept("preserve identity", "change identity")
        t2 = layer2.accept("preserve identity", "change identity")
        
        assert t1.id == t2.id
        assert t1.id.startswith("tension_")
    
    def test_id_order_independent(self):
        """Test that order of poles doesn't affect ID."""
        layer = AcceptanceLayer()
        
        t1 = layer.accept("preserve identity", "change identity")
        t2 = layer.accept("change identity", "preserve identity")
        
        # Should be same ID (order independent)
        assert t1.id == t2.id
    
    def test_reactivation_increments_counter(self):
        """Test that reactivating same tension increments counter."""
        layer = AcceptanceLayer()
        
        t1 = layer.accept("preserve identity", "change identity")
        assert t1.reactivations == 0
        
        t2 = layer.accept("preserve identity", "change identity")
        assert t2.reactivations == 1
        assert t1.id == t2.id  # Same object
    
    def test_different_pairs_different_ids(self):
        """Test that different pairs get different IDs."""
        layer = AcceptanceLayer()
        
        t1 = layer.accept("preserve identity", "change identity")
        t2 = layer.accept("stable structure", "transform structure")
        
        assert t1.id != t2.id
    
    def test_get_active_tensions(self):
        """Test retrieving all active tensions."""
        layer = AcceptanceLayer()
        
        layer.accept("preserve identity", "change identity")
        layer.accept("stable structure", "transform structure")
        
        tensions = layer.get_active_tensions()
        assert len(tensions) == 2
    
    def test_custom_detector(self):
        """Test using custom contradiction detector."""
        class AlwaysContradict:
            def detect(self, a: str, b: str) -> bool:
                return True
        
        layer = AcceptanceLayer(detector=AlwaysContradict())
        tension = layer.accept("any pattern", "other pattern")
        
        assert tension is not None


class TestKeywordContradictionDetector:
    """Test suite for KeywordContradictionDetector."""
    
    def test_detects_known_pairs(self):
        """Test detection of predefined opposing pairs."""
        detector = KeywordContradictionDetector()
        
        assert detector.detect("preserve identity", "change identity")
        assert detector.detect("stable system", "transform system")
        assert detector.detect("same state", "different state")
    
    def test_does_not_detect_unrelated(self):
        """Test that unrelated patterns don't trigger."""
        detector = KeywordContradictionDetector()
        
        assert not detector.detect("observe pattern", "recognize invariant")
        assert not detector.detect("track tension", "accept contradiction")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
