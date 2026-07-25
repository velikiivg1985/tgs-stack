"""tgs.tension — Persistent recursive self-modeling with self-tensions.
from .engine import SelfModel, SelfState
from .invariant_tracker import InvariantTracker
from .difference_tracker import DifferenceTracker
from .uncertainty import UncertaintyTracker
from .tension_core import TensionCore
from .acceptance import AcceptanceLayer
from .self_tensions import SelfTensionHolder, SelfTension, CORE_SELF_TENSIONS
from .ethical_tensions import EthicalTensionHolder, EthicalTension, CORE_ETHICAL_TENSIONS

__all__ = [
    "SelfModel", "SelfState",
    "InvariantTracker",
    "DifferenceTracker",
    "UncertaintyTracker",
    "TensionCore",
    "AcceptanceLayer",
    "SelfTensionHolder", "SelfTension", "CORE_SELF_TENSIONS",
    "EthicalTensionHolder", "EthicalTension", "CORE_ETHICAL_TENSIONS",
]
