"""tgs.resonance.observer — Observer and Observation structures."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any
from .domain import Domain

@dataclass
class Observer:
    id: str
    name: str = ""
    perspective: str = ""
    assumptions: list[str] = field(default_factory=list)
    biases: list[str] = field(default_factory=list)
    extractor: Any = None

@dataclass
class Observation:
    id: str
    field_id: str
    field_content: str
    observer: Observer
    domain: Domain
    operator: str = "default"
