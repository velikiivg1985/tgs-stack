"""TGS-Stack: Geometric Self-Unfolding as a Computational Framework."""
from .resonance import (
    Domain, Node, Edge, Evidence,
    Observer, Observation,
    ResonanceAnalysis, analyze, pattern_hashes,
    Difference, DifferencePreservingObserver, MetaState,
    TensionClassifier, classify_locally,
)

# Import tension module components here when ready
# from .tension import SelfModel, TensionCore, AcceptanceLayer 

__version__ = "1.1.0"
__all__ = [
    # Resonance
    "Domain", "Node", "Edge", "Evidence",
    "Observer", "Observation",
    "ResonanceAnalysis", "analyze", "pattern_hashes",
    "Difference", "DifferencePreservingObserver", "MetaState",
    "TensionClassifier", "classify_locally",
]
