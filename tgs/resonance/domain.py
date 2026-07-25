"""Core data structures: Domain, Node, Edge, Evidence"""
from __future__ import annotations
from dataclasses import dataclass, field
import hashlib


@dataclass
class Evidence:
    source: str
    excerpt: str = ""
    confidence: float = 1.0
    extractor_id: str = ""

    def to_dict(self) -> dict:
        return {
            "source": self.source,
            "excerpt": self.excerpt[:200],
            "confidence": self.confidence,
            "extractor_id": self.extractor_id,
        }


@dataclass
class Node:
    id: str
    label: str
    role: str | None = None
    metadata: dict = field(default_factory=dict)

    def signature(self) -> str:
        return f"{self.label}|{self.role or ''}"


@dataclass
class Edge:
    source: str
    target: str
    relation: str
    evidence: Evidence | None = None
    confidence: float = 1.0


@dataclass
class Domain:
    id: str
    name: str
    nodes: list[Node] = field(default_factory=list)
    edges: list[Edge] = field(default_factory=list)
    observer_id: str | None = None
    assumptions: list[str] = field(default_factory=list)
    source_text: str = ""

    @property
    def graph(self):
        import networkx as nx
        G = nx.DiGraph()
        for n in self.nodes:
            G.add_node(n.id, label=n.label, role=n.role)
        for e in self.edges:
            G.add_edge(e.source, e.target,
                       type=e.relation, confidence=e.confidence)
        return G

    def node_by_id(self, node_id: str) -> Node | None:
        return next((n for n in self.nodes if n.id == node_id), None)

    def add_node(self, node: Node) -> None:
        if not self.node_by_id(node.id):
            self.nodes.append(node)

    def add_edge(self, edge: Edge) -> None:
        if not self.node_by_id(edge.source):
            raise ValueError(f"Source node {edge.source!r} not in domain")
        if not self.node_by_id(edge.target):
            raise ValueError(f"Target node {edge.target!r} not in domain")
        self.edges.append(edge)

    def signature(self) -> str:
        node_sigs = sorted(n.signature() for n in self.nodes)
        edge_sigs = sorted(
            f"{self._role_of(e.source)}--{e.relation}-->{self._role_of(e.target)}"
            for e in self.edges
        )
        raw = "N:" + "|".join(node_sigs) + " E:" + "|".join(edge_sigs)
        return hashlib.md5(raw.encode()).hexdigest()[:12]

    def _role_of(self, node_id: str) -> str:
        n = self.node_by_id(node_id)
        return (n.role or n.label) if n else "?"

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "observer_id": self.observer_id,
            "nodes": [{"id": n.id, "label": n.label, "role": n.role}
                      for n in self.nodes],
            "edges": [
                {"source": e.source, "target": e.target,
                 "relation": e.relation, "confidence": e.confidence,
                 "evidence": e.evidence.to_dict() if e.evidence else None}
                for e in self.edges
            ],
            "assumptions": self.assumptions,
            "signature": self.signature(),
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Domain":
        d = cls(id=data["id"], name=data["name"],
                observer_id=data.get("observer_id"),
                assumptions=data.get("assumptions", []))
        for n in data.get("nodes", []):
            d.add_node(Node(id=n["id"], label=n["label"], role=n.get("role")))
        for e in data.get("edges", []):
            ev = None
            if e.get("evidence"):
                ev = Evidence(**e["evidence"])
            d.add_edge(Edge(source=e["source"], target=e["target"],
                            relation=e["relation"],
                            confidence=e.get("confidence", 1.0),
                            evidence=ev))
        return d
