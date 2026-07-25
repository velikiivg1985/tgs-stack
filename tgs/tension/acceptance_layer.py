"""
Acceptance Layer - converts incompatible patterns into persistent tensions.

Key fixes:
- Deterministic ID generation using SHA-256 (not Python hash())
- Separation of contradiction detection and acceptance
- Explicit tension lifecycle tracking
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from typing import Protocol


class ContradictionDetector(Protocol):
    """Protocol for detecting contradictions between patterns."""
    
    def detect(self, pattern_a: str, pattern_b: str) -> bool:
        """Return True if patterns are contradictory."""
        ...


@dataclass
class Tension:
    """Represents an unresolved tension between two poles."""
    
    id: str
    pole_a: str
    pole_b: str
    intensity: float = 1.0
    created_at: int = 0
    last_seen: int = 0
    reactivations: int = 0
    
    def reactivate(self, current_time: int) -> None:
        """Mark tension as reactivated."""
        self.last_seen = current_time
        self.reactivations += 1
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "pole_a": self.pole_a,
            "pole_b": self.pole_b,
            "intensity": self.intensity,
            "created_at": self.created_at,
            "last_seen": self.last_seen,
            "reactivations": self.reactivations,
        }


class KeywordContradictionDetector:
    """Simple rule-based contradiction detector using keyword pairs."""
    
    OPPOSING_PAIRS = [
        ("preserve", "change"),
        ("stable", "transform"),
        ("same", "different"),
        ("identity", "dissolve"),
        ("persist", "vanish"),
        ("maintain", "abandon"),
        ("coherent", "fragmented"),
    ]
    
    def detect(self, pattern_a: str, pattern_b: str) -> bool:
        """Check if patterns contain opposing keywords."""
        a_lower = pattern_a.lower()
        b_lower = pattern_b.lower()
        
        for term_a, term_b in self.OPPOSING_PAIRS:
            if (term_a in a_lower and term_b in b_lower) or \
               (term_b in a_lower and term_a in b_lower):
                return True
        
        return False


class AcceptanceLayer:
    """
    Converts incompatible patterns into persistent tensions.
    
    Unlike TensionCore (which detects tensions from system state),
    AcceptanceLayer actively chooses to hold contradictions together,
    making them part of the system's identity.
    """
    
    def __init__(
        self,
        detector: ContradictionDetector | None = None,
    ):
        self.detector = detector or KeywordContradictionDetector()
        self.tensions: dict[str, Tension] = {}
        self.step = 0
    
    def accept(self, pole_a: str, pole_b: str) -> Tension | None:
        """
        Accept a pair of patterns as a persistent tension.
        
        Returns the Tension object if contradiction detected, None otherwise.
        """
        # Check if detector identifies contradiction
        if not self.detector.detect(pole_a, pole_b):
            return None
        
        # Generate deterministic ID
        tension_id = self._make_id(pole_a, pole_b)
        
        # Create or reactivate tension
        if tension_id in self.tensions:
            tension = self.tensions[tension_id]
            tension.reactivate(self.step)
        else:
            tension = Tension(
                id=tension_id,
                pole_a=pole_a,
                pole_b=pole_b,
                created_at=self.step,
                last_seen=self.step,
            )
            self.tensions[tension_id] = tension
        
        self.step += 1
        return tension
    
    def _make_id(self, pole_a: str, pole_b: str) -> str:
        """
        Generate deterministic ID for tension.
        
        Uses SHA-256 instead of Python hash() for reproducibility
        across runs and platforms.
        """
        poles = sorted([pole_a.strip(), pole_b.strip()])
        raw = "\x00".join(poles).encode("utf-8")
        digest = hashlib.sha256(raw).hexdigest()[:16]
        return f"tension_{digest}"
    
    def get_active_tensions(self) -> list[Tension]:
        """Return all active tensions."""
        return list(self.tensions.values())
    
    def get_tension_count(self) -> int:
        """Return total number of tensions."""
        return len(self.tensions)
    
    def to_dict(self) -> dict:
        return {
            "step": self.step,
            "tensions": {tid: t.to_dict() for tid, t in self.tensions.items()},
        }
