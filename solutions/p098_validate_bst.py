# LC 98. 验证二叉搜索树 · Medium · 递归 / 中序
"""
🔹 直觉
    1. 递归带"上下界"边界:每个节点必须 ∈ (low, high)。
    2. 中序遍历必须严格递增。
    陷阱:仅检查"父子大小关系"是错的——不能保证孙子也在范围内。
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _common.ds import build_tree


class Solution:
    def isValidBST(self, root) -> bool:
        def ok(n, lo, hi):
            if not n:
                return True
            if n.val <= lo or n.val >= hi:
                return False
            return ok(n.left, lo, n.val) and ok(n.right, n.val, hi)
        return ok(root, float("-inf"), float("inf"))


def _test() -> None:
    s = Solution()
    assert s.isValidBST(build_tree([2, 1, 3])) is True
    assert s.isValidBST(build_tree([5, 1, 4, None, None, 3, 6])) is False
    assert s.isValidBST(build_tree([5, 4, 6, None, None, 3, 7])) is False
    print("✅ p098 通过")


if __name__ == "__main__":
    _test()
