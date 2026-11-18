"""node.py - search-tree node shared by every algorithm."""


class Node:
    """One node in the search tree (wraps a state + how we reached it)."""

    def __init__(self, state, parent=None, action=None, path_cost=0.0):
        self.state = state          # a city name (str)
        self.parent = parent        # previous Node (None for the root)
        self.action = action        # the action used to get here (next city)
        self.path_cost = path_cost  # g(n): total road distance so far

    def path(self):
        """Return the list of cities from start to this node."""
        node, cities = self, []
        while node:
            cities.append(node.state)
            node = node.parent
        return cities[::-1]

    # HINT: heapq compares Nodes when priorities tie -> without this you get
    # "TypeError: '<' not supported between Node and Node".
    def __lt__(self, other):
        return self.path_cost < other.path_cost

    def __repr__(self):
        return f"Node({self.state}, g={self.path_cost:.1f})"