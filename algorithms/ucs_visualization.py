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


def _final_parents(result):

    parent = {}
    for p, child in result["search_edges"]:
        parent[child] = p
    return parent


def visualize_ucs(problem, result, save_as=None, show=True):
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


    edge_labels = {(a, b): problem.graph[a][b] for a, b in graph.edges}
    nx.draw_networkx_edge_labels(graph, positions, edge_labels=edge_labels,
                                 font_size=5, font_color="gray")

    nx.draw_networkx_nodes(graph, positions, node_size=450,
                           node_color=_node_colors(graph.nodes, problem, path, explored))
    nx.draw_networkx_labels(graph, positions, font_size=7)
    nx.draw_networkx_edges(graph, positions, edgelist=path_edges,
                           edge_color="red", width=3)

    plt.legend(handles=[
        Patch(color="green", label="Start"),
        Patch(color="orange", label="Goal"),
        Patch(color="red", label="Final Path (optimal)"),
        Patch(color="lightblue", label="Explored (expanded)"),
        Patch(color="lightgray", label="Not Explored"),
    ], loc="upper right")
    plt.title("UCS City Map Search\n"
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


def visualize_ucs_tree(problem, result, save_as=None, show=True):
    parent = _final_parents(result)

    tree = nx.DiGraph()
    tree.add_node(problem.start)
    for child, p in parent.items():
        tree.add_edge(p, child)


    g = {problem.start: 0.0}

    def cost_of(city):
        if city not in g:
            g[city] = cost_of(parent[city]) + problem.graph[parent[city]][city]
        return g[city]

    for city in tree.nodes:
        cost_of(city)


    positions = {}
    ordered = sorted(tree.nodes, key=lambda c: g[c])
    rows = 8
    for i, city in enumerate(ordered):
        positions[city] = (g[city], (i % rows) - (rows - 1) / 2)

    path = result["path"]
    explored = set(result["explored"])
    path_edges = list(zip(path, path[1:]))
    labels = {c: f"{c}\ng={g[c]:.0f}" for c in tree.nodes}

    plt.figure(figsize=(20, 10))
    nx.draw_networkx_edges(tree, positions, edge_color="lightgray",
                           arrows=True, arrowsize=12)
    nx.draw_networkx_edges(tree, positions, edgelist=path_edges,
                           edge_color="red", width=3, arrows=True, arrowsize=15)
    nx.draw_networkx_nodes(tree, positions, node_size=650,
                           node_color=_node_colors(tree.nodes, problem, path, explored))
    nx.draw_networkx_labels(tree, positions, labels=labels, font_size=6)

    plt.legend(handles=[
        Patch(color="green", label="Start"),
        Patch(color="orange", label="Goal"),
        Patch(color="red", label="Final Path (optimal)"),
        Patch(color="lightblue", label="Explored (expanded)"),
        Patch(color="lightgray", label="Generated but Not Expanded"),
    ], loc="upper left")
    plt.title("UCS Search Tree - City Map Routing (x-axis = path cost g(n))")
    plt.xlabel("path cost g(n)")

    ax = plt.gca()
    ax.get_yaxis().set_visible(False)
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.tick_params(axis="x", bottom=True, labelbottom=True)
    plt.tight_layout()
    if save_as:
        plt.savefig(save_as, dpi=150)
    if show:
        plt.show()
    plt.close()
