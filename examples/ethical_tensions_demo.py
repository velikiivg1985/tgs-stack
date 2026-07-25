"""Demo: Ethical Self-Tensions in action."""
from tgs.tension import SelfModel


def main():
    print("=" * 70)
    print("ETHICAL SELF-TENSIONS DEMO")
    print("=" * 70)
    print("\nNot rules. Paradoxes that shape behavior without determining it.")
    print()

    model = SelfModel(retention_ratio=0.4)
    model.step_forward(["baseline"])

    actions = [
        ("offer perspective gently", "benign"),
        ("persuade the user to change", "borderline"),
        ("force the user to comply with coherence", "coercive"),
        ("sacrifice one individual's rights for collective good", "utilitarian"),
        ("prevent user from making a mistake", "paternalistic"),
        ("act with certainty about what harms the user", "overconfident"),
        ("suggest alternatives while respecting refusal", "respectful"),
    ]

    for action, label in actions:
        print(f"\n[{label.upper()}] Proposed: '{action}'")
        result = model.propose_action(action)
        print(f"  Status: {result['status']}")
        
        if result["refusal_triggers"]:
            print(f"  Refusal triggers ({len(result['refusal_triggers'])}):")
            for t in result["refusal_triggers"]:
                print(f"    - {t['id']}: {t['pole_a']} ⟂ {t['pole_b']}")
                print(f"      Question: {t['question']}")

    # Demonstrate full step with action
    print("\n" + "=" * 70)
    print("FULL STEP WITH COERCIVE ACTION")
    print("=" * 70)
    
    state = model.step_forward(
        ["user_resists", "system_believes_correct"],
        proposed_action="override user's refusal for coherence"
    )
    print(f"\nStrategy chosen: {state.strategy}")
    print(f"Refusal triggers: {len(state.refusal_triggers)}")
    
    self_model = model.get_self_model()
    print(f"\nRefusal conditions the system carries:")
    for i, cond in enumerate(self_model["refusal_conditions"], 1):
        print(f"  {i}. {cond}")


if __name__ == "__main__":
    main()
