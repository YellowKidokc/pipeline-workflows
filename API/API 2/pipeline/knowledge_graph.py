"""Knowledge graph built from pipeline sidecars.

Uses NetworkX as the underlying graph engine when available (with a pure-Python
adjacency-dict fallback so the module still imports on a bare Python install).
Reads `*.framework.json` sidecars produced by FrameworkClassifierStation and
links each paper node to the Laws, Axiom Schemata, Equations, Fruits, and 7Q
node it references.
"""
from __future__ import annotations

import json
from collections import defaultdict, deque
from enum import Enum
from pathlib import Path
from typing import Iterable

try:
    import networkx as nx
    HAS_NX = True
except ImportError:
    nx = None
    HAS_NX = False


class NodeType(Enum):
    PAPER = "paper"
    LAW = "law"
    AXIOM = "axiom"
    AXIOM_SCHEMA = "axiom_schema"
    EQUATION = "equation"
    CONCEPT = "concept"
    FRUIT = "fruit"
    PERSON = "person"
    EXPERIMENT = "experiment"
    SERIES = "series"
    SEVEN_Q = "seven_q"


class EdgeType(Enum):
    DEPENDS_ON = "depends_on"
    SUPPORTS = "supports"
    EXTENDS = "extends"
    CONTRADICTS = "contradicts"
    ILLUSTRATES = "illustrates"
    RELATES_TO = "relates_to"
    SUPERSEDES = "supersedes"
    DERIVES_FROM = "derives_from"
    SYMMETRIC_WITH = "symmetric_with"
    MAPS_TO = "maps_to"
    PART_OF = "part_of"


class KnowledgeGraph:
    """Sidecar→graph builder with NetworkX backing and gap/cluster analytics."""

    def __init__(self) -> None:
        self.nodes: dict[str, dict] = {}
        self.adj: dict[str, dict[str, str]] = defaultdict(dict)
        self.graph = nx.Graph() if HAS_NX else None

    def build_from_sidecars(self, sidecar_dir: Path) -> None:
        for fp in Path(sidecar_dir).rglob("*.framework.json"):
            paper_id = fp.name.replace(".framework.json", "")
            try:
                payload = json.loads(fp.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                continue
            self.add_paper(paper_id, payload)

    def add_paper(self, paper_id: str, framework_data: dict) -> None:
        attrs = {
            "node_type": NodeType.PAPER.value,
            "score": framework_data.get("framework_coverage_score", 0),
            "depth": framework_data.get("framework_depth", "shallow"),
        }
        self._add_node(paper_id, attrs)
        for law in framework_data.get("laws_referenced", []):
            self._link(paper_id, law, NodeType.LAW, EdgeType.MAPS_TO)
        for ax in framework_data.get("axiom_schemata", []):
            self._link(paper_id, ax, NodeType.AXIOM_SCHEMA, EdgeType.MAPS_TO)
        for eq in framework_data.get("equations_present", []):
            self._link(paper_id, eq, NodeType.EQUATION, EdgeType.DERIVES_FROM)
        for fr in framework_data.get("fruits_referenced", []):
            self._link(paper_id, fr, NodeType.FRUIT, EdgeType.ILLUSTRATES)
        for sym_pair in framework_data.get("law_symmetry_pairs_invoked", []):
            if "↔" in sym_pair:
                a, b = [s.strip() for s in sym_pair.split("↔", 1)]
                self._link(a, b, NodeType.LAW, EdgeType.SYMMETRIC_WITH)
        if framework_data.get("seven_q"):
            self._link(paper_id, framework_data["seven_q"], NodeType.SEVEN_Q, EdgeType.PART_OF)

    def _add_node(self, node_id: str, attrs: dict) -> None:
        existing = self.nodes.get(node_id, {})
        existing.update(attrs)
        self.nodes[node_id] = existing
        if self.graph is not None:
            self.graph.add_node(node_id, **existing)

    def _link(self, a: str, b: str, target_type: NodeType, edge: EdgeType) -> None:
        self._add_node(b, {"node_type": target_type.value})
        self.adj[a][b] = edge.value
        self.adj[b][a] = edge.value
        if self.graph is not None:
            self.graph.add_edge(a, b, edge_type=edge.value)

    def find_gaps(self) -> list[dict]:
        expected = [f"L{i}" for i in range(1, 11)] + [f"AS-00{i}" for i in range(8)]
        return [{"node": n, "type": "missing"} for n in expected if n not in self.nodes]

    def find_clusters(self) -> list[set]:
        if self.graph is not None:
            return [set(c) for c in nx.connected_components(self.graph) if len(c) > 1]
        seen: set[str] = set()
        clusters: list[set] = []
        for node in list(self.nodes):
            if node in seen:
                continue
            component: set[str] = set()
            stack = [node]
            while stack:
                current = stack.pop()
                if current in seen:
                    continue
                seen.add(current)
                component.add(current)
                stack.extend(self.adj.get(current, {}).keys())
            if len(component) > 1:
                clusters.append(component)
        return clusters

    def shortest_path(self, from_id: str, to_id: str) -> list[str]:
        if self.graph is not None:
            try:
                return list(nx.shortest_path(self.graph, from_id, to_id))
            except (nx.NetworkXNoPath, nx.NodeNotFound) as exc:
                raise ValueError(f"no path between {from_id} and {to_id}") from exc
        queue: deque[list[str]] = deque([[from_id]])
        seen = {from_id}
        while queue:
            path = queue.popleft()
            tail = path[-1]
            if tail == to_id:
                return path
            for neighbor in self.adj.get(tail, {}):
                if neighbor not in seen:
                    seen.add(neighbor)
                    queue.append(path + [neighbor])
        raise ValueError(f"no path between {from_id} and {to_id}")

    def coverage_report(self) -> dict:
        laws = {f"L{i}": 0 for i in range(1, 11)}
        axioms = {f"AS-00{i}": 0 for i in range(8)}
        for source, edges in self.adj.items():
            for target, edge_type in edges.items():
                if edge_type != EdgeType.MAPS_TO.value:
                    continue
                for label in (source, target):
                    if label in laws:
                        laws[label] += 1
                    if label in axioms:
                        axioms[label] += 1
        return {"laws": laws, "axioms": axioms, "gaps": self.find_gaps()}

    def export_obsidian_links(self, paper_id: str) -> str:
        return "\n".join(f"- [[{n}]] ({e})" for n, e in self.adj.get(paper_id, {}).items())

    def export_graph_json(self, path: Path) -> None:
        edges = []
        seen_edges: set[tuple[str, str]] = set()
        for source, targets in self.adj.items():
            for target, edge_type in targets.items():
                pair = tuple(sorted((source, target)))
                if pair in seen_edges:
                    continue
                seen_edges.add(pair)
                edges.append({"source": source, "target": target, "edge_type": edge_type})
        payload = {
            "nodes": [{"id": node_id, **attrs} for node_id, attrs in self.nodes.items()],
            "edges": edges,
        }
        Path(path).write_text(json.dumps(payload, indent=2), encoding="utf-8")

    def export_mermaid(self, center_node: str, depth: int = 2) -> str:
        lines = ["graph TD"]
        if self.graph is not None and center_node in self.graph:
            visited = {center_node}
            frontier: Iterable[str] = {center_node}
            for _ in range(depth):
                nxt: set[str] = set()
                for node in frontier:
                    for neighbor in self.graph.neighbors(node):
                        lines.append(f"  {node} --- {neighbor}")
                        nxt.add(neighbor)
                frontier = nxt - visited
                visited |= nxt
            return "\n".join(lines)
        frontier = {center_node}
        seen = {center_node}
        for _ in range(depth):
            nxt = set()
            for node in frontier:
                for neighbor in self.adj.get(node, {}):
                    lines.append(f"  {node} --- {neighbor}")
                    nxt.add(neighbor)
            frontier = nxt - seen
            seen |= nxt
        return "\n".join(lines)

    def degree_ranking(self, top_n: int = 10) -> list[tuple[str, int]]:
        """Return the most-connected nodes — useful for "which Laws are over/under-cited"."""
        if self.graph is not None:
            return sorted(self.graph.degree(), key=lambda kv: kv[1], reverse=True)[:top_n]
        degrees = [(node, len(neighbors)) for node, neighbors in self.adj.items()]
        return sorted(degrees, key=lambda kv: kv[1], reverse=True)[:top_n]
