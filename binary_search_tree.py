"""
Binary Search Tree (BST) - Data Structures & Algorithms project (Python)

A BST is a binary tree where for every node:
  - All values in the left subtree are smaller
  - All values in the right subtree are larger
  - No duplicates (this implementation rejects them on insert)

Operations:
  insert(value)        - O(log n) average, O(n) worst case (unbalanced tree)
  search(value)        - O(log n) average, O(n) worst case
  delete(value)        - O(log n) average, O(n) worst case
  inorder_traversal()  - O(n), yields values in sorted order
  preorder_traversal() - O(n), root first
  postorder_traversal()- O(n), root last
  min_value()          - O(log n) on average, find smallest
  max_value()          - O(log n) on average, find largest
  is_bst()             - O(n), verify BST property holds
  is_balanced()        - O(n), check if height-balanced (AVL-style)
  height()             - O(n), return tree height

Uses:
  - Dictionary/map implementations
  - Sorted data storage
  - Range queries
  - Self-balancing trees (AVL, Red-Black) build on BST
"""


class TreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


class BinarySearchTree:
    def __init__(self):
        self.root = None

    def insert(self, value):
        """Insert a value into the BST. Returns True if inserted, False if duplicate."""
        if self.root is None:
            self.root = TreeNode(value)
            return True
        return self._insert_recursive(self.root, value)

    def _insert_recursive(self, node, value):
        if value == node.value:
            return False  # duplicate, reject it

        if value < node.value:
            if node.left is None:
                node.left = TreeNode(value)
                return True
            return self._insert_recursive(node.left, value)
        else:
            if node.right is None:
                node.right = TreeNode(value)
                return True
            return self._insert_recursive(node.right, value)

    def search(self, value):
        """Return True if value exists in the BST, False otherwise."""
        return self._search_recursive(self.root, value)

    def _search_recursive(self, node, value):
        if node is None:
            return False

        if value == node.value:
            return True
        elif value < node.value:
            return self._search_recursive(node.left, value)
        else:
            return self._search_recursive(node.right, value)

    def delete(self, value):
        """Delete a value from the BST. Returns True if deleted, False if not found."""
        result, self.root = self._delete_recursive(self.root, value)
        return result

    def _delete_recursive(self, node, value):
        if node is None:
            return False, None

        if value < node.value:
            deleted, node.left = self._delete_recursive(node.left, value)
            return deleted, node

        elif value > node.value:
            deleted, node.right = self._delete_recursive(node.right, value)
            return deleted, node

        else:
            # Found the node to delete
            # Case 1: No children (leaf node)
            if node.left is None and node.right is None:
                return True, None

            # Case 2: One child
            if node.left is None:
                return True, node.right
            if node.right is None:
                return True, node.left

            # Case 3: Two children
            # Find the inorder successor (smallest in right subtree)
            successor_parent = node
            successor = node.right
            while successor.left is not None:
                successor_parent = successor
                successor = successor.left

            # Replace node's value with successor's value
            node.value = successor.value

            # Delete the successor node (has at most one right child)
            if successor_parent == node:
                node.right = successor.right
            else:
                successor_parent.left = successor.right

            return True, node

    def min_value(self):
        """Return the minimum value in the BST. Returns None if empty."""
        if self.root is None:
            return None
        node = self.root
        while node.left is not None:
            node = node.left
        return node.value

    def max_value(self):
        """Return the maximum value in the BST. Returns None if empty."""
        if self.root is None:
            return None
        node = self.root
        while node.right is not None:
            node = node.right
        return node.value

    def inorder_traversal(self):
        """Return values in sorted order (left, root, right)."""
        result = []
        self._inorder_recursive(self.root, result)
        return result

    def _inorder_recursive(self, node, result):
        if node is not None:
            self._inorder_recursive(node.left, result)
            result.append(node.value)
            self._inorder_recursive(node.right, result)

    def preorder_traversal(self):
        """Return values in preorder (root, left, right)."""
        result = []
        self._preorder_recursive(self.root, result)
        return result

    def _preorder_recursive(self, node, result):
        if node is not None:
            result.append(node.value)
            self._preorder_recursive(node.left, result)
            self._preorder_recursive(node.right, result)

    def postorder_traversal(self):
        """Return values in postorder (left, right, root)."""
        result = []
        self._postorder_recursive(self.root, result)
        return result

    def _postorder_recursive(self, node, result):
        if node is not None:
            self._postorder_recursive(node.left, result)
            self._postorder_recursive(node.right, result)
            result.append(node.value)

    def height(self):
        """Return the height of the tree. Empty tree has height -1."""
        return self._height_recursive(self.root)

    def _height_recursive(self, node):
        if node is None:
            return -1
        return 1 + max(self._height_recursive(node.left), self._height_recursive(node.right))

    def is_bst(self):
        """Verify that the tree satisfies BST property."""
        return self._is_bst_recursive(self.root, float('-inf'), float('inf'))

    def _is_bst_recursive(self, node, min_val, max_val):
        if node is None:
            return True

        if node.value <= min_val or node.value >= max_val:
            return False

        return (self._is_bst_recursive(node.left, min_val, node.value) and
                self._is_bst_recursive(node.right, node.value, max_val))

    def is_balanced(self):
        """Check if tree is height-balanced (AVL property: heights differ by at most 1)."""
        return self._is_balanced_recursive(self.root)[0]

    def _is_balanced_recursive(self, node):
        """Return (is_balanced, height) for efficiency."""
        if node is None:
            return True, -1

        left_balanced, left_height = self._is_balanced_recursive(node.left)
        if not left_balanced:
            return False, 0

        right_balanced, right_height = self._is_balanced_recursive(node.right)
        if not right_balanced:
            return False, 0

        # Check if current node is balanced
        if abs(left_height - right_height) > 1:
            return False, 0

        return True, 1 + max(left_height, right_height)


# ---------------------------------------------------------------------------
# Demonstration / self-test
# ---------------------------------------------------------------------------

def run_demo():
    print("===== Binary Search Tree Demo =====\n")

    bst = BinarySearchTree()
    values = [50, 30, 70, 20, 40, 60, 80, 10, 25, 35, 65]

    print(f"Inserting values: {values}")
    for v in values:
        bst.insert(v)

    print(f"\nInorder (sorted):  {bst.inorder_traversal()}")
    print(f"Preorder:          {bst.preorder_traversal()}")
    print(f"Postorder:         {bst.postorder_traversal()}")

    print(f"\nMin value: {bst.min_value()}")
    print(f"Max value: {bst.max_value()}")
    print(f"Height: {bst.height()}")
    print(f"Is BST: {bst.is_bst()}")
    print(f"Is balanced: {bst.is_balanced()}")

    print(f"\nSearch for 40: {bst.search(40)}")
    print(f"Search for 999: {bst.search(999)}")

    print(f"\nDelete 20 (leaf node)")
    bst.delete(20)
    print(f"Inorder after delete: {bst.inorder_traversal()}")

    print(f"\nDelete 30 (node with two children)")
    bst.delete(30)
    print(f"Inorder after delete: {bst.inorder_traversal()}")

    print(f"\nTrying to insert duplicate 50")
    result = bst.insert(50)
    print(f"Insert returned: {result} (False = rejected)")


def run_tests():
    print("\n===== Running correctness tests =====")

    # Test 1: Basic insert and search
    bst = BinarySearchTree()
    assert bst.insert(50) is True
    assert bst.insert(30) is True
    assert bst.insert(70) is True
    assert bst.insert(50) is False  # duplicate

    assert bst.search(30) is True
    assert bst.search(999) is False

    # Test 2: Min and max
    assert bst.min_value() == 30
    assert bst.max_value() == 70

    # Test 3: Traversals
    bst = BinarySearchTree()
    for v in [50, 30, 70, 20, 40, 60, 80]:
        bst.insert(v)

    assert bst.inorder_traversal() == [20, 30, 40, 50, 60, 70, 80]
    assert bst.preorder_traversal() == [50, 30, 20, 40, 70, 60, 80]
    assert bst.postorder_traversal() == [20, 40, 30, 60, 80, 70, 50]

    # Test 4: Delete leaf
    bst.delete(20)
    assert bst.search(20) is False
    assert bst.inorder_traversal() == [30, 40, 50, 60, 70, 80]

    # Test 5: Delete node with two children
    bst.delete(30)
    assert bst.search(30) is False
    assert bst.inorder_traversal() == [40, 50, 60, 70, 80]

    # Test 6: Height and balance
    bst2 = BinarySearchTree()
    for v in [50, 30, 70, 20, 40, 60, 80]:
        bst2.insert(v)
    assert bst2.height() == 2
    assert bst2.is_balanced() is True

    # Test 7: Unbalanced tree
    bst3 = BinarySearchTree()
    for v in [1, 2, 3, 4, 5]:  # creates a linear chain
        bst3.insert(v)
    assert bst3.height() == 4
    assert bst3.is_balanced() is False

    # Test 8: Empty tree
    bst4 = BinarySearchTree()
    assert bst4.min_value() is None
    assert bst4.max_value() is None
    assert bst4.height() == -1
    assert bst4.inorder_traversal() == []

    # Test 9: BST property verification
    bst5 = BinarySearchTree()
    for v in [50, 30, 70, 20, 40, 60, 80]:
        bst5.insert(v)
    assert bst5.is_bst() is True

    print("All tests passed!")


if __name__ == "__main__":
    run_demo()
    run_tests()
