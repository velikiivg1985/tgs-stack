"""tgs.resonance.domain — Core graph structures."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional
import networkx as nx

@dataclass
class Node:
    id: str
    label: str = ""
    role: str = ""
    attributes: dict = field(default_factory=dict)

@dataclass
class Edge:
    source: str
    target: str
    relation: str = "related_to"   # было 'type'
    weight: float = 1.0

@dataclass
class Evidence:
    text: str = ""
    source: str = ""

@dataclass
class Domain:
    id: str
    name: str = ""
    nodes: list[Node] = field(default_factory=list)
    edges: list[Edge] = field(default_factory=list)
    source_text: Optional[str] = None
    observer_id: Optional[str] = None

    @property
    def graph(self) -> nx.DiGraph:
        G = nx.DiGraph()
        for n in self.nodes:
            G.add_node(n.id, label=n.label, role=n.role, **n.attributes)
        for e in self.edges:
            G.add_edge(e.source, e.target, relation=e.relation, weight=e.weight)
        return G

    def add_node(self, node: Node) -> None:
        self.nodes.append(node)

    def add_edge(self, edge: Edge) -> None:
        self.edges.append(edge)

    def node_by_id(self, node_id: str) -> Optional[Node]:
        for n in self.nodes:
            if n.id == node_id:
                return n
        return None
