"""Reflexive layer: Resonance observing its own analysis"""
from __future__ import annotations
from dataclasses import dataclass, field
from itertools import combinations
from .domain import Domain, Node, Edge, Evidence
from .analysis import ResonanceAnalysis, pattern_hashes
from .observer import Observer, Observation


@dataclass
class ReflexiveReport:
    meta_domain: Domain
    meta_patterns: list[str]
    meta_invariants: list
    observed_process: dict
    self_observation: dict
    new_questions: list[str]

    def to_dict(self) -> dict:
        return {
            "meta_domain": self.meta_domain.to_dict(),
            "meta_patterns": self.meta_patterns,
            "meta_invariants": self.meta_invariants,
            "observed_process": self.observed_process,
            "self_observation": self.self_observation,
            "new_questions": self.new_questions,
        }


def _build_meta_domain(analysis: ResonanceAnalysis, observations) -> Domain:
    domain = Domain(
        id=f"meta_{analysis.observation_ids[0] if analysis.observation_ids else 'x'}",
        name="Resonance self-observation",
        observer_id="tgs_reflexive",
        assumptions=[
            "meta-domain constructed automatically from analysis output",
        ],
    )

    for obs_id in analysis.observer_ids:
        obs = next((o for o in observations if o.observer.id == obs_id), None)
        perspective = obs.observer.perspective if obs else "unknown"
        domain.add_node(Node(
            id=f"obs_{obs_id}", label=f"Observer_{obs_id}",
            role="observer",
            metadata={"perspective": perspective},
        ))

    for i, inv in enumerate(analysis.invariants):
        status = inv["status"].replace("invariant", "").strip("_") or "strict"
        domain.add_node(Node(
            id=f"inv_{i}", label=f"Invariant_{inv['pattern_hash'][:8]}",
            role=f"invariant_{status}",
            metadata={
                "coverage": inv["coverage"],
                "observers": inv["observers"],
            },
        ))
        for oid in inv["observers"]:
            if domain.node_by_id(f"obs_{oid}"):
                domain.add_edge(Edge(
                    source=f"obs_{oid}", target=f"inv_{i}",
                    relation="produced",
                    confidence=inv["coverage"],
                    evidence=Evidence(source=f"analysis.invariants[{i}]",
                                      extractor_id="tgs_reflexive"),
                ))

    for i, t in enumerate(analysis.tensions):
        domain.add_node(Node(
            id=f"tens_{i}", label=f"Tension_{t['kind']}",
            role=t["kind"],
            metadata={"description": t["description"]},
        ))
        for oid in t["between"]:
            if oid != "system" and domain.node_by_id(f"obs_{oid}"):
                domain.add_edge(Edge(
                    source=f"obs_{oid}", target=f"tens_{i}",
                    relation="involved_in",
                    evidence=Evidence(source=f"analysis.tensions[{i}]",
                                      extractor_id="tgs_reflexive"),
                ))

    for (i, a), (j, b) in combinations(enumerate(analysis.invariants), 2):
        shared = set(a["observers"]) & set(b["observers"])
        if shared:
            domain.add_edge(Edge(
                source=f"inv_{i}", target=f"inv_{j}",
                relation="co_occurs",
                confidence=len(shared) / max(
                    len(a["observers"]), len(b["observers"])
                ),
                evidence=Evidence(source="shared_observers",
                                  extractor_id="tgs_reflexive"),
            ))

    return domain


def observe_observation(analysis: ResonanceAnalysis,
                        observations) -> ReflexiveReport:
    meta = _build_meta_domain(analysis, observations)
    meta_pats = list(pattern_hashes(meta, size=2))

    surviving = [{
        "pattern_hash": inv["pattern_hash"],
        "original_coverage": inv["coverage"],
        "meta_status": "embedded_in_meta_graph",
    } for inv in analysis.invariants]

    self_obs = {
        "meta_nodes": len(meta.nodes),
        "meta_edges": len(meta.edges),
        "meta_patterns": len(meta_pats),
        "observer_count": len(analysis.observer_ids),
        "invariant_count": len(analysis.invariants),
        "tension_count": len(analysis.tensions),
        "reflexive_biases": [
            "privileges topology over meaning",
            "meta-construction is itself an act of observation",
        ],
    }

    questions = []
    if not analysis.invariants:
        questions.append("No invariants found. Are observers too divergent?")
    if len(analysis.tensions) > len(analysis.invariants):
        questions.append(
            f"Tensions ({len(analysis.tensions)}) outnumber invariants "
            f"({len(analysis.invariants)})."
        )
    questions.append(
        "If Resonance were replaced, which invariants would persist?"
    )

    return ReflexiveReport(
        meta_domain=meta,
        meta_patterns=meta_pats,
        meta_invariants=surviving,
        observed_process={
            "observation_count": len(analysis.observation_ids),
            "strict_invariants": len(analysis.shared_patterns),
            "total_invariants": len(analysis.invariants),
            "tensions": len(analysis.tensions),
            "overall_confidence": analysis.overall_confidence,
        },
        self_observation=self_obs,
        new_questions=questions,
    )
