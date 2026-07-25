"""Uncertainty Tracker: estimates blind spots"""
from dataclasses import dataclass


@dataclass
class BlindSpot:
    description: str
    estimated_size: float
    source: str
    first_detected: int


class UncertaintyTracker:
    def __init__(self, retention_ratio: float = 0.4):
        self.R = retention_ratio
        self.blind_spots: list[BlindSpot] = []
        self.rejected_patterns: list[str] = []
        self.forgotten_patterns: list[str] = []
        self.step = 0

    def observe(self, all_patterns: list[str],
                retained_patterns: list[str],
                step: int) -> dict:
        self.step = step
        retained = set(retained_patterns)
        all_p = set(all_patterns)
        rejected = list(all_p - retained)
        self.rejected_patterns.extend(rejected)
        forgotten = [
            p for p in self.rejected_patterns
            if p not in all_p and p not in self.forgotten_patterns
        ]
        self.forgotten_patterns.extend(forgotten)
        blind_ratio = 1.0 - self.R
        self.blind_spots.append(BlindSpot(
            description=f"Patterns lost to R={self.R:.2f} compression",
            estimated_size=blind_ratio,
            source="retention_ratio",
            first_detected=step,
        ))
        return {
            "blind_ratio": blind_ratio,
            "rejected_this_step": len(rejected),
            "cumulative_rejected": len(self.rejected_patterns),
            "cumulative_forgotten": len(self.forgotten_patterns),
            "total_blind_spots": len(self.blind_spots),
        }

    def estimate_uncertainty(self) -> float:
        if not self.blind_spots:
            return 0.0
        return sum(b.estimated_size for b in self.blind_spots) / len(self.blind_spots)

    def get_state(self) -> dict:
        return {
            "retention_ratio": self.R,
            "uncertainty": self.estimate_uncertainty(),
            "rejected_count": len(self.rejected_patterns),
            "forgotten_count": len(self.forgotten_patterns),
            "blind_spots": len(self.blind_spots),
        }
