import time
from node import Node

def dfs(problem):
    start_time = time.perf_counter()

    start = Node(problem.initial_state())
    stack = [start]
    visited = set()
    added = {start.state}

    nodes_generated = 1
    nodes_expanded = 0
    max_frontier = 1

    explored = []
    search_edges = []

    while stack:
        current = stack.pop()

        if current.state in visited:
            continue

        visited.add(current.state)
        explored.append(current.state)
        nodes_expanded += 1

        if problem.is_goal(current.state):
            time_taken = time.perf_counter() - start_time

            return {
                "path": current.path(),
                "cost": current.path_cost,
                "nodes_generated": nodes_generated,
                "nodes_expanded": nodes_expanded,
                "max_frontier": max_frontier,
                "time": time_taken,
                "explored": explored,
                "search_edges": search_edges
            }

        for action, next_state, cost in reversed(
            list(problem.successors(current.state))
        ):
            if next_state not in added:
                child = Node(
                    next_state,
                    current,
                    action,
                    current.path_cost + cost
                )

                stack.append(child)
                added.add(next_state)
                search_edges.append((current.state, next_state))
                nodes_generated += 1

        max_frontier = max(max_frontier, len(stack))

    time_taken = time.perf_counter() - start_time

    return {
        "path": [],
        "cost": float("inf"),
        "nodes_generated": nodes_generated,
        "nodes_expanded": nodes_expanded,
        "max_frontier": max_frontier,
        "time": time_taken,
        "explored": explored,
        "search_edges": search_edges
    }