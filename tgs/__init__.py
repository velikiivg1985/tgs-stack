"""TGS-Stack: Geometric Self-Unfolding as a Computational Framework for Reflexive Systems

Two complementary modules:

    tgs.resonance — Cross-domain structural invariant discovery
                    (what persists across different observers)

    tgs.tension   — Persistent recursive self-modeling with acceptance
                    (what persists through time via unresolved contradictions)

Together they form the architectural conditions for functional self-reference.
"""

from .resonance import (
    Domain, Node, Edge, Evidence,
    Observer, Observation,
    ResonanceKernel, ResonanceAnalysis,
    MutualObservationProtocol,
    analyze as resonance_analyze,
)
from .tension import (
    SelfModel, SelfState,
    InvariantTracker, InvariantRecord,
    DifferenceTracker, DifferenceRecord,
    UncertaintyTracker, BlindSpot,
    TensionCore, Tension,
    AcceptanceLayer, UnresolvedTension,
)

__version__ = "1.0.0"

__all__ = [
    # Resonance
    "Domain", "Node", "Edge", "Evidence",
    "Observer", "Observation",
    "ResonanceKernel", "ResonanceAnalysis",
    "MutualObservationProtocol",
    "resonance_analyze",
    # Tension
    "SelfModel", "SelfState",
    "InvariantTracker", "InvariantRecord",
    "DifferenceTracker", "DifferenceRecord",
    "UncertaintyTracker", "BlindSpot",
    "TensionCore", "Tension",
    "AcceptanceLayer", "UnresolvedTension",
]
