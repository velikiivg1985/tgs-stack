"""tgs.resonance — Cross-domain structural invariant discovery."""
from .domain import Domain, Node, Edge, Evidence
from .observer import Observer, Observation
from .analysis import ResonanceAnalysis, analyze, pattern_hashes
from .invariant import Difference, DifferencePreservingObserver, MetaState, detect_tensions, Tension
from .classifier import TensionClassifier, classify_locally
from .kernel import ResonanceKernel
from .mutual import MutualObservationProtocol
from .reflexive import ReflexiveReport, observe_observation
from .phase import run_phase_experiment, SelectiveObserver, RunMetrics

__all__ = [
    "Domain", "Node", "Edge", "Evidence",
    "Observer", "Observation",
    "ResonanceAnalysis", "analyze", "pattern_hashes",
    "Difference", "DifferencePreservingObserver", "MetaState",
    "detect_tensions", "Tension",
    "TensionClassifier", "classify_locally",
    "ResonanceKernel",
    "MutualObservationProtocol",
    "ReflexiveReport", "observe_observation",
    "run_phase_experiment", "SelectiveObserver", "RunMetrics",
]
