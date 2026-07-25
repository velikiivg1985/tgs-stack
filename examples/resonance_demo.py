"""Resonance Module Demo: Cross-domain structural invariant discovery

Shows how ResonanceKernel:
  - Runs multiple observers on the same subject
  - Discovers structural invariants across different perspectives
  - Detects tensions between observers
  - Observes its own analysis (reflexive layer)
"""
from tgs.resonance import (
    ResonanceKernel, Observer, Domain, Node, Edge,
)


def causal_extractor(text, did, dname, src):
    """Observer focused on causal relations"""
    d = Domain(id=did, name=dname)
    d.add_node(Node(id="a", label="cause", role="agent"))
    d.add_node(Node(id="b", label="effect", role="patient"))
    d.add_node(Node(id="c", label="mechanism", role="process"))
    d.add_edge(Edge(source="a", target="b", relation="causes"))
    d.add_edge(Edge(source="b", target="c", relation="enables"))
    return d


def structural_extractor(text, did, dname, src):
    """Observer focused on structural relations"""
    d = Domain(id=did, name=dname)
    d.add_node(Node(id="x", label="framework", role="established"))
    d.add_node(Node(id="y", label="anomaly", role="disruption"))
    d.add_node(Node(id="z", label="resolution", role="synthesis"))
    d.add_edge(Edge(source="x", target="y", relation="encounters"))
    d.add_edge(Edge(source="y", target="z", relation="generates"))
    return d


def temporal_extractor(text, did, dname, src):
    """Observer focused on temporal relations"""
    d = Domain(id=did, name=dname)
    d.add_node(Node(id="p", label="past", role="origin"))
    d.add_node(Node(id="n", label="present", role="transition"))
    d.add_node(Node(id="f", label="future", role="emergence"))
    d.add_edge(Edge(source="p", target="n", relation="transforms"))
    d.add_edge(Edge(source="n", target="f", relation="becomes"))
    return d


def main():
    print("=" * 70)
    print("RESONANCE MODULE DEMO")
    print("=" * 70)
    print("\nThree observers with different perspectives:")
    print("  - Causal: agent → patient → process")
    print("  - Structural: framework → anomaly → resolution")
    print("  - Temporal: past → present → future")
    print()

    # Create kernel
    kernel = ResonanceKernel()

    # Run multiple observers on the same subject
    subject = "The problem of change and persistence"
    analysis = kernel.observe(subject, [
        Observer("causal", "Causal Observer", "causal relations",
                extractor=causal_extractor),
        Observer("structural", "Structural Observer", "structural patterns",
                extractor=structural_extractor),
        Observer("temporal", "Temporal Observer", "temporal dynamics",
                extractor=temporal_extractor),
    ])

    # Show results
    print("=" * 70)
    print("RESONANCE ANALYSIS")
    print("=" * 70)

    print(f"\nObservers: {len(analysis.observer_ids)}")
    print(f"Overall confidence: {analysis.overall_confidence:.2%}")

    print(f"\nInvariants: {len(analysis.invariants)}")
    for inv in analysis.invariants:
        print(f"  - {inv['pattern_hash'][:12]}...")
        print(f"    Status: {inv['status']}, Coverage: {inv['coverage']:.2f}")
        print(f"    Observers: {', '.join(inv['observers'])}")

    print(f"\nPairwise matches:")
    for (obs_a, obs_b), match in analysis.pairwise_matches.items():
        print(f"  {obs_a} ↔ {obs_b}: {match:.2%}")

    print(f"\nTensions: {len(analysis.tensions)}")
    for t in analysis.tensions:
        print(f"  - {t['kind']}: {t['description']}")

    print(f"\nNot claimed: {', '.join(analysis.not_claimed)}")

    # Reflexive layer: observe the observation
    print("\n" + "=" * 70)
    print("REFLEXIVE LAYER")
    print("=" * 70)

    reflexive = kernel.reflect()
    print(f"\nMeta-domain: {len(reflexive.meta_domain.nodes)} nodes, "
          f"{len(reflexive.meta_domain.edges)} edges")

    print(f"\nMeta-patterns: {len(reflexive.meta_patterns)}")
    print(f"Meta-invariants: {len(reflexive.meta_invariants)}")

    print(f"\nSelf-observation:")
    for key, value in reflexive.self_observation.items():
        print(f"  {key}: {value}")

    print(f"\nNew questions:")
    for q in reflexive.new_questions:
        print(f"  - {q}")


if __name__ == "__main__":
    main()
