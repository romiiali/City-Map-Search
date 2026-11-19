import time
from collections import deque
from node import Node


def bfs(problem):
    start_time = time.perf_counter()

    start = Node(problem.initial_state())
    nodes_generated = 1
    nodes_expanded = 0
    max_frontier = 1

    explored = []
    search_edges = []

    if problem.is_goal(start.state):
        return _result(start, nodes_generated, nodes_expanded, max_frontier,
                       start_time, explored, search_edges)

    frontier = deque([start])
    reached = {start.state}

    while frontier:
        current = frontier.popleft()
        explored.append(current.state)
        nodes_expanded += 1

        for action, next_state, cost in problem.successors(current.state):
            if next_state in reached:
                continue

            child = Node(next_state, current, action, current.path_cost + cost)
            reached.add(next_state)
            search_edges.append((current.state, next_state))
            nodes_generated += 1

            if problem.is_goal(next_state):
                max_frontier = max(max_frontier, len(frontier) + 1)
                return _result(child, nodes_generated, nodes_expanded,
                               max_frontier, start_time, explored, search_edges)

            frontier.append(child)

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
