"""TGS-Stack: Geometric Self-Unfolding as a Computational Framework.

Two complementary modules:

    tgs.resonance — Cross-domain structural invariant discovery
    tgs.tension   — Persistent recursive self-modeling with self-tensions
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
    SelfTensionHolder, SelfTension, CORE_SELF_TENSIONS,
)

__version__ = "1.1.0"

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
    "SelfTensionHolder", "SelfTension", "CORE_SELF_TENSIONS",
]
