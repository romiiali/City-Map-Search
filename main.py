from problem import CityMapProblem
from algorithms.bfs import bfs
from algorithms.dfs import dfs
from algorithms.ucs import ucs
from algorithms.ids import ids
# from algorithms.astar import astar

# 7000 cities -> 7000 states (project needs 1K-10K states).
print("Building map (takes about a minute)...")
problem = CityMapProblem(num_cities=7000, seed=42)
print("Problem ready:", problem.start, "->", problem.goal)
print("Reachable states:", problem.count_states())
print()


algorithms = {
    "BFS": bfs,
    "DFS": dfs,
    "UCS": ucs,
    "IDS": ids,
}

results = {name: run(problem) for name, run in algorithms.items()}


header = (f"{'Algorithm':<10}{'Cost':>10}{'Hops':>7}{'Generated':>12}"
          f"{'Expanded':>11}{'Max frontier':>15}{'Time (s)':>11}")
print(header)
print("-" * len(header))
for name, r in results.items():
    print(f"{name:<10}{r['cost']:>10.1f}{len(r['path']) - 1:>7}"
          f"{r['nodes_generated']:>12}{r['nodes_expanded']:>11}"
          f"{r['max_frontier']:>15}{r['time']:>11.4f}")

# ----- sanity check: reported cost must equal the real cost of the path -----
for name, r in results.items():
    assert abs(problem.path_cost(r["path"]) - r["cost"]) < 1e-6, name

best = min(results, key=lambda n: results[n]["cost"])
print(f"\nCheapest path found by: {best} (cost {results[best]['cost']:.1f})")
