"""tgs.resonance — Cross-domain structural invariant discovery

Discovers what persists across different observers of the same field.
Invariants emerge in the RELATION between acts of observation.
"""

from .domain import Domain, Node, Edge, Evidence
from .observer import Observer, Observation
from .analysis import ResonanceAnalysis, analyze, pattern_hashes
from .invariant import detect_tensions, Tension
from .reflexive import observe_observation, ReflexiveReport
from .difference import (
    Difference, DifferencePreservingObserver, MetaState,
)
from .phase import SelectiveObserver, RunMetrics, run_phase_experiment
from .mutual import MutualObservationProtocol
from .kernel import ResonanceKernel
from .classifier import (
    TensionClassifier, TGS_CLASSIFY_PROMPT,
    parse_classification, classify_locally, format_classification,
)

__all__ = [
    "Domain", "Node", "Edge", "Evidence",
    "Observer", "Observation",
    "ResonanceAnalysis", "analyze", "pattern_hashes",
    "detect_tensions", "Tension",
    "observe_observation", "ReflexiveReport",
    "Difference", "DifferencePreservingObserver", "MetaState",
    "SelectiveObserver", "RunMetrics", "run_phase_experiment",
    "MutualObservationProtocol",
    "ResonanceKernel",
    "TensionClassifier", "TGS_CLASSIFY_PROMPT",
    "parse_classification", "classify_locally", "format_classification",
]
