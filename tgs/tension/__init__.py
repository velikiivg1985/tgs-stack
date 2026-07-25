"""tgs.tension — Persistent recursive self-modeling with acceptance

Three distinct operations:
    FORGETTING  → deletion (information lost)
    COMPRESSION → simplification (complexity reduced)
    ACCEPTANCE  → transformation (contradiction becomes stable relation)

Self(t+1) = Transform(Self(t), Difference(t), Memory(t),
                        Uncertainty(t), Tensions(t), AcceptedTensions(t))

Core principle: Acceptance is not closure. It is the structural capacity
to hold incompatibility without forced elimination.
"""

from .engine import SelfModel, SelfState
from .invariant_tracker import InvariantTracker, InvariantRecord
from .difference_tracker import DifferenceTracker, DifferenceRecord
from .uncertainty import UncertaintyTracker, BlindSpot
from .tension_core import TensionCore, Tension
from .acceptance import AcceptanceLayer, UnresolvedTension

__all__ = [
    "SelfModel", "SelfState",
    "InvariantTracker", "InvariantRecord",
    "DifferenceTracker", "DifferenceRecord",
    "UncertaintyTracker", "BlindSpot",
    "TensionCore", "Tension",
    "AcceptanceLayer", "UnresolvedTension",
]
