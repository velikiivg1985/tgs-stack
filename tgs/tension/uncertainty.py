"""Uncertainty Tracker: estimates blind spots and real uncertainty.

Sources of uncertainty:
1. Blind spots (from compression/retention)
2. Contradictions (incompatible observations)
3. Divergence (observers disagree)
4. Forgotten patterns (patterns that no longer appear)
5. Known unknowns (things we know we don't know)
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol


@dataclass
class BlindSpot:
    description: str
    estimated_size: float
    source: str
    first_detected: int


@dataclass
class UncertaintyState:
    """Structured view of current uncertainty."""
    blind_spot_ratio: float = 0.0
    contradiction_ratio: float = 0.0
    divergence_ratio: float = 0.0
    forgotten_ratio: float = 0.0
    
    # Counts
    observed_count: int = 0
    retained_count: int = 0
    rejected_count: int = 0
    forgotten_count: int = 0
    
    # Aggregate
    total: float = 0.0
    
    def to_dict(self) -> dict:
        return {
            "blind_spot_ratio": self.blind_spot_ratio,
            "contradiction_ratio": self.contradiction_ratio,
            "divergence_ratio": self.divergence_ratio,
            "forgotten_ratio": self.forgotten_ratio,
            "observed_count": self.observed_count,
            "retained_count": self.retained_count,
            "rejected_count": self.rejected_count,
            "forgotten_count": self.forgotten
