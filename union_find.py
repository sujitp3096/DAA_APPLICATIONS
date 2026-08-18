"""
Union-Find (Disjoint Set Union / DSU) - Data Structures & Algorithms project (Python)

A Union-Find data structure efficiently handles two core operations:
  union(x, y)  - Merge the set containing x with the set containing y
  find(x)      - Return the representative (root) of the set containing x

With path compression and union by rank, both operations run in nearly O(1)
amortized time: O(α(n)) where α is the inverse Ackermann function (< 5 for
all practical n).

Uses:
  - Detect cycles in an undirected graph
  - Find connected components
  - Kruskal's minimum spanning tree algorithm
  - Checking if two nodes are in the same connected component
"""


class UnionFind:
    def __init__(self, n):
        """Initialize a Union-Find with n elements (0 to n-1).
        Each element starts in its own set."""
        self.parent = list(range(n))
        self.rank = [0] * n
        self.size = [1] * n  # size of each component, useful for queries

    def find(self, x):
        """Find the representative (root) of the set containing x.
        With path compression: all nodes in the path now point directly to root."""
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # path compression
        return self.parent[x]

    def union(self, x, y):
        """Merge the set containing x with the set containing y.
        Uses union by rank to keep trees shallow.
        Returns True if they were in different sets and got merged, False if already same set."""
        root_x = self.find(x)
        root_y = self.find(y)

        if root_x == root_y:
            return False  # already in the same set

        # Union by rank: attach smaller tree under larger tree
        if self.rank[root_x] < self.rank[root_y]:
            self.parent[root_x] = root_y
            self.size[root_y] += self.size[root_x]
        elif self.rank[root_x] > self.rank[root_y]:
            self.parent[root_y] = root_x
            self.size[root_x] += self.size[root_y]
        else:
            # ranks are equal; arbitrarily pick root_x as parent and increment its rank
            self.parent[root_y] = root_x
            self.size[root_x] += self.size[root_y]
            self.rank[root_x] += 1

        return True

    def connected(self, x, y):
        """Check if x and y are in the same connected component."""
        return self.find(x) == self.find(y)

    def component_size(self, x):
        """Return the size of the component containing x."""
        return self.size[self.find(x)]

    def num_components(self):
        """Return the number of distinct connected components."""
        return len(set(self.find(i) for i in range(len(self.parent))))


# ---------------------------------------------------------------------------
# Example: Detect Cycle in Undirected Graph
# ---------------------------------------------------------------------------

def has_cycle(n, edges):
    """
    Given n vertices (0 to n-1) and a list of edges,
    return True if the graph has a cycle, False otherwise.

    Algorithm: For each edge (u, v), if u and v are already connected,
    there's a cycle. Otherwise, union them.
    """
    uf = UnionFind(n)

    for u, v in edges:
        if uf.connected(u, v):
            return True  # u and v are already connected; adding this edge creates a cycle
        uf.union(u, v)

    return False


# ---------------------------------------------------------------------------
# Example: Find Connected Components
# ---------------------------------------------------------------------------

def find_components(n, edges):
    """
    Given n vertices and a list of edges, return a list of sets,
    where each set contains the vertices in one connected component.
    """
    uf = UnionFind(n)

    for u, v in edges:
        uf.union(u, v)

    components = {}
    for i in range(n):
        root = uf.find(i)
        if root not in components:
            components[root] = set()
        components[root].add(i)

    return list(components.values())


# ---------------------------------------------------------------------------
# Demonstration / self-test
# ---------------------------------------------------------------------------

def run_demo():
    print("===== Union-Find Demo =====\n")

    uf = UnionFind(6)

    print("Initial state: 6 separate elements (0-5)")
    print(f"Number of components: {uf.num_components()}")
    print(f"Component size of 0: {uf.component_size(0)}\n")

    print("union(0, 1)")
    uf.union(0, 1)
    print(f"0 and 1 connected? {uf.connected(0, 1)}")
    print(f"Number of components: {uf.num_components()}\n")

    print("union(1, 2)")
    uf.union(1, 2)
    print(f"0 and 2 connected? {uf.connected(0, 2)}")
    print(f"Component size of 0: {uf.component_size(0)}\n")

    print("union(3, 4), union(4, 5)")
    uf.union(3, 4)
    uf.union(4, 5)
    print(f"3 and 5 connected? {uf.connected(3, 5)}")
    print(f"0 and 3 connected? {uf.connected(0, 3)}")
    print(f"Number of components: {uf.num_components()}\n")

    print("union(2, 3)  (merges the two components)")
    uf.union(2, 3)
    print(f"0 and 5 connected? {uf.connected(0, 5)}")
    print(f"Number of components: {uf.num_components()}\n")


def run_tests():
    print("\n===== Running correctness tests =====")

    # Test 1: Basic union and find
    uf = UnionFind(5)
    uf.union(0, 1)
    uf.union(1, 2)
    assert uf.connected(0, 2) is True
    assert uf.connected(0, 3) is False
    assert uf.component_size(0) == 3
    assert uf.component_size(3) == 1

    # Test 2: Cycle detection
    edges_with_cycle = [(0, 1), (1, 2), (2, 0)]
    assert has_cycle(3, edges_with_cycle) is True

    edges_no_cycle = [(0, 1), (1, 2), (2, 3)]
    assert has_cycle(4, edges_no_cycle) is False

    # Test 3: Connected components
    edges = [(0, 1), (1, 2), (3, 4), (5, 6), (6, 7)]
    components = find_components(8, edges)
    assert len(components) == 3  # {0,1,2}, {3,4}, {5,6,7}
    assert {0, 1, 2} in components
    assert {3, 4} in components
    assert {5, 6, 7} in components

    # Test 4: Union by rank keeps trees shallow (harder to test directly,
    # but we can at least verify it doesn't break)
    uf_large = UnionFind(100)
    for i in range(99):
        uf_large.union(i, i + 1)
    assert uf_large.num_components() == 1
    assert uf_large.component_size(0) == 100

    # Test 5: Multiple unions of same pair (should return False after first)
    uf = UnionFind(3)
    assert uf.union(0, 1) is True
    assert uf.union(0, 1) is False  # already connected
    assert uf.union(1, 0) is False  # order doesn't matter

    print("All tests passed!")


if __name__ == "__main__":
    run_demo()
    run_tests()
  
