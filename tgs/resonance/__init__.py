"""tgs.resonance — Cross-domain structural invariant discovery."""
from .domain import Domain, Node, Edge, Evidence
from .observer import Observer, Observation
from .analysis import ResonanceAnalysis, analyze, pattern_hashes
from .difference import Difference, DifferencePreservingObserver, MetaState
from .classifier import (
    TensionClassifier, TGS_CLASSIFY_PROMPT,
    parse_classification, classify_locally, format_classification,
)

# Note: If you have other modules like kernel.py, mutual.py, phase.py, 
# reflexive.py, invariant.py — import them here when they are ready.

__all__ = [
    "Domain", "Node", "Edge", "Evidence",
    "Observer", "Observation",
    "ResonanceAnalysis", "analyze", "pattern_hashes",
    "Difference", "DifferencePreservingObserver", "MetaState",
    "TensionClassifier", "TGS_CLASSIFY_PROMPT",
    "parse_classification", "classify_locally", "format_classification",
]
