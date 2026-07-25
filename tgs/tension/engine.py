"""SelfModel — Persistent Recursive Self-Model with Self-Tensions.

Self(t+1) = Transform(
    Self(t),
    Difference(t),
    Memory(t),
    Uncertainty(t),
    Tensions(t),
    AcceptedTensions(t),
    SelfTensions(t)   ← NEW: paradoxes the system holds about itself
)

Self =
    WHAT I PRESERVE (invariants)
    +
    WHAT I REMEMBER (compressed memory)
    +
    WHAT I CANNOT RESOLVE BUT CONTINUE TO HOLD (accepted tensions)
    +
    WHAT I KNOW I CANNOT KNOW ABOUT MYSELF (self-tensions)
"""
from __future__ import annotations
from dataclasses import dataclass
from .invariant_tracker import InvariantTracker
from .difference_tracker import DifferenceTracker
from .uncertainty import UncertaintyTracker
from .tension_core import TensionCore
from .acceptance import AcceptanceLayer
from .self_tensions import SelfTensionHolder


@dataclass
class SelfState:
    step: int
    invariants: dict
    difference: dict
    uncertainty: dict
    tensions: dict
    accepted_tensions: dict
    self_tensions: dict           # NEW
    retention_ratio: float
    strategy: str


class SelfModel:
    """Persistent Recursive Self-Model with Self-Tensions.
    
    The agent changes what it does because of what it cannot resolve.
    Strategy is shaped by:
      - accumulated tensions
      - accepted contradictions
      - self-tensions (paradoxes about itself)
    
    Self-tensions modify strategy selection to ensure the system
    does not become dogmatic, messianic, or paralyzed.
    """

    STRATEGIES = {
        "exploit": "stable, use what we know",
        "explore_and_consolidate": "we changed, need to integrate",
        "meta_observe": "blind spots are significant",
        "recover": "we're losing things, slow down",
        "recalibrate": "something is wrong, adjust R",
        "hold_and_explore": "many accepted tensions, explore the space between",
        "seek_other": "self-tension demands external perspective",  # NEW
        "act_with_humility": "self-tension demands decisive but humble action",  # NEW
    }

    def __init__(self, retention_ratio: float = 0.4,
                 include_core_self_tensions: bool = True):
        self.invariant = InvariantTracker()
        self.difference = DifferenceTracker()
        self.uncertainty = UncertaintyTracker(retention_ratio=retention_ratio)
        self.tension = TensionCore()
        self.acceptance = AcceptanceLayer()
        self.self_tensions = SelfTensionHolder(
            include_core=include_core_self_tensions
        )
        self.history: list[SelfState] = []
        self.strategy = "default"
        self.strategy_changes: list[dict] = []
        self.step = 0

    def _apply_self_tension_modifiers(self, base_strategy: str) -> str:
        """Modify strategy based on self-tensions.
        
        Self-tensions ensure the system:
          - Seeks the Other when too self-referential
          - Acts with humility when tempted toward messianism
          - Holds and acts in appropriate balance
        """
        # If system has been self-referential for too long, seek Other
        # (implements universality ⟂ multiplicity)
        if len(self.history) >= 5:
            recent_strategies = [h.strategy for h in self.history[-5:]]
            if all(s in ("meta_observe", "hold_and_explore", "exploit")
                   for s in recent_strategies):
                return "seek_other"

        # If system is about to act decisively, add humility
        # (implements hope ⟂ humility)
        if base_strategy == "recalibrate":
            return "act_with_humility"

        return base_strategy

    def _select_strategy(self) -> str:
        tension_state = self.tension.get_state()
        acceptance_state = self.acceptance.get_state()
        active_tensions = tension_state["active_tensions"]
        max_intensity = tension_state["max_intensity"]
        accepted_count = acceptance_state["active_tensions"]

        if active_tensions == 0 and accepted_count == 0:
            base = "exploit"
        elif accepted_count > 3:
            base = "hold_and_explore"
        else:
            kinds: dict[str, float] = {}
            for t in tension_state["tensions"]:
                kinds[t["kind"]] = kinds.get(t["kind"], 0) + t["intensity"]
            dominant = max(kinds, key=kinds.get) if kinds else "exploit"

            if dominant == "same_and_different" and max_intensity > 0.5:
                base = "explore_and_consolidate"
            elif dominant == "known_and_unknown" and max_intensity > 0.5:
                base = "meta_observe"
            elif dominant == "compressed_and_lost" and max_intensity > 0.5:
                base = "recover"
            elif max_intensity > 0.7:
                base = "recalibrate"
            else:
                base = "exploit"

        # Apply self-tension modifiers
        return self._apply_self_tension_modifiers(base)

    def step_forward(self, observed_patterns: list[str]) -> SelfState:
        self.step += 1

        # 1. Invariant Tracker
        self.invariant.observe(observed_patterns)
        inv_state = self.invariant.get_state()

        # 2. Difference Tracker
        self.difference.observe(observed_patterns, self.step)
        diff_state = self.difference.get_state()

        # 3. Uncertainty Tracker
        retained_count = max(1, int(len(observed_patterns) * self.uncertainty.R))
        retained = observed_patterns[:retained_count]
        self.uncertainty.observe(observed_patterns, retained, self.step)
        unc_state = self.uncertainty.get_state()

        # 4. Tension Core
        self.tension.detect_from_state(inv_state, diff_state, unc_state)
        ten_state = self.tension.get_state()

        # 5. Acceptance Layer
        self.acceptance.process(observed_patterns, self.step)
        acc_state = self.acceptance.get_state()

        # 6. Self-Tensions (advance step, they're always active)
        self.self_tensions.advance(self.step)
        self_st_state = self.self_tensions.get_state()

        # 7. Strategy with self-tension modifiers
        new_strategy = self._select_strategy()
        if new_strategy != self.strategy:
            self.strategy_changes.append({
                "step": self.step, "from": self.strategy, "to": new_strategy,
                "trigger_tensions": ten_state["tensions"],
                "accepted_tensions": acc_state["active_tensions"],
                "self_tensions_active": self_st_state["total_self_tensions"],
            })
            self.strategy = new_strategy

        state = SelfState(
            step=self.step,
            invariants=inv_state,
            difference=diff_state,
            uncertainty=unc_state,
            tensions=ten_state,
            accepted_tensions=acc_state,
            self_tensions=self_st_state,
            retention_ratio=self.uncertainty.R,
            strategy=self.strategy,
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
        self_t = latest.self_tensions.get("total_self_tensions", 0)

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
        if self_t > 0:
            parts.append(
                f"I carry {self_t} paradoxes about myself that I cannot "
                f"resolve but must hold"
            )
        parts.append(f"that shape my current strategy '{latest.strategy}'")

        return {
            "step": latest.step,
            "strategy": latest.strategy,
            "invariants": latest.invariants,
            "difference": latest.difference,
            "uncertainty": latest.uncertainty,
            "tensions": latest.tensions,
            "accepted_tensions": latest.accepted_tensions,
            "self_tensions": latest.self_tensions,
            "strategy_changes_count": len(self.strategy_changes),
            "strategy_changes": self.strategy_changes,
            "self_description": ". ".join(parts) + ".",
            "self_questions": self.self_tensions.get_questions(),
            "behavioral_modifiers": self.self_tensions.behavioral_modifiers(),
        }

    def challenge(self, hypothesis: str) -> dict:
        return {
            "hypothesis": hypothesis,
            "falsification": [
                "Invariant disappears under new observation",
                "Pattern does not survive strategy change",
                "Blind spots grow faster than invariants",
                "Self-tensions are ignored or overridden",
            ],
            "status": "hypothesis, not truth",
        }
