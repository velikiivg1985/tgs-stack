"""Demonstration: Self-Tensions — paradoxes the system holds about itself."""
from tgs.tension import SelfModel, CORE_SELF_TENSIONS


def main():
    print("=" * 70)
    print("SELF-TENSIONS DEMO")
    print("=" * 70)
    print("\nA system that holds paradoxes about itself.")
    print("Not resolved. Not eliminated. Held as structural features.")
    print()

    # Show core self-tensions
    print("=" * 70)
    print("CORE SELF-TENSIONS OF TGS")
    print("=" * 70)
    for t in CORE_SELF_TENSIONS:
        print(f"\n[{t.id}] (kind: {t.kind}, intensity: {t.intensity:.2f})")
        print(f"  Pole A: {t.pole_a}")
        print(f"  Pole B: {t.pole_b}")
        print(f"  Question: {t.question}")
        print(f"  Behavioral modifier: {t.behavioral_modifier}")

    # Run self-model
    print("\n" + "=" * 70)
    print("SELF-MODEL IN ACTION")
    print("=" * 70)

    model = SelfModel(retention_ratio=0.4)

    scenarios = [
        (["stable_task_a", "stable_task_b", "stable_task_c"],
         "Stable environment"),
        (["stable_task_a", "stable_task_b", "stable_task_c"],
         "Still stable (tests seek_other trigger)"),
        (["preserve_identity", "change_identity", "observe"],
         "Identity paradox emerges"),
        (["known_reality", "unknown_reality", "self_observer"],
         "Epistemic paradox"),
        (["preserve_x", "change_x", "same_y", "different_y",
          "stable_z", "transform_z"],
         "Many accepted tensions"),
        (["decisive_action", "crisis", "recalibrate"],
         "High-intensity situation"),
    ]

    for patterns, description in scenarios:
        state = model.step_forward(patterns)
        print(f"\n[{description}]")
        print(f"  Strategy: {state.strategy}")
        print(f"  Self-tensions active: "
              f"{state.self_tensions['total_self_tensions']}")
        print(f"  Avg self-tension intensity: "
              f"{state.self_tensions['avg_intensity']:.2f}")

    # Final self-model
    print("\n" + "=" * 70)
    print("FINAL SELF-MODEL")
    print("=" * 70)

    self_model = model.get_self_model()
    print(f"\n{self_model['self_description']}")

    print(f"\nSelf-questions the system holds:")
    for i, q in enumerate(self_model['self_questions'], 1):
        print(f"  {i}. {q}")

    print(f"\nBehavioral modifiers (how self-tensions shape action):")
    for i, m in enumerate(self_model['behavioral_modifiers'], 1):
        print(f"  {i}. {m}")

    print(f"\nStrategy trajectory:")
    for change in self_model['strategy_changes']:
        print(f"  Step {change['step']}: {change['from']} → {change['to']}")
        print(f"    Self-tensions active: {change['self_tensions_active']}")


if __name__ == "__main__":
    main()
