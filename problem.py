"""
problem.py - the City Map Routing problem space.

Every algorithm file (bfs.py, astar.py, ...) imports ONLY this class, so the
algorithms never touch the raw map data directly.

    State  : the city we are currently in (str)
    Action : travel along a road to a neighbouring city (action = that city)
    Cost   : road distance of the edge
"""
import math
import random


class CityMapProblem:
    def __init__(self, num_cities=60, seed=42, start=None, goal=None):
        self.coords = {}   # city -> (x, y)  used by heuristics + visualisation
        self.graph = {}    # city -> {neighbour: road_distance}
        self._generate_map(num_cities, seed)

        cities = sorted(self.graph)
        # HINT: pick far-apart start/goal so the search has real work to do.
        self.start = start or self._farthest_pair()[0]
        self.goal = goal or self._farthest_pair()[1]
        assert self.start in self.graph and self.goal in self.graph

        # Precomputed constants for heuristic h2
        self._min_edge = min(c for nb in self.graph.values() for c in nb.values())
        self._max_edge_euclid = max(
            self._euclid(a, b) for a in self.graph for b in self.graph[a]
        )

    # ------------------------------------------------------------------
    # Map construction
    # ------------------------------------------------------------------
    def _generate_map(self, n, seed):
        """Random connected road map (seeded -> whole team gets the SAME map).

        HINT: To use the real Romania map instead, delete this method and fill
        self.coords / self.graph by hand (or load them from a dict/JSON).
        Keep edges symmetric (add A->B and B->A).
        """
        rng = random.Random(seed)
        names = [f"City{i:02d}" for i in range(n)]
        for name in names:
            self.coords[name] = (rng.uniform(0, 100), rng.uniform(0, 100))
            self.graph[name] = {}

        # Connect each city to its 3 nearest neighbours.
        for a in names:
            nearest = sorted((b for b in names if b != a),
                             key=lambda b: self._euclid(a, b))[:3]
            for b in nearest:
                self._add_road(a, b)

        # Guarantee connectivity: link separate components together.
        comps = self._components()
        while len(comps) > 1:
            a, b = min(((x, y) for x in comps[0] for y in comps[1]),
                       key=lambda p: self._euclid(*p))
            self._add_road(a, b)
            comps = self._components()

    def _add_road(self, a, b):
        # Road length >= straight-line distance, so the straight-line
        # heuristic stays ADMISSIBLE. (Keep this property if you edit it!)
        d = round(self._euclid(a, b) * 1.1, 1)
        self.graph[a][b] = d
        self.graph[b][a] = d

    def _components(self):
        seen, comps = set(), []
        for s in self.graph:
            if s in seen:
                continue
            stack, comp = [s], set()
            while stack:
                c = stack.pop()
                if c in comp:
                    continue
                comp.add(c)
                stack.extend(self.graph[c])
            seen |= comp
            comps.append(comp)
        return comps

    def _farthest_pair(self):
        # Cheap approximation: the 2 cities with max straight-line distance.
        return max(((a, b) for a in self.graph for b in self.graph if a < b),
                   key=lambda p: self._euclid(*p))

    def _euclid(self, a, b):
        (x1, y1), (x2, y2) = self.coords[a], self.coords[b]
        return math.hypot(x1 - x2, y1 - y2)

    # ------------------------------------------------------------------
    # Standard search-problem interface  (what the algorithms call)
    # ------------------------------------------------------------------
    def initial_state(self):
        return self.start

    def is_goal(self, state):
        return state == self.goal

    def actions(self, state):
        """Legal actions = neighbouring cities (sorted -> deterministic runs)."""
        return sorted(self.graph[state])

    def result(self, state, action):
        """Transition model: travelling to city `action` puts us in `action`."""
        return action

    def step_cost(self, state, action):
        return self.graph[state][action]

    def successors(self, state):
        """Convenience: yields (action, next_state, step_cost)."""
        for a in self.actions(state):
            yield a, self.result(state, a), self.step_cost(state, a)

    # ------------------------------------------------------------------
    # Heuristics  (both ADMISSIBLE + CONSISTENT -> A* is optimal)
    # ------------------------------------------------------------------
    def h1(self, state):
        """Straight-line (Euclidean) distance to the goal."""
        return self._euclid(state, self.goal)

    def h2(self, state):
        """Lower bound = (min #hops needed) x (cheapest edge in the map).
        Each hop covers at most `max_edge_euclid`, so we need at least
        ceil(SLD / max_edge_euclid) hops.
        HINT: weaker than h1 -> expect A* to expand MORE nodes with h2.
        That comparison is a great point for your report."""
        hops = math.ceil(self._euclid(state, self.goal) / self._max_edge_euclid)
        return hops * self._min_edge

    # ------------------------------------------------------------------
    # Report helpers
    # ------------------------------------------------------------------
    def path_cost(self, path):
        """Total cost of a list of cities (use to verify every algorithm)."""
        return sum(self.graph[a][b] for a, b in zip(path, path[1:]))

    def count_states(self):
        """Reachable-state count for the 'size estimate' in the report."""
        seen, frontier = {self.start}, [self.start]
        while frontier:
            s = frontier.pop()
            for _, nxt, _ in self.successors(s):
                if nxt not in seen:
                    seen.add(nxt)
                    frontier.append(nxt)
        return len(seen)


if __name__ == "__main__":
    p = CityMapProblem()
    print("Start:", p.start, "| Goal:", p.goal)
    print("Reachable states:", p.count_states())
    print("Roads:", sum(len(v) for v in p.graph.values()) // 2)
    print("h1(start) =", round(p.h1(p.start), 1), "| h2(start) =", round(p.h2(p.start), 1))