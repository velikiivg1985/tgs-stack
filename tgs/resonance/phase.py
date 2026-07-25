"""Phase transition experiment: COLLAPSE ↔ STABLE ↔ EXPLOSION.

Discovers that self-reference is sustainable only in a narrow zone
of retention ratio (R ∈ [0.3, 0.5]). Too much compression = collapse,
too much retention = explosion. Stable self requires selective forgetting.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from collections import defaultdict
import hashlib
import time
from .domain import Domain, Node, Edge


@dataclass
class CompressedMemory:
    """What remains when a pattern is forgotten but not erased."""
    pattern_class: str
    count: int
    context_signature: str
    first_seen: int
    last_seen: int

    def label(self) -> str:
        return f"mem_{self.pattern_class[:6]}_x{self.count}"


@dataclass
class RunMetrics:
    """Metrics from a single phase-transition run."""
    retention_ratio: float
    iterations_completed: int
    final_nodes: int
    final_edges: int
    max_nodes: int
    total_compressed: int
    regime: str
    trajectory: list[int] = field(default_factory=list)


class SelectiveObserver:
    """Observer with tunable retention ratio and compressed memory."""

    def __init__(self, retention_ratio: float = 0.5, compress: bool = True):
        self.R = max(0.0, min(1.0, retention_ratio))
        self.compress = compress
        self.memories: dict[str, CompressedMemory] = {}
        self.history: list[dict] = []
        self.known_classes: set[str] = set()

    def _extract(self, domain: Domain) -> list[dict]:
        instances = []
        for i, e in enumerate(domain.edges):
            s = domain.node_by_id(e.source)
            t = domain.node_by_id(e.target)
            sr = (s.role or s.label) if s else "?"
            tr = (t.role or t.label) if t else "?"
            sig = f"{sr}--{e.relation}-->{tr}"
            h = hashlib.md5(sig.encode()).hexdigest()[:8]
            instances.append({
                "id": f"i{i}", "pc": h, "src": e.source,
                "tgt": e.target, "sig": sig, "pos": i,
            })
        return instances

    def _contexts(self, domain: Domain, instances: list[dict]) -> list[dict]:
        ctxs = []
        by_src = {i["src"]: i for i in instances}
        for start in instances:
            chain, cur, visited = [start], start, {start["id"]}
            for _ in range(len(instances)):
                nxt = by_src.get(cur["tgt"])
                if not nxt or nxt["id"] in visited:
                    break
                chain.append(nxt); visited.add(nxt["id"]); cur = nxt
                if cur["tgt"] == start["src"] and len(chain) >= 2:
                    h = hashlib.md5(
                        "|".join(i["id"] for i in chain).encode()
                    ).hexdigest()[:8]
                    ctxs.append({
                        "id": f"cyc_{h}", "kind": "cycle",
                        "instances": [i["id"] for i in chain],
                    })
                    break
        n2i = defaultdict(list)
        for inst in instances:
            n2i[inst["src"]].append(inst["id"])
            n2i[inst["tgt"]].append(inst["id"])
        for node, ids in n2i.items():
            if len(ids) >= 2:
                h = hashlib.md5(f"sh_{node}".encode()).hexdigest()[:8]
                ctxs.append({
                    "id": f"sh_{h}", "kind": "shared",
                    "instances": ids,
                })
        return ctxs

    def _relevance(self, pc: str, insts: list[dict], ctxs: list[dict]) -> float:
        """Multi-criteria relevance score."""
        mult = min(1.0, len(insts) / 5.0)
        pers = min(1.0, sum(
            1 for h in self.history
            if any(p["pc"] == pc for p in h.get("insts", []))
        ) / 3.0)
        iids = {i["id"] for i in insts}
        cent = min(1.0, sum(
            1 for c in ctxs
            if any(x in iids for x in c["instances"])
        ) / 3.0)
        nov = 0.0 if pc in self.known_classes else 1.0
        return 0.3 * pers + 0.2 * nov + 0.3 * cent + 0.2 * mult

    def observe(self, domain: Domain, iteration: int) -> dict:
        """One iteration of selective observation."""
        insts = self._extract(domain)
        ctxs = self._contexts(domain, insts)

        by_pc = defaultdict(list)
        for i in insts:
            by_pc[i["pc"]].append(i)

        rel = {pc: self._relevance(pc, il, ctxs) for pc, il in by_pc.items()}
        ranked = sorted(rel.items(), key=lambda x: x[1], reverse=True)
        keep_n = max(1, int(len(ranked) * self.R))
        kept = {pc for pc, _ in ranked[:keep_n]}
        dropped = {pc for pc, _ in ranked[keep_n:]}

        nodes, edges, seen = [], [], set()

        for pc in kept:
            for inst in by_pc[pc]:
                nid = f"k_{inst['id']}"
                if nid not in seen:
                    nodes.append(Node(id=nid, label=inst["sig"], role="kept"))
                    seen.add(nid)
            cid = f"cls_{pc}"
            if cid not in seen:
                nodes.append(Node(id=cid, label=f"Pat_{pc}", role="class"))
                seen.add(cid)
            for inst in by_pc[pc]:
                edges.append(Edge(source=f"k_{inst['id']}", target=cid,
                                  relation="instantiates"))

        if self.compress:
            for pc in dropped:
                for inst in by_pc[pc]:
                    if pc in self.memories:
                        self.memories[pc].count += 1
                        self.memories[pc].last_seen = iteration
                    else:
                        self.memories[pc] = CompressedMemory(
                            pc, 1, inst["sig"], iteration, iteration,
                        )
            for pc, mem in self.memories.items():
                mid = f"mem_{pc}"
                if mid not in seen:
                    nodes.append(Node(id=mid, label=mem.label(), role="memory"))
                    seen.add(mid)

        kept_ids = {i["id"] for pc in kept for i in by_pc[pc]}
        for ctx in ctxs:
            inv = [x for x in ctx["instances"] if x in kept_ids]
            if len(inv) >= 2:
                cxid = f"ctx_{ctx['id']}"
                if cxid not in seen:
                    nodes.append(Node(id=cxid, label=f"{ctx['kind']}", role="context"))
                    seen.add(cxid)
                for iid in inv:
                    edges.append(Edge(source=f"k_{iid}", target=cxid, relation="in"))

        new_dom = Domain(
            id=f"{domain.id}_i{iteration}",
            name=f"R={self.R} iter {iteration}",
            nodes=nodes, edges=edges,
        )
        self.known_classes.update(by_pc.keys())
        rec = {"iter": iteration, "insts": insts, "kept": list(kept), "dropped": list(dropped)}
        self.history.append(rec)
        return {"domain": new_dom, "kept": len(kept), "dropped": len(dropped), "mems": len(self.memories)}


def make_cycle_domain() -> Domain:
    """Canonical test domain: 3-cycle."""
    d = Domain(id="cycle3", name="3-cycle", source_text="cause → effect → mechanism → cause")
    d.add_node(Node(id="cause", label="cause", role="agent"))
    d.add_node(Node(id="effect", label="effect", role="patient"))
    d.add_node(Node(id="mech", label="mechanism", role="process"))
    d.add_edge(Edge(source="cause", target="effect", relation="produces"))
    d.add_edge(Edge(source="effect", target="mech", relation="enables"))
    d.add_edge(Edge(source="mech", target="cause", relation="feeds_back"))
    return d


def make_rich_domain() -> Domain:
    """Richer test domain with multiple cycles."""
    d = Domain(id="rich", name="Rich system")
    for i in range(8):
        d.add_node(Node(id=f"n{i}", label=f"c{i}", role=f"r{i % 3}"))
    for s, t, r in [("n0","n1","p"),("n1","n2","e"),("n2","n0","f"),
                    ("n3","n4","p"),("n4","n5","e"),("n5","n3","f"),
                    ("n1","n4","c"),("n2","n6","m"),("n6","n7","d"),
                    ("n7","n0","i")]:
        d.add_edge(Edge(source=s, target=t, relation=r))
    return d


def run_one(R: float, max_iter: int = 6, factory=make_cycle_domain) -> RunMetrics:
    """Run
