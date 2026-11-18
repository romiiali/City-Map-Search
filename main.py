"""main.py - runs every algorithm on the SAME problem and prints a comparison."""
from problem import CityMapProblem
# from algorithms.bfs import bfs
# from algorithms.astar import astar

problem = CityMapProblem(num_cities=60, seed=42)

# Each algorithm should return: (path, cost, nodes_expanded, time_taken)
# results = {"BFS": bfs(problem), "A* h1": astar(problem, problem.h1)}
# for name, (path, cost, expanded, t) in results.items():
#     print(f"{name:8} cost={cost:.1f} expanded={expanded} time={t:.4f}s")
print("Problem ready:", problem.start, "->", problem.goal)