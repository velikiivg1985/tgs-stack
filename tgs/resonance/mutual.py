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
                subject,
                f"{field_id}__{obs.id}",
                f"{obs.name} view",
                f"subject:{field_id}",
            )
            observations.append(Observation(
                id=f"obs_{obs.id}_{len(self.history)}",
                field_id=field_id,
                field_content=subject,
                observer=obs,
                domain=domain,
                operator=f"observer:{obs.id}",
            ))

        analysis = analyze(observations, pattern_size=2)
        detect_tensions(analysis, observations)
        self.history.append(analysis)

        # Track identity: invariants that persist across iterations
        inv_hashes = [inv["pattern_hash"] for inv in analysis.invariants]
        self.identity_invariants = list(
            set(self.identity_invariants) | set(inv_hashes)
        )
        return analysis

    def reflect(self) -> dict:
        """Compute identity continuity across iterations."""
        if not self.history:
            return {"status": "no history"}
        current_inv = set(
            inv["pattern_hash"] for inv in self.history[-1].invariants
        )
        past_inv = set(self.identity_invariants)
        persistent = current_inv & past_inv
        emerged = current_inv - past_inv
        lost = past_inv - current_inv
        return {
            "status": "reflected",
            "persistent_invariants": list(persistent),
            "emerged_invariants": list(emerged),
            "lost_invariants": list(lost),
            "identity_continuity": (
                len(persistent) / max(1, len(past_inv))
            ),
            "total_history_depth": len(self.history),
        }

    def challenge(self, hypothesis: str) -> dict:
        """Ask: under what conditions would this hypothesis NOT hold?"""
        return {
            "hypothesis": hypothesis,
            "falsification": [
                "Invariant disappears under new observer",
                "Invariant does not survive rephrasing",
                "Counter-example shows different structure",

