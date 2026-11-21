
import heapq
import itertools
import time

from node import Node


def ucs(problem):
    start_time = time.perf_counter()

    start = Node(problem.initial_state())

    counter = itertools.count()
    frontier = [(start.path_cost, next(counter), start)]


    best_cost = {start.state: 0.0}
    expanded = set()

    nodes_generated = 1
    nodes_expanded = 0
    max_frontier = 1

    explored = []
    search_edges = []

    while frontier:
        g, _, current = heapq.heappop(frontier)

        if current.state in expanded:
            continue


        if problem.is_goal(current.state):
            return _result(current, nodes_generated, nodes_expanded,
                           max_frontier, start_time, explored, search_edges)

        expanded.add(current.state)
        explored.append(current.state)
        nodes_expanded += 1

        for action, next_state, cost in problem.successors(current.state):
            if next_state in expanded:
                continue

            new_g = g + cost

            if new_g < best_cost.get(next_state, float("inf")):
                best_cost[next_state] = new_g
                child = Node(next_state, current, action, new_g)
                heapq.heappush(frontier, (new_g, next(counter), child))
                search_edges.append((current.state, next_state))
                nodes_generated += 1

        max_frontier = max(max_frontier, len(frontier))


    return {
        "path": [],
        "cost": float("inf"),
        "nodes_generated": nodes_generated,
        "nodes_expanded": nodes_expanded,
        "max_frontier": max_frontier,
        "time": time.perf_counter() - start_time,
        "explored": explored,
        "search_edges": search_edges,
    }


def _result(goal_node, generated, expanded, max_frontier, start_time,
            explored, search_edges):
    """Same output format as bfs.py / dfs.py so main.py can compare them."""
    return {
        "path": goal_node.path(),
        "cost": goal_node.path_cost,
        "nodes_generated": generated,
        "nodes_expanded": expanded,
        "max_frontier": max_frontier,
        "time": time.perf_counter() - start_time,
        "explored": explored,
        "search_edges": search_edges,
    }
