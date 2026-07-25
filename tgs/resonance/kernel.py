"""ResonanceKernel — main API for the Resonance module."""
from __future__ import annotations
from .observer import Observer, Observation
from .analysis import analyze, ResonanceAnalysis
from .invariant import detect_tensions
from .reflexive import observe_observation, ReflexiveReport


class ResonanceKernel:
    """Reflexive kernel for cross-domain structural invariant discovery.

    Resonance does not return TRUTH. It returns structural observations.

    Usage:
        kernel = ResonanceKernel()
        analysis = kernel.observe(subject, [observer1, observer2, ...])
        reflexive = kernel.reflect(analysis)
    """

    def __init__(self):
        self.observations: list[Observation] = []
        self.history: list[ResonanceAnalysis] = []

    def observe(self, subject: str, observers: list[Observer],
                field_id: str | None = None) -> ResonanceAnalysis:
        """Run multiple observers on the same subject, then analyze."""
        field_id = field_id or subject[:32].replace(" ", "_")

        new_obs = []
        for obs in observers:
            domain = obs.extract(
                subject,
                f"{field_id}__{obs.id}",
                f"{obs.name} on {subject[:30]}",
                f"subject:{field_id}",
            )
            observation = Observation(
                id=f"obs_{obs.id}_{len(self.observations)}",
                field_id=field_id,
                field_content=subject,
                observer=obs,
                domain=domain,
                operator=f"observer:{obs.id}",
            )
            new_obs.append(observation)

        self.observations.extend(new_obs)

        analysis = analyze(new_obs, pattern_size=2)
        detect_tensions(analysis, new_obs)
        self.history.append(analysis)
        return analysis

    def reflect(self,
                analysis: ResonanceAnalysis | None = None) -> ReflexiveReport:
        """Resonance observes its own analysis. Automatic."""
        if analysis is None:
            if not self.history:
                raise RuntimeError("No analysis to reflect on")
            analysis = self.history[-1]

        obs_ids = set(analysis.observation_ids)
        observations = [o for o in self.observations if o.id in obs_ids]
        return observe_observation(analysis, observations)

    def challenge(self, hypothesis: str) -> dict:
        """Ask: under what conditions would this NOT hold?"""
        return {
            "hypothesis": hypothesis,
            "falsification": [
                "Invariant disappears under new observer",
                "Invariant does not survive rephrasing",
                "Counter-example shows different structure",
            ],
            "status": "hypothesis, not truth",
        }
