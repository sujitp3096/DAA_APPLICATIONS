"""
Trie (Prefix Tree) - Data Structures & Algorithms project (Python)

A Trie is a tree where each path from the root spells out a prefix of
some inserted word. It's the standard data structure behind autocomplete,
spell-check suggestion lists, and IP routing tables.

Operations implemented:
  insert(word)          - O(L) where L = length of word
  search(word)           - O(L), exact match only
  starts_with(prefix)     - O(L), True if any word has this prefix
  autocomplete(prefix)    - O(L + number of matches), returns all words with this prefix
  delete(word)            - O(L), removes a word (and prunes now-unused nodes)
  count_words_with_prefix - O(L), how many stored words share this prefix
"""


class TrieNode:
    def __init__(self):
        self.children = {}       # character -> TrieNode
        self.is_end_of_word = False
        self.word_count = 0      # how many inserted words pass through this node (for prefix counts)


class Trie:
    def __init__(self):
        self.root = TrieNode()
        self.total_words = 0

    def insert(self, word):
        if not word:
            return

        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
            node.word_count += 1

        if not node.is_end_of_word:
            node.is_end_of_word = True
            self.total_words += 1

    def search(self, word):
        """Exact word match."""
        node = self._find_node(word)
        return node is not None and node.is_end_of_word

    def starts_with(self, prefix):
        """True if at least one stored word starts with this prefix."""
        return self._find_node(prefix) is not None

    def count_words_with_prefix(self, prefix):
        node = self._find_node(prefix)
        return node.word_count if node else 0

    def autocomplete(self, prefix, limit=None):
        """Returns all stored words starting with `prefix`, sorted alphabetically.
        If `limit` is given, returns at most that many suggestions."""
        node = self._find_node(prefix)
        if node is None:
            return []

        results = []
        self._collect_words(node, prefix, results)
        results.sort()

        return results[:limit] if limit else results

    def delete(self, word):
        """Removes a word from the trie. Returns True if it was present and removed."""
        if not self.search(word):
            return False

        node = self.root
        path = [node]
        for char in word:
            node = node.children[char]
            path.append(node)

        node.is_end_of_word = False
        self.total_words -= 1

        # Walk back up, decrementing word_count and pruning nodes that are no
        # longer needed (no children and not the end of another word).
        for i in range(len(word), 0, -1):
            char = word[i - 1]
            current = path[i]
            parent = path[i - 1]
            current.word_count -= 1

            if current.word_count == 0 and not current.is_end_of_word:
                del parent.children[char]
            else:
                break  # this node is still needed by other words, stop pruning

        return True

    def _find_node(self, prefix):
        node = self.root
        for char in prefix:
            if char not in node.children:
                return None
            node = node.children[char]
        return node

    def _collect_words(self, node, prefix, results):
        if node.is_end_of_word:
            results.append(prefix)

        for char, child in node.children.items():
            self._collect_words(child, prefix + char, results)


# ---------------------------------------------------------------------------
# Demonstration / self-test
# ---------------------------------------------------------------------------

def run_demo():
    print("===== Trie / Autocomplete Demo =====\n")

    trie = Trie()
    words = ["cat", "car", "card", "care", "careful", "dog", "do", "door"]

    print(f"Inserting words: {words}")
    for w in words:
        trie.insert(w)

    print(f"\nsearch('car')     -> {trie.search('car')}")
    print(f"search('ca')      -> {trie.search('ca')}")
    print(f"starts_with('ca') -> {trie.starts_with('ca')}")

    print(f"\nautocomplete('car')  -> {trie.autocomplete('car')}")
    print(f"autocomplete('do')   -> {trie.autocomplete('do')}")
    print(f"autocomplete('xyz')  -> {trie.autocomplete('xyz')}")

    print(f"\ncount_words_with_prefix('car') -> {trie.count_words_with_prefix('car')}")

    print(f"\ndelete('car') -> {trie.delete('car')}")
    print(f"search('car') after delete  -> {trie.search('car')}")
    print(f"search('card') after delete -> {trie.search('card')}  (should still exist)")
    print(f"autocomplete('car') after delete -> {trie.autocomplete('car')}")


def run_tests():
    print("\n===== Running correctness tests =====")

    trie = Trie()
    for w in ["cat", "car", "card", "care", "careful", "dog", "do", "door"]:
        trie.insert(w)

    assert trie.search("cat") is True
    assert trie.search("ca") is False, "‘ca’ was never inserted as a full word"
    assert trie.starts_with("ca") is True
    assert trie.starts_with("xyz") is False

    assert trie.autocomplete("car") == ["car", "card", "care", "careful"]
    assert trie.autocomplete("do") == ["do", "dog", "door"]
    assert trie.autocomplete("do", limit=2) == ["do", "dog"]
    assert trie.autocomplete("zzz") == []

    assert trie.count_words_with_prefix("car") == 4
    assert trie.count_words_with_prefix("care") == 2  # care, careful

    assert trie.delete("car") is True
    assert trie.search("car") is False
    assert trie.search("card") is True, "deleting 'car' must not remove 'card'"
    assert trie.autocomplete("car") == ["card", "care", "careful"]

    assert trie.delete("notpresent") is False

    # Deleting a word with no shared prefixes should prune all its nodes
    trie2 = Trie()
    trie2.insert("standalone")
    assert trie2.delete("standalone") is True
    assert trie2.starts_with("stand") is False
    assert len(trie2.root.children) == 0, "trie should be empty after removing its only word"

    print("All tests passed!")


if __name__ == "__main__":
    run_demo()
    run_tests()
