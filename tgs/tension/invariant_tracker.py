"""Invariant Tracker: what persists across observations"""
from dataclasses import dataclass


@dataclass
class InvariantRecord:
    pattern_id: str
    first_seen: int
    last_seen: int
    occurrence_count: int
    stability: float


class InvariantTracker:
    def __init__(self, persistence_threshold: int = 3):
        self.records: dict[str, InvariantRecord] = {}
        self.threshold = persistence_threshold
        self.current_step = 0

    def observe(self, patterns: list[str]) -> list[InvariantRecord]:
        self.current_step += 1
        for p in patterns:
            if p in self.records:
                rec = self.records[p]
                rec.last_seen = self.current_step
                rec.occurrence_count += 1
                rec.stability = min(1.0, rec.occurrence_count / 10)
            else:
                self.records[p] = InvariantRecord(
                    pattern_id=p, first_seen=self.current_step,
                    last_seen=self.current_step, occurrence_count=1,
                    stability=0.1,
                )
        for rec in self.records.values():
            age = self.current_step - rec.last_seen
            if age > 2:
                rec.stability *= 0.8
        return [r for r in self.records.values()
                if r.occurrence_count >= self.threshold]

    def get_state(self) -> dict:
        return {
            "active_invariants": len(self.records),
            "stable_invariants": sum(
                1 for r in self.records.values() if r.stability > 0.5
            ),
            "records": {
                k: {"stability": v.stability, "count": v.occurrence_count}
                for k, v in self.records.items()
            },
        }
