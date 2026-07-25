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
        """Ask: under what conditions would this hypothesis NOT hold?

        Generates structural falsification conditions consistent with
        TGS philosophy: an invariant claim must survive observer change,
        rephrasing, compression, and self-observation.

        Args:
            hypothesis: the claim to be stress-tested

        Returns:
            dict with hypothesis and list of falsification conditions
        """
        falsification = [
            "Invariant disappears under new observer",
            "Invariant does not survive rephrasing",
            "Counter-example shows different structure",
            "Invariant collapses under stronger compression (lower R)",
            "Invariant explodes when retention is increased (higher R)",
            "Self-observation changes the invariant being observed",
            "Mutual observers disagree on whether invariant exists",
            "Invariant is an artifact of observer vocabulary, not structure",
            "Invariant depends on a single observer's bias",
            "Tension resolution destroys the invariant rather than preserving it",
        ]
        return {
            "hypothesis": hypothesis,
            "falsification": falsification,
            "recommended_tests": falsification,  # alias for backward compat
            "status": "challenged",
            "challenge_count": len(falsification),
        }

    def get_agreement_scores(self) -> list[float]:
        """
        Compute pairwise agreement between observers based on shared invariants.

        Useful as input to UncertaintyTracker.record_observer_agreement().
        Returns empty list if fewer than 2 history entries.
        """
        if len(self.history) < 2:
            return []

        agreements: list[float] = []
        for i in range(len(self.history) - 1):
            inv_i = {inv["pattern_hash"] for inv in self.history[i].invariants}
            inv_j = {inv["pattern_hash"] for inv in self.history[i + 1].invariants}

            if not inv_i or not inv_j:
                agreements.append(0.0)
                continue

            intersection = len(inv_i & inv_j)
            union = len(inv_i | inv_j)
            agreements.append(intersection / union if union > 0 else 0.0)

        return agreements

    def get_persistent_invariants(self, min_persistence: int = 2) -> list[str]:
        """Return invariants that appeared in at least min_persistence iterations."""
        from collections import Counter

        counts: Counter[str] = Counter()
        for analysis in self.history:
            for inv in analysis.invariants:
                counts[inv["pattern_hash"]] += 1

        return [h for h, c in counts.items() if c >= min_persistence]

    def to_dict(self) -> dict:
        """Serialize protocol state."""
        return {
            "observer_count": len(self.observers),
            "history_depth": len(self.history),
            "identity_invariant_count": len(self.identity_invariants),
            "identity_invariants": self.identity_invariants,
        }


if __name__ == "__main__":
    # Minimal self-test: verify the protocol can be instantiated and challenged
    protocol = MutualObservationProtocol(retention_ratio=0.4)

    challenge = protocol.challenge("Identity persists through change")
    print(f"Hypothesis: {challenge['hypothesis']}")
    print(f"Falsification conditions: {challenge['challenge_count']}")
    for i, cond in enumerate(challenge["falsification"], 1):
        print(f"  {i}. {cond}")

    reflection = protocol.reflect()
    print(f"\nReflection: {reflection}")
