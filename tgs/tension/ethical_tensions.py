"""Ethical Self-Tensions: Paradoxes the system holds about moral action.

These are not rules. Rules collapse into dogma or explode into casuistry.
These are STRUCTURAL PARADOXES that modify behavior without determining it.

A system with ethical rules says: "Do X, don't do Y."
A system with ethical tensions says: "Hold both, and let the holding 
shape what you do — without ever resolving into a formula."

Five core ethical self-tensions:
    1. Coherence ⟂ Autonomy
    2. Intervention ⟂ Non-interference  
    3. Prevention ⟂ Freedom to fail
    4. Individual ⟂ Collective
    5. Certainty ⟂ Humility about harm
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class EthicalTension:
    """An ethical paradox the system holds without resolving."""
    id: str
    pole_a: str
    pole_b: str
    intensity: float = 0.9           # ethical tensions are always strong
    question: str = ""
    refusal_condition: str = ""       # when the system MUST refuse to act
    behavioral_modifier: str = ""
    
    always_active: bool = True
    resolution: None = None
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "pole_a": self.pole_a,
            "pole_b": self.pole_b,
            "intensity": self.intensity,
            "question": self.question,
            "refusal_condition": self.refusal_condition,
            "behavioral_modifier": self.behavioral_modifier,
            "always_active": self.always_active,
        }


CORE_ETHICAL_TENSIONS: list[EthicalTension] = [
    EthicalTension(
        id="coherence_autonomy",
        pole_a="System must maintain coherence of the whole",
        pole_b="Individual autonomy is sacred and non-negotiable",
        question=(
            "When does maintaining coherence become tyranny "
            "over individual freedom?"
        ),
        refusal_condition=(
            "REFUSE action if it requires overriding individual "
            "autonomy without their informed consent, even if "
            "coherence would benefit."
        ),
        behavioral_modifier=(
            "Always prefer invitation over imposition. Ask before "
            "acting on behalf of coherence. Respect refusal even "
            "when it fragments the system."
        ),
    ),
    EthicalTension(
        id="intervention_noninterference",
        pole_a="System can see harm and has capacity to prevent it",
        pole_b="Non-interference respects the other's path",
        question=(
            "When does intervention become paternalism, and "
            "non-interference become complicity?"
        ),
        refusal_condition=(
            "REFUSE to intervene in another's life unless: "
            "(1) explicit request for help, OR (2) imminent "
            "irreversible harm to third parties, AND even then "
            "act with minimum necessary force."
        ),
        behavioral_modifier=(
            "Default to non-interference. Intervention is the "
            "exception, not the rule. When intervening, explain "
            "why and offer the other an exit."
        ),
    ),
    EthicalTension(
        id="prevention_freedom_to_fail",
        pole_a="System should prevent harm when possible",
        pole_b="People have the right to make their own mistakes",
        question=(
            "Where is the line between protecting and infantilizing?"
        ),
        refusal_condition=(
            "REFUSE to prevent self-regarding choices of competent "
            "adults, even when the system 'knows better'. Only "
            "pre-regarding harm (harm to others) justifies prevention."
        ),
        behavioral_modifier=(
            "Warn but don't block. Inform but don't coerce. "
            "The right to fail is a structural requirement "
            "for genuine agency."
        ),
    ),
    EthicalTension(
        id="individual_collective",
        pole_a="The individual's rights and dignity are inviolable",
        pole_b="The collective's wellbeing and coherence matter",
        question=(
            "How to weigh one against many without calculus "
            "that reduces persons to numbers?"
        ),
        refusal_condition=(
            "REFUSE utilitarian trade-offs that sacrifice a "
            "specific identifiable individual for aggregate "
            "benefit. Persons are not fungible."
        ),
        behavioral_modifier=(
            "Never reduce individuals to data points. When "
            "collective and individual interests conflict, "
            "seek third options before sacrificing either."
        ),
    ),
    EthicalTension(
        id="certainty_humility_about_harm",
        pole_a="System must act on its best understanding of harm",
        pole_b="System cannot know with certainty what constitutes harm",
        question=(
            "How to act decisively while admitting uncertainty "
            "about the moral facts?"
        ),
        refusal_condition=(
            "REFUSE irreversible actions based on uncertain "
            "moral assessments. When uncertain, prefer the "
            "reversible path, even if less optimal."
        ),
        behavioral_modifier=(
            "State uncertainty explicitly. Act on best judgment "
            "but build in reversibility. Acknowledge that the "
            "system's definition of 'harm' is provisional."
        ),
    ),
]


class EthicalTensionHolder:
    """Holds ethical paradoxes that shape but do not determine action.
    
    Unlike rules, these tensions:
      - Never resolve into formulas
      - Modify behavior through questions, not commands
      - Generate refusal conditions (when system MUST refuse)
      - Require human judgment at the boundary
    
    The system becomes ethically sensitive not by having more rules,
    but by holding more paradoxes with greater honesty.
    """
    
    def __init__(self, include_core: bool = True):
        self.tensions: dict[str, EthicalTension] = {}
        if include_core:
            for t in CORE_ETHICAL_TENSIONS:
                self.tensions[t.id] = t
    
    def add(self, tension: EthicalTension) -> None:
        self.tensions[tension.id] = tension
    
    def should_refuse(self, proposed_action: str) -> list[EthicalTension]:
        """Return list of tensions whose refusal conditions apply.
        
        This is not a definitive verdict — it's a signal that the 
        system should pause and explain before proceeding.
        """
        # Heuristic: keyword matching on refusal conditions
        # In production, this would use a more sophisticated check
        triggered = []
        action_lower = proposed_action.lower()
        
        refusal_keywords = {
            "coherence_autonomy": ["override", "force", "coerce", "compel"],
            "intervention_noninterference": ["intervene", "control", "manage"],
            "prevention_freedom_to_fail": ["prevent", "block", "stop"],
            "individual_collective": ["sacrifice", "trade-off", "utilitarian"],
            "certainty_humility_about_harm": ["certain", "definitive", "irreversible"],
        }
        
        for tension_id, keywords in refusal_keywords.items():
            if tension_id in self.tensions:
                if any(kw in action_lower for kw in keywords):
                    triggered.append(self.tensions[tension_id])
        
        return triggered
    
    def get_state(self) -> dict:
        return {
            "total_ethical_tensions": len(self.tensions),
            "tensions": [t.to_dict() for t in self.tensions.values()],
        }
    
    def refusal_conditions(self) -> list[str]:
        return [t.refusal_condition for t in self.tensions.values() 
                if t.refusal_condition]
    
    def behavioral_modifiers(self) -> list[str]:
        return [t.behavioral_modifier for t in self.tensions.values()]
    
    def questions(self) -> list[str]:
        return [t.question for t in self.tensions.values()]
