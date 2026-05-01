# LC 543. 二叉树的直径 · Easy · 递归
"""
🔹 题面
    返回任意两节点的最长路径(以"边数"计)。

🔹 直觉
    后序求"以当前节点为最高点"的最长路径 = 左深度 + 右深度。
    全局取最大。注意:函数返回的是"该节点向下的最长路径长度"(深度),
    而 best 记录"穿过该节点的总路径"。
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _common.ds import build_tree


class Solution:
    def diameterOfBinaryTree(self, root) -> int:
        self.best = 0

        def depth(n):
            if not n:
                return 0
            l = depth(n.left)
            r = depth(n.right)
            self.best = max(self.best, l + r)
            return 1 + max(l, r)

        depth(root)
        return self.best


def _test() -> None:
    s = Solution()
    assert s.diameterOfBinaryTree(build_tree([1, 2, 3, 4, 5])) == 3
    assert s.diameterOfBinaryTree(build_tree([1, 2])) == 1
    assert s.diameterOfBinaryTree(build_tree([1])) == 0
    print("✅ p543 通过")


if __name__ == "__main__":
    _test()
