"""Tension Classifier with Chain-of-Thought reasoning.

Classifies the TYPE of structural tension between two positions.
Supports both LLM-based classification (when an API key is provided)
and a lightweight local heuristic fallback.
"""
from __future__ import annotations
import os
import re
from typing import Dict

TGS_CLASSIFY_PROMPT = """You are an analyst of structural tensions. Diagnose the TYPE of tension.

## CATEGORIES
1. **open_question** — Resolvable through refinement or data.
2. **reflexive_limitation** — Structural limitation of the observer position.
3. **real_contradiction** — Hard contradiction under given constraints.
4. **no_common_ground** — Independent phenomena mistakenly collapsed.

## OUTPUT FORMAT
Invariant A: [formulation]
Invariant B: [formulation]
Collision test: [YES/NO + explanation]
Tension type: [open_question | reflexive_limitation | real_contradiction | no_common_ground]
Diagnosis: [1-2 sentences]
"""

RelationMap = {
    "open_question": "related_to",
    "reflexive_limitation": "mirrors",
    "real_contradiction": "contradicts",
    "no_common_ground": "bridges",
}


def parse_classification(raw: str) -> Dict[str, str]:
    """Parse an LLM response into a structured dictionary."""
    result = {
        "invariant_a": "", "invariant_b": "", "collision": "",
        "tension_type": "unknown", "diagnosis": "", "raw": raw,
    }
    patterns = {
        "invariant_a": r"Invariant\s*A\s*:\s*(.*)",
        "invariant_b": r"Invariant\s*B\s*:\s*(.*)",
        "collision": r"Collision\s*test\s*:\s*(.*)",
        "tension_type": r"Tension\s*type\s*:\s*(.*)",
        "diagnosis": r"Diagnosis\s*:\s*(.*)",
    }
    for key, pat in patterns.items():
        m = re.search(pat, raw, re.IGNORECASE)
        if m:
            result[key] = m.group(1).strip()
    valid = {"open_question", "reflexive_limitation",
             "real_contradiction", "no_common_ground"}
    tt = result["tension_type"].lower()
    for vt in valid:
        if vt in tt:
            result["tension_type"] = vt
            break
    else:
        result["tension_type"] = "unknown"
    result["suggested_relation"] = RelationMap.get(
        result["tension_type"], "related_to"
    )
    return result


def classify_locally(a: str, b: str) -> Dict[str, str]:
    """Lightweight keyword-based classifier (fallback when LLM unavailable)."""
    text = f"{a} {b}".lower()
    if any(w in text for w in ["unrelated", "orthogonal"]):
        return {"tension_type": "no_common_ground",
                "diagnosis": "Independent.",
                "suggested_relation": "bridges"}
    if sum(1 for w in ["observer", "objective", "distortion"]
           if w in text) >= 2:
        return {"tension_type": "reflexive_limitation",
                "diagnosis": "Observer limitation.",
                "suggested_relation": "mirrors"}
    if any(w in text for w in ["budget", "fixed", "impossible", "zero-sum"]):
        return {"tension_type": "real_contradiction",
                "diagnosis": "Hard constraint.",
                "suggested_relation": "contradicts"}
    return {"tension_type": "open_question",
            "diagnosis": "LLM recommended.",
            "suggested_relation": "related_to"}


class TensionClassifier:
    """Classify tensions using an LLM backend or local heuristic."""

    def __init__(self, provider="local", model=None, api_key=None):
        self.provider = provider
        self.model = model
        self.api_key = api_key

    def classify(self, a: str, b: str) -> Dict[str, str]:
        if self.provider == "local":
            return classify_locally(a, b)
        prompt = TGS_CLASSIFY_PROMPT + (
            f"\n\nPosition A: {a}\nPosition B: {b}"
        )
        if self.provider == "openai":
            from openai import OpenAI
            key = self.api_key or os.environ.get("OPENAI_API_KEY", "")
            r = OpenAI(api_key=key).chat.completions.create(
                model=self.model or "gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.0,
            )
            return parse_classification(r.choices[0].message.content)
        elif self.provider == "anthropic":
            from anthropic import Anthropic
            key = self.api_key or os.environ.get("ANTHROPIC_API_KEY", "")
            r = Anthropic(api_key=key).messages.create(
                model=self.model or "claude-3-5-sonnet-20241022",
                max_tokens=1024,
                messages=[{"role": "user", "content": prompt}],
            )
            return parse_classification(r.content[0].text)
        raise ValueError(f"Unknown provider: {self.provider!r}")


def format_classification(result: Dict[str, str]) -> str:
    """Pretty-print a classification result."""
    return "\n".join([
        "─" * 50,
        f"Invariant A: {result.get('invariant_a', '—')}",
        f"Invariant B: {result.get('invariant_b', '—')}",
        f"Collision: {result.get('collision', '—')}",
        f"Type: {result.get('tension_type', 'unknown')}",
        f"Relation: {result.get('suggested_relation', '—')}",
        f"Diagnosis: {result.get('diagnosis', '—')}",
        "─" * 50,
    ])
