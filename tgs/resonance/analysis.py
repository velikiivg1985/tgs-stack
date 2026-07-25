"""Structural resonance analysis"""
from __future__ import annotations
from dataclasses import dataclass, field
from collections import defaultdict
from itertools import combinations
import hashlib
from .domain import Domain


@dataclass
class ResonanceAnalysis:
    observation_ids: list[str] = field(default_factory=list)
    observer_ids: list[str] = field(default_factory=list)

    pairwise_matches: dict = field(default_factory=dict)
    asymmetry: dict = field(default_factory=dict)
    shared_patterns: list = field(default_factory=list)
    unique_patterns: dict = field(default_factory=dict)

    invariants: list = field(default_factory=list)
    differences: list = field(default_factory=list)
    tensions: list = field(default_factory=list)

    overall_confidence: float = 0.0

    not_claimed: list[str] = field(default_factory=lambda: [
        "causal identity between domains",
        "ontological identity between domains",
        "scientific proof",
        "truth independent of observation",
    ])

    limitations: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "observation_ids": self.observation_ids,
            "observer_ids": self.observer_ids,
            "pairwise_matches": {
                f"{a}__{b}": v for (a, b), v in self.pairwise_matches.items()
            },
            "asymmetry": {
                f"{a}__{b}": v for (a, b), v in self.asymmetry.items()
            },
            "shared_patterns": self.shared_patterns,
            "unique_patterns": self.unique_patterns,
            "invariants": self.invariants,
            "differences": self.differences,
            "tensions": self.tensions,
            "overall_confidence": self.overall_confidence,
            "not_claimed": self.not_claimed,
            "limitations": self.limitations,
        }


def pattern_hashes(domain: Domain, size: int = 2) -> set[str]:
    from itertools import combinations as comb
    G = domain.graph
    hashes = set()
    for subset in comb(G.nodes(), size):
        sg = G.subgraph(subset)
        if sg.number_of_edges() == 0:
            continue
        triples = []
        for u, v, d in sg.edges(data=True):
            ru = sg.nodes[u].get("role") or sg.nodes[u].get("label", "?")
            rv = sg.nodes[v].get("role") or sg.nodes[v].get("label", "?")
            triples.append(f"{ru}--{d.get('type', '?')}-->{rv}")
        triples.sort()
        h = hashlib.md5("|".join(triples).encode()).hexdigest()[:12]
        hashes.add(h)
    return hashes


def analyze(observations, pattern_size: int = 2) -> ResonanceAnalysis:
    result = ResonanceAnalysis(
        observation_ids=[o.id for o in observations],
        observer_ids=[o.observer.id for o in observations],
    )

    patterns_per_obs: dict[str, set[str]] = {}
    for obs in observations:
        patterns_per_obs[obs.id] = pattern_hashes(obs.domain, pattern_size)

    all_patterns: dict[str, list[str]] = defaultdict(list)
    for obs_id, hashes in patterns_per_obs.items():
        for h in hashes:
            all_patterns[h].append(obs_id)

    strict = len(observations)
    for h, obs_ids in all_patterns.items():
        if len(obs_ids) == strict:
            result.shared_patterns.append(h)
            result.invariants.append({
                "pattern_hash": h, "coverage": 1.0,
                "observers": obs_ids, "status": "strict_invariant",
            })
        elif len(obs_ids) >= 2:
            result.invariants.append({
                "pattern_hash": h,
                "coverage": len(obs_ids) / strict,
                "observers": obs_ids, "status": "partial_invariant",
            })

    for obs_id, hashes in patterns_per_obs.items():
        unique = [h for h in hashes if len(all_patterns[h]) == 1]
        if unique:
            result.unique_patterns[obs_id] = unique
            for h in unique:
                result.differences.append({
                    "pattern_hash": h, "observer": obs_id,
                    "status": "observer_specific",
                })

    for obs_a, obs_b in combinations(observations, 2):
        pa = patterns_per_obs[obs_a.id]
        pb = patterns_per_obs[obs_b.id]
        union = pa | pb
        if not union:
            j = 1.0 if not pa and not pb else 0.0
        else:
            j = len(pa & pb) / len(union)
        result.pairwise_matches[(obs_a.id, obs_b.id)] = round(j, 4)

    for obs_a, obs_b in combinations(observations, 2):
        pa = patterns_per_obs[obs_a.id]
        pb = patterns_per_obs[obs_b.id]
        a_in_b = len(pa & pb) / max(1, len(pa))
        b_in_a = len(pa & pb) / max(1, len(pb))
        result.asymmetry[(obs_a.id, obs_b.id)] = round(abs(a_in_b - b_in_a), 4)

    if result.pairwise_matches:
        mean_m = (sum(result.pairwise_matches.values())
                  / len(result.pairwise_matches))
        result.overall_confidence = round(
            0.6 * mean_m + 0.4 * min(1.0, len(result.shared_patterns) / 5), 4
        )

    result.limitations.append(
        f"Analyzed {len(observations)} observations, pattern_size={pattern_size}"
    )
    result.limitations.append(
        "Structural similarity ≠ semantic or causal identity"
    )
    return result
