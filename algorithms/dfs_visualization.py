import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.patches import Patch


def visualize_dfs(problem, result):
    graph = nx.Graph()

    for city in problem.graph:
        graph.add_node(city)

        for neighbor in problem.graph[city]:
            graph.add_edge(city, neighbor)

    positions = problem.coords

    path = result["path"]
    explored = result["explored"]

    colors = []

    for city in graph.nodes:
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

    path_edges = []

    for i in range(len(path) - 1):
        path_edges.append((path[i], path[i + 1]))

    plt.figure(figsize=(15, 10))

    nx.draw_networkx_edges(
        graph,
        positions,
        edge_color="lightgray",
        width=1
    )

    nx.draw_networkx_nodes(
        graph,
        positions,
        node_color=colors,
        node_size=450
    )

    nx.draw_networkx_labels(
        graph,
        positions,
        font_size=7
    )

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
        Patch(color="lightblue", label="Explored"),
        Patch(color="lightgray", label="Not Explored")
    ]

    plt.legend(handles=legend, loc="upper right")

    plt.title(
        "DFS City Map Search\n"
        f"Start: {problem.start} | Goal: {problem.goal} | "
        f"Cost: {result['cost']:.1f}"
    )

    plt.axis("off")
    plt.tight_layout()
    plt.show()


def visualize_dfs_tree(problem, result):
    tree = nx.DiGraph()

    for parent, child in result["search_edges"]:
        tree.add_edge(parent, child)

    tree.add_node(problem.start)

    path = result["path"]
    explored = result["explored"]

    path_edges = []

    for i in range(len(path) - 1):
        path_edges.append((path[i], path[i + 1]))

    levels = {problem.start: 0}

    for parent, child in result["search_edges"]:
        levels[child] = levels[parent] + 1

    positions = {}

    for level in set(levels.values()):
        cities = []

        for city in tree.nodes:
            if levels[city] == level:
                cities.append(city)

        for i, city in enumerate(cities):
            positions[city] = (
                level,
                i - (len(cities) - 1) / 2
            )

    colors = []

    for city in tree.nodes:
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
        node_color=colors,
        node_size=450
    )

    nx.draw_networkx_labels(
        tree,
        positions,
        font_size=7
    )

    legend = [
        Patch(color="green", label="Start"),
        Patch(color="orange", label="Goal"),
        Patch(color="red", label="Final Path"),
        Patch(color="lightblue", label="Explored"),
        Patch(color="lightgray", label="Generated but Not Explored")
    ]

    plt.legend(handles=legend, loc="upper right")

    plt.title("DFS Search Tree - City Map Routing")

    plt.axis("off")
    plt.tight_layout()
    plt.show()