# LC 124. 二叉树中的最大路径和 · Hard · 递归
"""
🔹 题面
    求任意"路径"(任意两节点)节点和最大值。可只一个节点。

🔹 直觉
    后序返回"以当前节点为顶端、必须包含它、向下走单边"的最大贡献。
    全局答案在每个节点处尝试"左贡献 + 节点 + 右贡献"。
    单边贡献若 < 0,丢弃(置 0)。

🔹 复杂度 O(n) / O(h)
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _common.ds import build_tree


class Solution:
    def maxPathSum(self, root) -> int:
        self.best = float("-inf")

        def gain(n):
            if not n:
                return 0
            l = max(0, gain(n.left))
            r = max(0, gain(n.right))
            self.best = max(self.best, n.val + l + r)
            return n.val + max(l, r)

        gain(root)
        return self.best


def _test() -> None:
    s = Solution()
    assert s.maxPathSum(build_tree([1, 2, 3])) == 6
    assert s.maxPathSum(build_tree([-10, 9, 20, None, None, 15, 7])) == 42
    assert s.maxPathSum(build_tree([-3])) == -3
    print("✅ p124 通过")


if __name__ == "__main__":
    _test()
