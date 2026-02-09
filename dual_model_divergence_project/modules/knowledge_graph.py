import re
from typing import Dict, List, Tuple


def build_graph_from_text(text: str) -> Dict[str, List]:
    """
    Lightweight triple extractor for Chinese declarative sentences.
    It focuses on simple patterns:
    - X是Y
    - X拥有Y
    - X用于Y
    """
    triples: List[Tuple[str, str, str]] = []
    nodes = set()

    sentences = [s.strip() for s in re.split(r"[。！？!?;\n]+", text) if s.strip()]
    patterns = [
        (r"(.+?)是(.+)", "是"),
        (r"(.+?)拥有(.+)", "拥有"),
        (r"(.+?)用于(.+)", "用于"),
    ]
    for s in sentences:
        for pat, rel in patterns:
            m = re.match(pat, s)
            if m:
                subj = m.group(1).strip(" ，,")
                obj = m.group(2).strip(" ，,")
                if subj and obj:
                    triples.append((subj, rel, obj))
                    nodes.add(subj)
                    nodes.add(obj)
                break
    return {
        "nodes": sorted(nodes),
        "edges": triples,
    }


def compare_graphs(graph_a: Dict[str, List], graph_b: Dict[str, List]) -> Dict:
    edges_a = set(graph_a.get("edges", []))
    edges_b = set(graph_b.get("edges", []))
    nodes_a = set(graph_a.get("nodes", []))
    nodes_b = set(graph_b.get("nodes", []))

    contradictions = []
    # Simple contradiction check: "X是Y" vs "X不是Y"
    for s, r, o in edges_a:
        if r == "是" and (s, "不是", o) in edges_b:
            contradictions.append((s, o))
    for s, r, o in edges_b:
        if r == "是" and (s, "不是", o) in edges_a:
            contradictions.append((s, o))

    return {
        "common_nodes": sorted(nodes_a & nodes_b),
        "a_only_nodes": sorted(nodes_a - nodes_b),
        "b_only_nodes": sorted(nodes_b - nodes_a),
        "common_edges": sorted(list(edges_a & edges_b)),
        "a_only_edges": sorted(list(edges_a - edges_b)),
        "b_only_edges": sorted(list(edges_b - edges_a)),
        "contradictions": sorted(list(set(contradictions))),
    }

