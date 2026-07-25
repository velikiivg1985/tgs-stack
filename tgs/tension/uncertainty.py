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

    # Known unknowns
    known_unknowns: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "blind_spot_ratio": self.blind_spot_ratio,
            "contradiction_ratio": self.contradiction_ratio,
            "divergence_ratio": self.divergence_ratio,
            "forgotten_ratio": self.forgotten_ratio,
            "observed_count": self.observed_count,
            "retained_count": self.retained_count,
            "rejected_count": self.rejected_count,
            "forgotten_count": self.forgotten_count,
            "total": self.total,
            "uncertainty": self.total,  # alias for backward compatibility
            "known_unknowns": self.known_unknowns,
        }


class UncertaintyTracker:
    """
    Tracks uncertainty arising from multiple sources.

    Key change from v0.1:
    - blind_ratio is MEASURED from data, not computed from R
    - Explicit tracking of observed vs retained vs forgotten
    - Support for contradiction and divergence measurement
    """

    def __init__(
        self,
        retention_ratio: float = 0.4,
        weights: dict[str, float] | None = None,
    ):
        self.R = retention_ratio
        self.blind_spots: list[BlindSpot] = []
        self.rejected_patterns: list[str] = []
        self.forgotten_patterns: list[str] = []
        self.step = 0

        # Per-step tracking
        self._cumulative_observed = 0
        self._cumulative_retained = 0
        self._cumulative_rejected = 0

        # Additional uncertainty sources
        self._contradiction_count = 0
        self._contradiction_pairs_checked = 0
        self._divergence_scores: list[float] = []
        self._known_unknowns: list[str] = []

        # Weights for aggregate uncertainty
        self.weights = weights or {
            "blind_spot": 0.35,
            "contradiction": 0.25,
            "divergence": 0.20,
            "forgotten": 0.20,
        }

    def observe(
        self,
        all_patterns: list[str],
        retained_patterns: list[str],
        step: int,
    ) -> dict:
        """
        Record an observation cycle.

        blind_ratio = rejected / observed  (measured from data, not 1-R)
        """
        self.step = step

        retained = set(retained_patterns)
        all_p = set(all_patterns)

        observed_this_step = len(all_p)
        retained_this_step = len(retained & all_p)
        rejected_this_step = observed_this_step - retained_this_step

        self._cumulative_observed += observed_this_step
        self._cumulative_retained += retained_this_step
        self._cumulative_rejected += rejected_this_step

        rejected = list(all_p - retained)
        self.rejected_patterns.extend(rejected)

        new_forgotten = [
            p for p in self.rejected_patterns
            if p not in all_p and p not in self.forgotten_patterns
        ]
        self.forgotten_patterns.extend(new_forgotten)

        # Real measurement (not 1 - R)
        if observed_this_step > 0:
            blind_ratio = rejected_this_step / observed_this_step
        else:
            blind_ratio = 0.0

        self.blind_spots.append(BlindSpot(
            description=(
                f"Compression lost {rejected_this_step}/{observed_this_step} "
                f"patterns (R={self.R:.2f}, measured={blind_ratio:.2f})"
            ),
            estimated_size=blind_ratio,
            source="compression_measurement",
            first_detected=step,
        ))

        return {
            "blind_ratio": blind_ratio,
            "rejected_this_step": rejected_this_step,
            "cumulative_rejected": len(self.rejected_patterns),
            "cumulative_forgotten": len(self.forgotten_patterns),
            "total_blind_spots": len(self.blind_spots),
            "measured_vs_configured": {
                "measured": blind_ratio,
                "configured_R": 1.0 - self.R,
                "match": abs(blind_ratio - (1.0 - self.R)) < 0.05,
            },
        }

    def record_contradiction(self, pattern_a: str, pattern_b: str) -> None:
        """Record that two observed patterns contradict each other."""
        self._contradiction_count += 1
        self._contradiction_pairs_checked += 1

    def record_compatible_pair(self, pattern_a: str, pattern_b: str) -> None:
        """Record that two observed patterns are compatible."""
        self._contradiction_pairs_checked += 1

    def record_observer_agreement(self, agreement_score: float) -> None:
        """Record agreement between two observers (0.0 to 1.0)."""
        if 0.0 <= agreement_score <= 1.0:
            self._divergence_scores.append(agreement_score)

    def add_known_unknown(self, description: str) -> None:
        """Explicitly track something we know we don't know."""
        if description not in self._known_unknowns:
            self._known_unknowns.append(description)

    def estimate_uncertainty(self) -> float:
        """Backward-compatible estimate of total uncertainty."""
        return self.get_state().total

    def get_state(self) -> UncertaintyState:
        """Return structured uncertainty state."""
        if self._cumulative_observed > 0:
            blind_ratio = self._cumulative_rejected / self._cumulative_observed
        else:
            blind_ratio = 0.0

        if self._contradiction_pairs_checked > 0:
            contradiction_ratio = (
                self._contradiction_count / self._contradiction_pairs_checked
            )
        else:
            contradiction_ratio = 0.0

        if self._divergence_scores:
            avg_agreement = sum(self._divergence_scores) / len(self._divergence_scores)
            divergence_ratio = 1.0 - avg_agreement
        else:
            divergence_ratio = 0.0

        total_seen = self._cumulative_observed + len(self.forgotten_patterns)
        if total_seen > 0:
            forgotten_ratio = len(self.forgotten_patterns) / total_seen
        else:
            forgotten_ratio = 0.0

        total = (
            self.weights["blind_spot"] * blind_ratio
            + self.weights["contradiction"] * contradiction_ratio
            + self.weights["divergence"] * divergence_ratio
            + self.weights["forgotten"] * forgotten_ratio
        )

        return UncertaintyState(
            blind_spot_ratio=blind_ratio,
            contradiction_ratio=contradiction_ratio,
            divergence_ratio=divergence_ratio,
            forgotten_ratio=forgotten_ratio,
            observed_count=self._cumulative_observed,
            retained_count=self._cumulative_retained,
            rejected_count=self._cumulative_rejected,
            forgotten_count=len(self.forgotten_patterns),
            total=total,
            known_unknowns=list(self._known_unknowns),
        )

    def get(self, key: str, default=None):
        """Dict-like access for compatibility with TensionCore."""
        state_dict = self.get_state().to_dict()
        return state_dict.get(key, default)

    def __getitem__(self, key: str):
        """Dict-like access for compatibility with TensionCore."""
        state_dict = self.get_state().to_dict()
        return state_dict[key]
