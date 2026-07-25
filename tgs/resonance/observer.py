"""Observer, Observation, and Extractor protocol"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Protocol
from datetime import datetime
from .domain import Domain


class Extractor(Protocol):
    def __call__(self, text: str, domain_id: str, domain_name: str,
                 source: str) -> Domain: ...


@dataclass
class Observer:
    id: str
    name: str
    perspective: str
    assumptions: list[str] = field(default_factory=list)
    extractor: Extractor | None = None
    biases: list[str] = field(default_factory=list)

    def extract(self, text: str, domain_id: str, domain_name: str,
                source: str) -> Domain:
        if self.extractor is None:
            raise RuntimeError(f"Observer {self.id!r} has no extractor")
        domain = self.extractor(text, domain_id, domain_name, source)
        domain.observer_id = self.id
        domain.assumptions = list(self.assumptions)
        return domain


@dataclass
class Observation:
    id: str
    field_id: str
    field_content: str
    observer: Observer
    domain: Domain
    operator: str = ""
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    metadata: dict = field(default_factory=dict)

    def node_labels(self) -> set[str]:
        return {d.label for d in self.domain.nodes}

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "field_id": self.field_id,
            "observer": {
                "id": self.observer.id, "name": self.observer.name,
                "perspective": self.observer.perspective,
                "assumptions": self.observer.assumptions,
                "biases": self.observer.biases,
            },
            "domain": self.domain.to_dict(),
            "operator": self.operator,
            "timestamp": self.timestamp,
            "metadata": self.metadata,
        }
