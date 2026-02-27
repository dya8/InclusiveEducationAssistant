# core/nlp/trie.py

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_word = False
        self.frequency = 0


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word, frequency=1):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_word = True
        node.frequency = frequency

    def _dfs(self, node, prefix, results):
        if node.is_word:
            results.append((prefix, node.frequency))
        for char, child in node.children.items():
            self._dfs(child, prefix + char, results)

    def get_words_with_prefix(self, prefix):
        node = self.root
        for char in prefix:
            if char not in node.children:
                return []
            node = node.children[char]

        results = []
        self._dfs(node, prefix, results)
        return results