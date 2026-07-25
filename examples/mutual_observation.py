"""Mutual Observation Protocol: Self-reference through difference

Demonstrates how self-reference emerges through the relation between
multiple observers, not within any single observer.

Key insight:
  Not: Self → Self (collapses)
  But: Observer₁ ↔ Observer₂ ↔ Observer₃ → Resonance → Invariant
"""
from tgs.resonance import (
    MutualObservationProtocol, Observer, Domain, Node, Edge,
)


def perspective_a_extractor(text, did, dname, src):
    """First perspective: focuses on stability"""
    d = Domain(id=did, name=dname)
    d.add_node(Node(id="identity", label="identity", role="stable"))
    d.add_node(Node(id="continuity", label="continuity", role="persistent"))
    d.add_node(Node(id="memory", label="memory", role="preserved"))
    d.add_edge(Edge(source="identity", target="continuity", relation="maintains"))
    d.add_edge(Edge(source="continuity", target="memory", relation="relies_on"))
    return d


def perspective_b_extractor(text, did, dname, src):
    """Second perspective: focuses on change"""
    d = Domain(id=did, name=dname)
    d.add_node(Node(id="transformation", label="transformation", role="dynamic"))
    d.add_node(Node(id="difference", label="difference", role="emergent"))
    d.add_node(Node(id="adaptation", label="adaptation", role="responsive"))
    d.add_edge(Edge(source="transformation", target="difference", relation="creates"))
    d.add_edge(Edge(source="difference", target="adaptation", relation="drives"))
    return d


def perspective_c_extractor(text, did, dname, src):
    """Third perspective: focuses on relation"""
    d = Domain(id=did, name=dname)
    d.add_node(Node(id="observer", label="observer", role="subject"))
    d.add_node(Node(id="observed", label="observed", role="object"))
    d.add_node(Node(id="relation", label="relation", role="mediating"))
    d.add_edge(Edge(source="observer", target="relation", relation="establishes"))
    d.add_edge(Edge(source="relation", target="observed", relation="constitutes"))
    return d


def main():
    print("=" * 70)
    print("MUTUAL OBSERVATION PROTOCOL")
    print("=" * 70)
    print("\nThree perspectives on the same subject:")
    print("  - Perspective A: stability (identity, continuity, memory)")
    print("  - Perspective B: change (transformation, difference, adaptation)")
    print("  - Perspective C: relation (observer, observed, relation)")
    print()
    print("Key question: What invariants emerge across these perspectives?")
    print()

    # Create protocol
    protocol = MutualObservationProtocol(retention_ratio=0.4)

    # Add observers
    protocol.add_observer(Observer(
        "perspective_a", "Stability Observer",
        "stability and persistence",
        extractor=perspective_a_extractor
    ))
    protocol.add_observer(Observer(
        "perspective_b", "Change Observer",
        "transformation and difference",
        extractor=perspective_b_extractor
    ))
    protocol.add_observer(Observer(
        "perspective_c", "Relation Observer",
        "relational structure",
        extractor=perspective_c_extractor
    ))

    # Run multiple iterations
    subject = "The nature of self through time"
    print("Running 3 iterations of mutual observation:")
    print()

    for i in range(3):
        print(f"[Iteration {i+1}]")
        analysis = protocol.observe_through_difference(
            subject, field_id=f"iter_{i}"
        )

        print(f"  Invariants found: {len(analysis.invariants)}")
        print(f"  Tensions detected: {len(analysis.tensions)}")
        print(f"  Confidence: {analysis.overall_confidence:.2%}")

        # Show invariants
        for inv in analysis.invariants[:3]:
            print(f"    - {inv['pattern_hash'][:12]}... "
                  f"({inv['status']}, coverage={inv['coverage']:.2f})")

        print()

    # Reflect on identity continuity
    print("=" * 70)
    print("IDENTITY CONTINUITY")
    print("=" * 70)

    reflection = protocol.reflect()
    print(f"\nStatus: {reflection['status']}")
    print(f"Total history depth: {reflection['total_history_depth']}")
    print(f"Persistent invariants: {len(reflection['persistent_invariants'])}")
    print(f"Emergent invariants: {len(reflection['emerged_invariants'])}")
    print(f"Lost invariants: {len(reflection['lost_invariants'])}")
    print(f"Identity continuity: {reflection['identity_continuity']:.2%}")

    # Challenge a hypothesis
    print("\n" + "=" * 70)
    print("HYPOTHESIS TESTING")
    print("=" * 70)

    hypothesis = "Self is the persistence of invariants through transformation"
    challenge = protocol.challenge(hypothesis)
    print(f"\nHypothesis: {challenge['hypothesis']}")
    print(f"Status: {challenge['status']}")
    print("\nFalsification conditions:")
    for condition in challenge['falsification']:
        print(f"  - {condition}")
    print("\nRecommended tests:")
    for test in challenge['recommended_tests']:
        print(f"  - {test}")


if __name__ == "__main__":
    main()
