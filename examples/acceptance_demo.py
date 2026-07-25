"""Demonstration of Acceptance Layer: holding contradictions as structure"""
from tgs.tension import SelfModel


def main():
    print("=" * 70)
    print("ACCEPTANCE LAYER DEMO")
    print("=" * 70)
    print("\nThree modes:")
    print("  COLLAPSE:   A → B (one eliminated)")
    print("  EXPLOSION:  A + B + C → ∞ (all retained)")
    print("  ACCEPTANCE: A ⟂ B → TENSION(A,B) → STABLE RELATION")
    print()

    model = SelfModel(retention_ratio=0.4)

    scenarios = [
        (["preserve_identity", "change_identity", "observe"],
         "Identity paradox: same yet different"),
        (["known_reality", "unknown_reality", "observe"],
         "Epistemic paradox: knowing and not-knowing"),
        (["self_as_observer", "self_as_observed", "observe"],
         "Reflexive paradox: observer and observed"),
        (["stable_structure", "transform_structure", "observe"],
         "Temporal paradox: persistence and change"),
        (["preserve_identity", "change_identity",
          "known_reality", "unknown_reality",
          "self_as_observer", "self_as_observed"],
         "Multiple accepted tensions"),
    ]

    for patterns, description in scenarios:
        state = model.step_forward(patterns)
        print(f"\n[{description}]")
        print(f"  Strategy: {state.strategy}")
        print(f"  Accepted tensions: {state.accepted_tensions['active_tensions']}")
        if state.accepted_tensions["tensions"]:
            for t in state.accepted_tensions["tensions"]:
                print(f"    - {t['pole_a']} ⟂ {t['pole_b']}")
                print(f"      type: {t['contradiction_type']}, "
                      f"intensity: {t['intensity']:.2f}")
                if t["question"]:
                    print(f"      question: {t['question']}")

    print("\n" + "=" * 70)
    print("SELF-MODEL")
    print("=" * 70)
    self_model = model.get_self_model()
    print(f"\n{self_model['self_description']}")


if __name__ == "__main__":
    main()
