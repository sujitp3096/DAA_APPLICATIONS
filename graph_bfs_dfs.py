"""
Graph with BFS & DFS - Data Structures & Algorithms project (Python)

A Graph can be represented as:
  - Adjacency List (this implementation): node -> list of neighbors
  - Adjacency Matrix: 2D array of weights/edges

BFS (Breadth-First Search):
  - Explores level by level using a queue
  - Finds shortest path in unweighted graphs
  - Time: O(V + E), Space: O(V)

DFS (Depth-First Search):
  - Explores as deep as possible using a stack (or recursion)
  - Useful for topological sort, cycle detection, connected components
  - Time: O(V + E), Space: O(V)

Uses:
  - Finding shortest path in unweighted graphs (BFS)
  - Detecting cycles
  - Finding connected components
  - Topological sorting
  - Strongly connected components (Kosaraju/Tarjan)
"""

from collections import deque, defaultdict


class Graph:
    def __init__(self, directed=False):
        """Initialize a graph. If directed=True, edges go one way only."""
        self.graph = defaultdict(list)
        self.directed = directed
        self.nodes = set()

    def add_edge(self, u, v, weight=1):
        """Add an edge from u to v. If undirected, also add v to u."""
        self.graph[u].append((v, weight))
        self.nodes.add(u)
        self.nodes.add(v)

        if not self.directed:
            self.graph[v].append((u, weight))

    def bfs(self, start):
        """Breadth-First Search from a starting node.
        Returns list of nodes in BFS order."""
        visited = set()
        queue = deque([start])
        visited.add(start)
        result = []

        while queue:
            node = queue.popleft()
            result.append(node)

            for neighbor, _ in self.graph[node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)

        return result

    def dfs(self, start):
        """Depth-First Search from a starting node.
        Returns list of nodes in DFS order (recursive)."""
        visited = set()
        result = []

        def dfs_recursive(node):
            visited.add(node)
            result.append(node)
            for neighbor, _ in self.graph[node]:
                if neighbor not in visited:
                    dfs_recursive(neighbor)

        dfs_recursive(start)
        return result

    def dfs_iterative(self, start):
        """DFS using explicit stack instead of recursion."""
        visited = set()
        stack = [start]
        result = []

        while stack:
            node = stack.pop()
            if node not in visited:
                visited.add(node)
                result.append(node)
                # Push neighbors in reverse order to match recursive DFS traversal
                for neighbor, _ in reversed(self.graph[node]):
                    if neighbor not in visited:
                        stack.append(neighbor)

        return result

    def shortest_path_bfs(self, start, end):
        """Find shortest path from start to end in unweighted graph.
        Returns list of nodes, or None if no path exists."""
        if start not in self.nodes or end not in self.nodes:
            return None

        visited = set()
        queue = deque([(start, [start])])
        visited.add(start)

        while queue:
            node, path = queue.popleft()

            if node == end:
                return path

            for neighbor, _ in self.graph[node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))

        return None

    def has_cycle(self):
        """Detect cycle in an undirected graph using DFS."""
        visited = set()

        def dfs_cycle(node, parent):
            visited.add(node)
            for neighbor, _ in self.graph[node]:
                if neighbor not in visited:
                    if dfs_cycle(neighbor, node):
                        return True
                elif neighbor != parent:
                    return True
            return False

        for node in self.nodes:
            if node not in visited:
                if dfs_cycle(node, None):
                    return True
        return False

    def connected_components(self):
        """Find all connected components in an undirected graph.
        Returns list of sets, each set is one component."""
        visited = set()
        components = []

        def dfs_component(node, component):
            visited.add(node)
            component.add(node)
            for neighbor, _ in self.graph[node]:
                if neighbor not in visited:
                    dfs_component(neighbor, component)

        for node in self.nodes:
            if node not in visited:
                component = set()
                dfs_component(node, component)
                components.append(component)

        return components

    def topological_sort(self):
        """Topological sort for a directed acyclic graph (DAG).
        Returns list of nodes in topological order, or None if cycle exists."""
        if not self.directed:
            return None  # topological sort only makes sense for directed graphs

        # Check for cycles
        visited = set()
        rec_stack = set()

        def has_cycle_dfs(node):
            visited.add(node)
            rec_stack.add(node)

            for neighbor, _ in self.graph[node]:
                if neighbor not in visited:
                    if has_cycle_dfs(neighbor):
                        return True
                elif neighbor in rec_stack:
                    return True

            rec_stack.remove(node)
            return False

        for node in self.nodes:
            if node not in visited:
                if has_cycle_dfs(node):
                    return None  # cycle detected

        # Topological sort using DFS
        visited = set()
        stack = []

        def dfs_topo(node):
            visited.add(node)
            for neighbor, _ in self.graph[node]:
                if neighbor not in visited:
                    dfs_topo(neighbor)
            stack.append(node)

        for node in self.nodes:
            if node not in visited:
                dfs_topo(node)

        return stack[::-1]


# ---------------------------------------------------------------------------
# Demonstration / self-test
# ---------------------------------------------------------------------------

def run_demo():
    print("===== Graph BFS & DFS Demo =====\n")

    # Undirected graph
    graph = Graph(directed=False)
    edges = [(0, 1), (0, 2), (1, 3), (2, 3), (3, 4), (4, 5)]
    for u, v in edges:
        graph.add_edge(u, v)

    print(f"Undirected graph edges: {edges}")
    print(f"BFS from 0:  {graph.bfs(0)}")
    print(f"DFS from 0:  {graph.dfs(0)}")

    print(f"\nShortest path from 0 to 5: {graph.shortest_path_bfs(0, 5)}")
    print(f"Has cycle: {graph.has_cycle()}")

    print(f"\nConnected components: {graph.connected_components()}")

    # Graph with cycle
    print("\n--- Graph with a cycle ---")
    g_cycle = Graph(directed=False)
    for u, v in [(0, 1), (1, 2), (2, 0)]:
        g_cycle.add_edge(u, v)

    print(f"Has cycle: {g_cycle.has_cycle()}")

    # Directed acyclic graph (DAG)
    print("\n--- Directed Acyclic Graph (Topological Sort) ---")
    dag = Graph(directed=True)
    for u, v in [(5, 2), (5, 0), (4, 0), (4, 1), (2, 3), (3, 1)]:
        dag.add_edge(u, v)

    topo = dag.topological_sort()
    print(f"Topological sort: {topo}")


def run_tests():
    print("\n===== Running correctness tests =====")

    # Test 1: BFS and DFS
    g = Graph(directed=False)
    for u, v in [(0, 1), (0, 2), (1, 3), (2, 3), (3, 4)]:
        g.add_edge(u, v)

    bfs_result = g.bfs(0)
    assert bfs_result == [0, 1, 2, 3, 4], f"Expected [0, 1, 2, 3, 4], got {bfs_result}"

    dfs_result = g.dfs(0)
    assert len(dfs_result) == 5 and dfs_result[0] == 0, "DFS should visit all nodes starting from 0"

    # Test 2: Shortest path
    path = g.shortest_path_bfs(0, 4)
    assert path == [0, 1, 3, 4] or path == [0, 2, 3, 4], f"Shortest path should work, got {path}"

    # Test 3: Cycle detection (undirected)
    g_acyclic = Graph(directed=False)
    for u, v in [(0, 1), (1, 2), (2, 3)]:
        g_acyclic.add_edge(u, v)
    assert g_acyclic.has_cycle() is False

    g_cyclic = Graph(directed=False)
    for u, v in [(0, 1), (1, 2), (2, 0)]:
        g_cyclic.add_edge(u, v)
    assert g_cyclic.has_cycle() is True

    # Test 4: Connected components
    g_multi = Graph(directed=False)
    for u, v in [(0, 1), (1, 2), (3, 4)]:
        g_multi.add_edge(u, v)

    components = g_multi.connected_components()
    assert len(components) == 2
    assert {0, 1, 2} in components
    assert {3, 4} in components

    # Test 5: Topological sort
    dag = Graph(directed=True)
    for u, v in [(5, 2), (5, 0), (4, 0), (4, 1), (2, 3), (3, 1)]:
        dag.add_edge(u, v)

    topo = dag.topological_sort()
    assert topo is not None
    # Verify ordering: 5 before 2 and 0, 4 before 0 and 1, 2 before 3, 3 before 1
    assert topo.index(5) < topo.index(2)
    assert topo.index(5) < topo.index(0)
    assert topo.index(4) < topo.index(1)

    # Directed graph with cycle should return None for topological sort
    dag_cyclic = Graph(directed=True)
    for u, v in [(0, 1), (1, 2), (2, 0)]:
        dag_cyclic.add_edge(u, v)

    assert dag_cyclic.topological_sort() is None

    print("All tests passed!")


if __name__ == "__main__":
    run_demo()
    run_tests()
