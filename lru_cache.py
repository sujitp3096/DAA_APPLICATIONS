"""
LRU Cache - Data Structures & Algorithms project (Python)

Implements a Least Recently Used (LRU) cache with O(1) time complexity
for both get() and put() operations.

Core idea:
  - A hash map gives O(1) lookup of a key -> node.
  - A doubly linked list keeps nodes ordered by recency of use:
        head (most recently used) <-> ... <-> tail (least recently used)
  - On get(key): move the accessed node to the head (most recently used).
  - On put(key, value): insert/update at the head; if capacity is exceeded,
    evict the node just before the tail (least recently used).

This mirrors how LeetCode's "LRU Cache" problem (#146) is typically solved,
and is a common interview topic, without relying on collections.OrderedDict.
"""


class Node:
    """A node in the doubly linked list, storing a key/value pair.
    The key is stored on the node too so that when we evict the LRU
    node we know which key to remove from the hash map in O(1)."""

    def __init__(self, key=None, value=None):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None


class LRUCache:
    def __init__(self, capacity):
        if capacity <= 0:
            raise ValueError("Capacity must be a positive integer.")

        self.capacity = capacity
        self.cache = {}  # key -> Node

        # Dummy head/tail sentinel nodes simplify edge cases
        # (no need for null checks when inserting/removing at the ends).
        self.head = Node()
        self.tail = Node()
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node):
        """Unlink a node from the doubly linked list."""
        prev_node = node.prev
        next_node = node.next
        prev_node.next = next_node
        next_node.prev = prev_node

    def _insert_at_head(self, node):
        """Insert a node right after the head sentinel (most recently used position)."""
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node

    def get(self, key):
        if key not in self.cache:
            return -1

        node = self.cache[key]
        self._remove(node)
        self._insert_at_head(node)  # mark as most recently used
        return node.value

    def put(self, key, value):
        if key in self.cache:
            node = self.cache[key]
            node.value = value
            self._remove(node)
            self._insert_at_head(node)
            return

        if len(self.cache) >= self.capacity:
            # Evict the least recently used node (just before tail sentinel)
            lru_node = self.tail.prev
            self._remove(lru_node)
            del self.cache[lru_node.key]

        new_node = Node(key, value)
        self.cache[key] = new_node
        self._insert_at_head(new_node)

    def __len__(self):
        return len(self.cache)

    def keys_in_order(self):
        """Returns keys ordered from most recently used to least recently used.
        Useful for debugging/testing, not part of the core O(1) API."""
        result = []
        current = self.head.next
        while current != self.tail:
            result.append(current.key)
            current = current.next
        return result

    def __repr__(self):
        return f"LRUCache(capacity={self.capacity}, order_mru_to_lru={self.keys_in_order()})"


# ---------------------------------------------------------------------------
# Demonstration / self-test
# ---------------------------------------------------------------------------

def run_demo():
    print("===== LRU Cache Demo =====\n")

    cache = LRUCache(capacity=3)

    print("put(1, 'A')");  cache.put(1, "A")
    print("put(2, 'B')");  cache.put(2, "B")
    print("put(3, 'C')");  cache.put(3, "C")
    print("State:", cache)

    print("\nget(1) ->", cache.get(1), "  (moves key 1 to most recently used)")
    print("State:", cache)

    print("\nput(4, 'D')  -> capacity is 3, so this evicts the LRU key (2)")
    cache.put(4, "D")
    print("State:", cache)

    print("\nget(2) ->", cache.get(2), " (should be -1, was evicted)")

    print("\nput(3, 'C-updated')  -> updates existing key, moves to MRU")
    cache.put(3, "C-updated")
    print("State:", cache)
    print("get(3) ->", cache.get(3))


def run_tests():
    """Basic correctness tests using plain asserts."""
    print("\n===== Running correctness tests =====")

    cache = LRUCache(capacity=2)
    cache.put(1, 1)
    cache.put(2, 2)
    assert cache.get(1) == 1, "Expected get(1) == 1"

    cache.put(3, 3)  # evicts key 2 (least recently used)
    assert cache.get(2) == -1, "Expected key 2 to be evicted"

    cache.put(4, 4)  # evicts key 1 (least recently used)
    assert cache.get(1) == -1, "Expected key 1 to be evicted"
    assert cache.get(3) == 3, "Expected get(3) == 3"
    assert cache.get(4) == 4, "Expected get(4) == 4"

    # Test capacity validation
    try:
        LRUCache(capacity=0)
        assert False, "Expected ValueError for capacity=0"
    except ValueError:
        pass

    # Test updating an existing key
    cache2 = LRUCache(capacity=2)
    cache2.put("x", 100)
    cache2.put("y", 200)
    cache2.put("x", 999)  # update, and x becomes most recently used
    cache2.put("z", 300)  # capacity exceeded, evicts "y" (least recently used)
    assert cache2.get("y") == -1, "Expected 'y' to be evicted"
    assert cache2.get("x") == 999, "Expected 'x' to be updated to 999"
    assert cache2.get("z") == 300

    print("All tests passed!")


if __name__ == "__main__":
    run_demo()
    run_tests()
