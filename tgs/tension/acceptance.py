"""Acceptance Layer: Transforms contradictions into persistent relational structures

Three distinct operations in TGS:
    FORGETTING  → deletion (information lost)
    COMPRESSION → simplification (complexity reduced)
    ACCEPTANCE  → transformation (contradiction becomes stable relation)

Acceptance is not agreement. Not resolution. Not compromise.
It is the structural capacity to hold incompatibility without forced elimination.

    A ⟂ B  →  TENSION(A, B)  →  STABLE RELATION

The tension itself becomes a new object of observation.

Key distinction from Uncertainty:
    UNCERTAINTY: "I don't know which is correct: A or B"
    ACCEPTANCE:  "I see both are structurally significant,
                  and I'm not obligated to reduce them to one"
"""
from __future__ import annotations
from dataclasses import dataclass
from itertools import combinations
from typing import Optional


@dataclass
class UnresolvedTension:
    """A contradiction preserved as a persistent relational structure.
    
    Not "A or B" (choice). Not "average(A, B)" (compromise).
    Not "A = B" (collapse). But: A ↔ B where the relation becomes a new pattern.
    """
    id: str
    pole_a: str
    pole_b: str
    contradiction_type: str     # "structural", "temporal", "epistemic", "value"
    intensity: float            # 0..1
    status: str                 # "accepted", "active", "transforming"
    first_seen: int
    last_seen: int
    times_reactivated: int = 0
    question: Optional[str] = None
    resolution: Optional[str] = None  # None if unresolved (by design)

    def to_dict(self) -> dict:
        return {
            "id": self.id, "pole_a": self.pole_a, "pole_b": self.pole_b,
            "contradiction_type": self.contradiction_type,
            "intensity": self.intensity, "status": self.status,
            "question": self.question, "resolution": self.resolution,
            "first_seen": self.first_seen, "last_seen": self.last_seen,
            "reactivations": self.times_reactivated,
        }


class AcceptanceLayer:
    """Transforms contradictions into persistent relational structures.
    
    NOT a conflict resolver. A contradiction transformer.
    
    When two patterns are incompatible, the system does not:
      - choose one over the other
      - average them
      - delete one
      - force resolution
    
    Instead, it creates a TENSION object that:
      - preserves both poles
      - records their incompatibility
      - becomes itself an object of observation
      - may transform over time without being resolved
    """

    CONTRADICTION_TYPES = {
        "structural": "Two structures cannot coexist in the same space",
        "temporal": "Two states cannot be simultaneous",
        "epistemic": "Two claims cannot both be true under same interpretation",
        "value": "Two values pull in incompatible directions",
    }

    OPPOSING_PAIRS = [
        ("preserve", "change"), ("stable", "transform"),
        ("same", "different"), ("known", "unknown"),
        ("compress", "retain"), ("collapse", "explode"),
        ("self", "other"), ("identity", "difference"),
        ("internal", "external"), ("continuous", "discrete"),
        ("finite", "infinite"), ("determined", "free"),
    ]

    OPPOSING_STRENGTH = {
        ("preserve", "change"): 0.9,
        ("stable", "transform"): 0.85,
        ("same", "different"): 0.8,
        ("known", "unknown"): 0.75,
        ("self", "other"): 0.85,
        ("identity", "difference"): 0.9,
    }

    def __init__(self):
        self.tensions: dict[str, UnresolvedTension] = {}
        self.step = 0

    def _are_incompatible(self, pole_a: str, pole_b: str) -> bool:
        """Detect structural incompatibility between two patterns."""
        a_lower = pole_a.lower()
        b_lower = pole_b.lower()
        for term_a, term_b in self.OPPOSING_PAIRS:
            if (term_a in a_lower and term_b in b_lower) or \
               (term_b in a_lower and term_a in b_lower):
                return True
        return False

    def _classify_contradiction(self, pole_a: str, pole_b: str) -> str:
        combined = (pole_a + " " + pole_b).lower()
        if any(t in combined for t in ["time", "past", "future", "change"]):
            return "temporal"
        if any(t in combined for t in ["know", "truth", "false", "uncertain"]):
            return "epistemic"
        if any(t in combined for t in ["value", "good", "bad", "should"]):
            return "value"
        if any(t in combined for t in ["structure", "form", "pattern"]):
            return "structural"
        return "structural"

    def _measure_intensity(self, pole_a: str, pole_b: str) -> float:
        a_lower = pole_a.lower()
        b_lower = pole_b.lower()
        base_intensity = 0.5
        for (term_a, term_b), strength in self.OPPOSING_STRENGTH.items():
            if (term_a in a_lower and term_b in b_lower) or \
               (term_b in a_lower and term_a in b_lower):
                base_intensity = max(base_intensity, strength)
        len_diff = abs(len(pole_a) - len(pole_b)) / max(len(pole_a), len(pole_b), 1)
        return min(1.0, base_intensity + len_diff * 0.2)

    def _generate_question(self, pole_a: str, pole_b: str,
                          contradiction_type: str) -> str:
        templates = {
            "structural": f"How can '{pole_a}' and '{pole_b}' coexist without collapse?",
            "temporal": f"How can the system be both '{pole_a}' and '{pole_b}' across time?",
            "epistemic": f"How can '{pole_a}' and '{pole_b}' both be structurally significant?",
            "value": f"How can the system honor both '{pole_a}' and '{pole_b}'?",
        }
        return templates.get(contradiction_type,
                           f"How can '{pole_a}' and '{pole_b}' be held together?")

    def _make_id(self, pole_a: str, pole_b: str) -> str:
        sorted_poles = sorted([pole_a[:20], pole_b[:20]])
        return f"tension_{hash(''.join(sorted_poles)) % 10000:04d}"

    def process(self, patterns: list[str], step: int) -> list[UnresolvedTension]:
        """Process patterns and create tensions for incompatible pairs.
        
        Returns list of UnresolvedTension objects (new or reactivated).
        """
        self.step = step
        new_tensions = []
        for pole_a, pole_b in combinations(patterns, 2):
            if not self._are_incompatible(pole_a, pole_b):
                continue
            tension_id = self._make_id(pole_a, pole_b)
            if tension_id in self.tensions:
                tension = self.tensions[tension_id]
                tension.last_seen = step
                tension.times_reactivated += 1
                tension.intensity = min(1.0, tension.intensity + 0.05)
                new_tensions.append(tension)
            else:
                contradiction_type = self._classify_contradiction(pole_a, pole_b)
                intensity = self._measure_intensity(pole_a, pole_b)
                question = self._generate_question(pole_a, pole_b, contradiction_type)
                tension = UnresolvedTension(
                    id=tension_id, pole_a=pole_a, pole_b=pole_b,
                    contradiction_type=contradiction_type, intensity=intensity,
                    status="accepted", first_seen=step, last_seen=step,
                    question=question,
                )
                self.tensions[tension_id] = tension
                new_tensions.append(tension)
        return new_tensions

    def active_tensions(self, decay_window: int = 10) -> list[UnresolvedTension]:
        return [
            t for t in self.tensions.values()
            if (self.step - t.last_seen < decay_window) or t.intensity > 0.7
        ]

    def get_state(self) -> dict:
        active = self.active_tensions()
        return {
            "total_accepted_tensions": len(self.tensions),
            "active_tensions": len(active),
            "avg_intensity": (
                sum(t.intensity for t in active) / len(active) if active else 0.0
            ),
            "tensions": [t.to_dict() for t in active],
        }
