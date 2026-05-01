# LC 114. 二叉树展开为链表 · Medium · 后序 / 反向先序
"""
🔹 题面
    将二叉树原地展开为前序顺序的"右侧链表"(left 全 None)。

🔹 直觉(反向先序)
    定义 prev(全局),按"右-左-根"递归;访问到每个节点时:
        node.right = prev
        node.left  = None
        prev = node
    妙在它构成的就是 "根-左-右" 反过来 = 先序的逆序。
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _common.ds import build_tree


class Solution:
    def flatten(self, root) -> None:
        self.prev = None

        def dfs(n):
            if not n:
                return
            dfs(n.right)
            dfs(n.left)
            n.right = self.prev
            n.left = None
            self.prev = n

        dfs(root)


def _to_chain(root) -> list[int]:
    out = []
    while root:
        out.append(root.val)
        assert root.left is None
        root = root.right
    return out


def _test() -> None:
    s = Solution()
    t = build_tree([1, 2, 5, 3, 4, None, 6])
    s.flatten(t)
    assert _to_chain(t) == [1, 2, 3, 4, 5, 6]
    s.flatten(None)
    print("✅ p114 通过")


if __name__ == "__main__":
    _test()
