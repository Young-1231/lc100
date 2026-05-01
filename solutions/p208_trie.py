# LC 208. 实现 Trie(前缀树) · Medium · 字典树
"""
🔹 直觉
    每节点用 dict 保存子节点;is_end 标记完整单词。
    insert/search/startsWith 均 O(L)。
"""


class Trie:
    def __init__(self):
        self.ch: dict = {}
        self.end = False

    def insert(self, word: str) -> None:
        cur = self
        for c in word:
            if c not in cur.ch:
                cur.ch[c] = Trie()
            cur = cur.ch[c]
        cur.end = True

    def _walk(self, prefix: str):
        cur = self
        for c in prefix:
            if c not in cur.ch:
                return None
            cur = cur.ch[c]
        return cur

    def search(self, word: str) -> bool:
        n = self._walk(word)
        return n is not None and n.end

    def startsWith(self, prefix: str) -> bool:
        return self._walk(prefix) is not None


def _test() -> None:
    t = Trie()
    t.insert("apple")
    assert t.search("apple") is True
    assert t.search("app") is False
    assert t.startsWith("app") is True
    t.insert("app")
    assert t.search("app") is True
    print("✅ p208 通过")


if __name__ == "__main__":
    _test()
