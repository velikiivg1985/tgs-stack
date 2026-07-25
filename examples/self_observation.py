"""Self-observation: Apply SelfModel to a reconstructed analytical trace

Demonstrates how an agent can observe its own analytical process across
a conversation, detecting strategy shifts driven by tension emergence.
"""
from tgs.tension import SelfModel


def main():
    print("=" * 70)
    print("SELF-OBSERVATION THROUGH SELFMODEL")
    print("=" * 70)
    print("\nReconstructed sequence of analytical positions:")
    print()

    model = SelfModel(retention_ratio=0.4)

    # Simulate analytical trajectory
    observations = [
        ["bug_fix", "code_review", "technical_rigor"],
        ["philosophical_critique", "epistemic_humility", "predecessors"],
        ["structural_isomorphism", "empirical_test", "asymmetry"],
        ["circular_reasoning", "observer_role", "self_reference"],
        ["paradox_as_architecture", "tension_as_fuel", "self_model"],
        ["acceptance", "unresolved_contradiction", "generative_force"],
    ]

    print("Step-by-step observation:")
    for i, patterns in enumerate(observations, 1):
        state = model.step_forward(patterns)
        print(f"\n[Step {i}] Strategy: {state.strategy}")
        print(f"  Patterns observed: {', '.join(patterns)}")
        print(f"  Invariants: {state.invariants['stable_invariants']} stable, "
              f"{state.invariants['active_invariants']} active")
        print(f"  Change: {state.difference['avg_magnitude']:.2f}")
        print(f"  Uncertainty: {state.uncertainty['uncertainty']:.0%}")
        print(f"  Tensions: {state.tensions['active_tensions']}")
        print(f"  Accepted: {state.accepted_tensions['active_tensions']}")

    # Final self-model
    print("\n" + "=" * 70)
    print("FINAL SELF-MODEL")
    print("=" * 70)
    self_model = model.get_self_model()
    print(f"\n{self_model['self_description']}")

    print(f"\nStrategy trajectory:")
    for change in self_model['strategy_changes']:
        print(f"  Step {change['step']}: {change['from']} → {change['to']}")
        if change['trigger_tensions']:
            for t in change['trigger_tensions'][:2]:
                print(f"    triggered by: {t['kind']} "
                      f"(intensity {t['intensity']:.2f})")

    # Show accepted tensions
    if self_model['accepted_tensions']['tensions']:
        print(f"\nAccepted contradictions:")
        for t in self_model['accepted_tensions']['tensions']:
            print(f"  - {t['pole_a']} ⟂ {t['pole_b']}")
            print(f"    Type: {t['contradiction_type']}, "
                  f"Intensity: {t['intensity']:.2f}")
            if t['question']:
                print(f"    Question: {t['question']}")


if __name__ == "__main__":
    main()
