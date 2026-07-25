"""SelfModel — Persistent Recursive Self-Model with Acceptance Layer

Self(t+1) = Transform(Self(t), Difference(t), Memory(t),
                        Uncertainty(t), Tensions(t), AcceptedTensions(t))

New formula for Self:

    SELF =
    WHAT I PRESERVE (invariants)
    +
    WHAT I REMEMBER (compressed memory)
    +
    WHAT I CANNOT RESOLVE BUT CONTINUE TO HOLD (accepted tensions)

Three operational modes:
    COLLAPSE:   A → B (one eliminated)
    EXPLOSION:  A + B + C + ... → ∞ (all retained)
    ACCEPTANCE: A ⟂ B → TENSION(A,B) → STABLE RELATION
"""
from __future__ import annotations
from dataclasses import dataclass
from .invariant_tracker import InvariantTracker
from .difference_tracker import DifferenceTracker
from .uncertainty import UncertaintyTracker
from .tension_core import TensionCore
from .acceptance import AcceptanceLayer


@dataclass
class SelfState:
    step: int
    invariants: dict
    difference: dict
    uncertainty: dict
    tensions: dict
    accepted_tensions: dict
    retention_ratio: float
    strategy: str


class SelfModel:
    """Persistent Recursive Self-Model with Acceptance Layer.
    
    The agent changes what it does because of what it cannot resolve.
    Strategy is a function of accumulated tensions AND accepted contradictions.
    """

    STRATEGIES = {
        "exploit": "stable, use what we know",
        "explore_and_consolidate": "we changed, need to integrate",
        "meta_observe": "blind spots are significant",
        "recover": "we're losing things, slow down",
        "recalibrate": "something is wrong, adjust R",
        "hold_and_explore": "many accepted tensions, explore the space between",
    }

    def __init__(self, retention_ratio: float = 0.4):
        self.invariant = InvariantTracker()
        self.difference = DifferenceTracker()
        self.uncertainty = UncertaintyTracker(retention_ratio=retention_ratio)
        self.tension = TensionCore()
        self.acceptance = AcceptanceLayer()
        self.history: list[SelfState] = []
        self.strategy = "default"
        self.strategy_changes: list[dict] = []
        self.step = 0

    def _select_strategy(self) -> str:
        tension_state = self.tension.get_state()
        acceptance_state = self.acceptance.get_state()
        active_tensions = tension_state["active_tensions"]
        max_intensity = tension_state["max_intensity"]
        accepted_count = acceptance_state["active_tensions"]

        if active_tensions == 0 and accepted_count == 0:
            return "exploit"
        if accepted_count > 3:
            return "hold_and_explore"

        kinds: dict[str, float] = {}
        for t in tension_state["tensions"]:
            kinds[t["kind"]] = kinds.get(t["kind"], 0) + t["intensity"]
        dominant = max(kinds, key=kinds.get) if kinds else "exploit"

        if dominant == "same_and_different" and max_intensity > 0.5:
            return "explore_and_consolidate"
        elif dominant == "known_and_unknown" and max_intensity > 0.5:
            return "meta_observe"
        elif dominant == "compressed_and_lost" and max_intensity > 0.5:
            return "recover"
        elif max_intensity > 0.7:
            return "recalibrate"
        else:
            return "exploit"

    def step_forward(self, observed_patterns: list[str]) -> SelfState:
        self.step += 1
        self.invariant.observe(observed_patterns)
        inv_state = self.invariant.get_state()
        self.difference.observe(observed_patterns, self.step)
        diff_state = self.difference.get_state()
        retained_count = max(1, int(len(observed_patterns) * self.uncertainty.R))
        retained = observed_patterns[:retained_count]
        self.uncertainty.observe(observed_patterns, retained, self.step)
        unc_state = self.uncertainty.get_state()
        self.tension.detect_from_state(inv_state, diff_state, unc_state)
        ten_state = self.tension.get_state()
        self.acceptance.process(observed_patterns, self.step)
        acc_state = self.acceptance.get_state()

        new_strategy = self._select_strategy()
        if new_strategy != self.strategy:
            self.strategy_changes.append({
                "step": self.step, "from": self.strategy, "to": new_strategy,
                "trigger_tensions": ten_state["tensions"],
                "accepted_tensions": acc_state["active_tensions"],
            })
            self.strategy = new_strategy

        state = SelfState(
            step=self.step, invariants=inv_state, difference=diff_state,
            uncertainty=unc_state, tensions=ten_state,
            accepted_tensions=acc_state,
            retention_ratio=self.uncertainty.R, strategy=self.strategy,
        )
        self.history.append(state)
        return state

    def get_self_model(self) -> dict:
        if not self.history:
            return {"status": "no history"}
        latest = self.history[-1]
        stable = latest.invariants.get("stable_invariants", 0)
        magnitude = latest.difference.get("avg_magnitude", 0)
        uncertainty = latest.uncertainty.get("uncertainty", 0)
        active_t = latest.tensions.get("active_tensions", 0)
        accepted = latest.accepted_tensions.get("active_tensions", 0)

        parts = [
            f"I maintain {stable} stable invariants",
            f"while changing at rate {magnitude:.2f}",
            f"My blind spots cover {uncertainty:.0%} of my observation space",
            f"I hold {active_t} active tensions",
        ]
        if accepted > 0:
            parts.append(
                f"I accept {accepted} unresolved contradictions "
                f"as persistent relational structures"
            )
        parts.append(f"that shape my current strategy '{latest.strategy}'")

        return {
            "step": latest.step, "strategy": latest.strategy,
            "invariants": latest.invariants, "difference": latest.difference,
            "uncertainty": latest.uncertainty, "tensions": latest.tensions,
            "accepted_tensions": latest.accepted_tensions,
            "strategy_changes_count": len(self.strategy_changes),
            "strategy_changes": self.strategy_changes,
            "self_description": ". ".join(parts) + ".",
        }

    def challenge(self, hypothesis: str) -> dict:
        return {
            "hypothesis": hypothesis,
            "falsification": [
                "Invariant disappears under new observation",
                "Pattern does not survive strategy change",
                "Blind spots grow faster than invariants",
            ],
            "status": "hypothesis, not truth",
        }
