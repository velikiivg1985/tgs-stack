"""Tension detection across observations"""
from __future__ import annotations
from dataclasses import dataclass
from .analysis import ResonanceAnalysis

TENSION_TYPES = {
    "open_question": "Resolvable through refinement or new data",
    "reflexive_limitation": "Built into the observer's position",
    "real_contradiction": "Hard mutual exclusion under given constraints",
    "no_common_ground": "Independent phenomena mistakenly collapsed",
}


@dataclass
class Tension:
    kind: str
    between: tuple[str, ...]
    description: str
    evidence: list[str]

    def to_dict(self) -> dict:
        return {
            "kind": self.kind, "between": list(self.between),
            "description": self.description, "evidence": self.evidence,
        }


def detect_tensions(analysis: ResonanceAnalysis, observations) -> list[Tension]:
    tensions: list[Tension] = []

    for (a, b), match in analysis.pairwise_matches.items():
        if match < 0.2:
            obs_a = next(o for o in observations if o.id == a)
            obs_b = next(o for o in observations if o.id == b)
            la = {n.label.lower() for n in obs_a.domain.nodes}
            lb = {n.label.lower() for n in obs_b.domain.nodes}
            vocab = len(la & lb) / max(1, len(la | lb))

            if vocab < 0.1:
                kind = "no_common_ground"
                desc = (f"Observers {a!r} and {b!r} use nearly disjoint "
                        f"vocabularies (overlap {vocab:.1%})")
            elif match == 0:
                kind = "real_contradiction"
                desc = (f"Observers {a!r} and {b!r} share zero structural "
                        f"patterns despite observing the same field")
            else:
                kind = "open_question"
                desc = (f"Observers {a!r} and {b!r} have low structural "
                        f"agreement ({match:.1%}); cause unclear")

            tensions.append(Tension(
                kind, (a, b), desc,
                [f"pairwise_match={match:.2f}", f"vocab_overlap={vocab:.2f}"],
            ))

    for obs_id, unique in analysis.unique_patterns.items():
        obs_invariants = [i for i in analysis.invariants
                          if obs_id in i["observers"]]
        if len(unique) > 3 and not obs_invariants:
            tensions.append(Tension(
                "reflexive_limitation", (obs_id, "system"),
                f"Observer {obs_id!r} produces {len(unique)} unique "
                f"patterns that no other observer sees.",
                [f"unique_count={len(unique)}"],
            ))

    analysis.tensions = [t.to_dict() for t in tensions]
    return tensions
from .analysis import ResonanceAnalysis
from dataclasses import dataclass

TENSION_TYPES = {
    "open_question": "Resolvable through refinement or new data",
    "reflexive_limitation": "Built into the observer's position",
    "real_contradiction": "Hard mutual exclusion under given constraints",
    "no_common_ground": "Independent phenomena mistakenly collapsed",
}

@dataclass
class Tension:
    kind: str
    between: tuple[str, ...]
    description: str
    evidence: list[str]

    def to_dict(self) -> dict:
        return {
            "kind": self.kind, "between": list(self.between),
            "description": self.description, "evidence": self.evidence,
        }

def detect_tensions(analysis: ResonanceAnalysis, observations) -> list[Tension]:
    tensions: list[Tension] = []

    for (a, b), match in analysis.pairwise_matches.items():
        if match < 0.2:
            obs_a = next(o for o in observations if o.id == a)
            obs_b = next(o for o in observations if o.id == b)
            la = {n.label.lower() for n in obs_a.domain.nodes}
            lb = {n.label.lower() for n in obs_b.domain.nodes}
            vocab = len(la & lb) / max(1, len(la | lb))

            if vocab < 0.1:
                kind = "no_common_ground"
                desc = (f"Observers {a!r} and {b!r} use nearly disjoint "
                        f"vocabularies (overlap {vocab:.1%})")
            elif match == 0:
                kind = "real_contradiction"
                desc = (f"Observers {a!r} and {b!r} share zero structural "
                        f"patterns despite observing the same field")
            else:
                kind = "open_question"
                desc = (f"Observers {a!r} and {b!r} have low structural "
                        f"agreement ({match:.1%}); cause unclear")

            tensions.append(Tension(
                kind, (a, b), desc,
                [f"pairwise_match={match:.2f}", f"vocab_overlap={vocab:.2f}"],
            ))

    for obs_id, unique in analysis.unique_patterns.items():
        obs_invariants = [i for i in analysis.invariants
                          if obs_id in i["observers"]]
        if len(unique) > 3 and not obs_invariants:
            tensions.append(Tension(
                "reflexive_limitation", (obs_id, "system"),
                f"Observer {obs_id!r} produces {len(unique)} unique "
                f"patterns that no other observer sees.",
                [f"unique_count={len(unique)}"],
            ))

    analysis.tensions = [t.to_dict() for t in tensions]
    return tensions
