# LC 226. 翻转二叉树 · Easy · 递归
"""
🔹 题面
    把二叉树的每个节点的左右子树交换。

🔹 解法对比
    | 方法     | 时间 | 空间 | 备注      |
    |----------|------|------|-----------|
    | 递归 ★  | O(n) | O(h) | 简洁       |
    | BFS 迭代 | O(n) | O(w) | 用队列扫每层 |
"""
from collections import deque
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _common.ds import build_tree, tree_to_level


class Solution:
    # 解法 1:递归 ★ — O(n) / O(h)
    def invertTree(self, root):
        if not root:
            return None
        root.left, root.right = self.invertTree(root.right), self.invertTree(root.left)
        return root

    # 解法 2:BFS 迭代 — O(n) / O(w)
    def invertTree_bfs(self, root):
        if not root:
            return None
        q = deque([root])
        while q:
            n = q.popleft()
            n.left, n.right = n.right, n.left
            if n.left:
                q.append(n.left)
            if n.right:
                q.append(n.right)
        return root


def _test() -> None:
    s = Solution()
    arg = [4, 2, 7, 1, 3, 6, 9]
    want = [4, 7, 2, 9, 6, 3, 1]
    for fn in (s.invertTree, s.invertTree_bfs):
        assert tree_to_level(fn(build_tree(arg))) == want
        assert fn(None) is None
    print("✅ p226 通过 2 解法")


if __name__ == "__main__":
    _test()
