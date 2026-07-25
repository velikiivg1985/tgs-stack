"""Demonstration of Tension Module with Acceptance Layer

Shows how the SelfModel:
  - Tracks what persists (invariants)
  - Tracks what changes (differences)
  - Tracks blind spots (uncertainty)
  - Holds tensions as generative forces
  - Accepts contradictions as persistent relational structures
"""
from tgs.tension import SelfModel


def main():
    print("=" * 70)
    print("TENSION MODULE DEMO")
    print("=" * 70)
    print("\nSelfModel maintains identity through:")
    print("  - Invariants (what persists)")
    print("  - Differences (what changes)")
    print("  - Uncertainty (blind spots)")
    print("  - Tensions (generative forces)")
    print("  - Accepted contradictions (held without resolution)")
    print()

    # Create self-model with retention ratio in stable zone
    model = SelfModel(retention_ratio=0.4)

    # Simulate changing environment with paradoxes
    scenarios = [
        (["task_a", "task_b", "task_c"], "Routine work"),
        (["task_a", "task_b", "task_c"], "Routine work (stability)"),
        (["task_a", "problem_x", "task_b"], "New problem emerges"),
        (["problem_x", "problem_y", "problem_z"], "Full shift"),
        (["preserve_identity", "change_identity", "observe"],
         "Identity paradox"),
        (["known_reality", "unknown_reality", "observe"],
         "Epistemic paradox"),
        (["task_a", "problem_x", "new_insight"], "Integration attempt"),
    ]

    for patterns, description in scenarios:
        state = model.step_forward(patterns)
        print(f"\n[{description}]")
        print(f"  Strategy: {state.strategy}")
        print(f"  Invariants: {state.invariants['stable_invariants']} stable")
        print(f"  Change: {state.difference['avg_magnitude']:.2f}")
        print(f"  Tensions: {state.tensions['active_tensions']}")
        print(f"  Accepted: {state.accepted_tensions['active_tensions']}")

        # Show active tensions
        if state.tensions["tensions"]:
            print("  Active tensions:")
            for t in state.tensions["tensions"][:3]:
                print(f"    - {t['kind']} (intensity: {t['intensity']:.2f})")

        # Show accepted contradictions
        if state.accepted_tensions["tensions"]:
            print("  Accepted contradictions:")
            for t in state.accepted_tensions["tensions"][:2]:
                print(f"    - {t['pole_a']} ⟂ {t['pole_b']}")
                if t["question"]:
                    print(f"      Question: {t['question']}")

    # Show final self-model
    print("\n" + "=" * 70)
    print("FINAL SELF-MODEL")
    print("=" * 70)
    self_model = model.get_self_model()
    print(f"\n{self_model['self_description']}")

    print(f"\nStrategy changes: {self_model['strategy_changes_count']}")
    for change in self_model['strategy_changes'][:3]:
        print(f"  Step {change['step']}: {change['from']} → {change['to']}")


if __name__ == "__main__":
    main()
