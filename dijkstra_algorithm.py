"""
Dijkstra's Algorithm - Data Structures & Algorithms project (Python)

Dijkstra's algorithm finds the shortest path from a source node to all other
nodes in a weighted graph with non-negative edge weights.

Key idea:
  - Use a min-heap (priority queue) to always process the closest unvisited node
  - Maintain distance estimates to all nodes, updating them as we find shorter paths
  - Once a node is visited, its distance is final

Time Complexity: O((V + E) log V) with a min-heap
  - V iterations of heap operations (each O(log V))
  - E edge relaxations (each pushing to heap, O(log V))

Space Complexity: O(V)

Constraints:
  - Only works with non-negative edge weights
  - For negative weights, use Bellman-Ford algorithm instead

Uses:
  - GPS/navigation (finding shortest route)
  - Network routing protocols (OSPF)
  - Game pathfinding
  - Social network analysis
"""

import heapq
from collections import defaultdict


class Graph:
    def __init__(self):
        """Weighted graph using adjacency list representation."""
        self.graph = defaultdict(list)
        self.nodes = set()

    def add_edge(self, u, v, weight):
        """Add a weighted edge from u to v."""
        if weight < 0:
            raise ValueError("Dijkstra's algorithm requires non-negative weights")
        self.graph[u].append((v, weight))
        self.nodes.add(u)
        self.nodes.add(v)

    def dijkstra(self, source):
        """
        Find shortest path from source to all other nodes.
        
        Returns:
          - distances: dict mapping node -> shortest distance from source
          - parents: dict mapping node -> previous node in shortest path
        """
        if source not in self.nodes:
            raise ValueError(f"Source node {source} not in graph")

        # Initialize distances: source is 0, all others are infinity
        distances = {node: float('inf') for node in self.nodes}
        distances[source] = 0

        # Track the previous node in the shortest path (for path reconstruction)
        parents = {node: None for node in self.nodes}

        # Min-heap: (distance, node)
        # Python's heapq is a min-heap by default
        heap = [(0, source)]
        visited = set()

        while heap:
            current_distance, current_node = heapq.heappop(heap)

            # If we've already processed this node, skip it
            if current_node in visited:
                continue

            visited.add(current_node)

            # If this distance is worse than what we've found, skip
            # (this can happen due to duplicate entries in heap)
            if current_distance > distances[current_node]:
                continue

            # Relax edges: check if we can reach neighbors via this node with a shorter path
            for neighbor, weight in self.graph[current_node]:
                new_distance = distances[current_node] + weight

                # Found a shorter path to neighbor
                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    parents[neighbor] = current_node
                    heapq.heappush(heap, (new_distance, neighbor))

        return distances, parents

    def shortest_path(self, source, destination):
        """
        Find the shortest path from source to destination.
        
        Returns:
          - path: list of nodes from source to destination, or None if unreachable
          - distance: total distance, or float('inf') if unreachable
        """
        distances, parents = self.dijkstra(source)

        if distances[destination] == float('inf'):
            return None, float('inf')

        # Reconstruct path by walking backwards from destination
        path = []
        current = destination
        while current is not None:
            path.append(current)
            current = parents[current]

        path.reverse()
        return path, distances[destination]

    def all_shortest_paths(self, source):
        """
        Get shortest distances and paths from source to all reachable nodes.
        
        Returns:
          - dict mapping destination node -> (distance, path)
        """
        distances, parents = self.dijkstra(source)
        result = {}

        for dest in self.nodes:
            if distances[dest] != float('inf'):
                # Reconstruct path
                path = []
                current = dest
                while current is not None:
                    path.append(current)
                    current = parents[current]
                path.reverse()
                result[dest] = (distances[dest], path)

        return result


# ---------------------------------------------------------------------------
# Demonstration / self-test
# ---------------------------------------------------------------------------

def run_demo():
    print("===== Dijkstra's Algorithm Demo =====\n")

    graph = Graph()

    # Build a sample weighted graph
    edges = [
        ('A', 'B', 4),
        ('A', 'C', 2),
        ('B', 'C', 1),
        ('B', 'D', 5),
        ('C', 'D', 8),
        ('C', 'E', 10),
        ('D', 'E', 2),
        ('D', 'F', 6),
        ('E', 'F', 3),
    ]

    print("Graph edges (u, v, weight):")
    for u, v, w in edges:
        graph.add_edge(u, v, w)
        print(f"  {u} -> {v}: {w}")

    print("\n--- Shortest paths from A ---")
    distances, _ = graph.dijkstra('A')
    for node in sorted(distances.keys()):
        dist = distances[node]
        if dist == float('inf'):
            print(f"  A to {node}: unreachable")
        else:
            print(f"  A to {node}: {dist}")

    print("\n--- Detailed paths from A ---")
    all_paths = graph.all_shortest_paths('A')
    for dest in sorted(all_paths.keys()):
        dist, path = all_paths[dest]
        print(f"  A to {dest}: {' -> '.join(path)} (distance: {dist})")

    print("\n--- Single path query: A to F ---")
    path, distance = graph.shortest_path('A', 'F')
    if path:
        print(f"  Path: {' -> '.join(path)}")
        print(f"  Distance: {distance}")
    else:
        print("  No path found")


def run_tests():
    print("\n===== Running correctness tests =====")

    # Test 1: Simple path
    g = Graph()
    edges = [('A', 'B', 1), ('B', 'C', 2), ('A', 'C', 5)]
    for u, v, w in edges:
        g.add_edge(u, v, w)

    distances, _ = g.dijkstra('A')
    assert distances['A'] == 0
    assert distances['B'] == 1
    assert distances['C'] == 3, f"Expected 3, got {distances['C']}"

    # Test 2: Shortest path reconstruction
    path, distance = g.shortest_path('A', 'C')
    assert path == ['A', 'B', 'C']
    assert distance == 3

    # Test 3: Unreachable node
    g2 = Graph()
    g2.add_edge('A', 'B', 1)
    g2.add_edge('C', 'D', 1)  # disconnected component

    path, distance = g2.shortest_path('A', 'D')
    assert path is None
    assert distance == float('inf')

    # Test 4: Single node
    g3 = Graph()
    g3.add_edge('A', 'A', 0)  # self-loop
    distances, _ = g3.dijkstra('A')
    assert distances['A'] == 0

    # Test 5: More complex graph
    g4 = Graph()
    edges = [
        (0, 1, 4),
        (0, 2, 2),
        (1, 2, 1),
        (1, 3, 5),
        (2, 3, 8),
        (2, 4, 10),
        (3, 4, 2),
    ]
    for u, v, w in edges:
        g4.add_edge(u, v, w)

    distances, _ = g4.dijkstra(0)
    assert distances[0] == 0
    assert distances[1] == 4, f"Expected 4 to node 1, got {distances[1]}"
    assert distances[2] == 2
    assert distances[3] == 9, f"Expected 9 to node 3, got {distances[3]}"  # 0->1->3 = 4+5
    assert distances[4] == 11  # 0->1->3->4 = 4+5+2

    # Test 6: All paths from source
    all_paths = g4.all_shortest_paths(0)
    assert len(all_paths) == 5
    assert all_paths[0] == (0, [0])
    assert all_paths[3][0] == 9  # distance 0->1->3
    assert all_paths[3][1] == [0, 1, 3]  # path

    # Test 7: Negative weight should raise error
    g5 = Graph()
    try:
        g5.add_edge('A', 'B', -1)
        assert False, "Should have raised ValueError for negative weight"
    except ValueError:
        pass

    print("All tests passed!")


if __name__ == "__main__":
    run_demo()
    run_tests()
