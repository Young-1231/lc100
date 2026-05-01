# LC 104. 二叉树的最大深度 · Easy · 递归 / BFS
"""
🔹 解法对比
    | 方法     | 时间 | 空间 | 备注              |
    |----------|------|------|-------------------|
    | 递归 DFS | O(n) | O(h) | 简洁              |
    | 迭代 BFS | O(n) | O(w) | 层序逐层加        |
"""
from collections import deque
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _common.ds import build_tree


class Solution:
    # 解法 1:递归 — O(n) / O(h)
    def maxDepth(self, root) -> int:
        if not root:
            return 0
        return 1 + max(self.maxDepth(root.left), self.maxDepth(root.right))

    # 解法 2:BFS — O(n) / O(w)
    def maxDepth_bfs(self, root) -> int:
        if not root:
            return 0
        q = deque([root])
        d = 0
        while q:
            d += 1
            for _ in range(len(q)):
                n = q.popleft()
                if n.left:
                    q.append(n.left)
                if n.right:
                    q.append(n.right)
        return d


def _test() -> None:
    s = Solution()
    for fn in (s.maxDepth, s.maxDepth_bfs):
        assert fn(build_tree([3, 9, 20, None, None, 15, 7])) == 3
        assert fn(None) == 0
        assert fn(build_tree([1, None, 2])) == 2
    print("✅ p104 通过 2 解法")


if __name__ == "__main__":
    _test()
