"""tgs.resonance.difference — Difference-preserving observer."""
from __future__ import annotations
from dataclasses import dataclass, field
from .domain import Domain, Node
from .observer import Observer, Observation
from .analysis import analyze, ResonanceAnalysis, pattern_hashes

@dataclass
class Difference:
    remained: list[str] = field(default_factory=list)
    transformed: list[dict] = field(default_factory=list)
    lost: list[str] = field(default_factory=list)
    emerged: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "remained": self.remained, "transformed": self.transformed,
            "lost": self.lost, "emerged": self.emerged,
            "summary": {"invariant": len(self.remained), "lost": len(self.lost), "emerged": len(self.emerged)},
        }

@dataclass
class MetaState:
    iteration: int
    state_before: Domain
    observer: Observer
    state_after: Domain
    difference: Difference
    analysis: ResonanceAnalysis

class DifferencePreservingObserver:
    def __init__(self, initial_observer: Observer):
        self.current_observer = initial_observer
        self.history: list[MetaState] = []

    def _compute_difference(self, g_before: Domain, g_after: Domain) -> Difference:
        pb, pa = pattern_hashes(g_before, size=2), pattern_hashes(g_after, size=2)
        return Difference(remained=list(pb & pa), lost=list(pb - pa), emerged=list(pa - pb))

    def _next_observer(self, diff: Difference, iteration: int) -> Observer:
        if diff.emerged:
            p, a, b = "attends to emergent patterns", ["prioritize newly emerged structures"], ["emergence_bias"]
        elif diff.lost:
            p, a, b = "attends to dissipated patterns", ["investigate lost patterns"], ["conservation_bias"]
        elif diff.remained:
            p, a, b = "attends to persistent invariants", ["prioritize stable structures"], ["stability_bias"]
        else:
            p, a, b = "exploratory observer", ["no strong prior"], ["exploration_bias"]

        return Observer(id=f"observer_iter_{iteration}", name=f"Observer (iter {iteration})",
                        perspective=p, assumptions=a, biases=b, extractor=self.current_observer.extractor)

    def observe_once(self, domain: Domain) -> MetaState:
        i = len(self.history)
        observation = Observation(id=f"obs_{i}", field_id=domain.id, field_content=domain.source_text or "",
                                  observer=self.current_observer, domain=domain, operator=f"diff_preserving_{i}")
        pats = pattern_hashes(domain, size=2)
        g_after = Domain(id=f"{domain.id}_i{i}", name=f"Patterns iter {i}",
                         nodes=[Node(id=f"p_{h[:8]}", label=f"Pat_{h[:8]}", role="pattern") for h in pats],
                         edges=[], observer_id=self.current_observer.id)
        
        diff = Difference(emerged=list(pats)) if i == 0 else self._compute_difference(self.history[-1].state_after, g_after)
        analysis_result = analyze([observation], pattern_size=2)
        
        meta = MetaState(iteration=i, state_before=domain, observer=self.current_observer,
                         state_after=g_after, difference=diff, analysis=analysis_result)
        self.history.append(meta)
        self.current_observer = self._next_observer(diff, i + 1)
        return meta

    def observe_recursively(self, domain: Domain, max_iter: int = 8) -> list[MetaState]:
        current = domain
        for _ in range(max_iter):
            meta = self.observe_once(current)
            if len(meta.state_after.nodes) < 2: break
            current = meta.state_after
        return self.history
