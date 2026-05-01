# LC 199. 二叉树的右视图 · Medium · BFS / DFS
"""
🔹 题面
    返回从右侧能看到的节点(每层最右一个)。

🔹 解法对比
    | 方法    | 时间 | 空间 | 备注              |
    |---------|------|------|-------------------|
    | BFS ★  | O(n) | O(w) | 每层最后一个      |
    | DFS     | O(n) | O(h) | 先右后左,每层第一次访问即可 |
"""
from collections import deque
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _common.ds import build_tree


class Solution:
    # 解法 1:BFS ★ — O(n) / O(w)
    def rightSideView(self, root) -> list[int]:
        if not root:
            return []
        out, q = [], deque([root])
        while q:
            sz = len(q)
            for i in range(sz):
                n = q.popleft()
                if i == sz - 1:
                    out.append(n.val)
                if n.left:
                    q.append(n.left)
                if n.right:
                    q.append(n.right)
        return out

    # 解法 2:DFS(先右后左)— O(n) / O(h)
    def rightSideView_dfs(self, root) -> list[int]:
        out: list[int] = []

        def dfs(n, d):
            if not n:
                return
            if d == len(out):
                out.append(n.val)
            dfs(n.right, d + 1)
            dfs(n.left, d + 1)

        dfs(root, 0)
        return out


def _test() -> None:
    s = Solution()
    cases = [
        ([1, 2, 3, None, 5, None, 4], [1, 3, 4]),
        ([1, None, 3], [1, 3]),
        ([], []),
    ]
    for arg, want in cases:
        for fn in (s.rightSideView, s.rightSideView_dfs):
            assert fn(build_tree(arg)) == want
    print("✅ p199 通过 2 解法")


if __name__ == "__main__":
    _test()
