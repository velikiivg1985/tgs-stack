"""tgs.tension — Persistent recursive self-modeling with self-tensions.

Four distinct operations:
    FORGETTING     → deletion (information lost)
    COMPRESSION    → simplification (complexity reduced)
    ACCEPTANCE     → transformation (contradiction becomes stable relation)
    SELF-TENSION   → architectural paradox (system holds about itself)

Self =
    WHAT I PRESERVE
    +
    WHAT I REMEMBER
    +
    WHAT I CANNOT RESOLVE BUT CONTINUE TO HOLD
    +
    WHAT I KNOW I CANNOT KNOW ABOUT MYSELF
"""

from .engine import SelfModel, SelfState
from .invariant_tracker import InvariantTracker, InvariantRecord
from .difference_tracker import DifferenceTracker, DifferenceRecord
from .uncertainty import UncertaintyTracker, BlindSpot
from .tension_core import TensionCore, Tension
from .acceptance import AcceptanceLayer, UnresolvedTension
from .self_tensions import (
    SelfTensionHolder, SelfTension, CORE_SELF_TENSIONS,
)

__all__ = [
    "SelfModel", "SelfState",
    "InvariantTracker", "InvariantRecord",
    "DifferenceTracker", "DifferenceRecord",
    "UncertaintyTracker", "BlindSpot",
    "TensionCore", "Tension",
    "AcceptanceLayer", "UnresolvedTension",
    "SelfTensionHolder", "SelfTension", "CORE_SELF_TENSIONS",
]
