"""Difference Tracker: what changed between states"""
from dataclasses import dataclass, field


@dataclass
class DifferenceRecord:
    step: int
    emerged: list[str]
    vanished: list[str]
    transformed: list[dict]
    magnitude: float


class DifferenceTracker:
    def __init__(self):
        self.history: list[DifferenceRecord] = []
        self.previous_patterns: set[str] = set()

    def observe(self, current_patterns: list[str],
                step: int) -> DifferenceRecord:
        current = set(current_patterns)
        emerged = list(current - self.previous_patterns)
        vanished = list(self.previous_patterns - current)
        union = current | self.previous_patterns
        sym_diff = current ^ self.previous_patterns
        magnitude = len(sym_diff) / max(1, len(union))
        record = DifferenceRecord(
            step=step, emerged=emerged, vanished=vanished,
            transformed=[], magnitude=magnitude,
        )
        self.history.append(record)
        self.previous_patterns = current
        return record

    def get_cumulative_change(self) -> float:
        if not self.history:
            return 0.0
        return sum(r.magnitude for r in self.history) / len(self.history)

    def get_state(self) -> dict:
        return {
            "total_changes": len(self.history),
            "avg_magnitude": self.get_cumulative_change(),
            "last_emerged": self.history[-1].emerged if self.history else [],
            "last_vanished": self.history[-1].vanished if self.history else [],
        }
