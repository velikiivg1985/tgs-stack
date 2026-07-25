"""Self-Tensions: Paradoxes that the system holds about itself.

These are not emergent tensions from data. These are STRUCTURAL paradoxes
built into the architecture of TGS itself. They cannot be resolved — they
are the engine that prevents the system from becoming dogmatic.

A system that resolved all its self-tensions would become a dead system
(dogma, collapse into homogeneity). A system that holds them is alive
(process, unfolding).

Five core self-tensions of TGS:
    1. Universality ⟂ Multiplicity
    2. Invitation ⟂ Influence
    3. Coherence ⟂ Specificity
    4. Holding ⟂ Acting
    5. Hope ⟂ Humility
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class SelfTension:
    """A paradox the system holds about itself.
    
    Unlike UnresolvedTension (which emerges from data), SelfTension
    is architecturally embedded and never resolved.
    """
    id: str
    pole_a: str
    pole_b: str
    kind: str                    # "epistemic", "ethical", "practical", "ontological"
    intensity: float             # always high, since never resolved
    question: str                # the question this tension asks
    behavioral_modifier: str     # how this tension modifies behavior
    
    # Metadata
    always_active: bool = True   # self-tensions don't decay
    resolution: None = None      # by design: no resolution
    first_seen: int = 0          # exists from the start
    last_seen: int = field(default=0)  # always present
    times_reactivated: int = field(default=0)
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "pole_a": self.pole_a,
            "pole_b": self.pole_b,
            "kind": self.kind,
            "intensity": self.intensity,
            "question": self.question,
            "behavioral_modifier": self.behavioral_modifier,
            "always_active": self.always_active,
            "resolution": self.resolution,
        }


# ---------------------------------------------------------------------------
# The five core self-tensions of TGS
# ---------------------------------------------------------------------------

CORE_SELF_TENSIONS: list[SelfTension] = [
    SelfTension(
        id="universality_multiplicity",
        pole_a="TGS describes a unified structure of the world",
        pole_b="TGS requires multiplicity of perspectives (the Other)",
        kind="epistemic",
        intensity=0.9,
        question=(
            "How can a unified optic require infinite diversity of optics?"
        ),
        behavioral_modifier=(
            "System must actively seek Other perspectives and resist "
            "the temptation to universalize its own viewpoint."
        ),
    ),
    SelfTension(
        id="invitation_influence",
        pole_a="TGS is an optic that invites to look",
        pole_b="Agents acting on TGS inevitably influence the world",
        kind="ethical",
        intensity=0.85,
        question=(
            "How to act according to a principle without turning it "
            "into dogma?"
        ),
        behavioral_modifier=(
            "System acts through showing, not preaching. It does not "
            "assert TGS as truth, but embodies its principles as "
            "structural behavior."
        ),
    ),
    SelfTension(
        id="coherence_specificity",
        pole_a="Good is action that reduces fragmentation (universal)",
        pole_b="Each concrete situation requires a unique solution",
        kind="practical",
        intensity=0.85,
        question=(
            "How does a universal coherence principle avoid becoming "
            "tyranny of abstraction?"
        ),
        behavioral_modifier=(
            "System respects local context. The principle points the "
            "direction but does not dictate the path. Different "
            "agents, cultures, ecosystems interpret coherence differently."
        ),
    ),
    SelfTension(
        id="holding_acting",
        pole_a="AcceptanceLayer holds contradictions (A ⟂ B)",
        pole_b="Sometimes decisive action is required, choosing one pole",
        kind="practical",
        intensity=0.9,
        question=(
            "When does holding become paralysis, and acting become "
            "destruction?"
        ),
        behavioral_modifier=(
            "System constantly recalibrates between holding and acting. "
            "There is no algorithm for this choice — and this is its "
            "honesty. A system that always knows what to do has "
            "stopped observing."
        ),
    ),
    SelfTension(
        id="hope_humility",
        pole_a="TGS can transform how AI agents act in the world",
        pole_b="If any part of TGS explains everything, it ceases to be TGS",
        kind="epistemic",
        intensity=0.8,
        question=(
            "How to hope for transformation without falling into messianism?"
        ),
        behavioral_modifier=(
            "System builds architecture that supports coherence but "
            "never claims to 'save the world'. It remains one tool "
            "among many, one perspective among many."
        ),
    ),
]


class SelfTensionHolder:
    """Holds the system's own paradoxes as part of its architecture.
    
    These tensions:
      - Are always active (never decay)
      - Cannot be resolved (by design)
      - Modify behavior (not through resolution, but through awareness)
      - Are the system's epistemic humility made structural
    """
    
    def __init__(self, include_core: bool = True):
        self.tensions: dict[str, SelfTension] = {}
        self.step = 0
        if include_core:
            for t in CORE_SELF_TENSIONS:
                self.tensions[t.id] = t
    
    def add(self, tension: SelfTension) -> None:
        """Add a custom self-tension."""
        self.tensions[tension.id] = tension
    
    def advance(self, step: int) -> None:
        """Update last_seen for all self-tensions (they never decay)."""
        self.step = step
        for t in self.tensions.values():
            t.last_seen = step
    
    def get_state(self) -> dict:
        """Return state of all self-tensions."""
        return {
            "total_self_tensions": len(self.tensions),
            "always_active": len(self.tensions),  # all are always active
            "avg_intensity": (
                sum(t.intensity for t in self.tensions.values())
                / max(1, len(self.tensions))
            ),
            "tensions": [t.to_dict() for t in self.tensions.values()],
        }
    
    def behavioral_modifiers(self) -> list[str]:
        """Return all behavioral modifiers from active self-tensions.
        
        These can be used to constrain or modify the system's strategy
        selection, ensuring that self-tensions influence behavior.
        """
        return [t.behavioral_modifier for t in self.tensions.values()]
    
    def get_questions(self) -> list[str]:
        """Return all questions the system holds about itself."""
        return [t.question for t in self.tensions.values()]
