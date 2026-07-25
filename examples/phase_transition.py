"""Phase Transition Experiment: COLLAPSE ↔ STABLE ↔ EXPLOSION

Demonstrates that self-reference is sustainable only in a narrow zone
of retention ratio (R ∈ [0.3, 0.5]).

Three regimes:
  - COLLAPSE: Too much compression → identity dissolves
  - STABLE: Selective forgetting → persistent self-model
  - EXPLOSION: Too much retention → complexity overwhelms
"""
from tgs.resonance.phase import run_phase_experiment, make_cycle_domain


def main():
    print("=" * 70)
    print("PHASE TRANSITION EXPERIMENT")
    print("=" * 70)
    print("\nTesting retention ratios R ∈ [0.0, 0.1, ..., 1.0]")
    print("on canonical 3-cycle domain")
    print()
    print("Expected results:")
    print("  Low R (0.0-0.2)    → COLLAPSE (too much compression)")
    print("  Medium R (0.3-0.5) → STABLE (selective forgetting)")
    print("  High R (0.6-1.0)   → EXPLOSION (too much retention)")
    print()

    # Run experiment with default parameters
    results = run_phase_experiment()

    # Analyze results
    print("\n" + "=" * 70)
    print("ANALYSIS")
    print("=" * 70)

    for domain_name, runs in results.items():
        print(f"\n[{domain_name}]")

        # Count regimes
        regimes = {}
        for run in runs:
            regimes[run.regime] = regimes.get(run.regime, 0) + 1

        print(f"  Regime distribution:")
        for regime, count in sorted(regimes.items()):
            print(f"    {regime}: {count}/{len(runs)}")

        # Find stable zone
        stable_runs = [r for r in runs if r.regime == "stable"]
        if stable_runs:
            stable_rs = [r.retention_ratio for r in stable_runs]
            print(f"\n  Stable zone: R ∈ [{min(stable_rs):.1f}, {max(stable_rs):.1f}]")
            print(f"  Average final nodes in stable zone: "
                  f"{sum(r.final_nodes for r in stable_runs) / len(stable_runs):.1f}")

        # Show example trajectories
        print(f"\n  Example trajectories:")
        for run in runs[:3]:  # Show first 3
            print(f"    R={run.retention_ratio:.1f}: {' → '.join(map(str, run.trajectory))} "
                  f"[{run.regime}]")


if __name__ == "__main__":
    main()
