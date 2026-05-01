# LC 102. 二叉树的层序遍历 · Medium · BFS
"""
🔹 题面
    返回层序遍历结果(每层一个数组)。

🔹 解法对比
    | 方法    | 时间 | 空间 | 备注                  |
    |---------|------|------|-----------------------|
    | BFS ★  | O(n) | O(w) | 队列,每层批量出队     |
    | DFS+层号| O(n) | O(h) | 递归带 depth,按层 push |
"""
from collections import deque
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _common.ds import build_tree


class Solution:
    # 解法 1:BFS ★ — O(n) / O(w)
    def levelOrder(self, root) -> list[list[int]]:
        if not root:
            return []
        out, q = [], deque([root])
        while q:
            level = []
            for _ in range(len(q)):
                n = q.popleft()
                level.append(n.val)
                if n.left:
                    q.append(n.left)
                if n.right:
                    q.append(n.right)
            out.append(level)
        return out

    # 解法 2:DFS + 层号 — O(n) / O(h)
    def levelOrder_dfs(self, root) -> list[list[int]]:
        out: list[list[int]] = []

        def dfs(n, d):
            if not n:
                return
            if d == len(out):
                out.append([])
            out[d].append(n.val)
            dfs(n.left, d + 1)
            dfs(n.right, d + 1)

        dfs(root, 0)
        return out


def _test() -> None:
    s = Solution()
    cases = [
        ([3, 9, 20, None, None, 15, 7], [[3], [9, 20], [15, 7]]),
        ([], []),
        ([1], [[1]]),
    ]
    for arg, want in cases:
        for fn in (s.levelOrder, s.levelOrder_dfs):
            assert fn(build_tree(arg)) == want
    print("✅ p102 通过 2 解法")


if __name__ == "__main__":
    _test()
