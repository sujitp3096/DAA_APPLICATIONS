"""
Min-Heap (Priority Queue) - Data Structures & Algorithms project (Python)

A Min-Heap is a complete binary tree where every parent is smaller than
its children. It's the standard data structure for priority queues.

Operations (all O(log n)):
  push(value)      - Add a value to the heap
  pop()            - Remove and return the minimum value
  peek()           - Return (but don't remove) the minimum value

Uses:
  - Dijkstra's shortest path algorithm
  - Heap sort
  - Load balancing (process shortest task first)
  - Median finder (combine min-heap and max-heap)

This implementation is built from scratch without using Python's heapq,
to demonstrate the underlying mechanics: array-based tree, sift-up/down.
"""


class MinHeap:
    def __init__(self):
        """Initialize an empty min-heap using a dynamic array."""
        self.heap = []

    def push(self, value):
        """Insert a value into the heap in O(log n) time.
        Add to end, then sift up to restore heap property."""
        self.heap.append(value)
        self._sift_up(len(self.heap) - 1)

    def pop(self):
        """Remove and return the minimum value in O(log n) time.
        If heap is empty, raise IndexError."""
        if not self.heap:
            raise IndexError("pop from empty heap")

        min_val = self.heap[0]

        # Move last element to root
        last = self.heap.pop()
        if self.heap:  # if there are still elements
            self.heap[0] = last
            self._sift_down(0)

        return min_val

    def peek(self):
        """Return the minimum value without removing it. O(1) time."""
        if not self.heap:
            raise IndexError("peek from empty heap")
        return self.heap[0]

    def __len__(self):
        return len(self.heap)

    def __bool__(self):
        return len(self.heap) > 0

    def _sift_up(self, index):
        """Move a value up the tree until heap property is restored.
        Used after insertion at the end."""
        while index > 0:
            parent_index = (index - 1) // 2
            if self.heap[index] < self.heap[parent_index]:
                self.heap[index], self.heap[parent_index] = self.heap[parent_index], self.heap[index]
                index = parent_index
            else:
                break

    def _sift_down(self, index):
        """Move a value down the tree until heap property is restored.
        Used after removing the root and moving last element to root."""
        while True:
            smallest = index
            left_child_index = 2 * index + 1
            right_child_index = 2 * index + 2

            if (left_child_index < len(self.heap) and
                    self.heap[left_child_index] < self.heap[smallest]):
                smallest = left_child_index

            if (right_child_index < len(self.heap) and
                    self.heap[right_child_index] < self.heap[smallest]):
                smallest = right_child_index

            if smallest != index:
                self.heap[index], self.heap[smallest] = self.heap[smallest], self.heap[index]
                index = smallest
            else:
                break

    def __repr__(self):
        return f"MinHeap({self.heap})"


# ---------------------------------------------------------------------------
# Example: Heap Sort
# ---------------------------------------------------------------------------

def heap_sort(arr):
    """Sort an array using a min-heap. O(n log n) time."""
    heap = MinHeap()
    for val in arr:
        heap.push(val)

    sorted_arr = []
    while heap:
        sorted_arr.append(heap.pop())

    return sorted_arr


# ---------------------------------------------------------------------------
# Example: Find K Smallest Elements
# ---------------------------------------------------------------------------

def k_smallest(arr, k):
    """Return the k smallest elements from arr in sorted order."""
    if k <= 0 or k > len(arr):
        return []

    heap = MinHeap()
    for val in arr:
        heap.push(val)

    result = []
    for _ in range(k):
        result.append(heap.pop())

    return result


# ---------------------------------------------------------------------------
# Demonstration / self-test
# ---------------------------------------------------------------------------

def run_demo():
    print("===== Min-Heap Demo =====\n")

    heap = MinHeap()

    values = [5, 3, 7, 1, 9, 2, 6]
    print(f"Pushing values: {values}")
    for v in values:
        heap.push(v)

    print(f"Heap structure (array): {heap.heap}\n")

    print(f"peek() = {heap.peek()} (should be minimum)")
    print(f"pop()  = {heap.pop()}")
    print(f"Heap after one pop: {heap.heap}\n")

    print("Popping all remaining elements:")
    while heap:
        print(f"  {heap.pop()}", end="")
    print(" (should be sorted)\n")

    print("Heap sort example:")
    arr = [64, 34, 25, 12, 22, 11, 90]
    sorted_arr = heap_sort(arr)
    print(f"  Original: {arr}")
    print(f"  Sorted:   {sorted_arr}\n")

    print("Find 3 smallest elements:")
    arr = [7, 1, 5, 8, 2, 9, 3]
    k = 3
    smallest = k_smallest(arr, k)
    print(f"  Array: {arr}")
    print(f"  {k} smallest: {smallest}\n")


def run_tests():
    print("\n===== Running correctness tests =====")

    # Test 1: Basic push/pop
    heap = MinHeap()
    heap.push(5)
    heap.push(3)
    heap.push(7)
    assert heap.pop() == 3
    assert heap.pop() == 5
    assert heap.pop() == 7
    assert len(heap) == 0

    # Test 2: Peek doesn't remove
    heap = MinHeap()
    heap.push(10)
    heap.push(20)
    assert heap.peek() == 10
    assert heap.peek() == 10  # still there
    assert len(heap) == 2

    # Test 3: Many insertions maintain heap property
    heap = MinHeap()
    values = [15, 10, 20, 8, 2, 30, 5, 12, 25, 1]
    for v in values:
        heap.push(v)

    popped = []
    while heap:
        popped.append(heap.pop())
    assert popped == sorted(values), f"Expected {sorted(values)}, got {popped}"

    # Test 4: Heap sort
    arr = [64, 34, 25, 12, 22, 11, 90]
    assert heap_sort(arr) == sorted(arr)

    # Test 5: K smallest
    arr = [7, 1, 5, 8, 2, 9, 3]
    assert k_smallest(arr, 3) == [1, 2, 3]
    assert k_smallest(arr, 1) == [1]
    assert k_smallest(arr, 0) == []

    # Test 6: Error handling
    heap = MinHeap()
    try:
        heap.pop()
        assert False, "Should have raised IndexError"
    except IndexError:
        pass

    try:
        heap.peek()
        assert False, "Should have raised IndexError"
    except IndexError:
        pass

    # Test 7: Single element
    heap = MinHeap()
    heap.push(42)
    assert heap.peek() == 42
    assert heap.pop() == 42
    assert len(heap) == 0

    # Test 8: Duplicates
    heap = MinHeap()
    for v in [5, 3, 5, 1, 5]:
        heap.push(v)
    assert heap.pop() == 1
    assert heap.pop() == 3
    assert heap.pop() == 5
    assert heap.pop() == 5
    assert heap.pop() == 5

    print("All tests passed!")


if __name__ == "__main__":
    run_demo()
    run_tests()
