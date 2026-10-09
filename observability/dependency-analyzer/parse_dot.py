
from pathlib import Path

import pydot


def parse_dot(path: Path) -> dict:
    graphs = pydot.graph_from_dot_file(str(path))

    if not graphs:
        raise ValueError(f"No DOT graph found in {path}")

    graph = graphs[0]
    nodes = {}
    edges = []

    for node in graph.get_nodes():
        node_id = node.get_name().strip('"')

        # Graphviz-Metadaten wie graph, node und edge
        # sind keine echten Module.
        if node_id in {"graph", "node", "edge", "\\n"}:
            continue

        nodes[node_id] = {
            "id": node_id,
            "title": node_id,
        }

    for edge in graph.get_edges():
        source = edge.get_source().strip('"')
        target = edge.get_destination().strip('"')

        nodes.setdefault(source, {"id": source, "title": source})
        nodes.setdefault(target, {"id": target, "title": target})

        edges.append({
            "id": f"{source}->{target}",
            "source": source,
            "target": target,
        })

    return {
        "nodes": list(nodes.values()),
        "edges": edges,
    }