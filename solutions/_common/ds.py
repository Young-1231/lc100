"""通用数据结构定义:链表、二叉树、Trie、并查集。

所有题解共享此模块:
    from _common.ds import ListNode, TreeNode, build_list, build_tree
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, Iterable, Any


# ---------- 链表 ----------
class ListNode:
    __slots__ = ("val", "next")

    def __init__(self, val: int = 0, nxt: "ListNode | None" = None):
        self.val = val
        self.next = nxt

    def __repr__(self) -> str:
        vals, cur, seen = [], self, set()
        while cur and id(cur) not in seen:
            seen.add(id(cur))
            vals.append(str(cur.val))
            cur = cur.next
            if len(vals) > 50:
                vals.append("…")
                break
        return " -> ".join(vals) or "∅"


def build_list(vals: Iterable[int]) -> Optional[ListNode]:
    """[1,2,3] -> 1 -> 2 -> 3."""
    dummy = ListNode()
    cur = dummy
    for v in vals:
        cur.next = ListNode(v)
        cur = cur.next
    return dummy.next


def list_to_array(head: Optional[ListNode]) -> list[int]:
    out, cur, seen = [], head, set()
    while cur and id(cur) not in seen:
        seen.add(id(cur))
        out.append(cur.val)
        cur = cur.next
    return out


# ---------- 二叉树 ----------
class TreeNode:
    __slots__ = ("val", "left", "right")

    def __init__(self, val: int = 0,
                 left: "TreeNode | None" = None,
                 right: "TreeNode | None" = None):
        self.val = val
        self.left = left
        self.right = right

    def __repr__(self) -> str:
        return f"TreeNode({self.val})"


def build_tree(vals: list[Any]) -> Optional[TreeNode]:
    """LeetCode 层序数组 -> 二叉树。None 表示空位。

    [1, 2, 3, None, 4] ->
            1
           / \\
          2   3
           \\
            4
    """
    if not vals or vals[0] is None:
        return None
    root = TreeNode(vals[0])
    queue = [root]
    i = 1
    while queue and i < len(vals):
        node = queue.pop(0)
        if i < len(vals) and vals[i] is not None:
            node.left = TreeNode(vals[i])
            queue.append(node.left)
        i += 1
        if i < len(vals) and vals[i] is not None:
            node.right = TreeNode(vals[i])
            queue.append(node.right)
        i += 1
    return root


def tree_to_level(root: Optional[TreeNode]) -> list[Any]:
    """二叉树 -> LeetCode 层序数组(去掉末尾的 None)。"""
    if not root:
        return []
    out, q = [], [root]
    while q:
        n = q.pop(0)
        if n is None:
            out.append(None)
        else:
            out.append(n.val)
            q.append(n.left)
            q.append(n.right)
    while out and out[-1] is None:
        out.pop()
    return out


# ---------- 并查集 ----------
class UnionFind:
    __slots__ = ("parent", "rank", "count")

    def __init__(self, n: int):
        self.parent = list(range(n))
        self.rank = [0] * n
        self.count = n  # 连通分量数量

    def find(self, x: int) -> int:
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]  # 路径压缩
            x = self.parent[x]
        return x

    def union(self, x: int, y: int) -> bool:
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return False
        if self.rank[rx] < self.rank[ry]:
            rx, ry = ry, rx
        self.parent[ry] = rx
        if self.rank[rx] == self.rank[ry]:
            self.rank[rx] += 1
        self.count -= 1
        return True


# ---------- Trie ----------
class TrieNode:
    __slots__ = ("children", "is_end")

    def __init__(self):
        self.children: dict[str, "TrieNode"] = {}
        self.is_end = False


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        cur = self.root
        for c in word:
            cur = cur.children.setdefault(c, TrieNode())
        cur.is_end = True

    def _walk(self, prefix: str) -> Optional[TrieNode]:
        cur = self.root
        for c in prefix:
            if c not in cur.children:
                return None
            cur = cur.children[c]
        return cur

    def search(self, word: str) -> bool:
        n = self._walk(word)
        return n is not None and n.is_end

    def startsWith(self, prefix: str) -> bool:
        return self._walk(prefix) is not None
