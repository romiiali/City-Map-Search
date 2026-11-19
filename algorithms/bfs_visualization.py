import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.patches import Patch


def _node_colors(nodes, problem, path, explored):
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


def visualize_bfs(problem, result, save_as=None, show=True):
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
    nx.draw_networkx_nodes(graph, positions, node_size=450,
                           node_color=_node_colors(graph.nodes, problem, path, explored))
    nx.draw_networkx_labels(graph, positions, font_size=7)
    nx.draw_networkx_edges(graph, positions, edgelist=path_edges,
                           edge_color="red", width=3)

    plt.legend(handles=[
        Patch(color="green", label="Start"),
        Patch(color="orange", label="Goal"),
        Patch(color="red", label="Final Path"),
        Patch(color="lightblue", label="Explored (expanded)"),
        Patch(color="lightgray", label="Not Explored"),
    ], loc="upper right")
    plt.title("BFS City Map Search\n"
              f"Start: {problem.start} | Goal: {problem.goal} | "
              f"Cost: {result['cost']:.1f} | Hops: {len(path) - 1} | "
              f"Expanded: {result['nodes_expanded']}")
    plt.axis("off")
    plt.tight_layout()
    if save_as:
        plt.savefig(save_as, dpi=150)
    if show:
        plt.show()
    plt.close()


def visualize_bfs_tree(problem, result, save_as=None, show=True):
    tree = nx.DiGraph()
    tree.add_node(problem.start)
    for parent, child in result["search_edges"]:
        tree.add_edge(parent, child)

    path = result["path"]
    explored = set(result["explored"])
    path_edges = list(zip(path, path[1:]))

    levels = {problem.start: 0}
    for parent, child in result["search_edges"]:
        levels[child] = levels[parent] + 1

    by_level = {}
    for city in tree.nodes:
        by_level.setdefault(levels[city], []).append(city)

    positions = {}
    for level, cities in by_level.items():
        for i, city in enumerate(cities):
            positions[city] = (level, i - (len(cities) - 1) / 2)

    plt.figure(figsize=(18, 10))
    nx.draw_networkx_edges(tree, positions, edge_color="lightgray",
                           arrows=True, arrowsize=12)
    nx.draw_networkx_edges(tree, positions, edgelist=path_edges,
                           edge_color="red", width=3, arrows=True, arrowsize=15)
    nx.draw_networkx_nodes(tree, positions, node_size=450,
                           node_color=_node_colors(tree.nodes, problem, path, explored))
    nx.draw_networkx_labels(tree, positions, font_size=7)

    plt.legend(handles=[
        Patch(color="green", label="Start"),
        Patch(color="orange", label="Goal"),
        Patch(color="red", label="Final Path"),
        Patch(color="lightblue", label="Explored (expanded)"),
        Patch(color="lightgray", label="Generated but Not Expanded"),
    ], loc="upper right")
    plt.title("BFS Search Tree - City Map Routing (x-axis = depth)")
    plt.axis("off")
    plt.tight_layout()
    if save_as:
        plt.savefig(save_as, dpi=150)
    if show:
        plt.show()
    plt.close()
