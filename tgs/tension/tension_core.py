"""Tension Core: holds unresolved contradictions as generative forces"""
from dataclasses import dataclass


@dataclass
class Tension:
    id: str
    pole_a: str
    pole_b: str
    kind: str
    intensity: float
    first_detected: int
    last_active: int
    times_reactivated: int = 0


class TensionCore:
    VALID_KINDS = {
        "same_and_different", "known_and_unknown",
        "observer_and_observed", "stable_and_changing",
        "compressed_and_lost",
    }

    def __init__(self):
        self.tensions: dict[str, Tension] = {}
        self.step = 0

    def detect(self, kind: str, pole_a: str, pole_b: str,
               intensity: float = 0.5) -> Tension:
        if kind not in self.VALID_KINDS:
            raise ValueError(f"Unknown tension kind: {kind}")
        self.step += 1
        tid = f"{kind}:{pole_a[:8]}:{pole_b[:8]}"
        if tid in self.tensions:
            t = self.tensions[tid]
            t.last_active = self.step
            t.times_reactivated += 1
            t.intensity = min(1.0, t.intensity + 0.1)
        else:
            t = Tension(id=tid, pole_a=pole_a, pole_b=pole_b, kind=kind,
                       intensity=intensity, first_detected=self.step,
                       last_active=self.step)
            self.tensions[tid] = t
        return t

    def detect_from_state(self, invariant_state: dict,
                          difference_state: dict,
                          uncertainty_state: dict) -> list[Tension]:
        detected = []
        if (invariant_state.get("stable_invariants", 0) > 0
                and difference_state.get("avg_magnitude", 0) > 0.1):
            detected.append(self.detect(
                "same_and_different",
                f"invariants={invariant_state['stable_invariants']}",
                f"change={difference_state['avg_magnitude']:.2f}",
                intensity=0.6,
            ))
        if (invariant_state.get("stable_invariants", 0) > 0
                and uncertainty_state.get("uncertainty", 0) > 0.2):
            detected.append(self.detect(
                "known_and_unknown",
                f"known={invariant_state['stable_invariants']}",
                f"uncertainty={uncertainty_state['uncertainty']:.2f}",
                intensity=0.5,
            ))
        if (uncertainty_state.get("rejected_count", 0) > 0
                and uncertainty_state.get("forgotten_count", 0) > 0):
            detected.append(self.detect(
                "compressed_and_lost",
                f"rejected={uncertainty_state['rejected_count']}",
                f"forgotten={uncertainty_state['forgotten_count']}",
                intensity=0.4,
            ))
        return detected

    def active_tensions(self, decay_window: int = 5) -> list[Tension]:
        return [
            t for t in self.tensions.values()
            if (self.step - t.last_active < decay_window) or t.intensity > 0.7
        ]

    def get_state(self) -> dict:
        active = self.active_tensions()
        return {
            "total_tensions": len(self.tensions),
            "active_tensions": len(active),
            "max_intensity": max((t.intensity for t in active), default=0.0),
            "tensions": [
                {"id": t.id, "kind": t.kind, "intensity": t.intensity,
                 "reactivations": t.times_reactivated}
                for t in active
            ],
        }
