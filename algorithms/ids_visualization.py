import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.patches import Patch


def node_colors(nodes, problem, path, explored):
    colors = []

    for city in nodes:
        if city == problem.start:
            colors.append("green")
        elif city == problem.goal:
            colors.append("orange")
        elif city in path:
            colors.append("red")
        elif city in explored:
            colors.append("lightblue")
        else:
            colors.append("lightgray")

    return colors


def visualize_ids(problem, result):
    graph = nx.Graph()

    for city in problem.graph:
        graph.add_node(city)

        for neighbor in problem.graph[city]:
            graph.add_edge(city, neighbor)

    positions = problem.coords
    path = result["path"]
    explored = set(result["explored"])
    path_edges = list(zip(path, path[1:]))

    plt.figure(figsize=(15, 10))

    nx.draw_networkx_edges(graph, positions, edge_color="lightgray", width=1)
    nx.draw_networkx_nodes(
        graph,
        positions,
        node_color=node_colors(graph.nodes, problem, path, explored),
        node_size=450
    )
    nx.draw_networkx_labels(graph, positions, font_size=7)
    nx.draw_networkx_edges(
        graph,
        positions,
        edgelist=path_edges,
        edge_color="red",
        width=3
    )

    legend = [
        Patch(color="green", label="Start"),
        Patch(color="orange", label="Goal"),
        Patch(color="red", label="Final Path"),
        Patch(color="lightblue", label="Explored (last iteration)"),
        Patch(color="lightgray", label="Not Explored")
    ]

    plt.legend(handles=legend, loc="upper right")

    plt.title(
        "IDS City Map Search\n"
        f"Start: {problem.start} | Goal: {problem.goal} | "
        f"Cost: {result['cost']:.1f} | Depth: {result['depth']}"
    )

    plt.axis("off")
    plt.tight_layout()
    plt.show()


def visualize_ids_tree(problem, result):
    parent = {}

    for p, child in result["search_edges"]:
        parent[child] = p

    tree = nx.DiGraph()
    tree.add_node(problem.start)

    for child, p in parent.items():
        tree.add_edge(p, child)

    levels = {problem.start: 0}

    def level_of(city):
        if city not in levels:
            levels[city] = level_of(parent[city]) + 1
        return levels[city]

    for city in tree.nodes:
        level_of(city)

    positions = {}

    for level in set(levels.values()):
        cities = [city for city in tree.nodes if levels[city] == level]

        for i, city in enumerate(cities):
            positions[city] = (level, i - (len(cities) - 1) / 2)

    path = result["path"]
    explored = set(result["explored"])
    path_edges = list(zip(path, path[1:]))

    plt.figure(figsize=(18, 10))

    nx.draw_networkx_edges(
        tree,
        positions,
        edge_color="lightgray",
        arrows=True,
        arrowsize=12
    )
    nx.draw_networkx_edges(
        tree,
        positions,
        edgelist=path_edges,
        edge_color="red",
        width=3,
        arrows=True,
        arrowsize=15
    )
    nx.draw_networkx_nodes(
        tree,
        positions,
        node_color=node_colors(tree.nodes, problem, path, explored),
        node_size=450
    )
    nx.draw_networkx_labels(tree, positions, font_size=7)

    legend = [
        Patch(color="green", label="Start"),
        Patch(color="orange", label="Goal"),
        Patch(color="red", label="Final Path"),
        Patch(color="lightblue", label="Explored"),
        Patch(color="lightgray", label="Generated but Not Explored")
    ]

    plt.legend(handles=legend, loc="upper right")

    plt.title(f"IDS Search Tree (last iteration, depth limit {result['depth']})")

    plt.axis("off")
    plt.tight_layout()
    plt.show()
