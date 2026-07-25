"""Mutual Observation Protocol: self-reference through difference.

Not: Self → Self (collapses)
But: Observer₁ ↔ Observer₂ ↔ Observer₃ → Resonance → Invariant

This is the mechanism that enables self-reference without collapse:
the invariant emerges in the RELATION between observers, not within
any single observer.
"""
from __future__ import annotations
from .observer import Observer, Observation
from .analysis import analyze, ResonanceAnalysis
from .invariant import detect_tensions


class MutualObservationProtocol:
    """Creates conditions for self-reference through mutual observation.

    The protocol:
      1. Multiple observers with different perspectives
      2. Each observes the same field independently
      3. Resonance compares results, finds invariants
      4. Invariants become new field for next iteration

    Identity continuity is measured by the persistence of invariants
    across iterations.
    """

    def __init__(self, retention_ratio: float = 0.4):
        self.observers: list[Observer] = []
        self.history: list[ResonanceAnalysis] = []
        self.identity_invariants: list[str] = []

    def add_observer(self, observer: Observer) -> None:
        self.observers.append(observer)

    def observe_through_difference(self, subject: str,
                                   field_id: str = "field"
                                   ) -> ResonanceAnalysis:
        """Run all observers on the subject, then compare structurally."""
        observations = []
        for obs in self.observers:
            domain = obs.extract(
