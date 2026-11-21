import time
from node import Node


def depth_limited_search(problem, limit, stats):
    start = Node(problem.initial_state())
    stack = [(start, 0)]
    best_depth = {start.state: 0}

    explored = []
    search_edges = []
    cutoff = False

    while stack:
        current, depth = stack.pop()

        if depth > best_depth[current.state]:
            continue

        explored.append(current.state)
        stats["expanded"] += 1

        if problem.is_goal(current.state):
            return current, explored, search_edges, False

        if depth == limit:
            cutoff = True
            continue

        for action, next_state, cost in reversed(
            list(problem.successors(current.state))
        ):
            if depth + 1 < best_depth.get(next_state, float("inf")):
                best_depth[next_state] = depth + 1
                child = Node(
                    next_state,
                    current,
                    action,
                    current.path_cost + cost
                )

                stack.append((child, depth + 1))
                search_edges.append((current.state, next_state))
                stats["generated"] += 1

        stats["max_frontier"] = max(stats["max_frontier"], len(stack))

    return None, explored, search_edges, cutoff


def ids(problem, max_depth=10000):
    start_time = time.perf_counter()

    stats = {"generated": 0, "expanded": 0, "max_frontier": 1}
    explored = []
    search_edges = []

    for limit in range(max_depth + 1):
        stats["generated"] += 1
        goal, explored, search_edges, cutoff = depth_limited_search(
            problem, limit, stats
        )

        if goal is not None:
            return {
                "path": goal.path(),
                "cost": goal.path_cost,
                "nodes_generated": stats["generated"],
                "nodes_expanded": stats["expanded"],
                "max_frontier": stats["max_frontier"],
                "time": time.perf_counter() - start_time,
                "explored": explored,
                "search_edges": search_edges,
                "depth": limit
            }

        if not cutoff:
            break

    return {
        "path": [],
        "cost": float("inf"),
        "nodes_generated": stats["generated"],
        "nodes_expanded": stats["expanded"],
        "max_frontier": stats["max_frontier"],
        "time": time.perf_counter() - start_time,
        "explored": explored,
        "search_edges": search_edges,
        "depth": None
    }
