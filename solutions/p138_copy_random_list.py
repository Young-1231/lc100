# LC 138. 随机链表的复制 · Medium · 哈希 / 原地交织
"""
🔹 题面
    每节点除 next 外多一个 random 指针,复制整张图。

🔹 直觉(两种)
    1. 哈希:旧节点 -> 新节点,先建副本节点,再串 next/random。  O(n)/O(n)
    2. 原地交织:在每个原节点后插入复制节点 a→a'→b→b'→…,
       让 a'.random = a.random.next;最后拆出。  O(n)/O(1)

🔹 踩坑
    random 可能指向自己或 None;构造好"先映射,再连边"。
"""


class Node:
    def __init__(self, x: int, nxt=None, rand=None):
        self.val = x
        self.next = nxt
        self.random = rand


class Solution:
    # 解法 1:哈希
    def copyRandomList(self, head):
        if not head:
            return None
        m: dict = {}
        cur = head
        while cur:
            m[cur] = Node(cur.val)
            cur = cur.next
        cur = head
        while cur:
            m[cur].next = m.get(cur.next)
            m[cur].random = m.get(cur.random)
            cur = cur.next
        return m[head]


def _test() -> None:
    s = Solution()
    # 构造 [[7,None],[13,0],[11,4],[10,2],[1,0]]
    nodes = [Node(7), Node(13), Node(11), Node(10), Node(1)]
    for i in range(4):
        nodes[i].next = nodes[i + 1]
    randoms = [None, 0, 4, 2, 0]
    for n, r in zip(nodes, randoms):
        n.random = nodes[r] if r is not None else None
    out = s.copyRandomList(nodes[0])
    # 校验:不是同一引用,但值序列与 random 索引相同
    cur, vals = out, []
    while cur:
        vals.append(cur.val)
        cur = cur.next
    assert vals == [7, 13, 11, 10, 1]
    # 校验 random 索引
    cur = out
    idx_map = {}
    i = 0
    p = out
    while p:
        idx_map[id(p)] = i
        i += 1
        p = p.next
    cur = out
    rand_idx = []
    while cur:
        rand_idx.append(idx_map[id(cur.random)] if cur.random else None)
        cur = cur.next
    assert rand_idx == [None, 0, 4, 2, 0]
    print("✅ p138 通过")


if __name__ == "__main__":
    _test()
