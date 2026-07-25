"""Difference-preserving observer with three-layer architecture.

Tracks how an observation changes the observation itself — what
remained, what emerged, what was lost. The next observer is generated
from the difference, not from a static protocol.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from .domain import Domain, Node
from .observer import Observer, Observation
from .analysis import analyze, ResonanceAnalysis, pattern_hashes


@dataclass
class Difference:
    """What changed between two observation states."""
    remained: list[str] = field(default_factory=list)
    transformed: list[dict] = field(default_factory=list)
    lost: list[str] = field(default_factory=list)
    emerged: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "remained": self.remained,
            "transformed": self.transformed,
            "lost": self.lost,
            "emerged": self.emerged,
            "summary": {
                "invariant": len(self.remained),
                "lost": len(self.lost),
                "emerged": len(self.emerged),
            },
        }


@dataclass
class MetaState:
    """The full record of one observation cycle."""
    iteration: int
    state_before: Domain
    observer: Observer
    state_after: Domain
    difference: Difference
    analysis: ResonanceAnalysis


class DifferencePreservingObserver:
    """Observer that tracks its own transformation effect.

    Unlike a collapsing observer, this one:
      1. Observes G_n → produces G_{n+1}
      2. Computes Difference(G_n, G_{n+1})
      3. Generates Observer_{n+1} from the difference
      4. Preserves history of all transformations
    """

    def __init__(self, initial_observer: Observer):
        self.current_observer = initial_observer
        self.history: list[MetaState] = []

    def _compute_difference(self, g_before: Domain,
                            g_after: Domain) -> Difference:
        pb = pattern_hashes(g_before, size=2)
        pa = pattern_hashes(g_after, size=2)
        return Difference(
            remained=list(pb & pa),
            lost=list(pb - pa),
            emerged=list(pa - pb),
        )

    def _next_observer(self, diff: Difference, iteration: int) -> Observer:
        """Generate Observer_{n+1} from the difference."""
        if diff.emerged:
            p = "attends to emergent patterns"
            a = ["prioritize newly emerged structures",
                 f"track {len(diff.emerged)} emergent patterns"]
            b = ["emergence_bias", "novelty_seeking"]
        elif diff.lost:
            p = "attends to dissipated patterns"
            a = ["investigate why patterns were lost",
                 f"track {len(diff.lost)} lost patterns"]
            b = ["conservation_bias", "loss_aversion"]
        elif diff.remained:
            p = "attends to persistent invariants"
            a = ["prioritize stable structures",
                 f"track {len(diff.remained)} invariants"]
            b = ["stability_bias", "invariant_seeking"]
        else:
            p = "exploratory observer"
            a = ["no strong prior"]
            b = ["exploration_bias"]

        return Observer(
            id=f"observer_iter_{iteration}",
            name=f"Observer (iter {iteration})",
            perspective=p,
            assumptions=a,
            biases=b,
            extractor=self.current_observer.extractor,
        )

    def observe_once(self, domain: Domain) -> MetaState:
        """One cycle: observe → compute difference → generate next observer."""
        i = len(self.history)

        observation = Observation(
            id=f"obs_{i}",
            field_id=domain.id,
            field_content=domain.source_text or "",
            observer=self.current_observer,
            domain=domain,
            operator=f"diff_preserving_{i}",
        )

        pats = pattern_hashes(domain, size=2)
        g_after = Domain(
            id=f"{domain.id}_i{i}",
            name=f"Patterns iter {i}",
            nodes=[Node(id=f"p_{h[:8]}", label=f"Pat_{h[:8]}",
                        role="pattern")
                   for h in pats],
            edges=[],
            observer_id=self.current_observer.id,
        )

        if i == 0:
            diff = Difference(emerged=list(pats))
        else:
            diff = self._compute_difference(
                self.history[-1].state_after, g_after
            )

        analysis_result = analyze([observation], pattern_size=2)

        meta = MetaState(
            iteration=i,
            state_before=domain,
            observer=self.current_observer,
            state_after=g_after,
            difference=diff,
            analysis=analysis_result,
        )
        self.history.append(meta)

        # Generate next observer from the difference
        self.current_observer = self._next_observer(diff, i + 1)

        return meta

    def observe_recursively(self, domain: Domain,
                            max_iter: int = 8) -> list[MetaState]:
        """Run multiple iterations, each time generating a new observer."""
        current = domain
        for i in range(max_iter):
            meta = self.observe_once(current)
            if len(meta.state_after.nodes) < 2:
                break
            current = meta.state_after
        return self.history
