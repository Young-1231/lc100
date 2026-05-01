# LC 146. LRU 缓存 · Medium · 哈希 + 双向链表
"""
🔹 题面
    实现 LRU:get/put 都 O(1)。

🔹 直觉
    哈希表 → 双向链表节点。命中或写入移到链表头(最近使用);超容量时
    剔除尾部(最久未使用)。

🔹 关键
    - 哑头/哑尾节点,简化边界。
    - move_to_head = remove + add_to_head。
    - put 已存在 → 更新 value 并移到头。

🔹 复杂度 O(1) / O(capacity)
"""


class _Node:
    __slots__ = ("key", "val", "prev", "next")

    def __init__(self, k=0, v=0):
        self.key, self.val = k, v
        self.prev = self.next = None


class LRUCache:
    def __init__(self, capacity: int):
        self.cap = capacity
        self.map: dict[int, _Node] = {}
        self.head, self.tail = _Node(), _Node()
        self.head.next = self.tail
        self.tail.prev = self.head

    def _add(self, n: _Node) -> None:
        n.prev = self.head
        n.next = self.head.next
        self.head.next.prev = n
        self.head.next = n

    def _remove(self, n: _Node) -> None:
        n.prev.next = n.next
        n.next.prev = n.prev

    def get(self, key: int) -> int:
        if key not in self.map:
            return -1
        n = self.map[key]
        self._remove(n); self._add(n)
        return n.val

    def put(self, key: int, value: int) -> None:
        if key in self.map:
            n = self.map[key]
            n.val = value
            self._remove(n); self._add(n)
            return
        if len(self.map) >= self.cap:
            lru = self.tail.prev
            self._remove(lru)
            del self.map[lru.key]
        n = _Node(key, value)
        self._add(n)
        self.map[key] = n


def _test() -> None:
    c = LRUCache(2)
    c.put(1, 1); c.put(2, 2)
    assert c.get(1) == 1
    c.put(3, 3)            # 淘汰 2
    assert c.get(2) == -1
    c.put(4, 4)            # 淘汰 1
    assert c.get(1) == -1
    assert c.get(3) == 3
    assert c.get(4) == 4
    print("✅ p146 通过")


if __name__ == "__main__":
    _test()
